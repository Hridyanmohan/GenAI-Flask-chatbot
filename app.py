from flask import Flask, request, jsonify, render_template
from model import llama_response, granite_response, mistral_response
import sqlite3
import time
import uuid

app = Flask(__name__)

# Initialize Local Database for Chat Architecture
def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    # Table for separate conversation threads
    cursor.execute('''CREATE TABLE IF NOT EXISTS threads 
                      (id TEXT PRIMARY KEY, title TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    # Table for individual messages inside threads
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, thread_id TEXT, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# --- SIDEBAR HISTORY API ENDPOINTS ---

@app.route('/threads', methods=['GET'])
def get_threads():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM threads ORDER BY timestamp DESC")
    threads = [{"id": row[0], "title": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(threads)

@app.route('/threads/<thread_id>/messages', methods=['GET'])
def get_messages(thread_id):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM messages WHERE thread_id = ? ORDER BY id ASC", (thread_id,))
    messages = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(messages)

@app.route('/threads/<thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE thread_id = ?", (thread_id,))
    cursor.execute("DELETE FROM threads WHERE id = ?", (thread_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# --- INFERENCE PIPELINE ---

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    # Change this line inside app.py:
    user_message = data.get('message', '').strip()
    model = data.get('model')
    thread_id = data.get('thread_id')
    
    if not user_message or not model:
        return jsonify({"error": "Missing message or model selection"}), 400
    
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()

    # Create a brand new thread tracker if one wasn't passed from UI
    if not thread_id:
        thread_id = str(uuid.uuid4())
        # Truncate title length to keep sidebar clean
        title = user_message[:24] + "..." if len(user_message) > 24 else user_message
        cursor.execute("INSERT INTO threads (id, title) VALUES (?, ?)", (thread_id, title))
    
    # Fetch historical data context logs from this specific thread
    cursor.execute("SELECT role, content FROM messages WHERE thread_id = ? ORDER BY id ASC", (thread_id,))
    past_turns = cursor.fetchall()
    
    # STRICT SHORTENING INSTRUCTIONS ADDED HERE
    #system_prompt = (
     #   "You are Sarvam Maya, a helpful AI assistant. "
       # "CRITICAL: Keep your answers ultra-short, concise, and direct. "
     #   "Never use conversational filler or long explanations unless explicitly requested. "
      #  "Get straight to the point in 1-3 sentences maximum using bold markdown tags if appropriate."
    #)
    # Inside app.py under def generate():
    system_prompt = (
        "You are Sarvam Maya, a highly intelligent and adaptive AI assistant. "
        "Your task is to dynamically adjust the length of your response based on the user's intent:\n\n"
        
        "1. SHORT ANSWERS (1-2 sentences): Use this for simple factual lookups, greetings, "
        "or binary questions (e.g., yes/no, definitions, capitals, greetings).\n"
        
        "2. MEDIUM ANSWERS (1-3 brief paragraphs): Use this for conceptual explanations, 'how-to' questions, "
        "or summaries. Keep it structured using bold text (**).\n"
        
        "3. LONG ANSWERS (Comprehensive layout): Use this ONLY when the user explicitly asks for detailed guides, "
        "code generation, roadmaps, comparison essays, or complex troubleshooting. "
        "Structure these heavily with Markdown headers (##), bold text, and bullet points.\n\n"
        
        "Analyze the user's prompt carefully and choose the most effective layout style instantly. "
        "Avoid unnecessary conversational filler in all modes."
    )
    
    # Build historical prompt compilation context
    history_context = ""
    if past_turns:
        history_context = "\n\n--- Prior Chat Log Context ---\n"
        for role, content in past_turns[-6:]:
            history_context += f"{role.upper()}: {content}\n"
        history_context += "---------------------------------\n"
        
    full_prompt = f"{history_context}USER: {user_message}"
    start_time = time.time()
    
    try:
        if model == 'llama':
            result = llama_response(system_prompt, full_prompt)
        elif model == 'granite':
            result = granite_response(system_prompt, full_prompt)
        elif model == 'mistral':
            result = mistral_response(system_prompt, full_prompt)
        else:
            return jsonify({"error": "Invalid model selection"}), 400
        
        ai_response_text = result['response_text'].strip()
        
        # Log conversational updates straight to DB
        cursor.execute("INSERT INTO messages (thread_id, role, content) VALUES (?, 'user', ?)", (thread_id, user_message))
        cursor.execute("INSERT INTO messages (thread_id, role, content) VALUES (?, 'assistant', ?)", (thread_id, ai_response_text))
        conn.commit()
        conn.close()
        
        return jsonify({
            "response_text": ai_response_text,
            "thread_id": thread_id,
            "duration": time.time() - start_time
        })
        
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)