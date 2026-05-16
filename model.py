import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Clean Chat Prompt Template (No structural constraints)
chat_template = ChatPromptTemplate.from_messages([
    ("system", "{system_prompt}"),
    ("user", "{user_prompt}")
])

# 2. Function to initialize models using your working API key
def initialize_model(model_id):
    api_key = "Paste_your_key_here_for_testing"  # Replace with your actual key for testing
    return ChatGroq(
        model=model_id,
        groq_api_key=api_key,
        temperature=0.7 # Raised slightly from 0.0 to make conversations natural and less robotic
    )

# 3. Initialize just our TWO live models
llama_heavy = initialize_model("llama-3.3-70b-versatile")
llama_fast = initialize_model("llama-3.1-8b-instant")

# 4. Core generation function that returns clean text
def get_ai_response(model, system_prompt, user_prompt):
    chain = chat_template | model
    response = chain.invoke({
        'system_prompt': system_prompt, 
        'user_prompt': user_prompt
    })
    # Return a regular dictionary with text content so app.py stays compatible
    return {"response_text": response.content}

# 5. Maintain model-specific functions for app.py
def llama_response(system_prompt, user_prompt):
    return get_ai_response(llama_heavy, system_prompt, user_prompt)

def mistral_response(system_prompt, user_prompt):
    return get_ai_response(llama_fast, system_prompt, user_prompt)

def granite_response(system_prompt, user_prompt):
    return get_ai_response(llama_fast, system_prompt, user_prompt)