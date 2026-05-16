import os
from groq import Groq

# Paste your actual gsk_... key string directly here just to test
api_key = "Paste_your_key_here_for_testing"

# Initialize the Groq client
client = Groq(api_key=api_key)

#text = "Only reply with the answer. What is the capital of Canada?"
text = """
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an expert assistant who provides concise and accurate answers.<|eot_id|>

<|start_header_id|>user<|end_header_id|>
What is the capital of Canada?<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": text
        }
    ],
    temperature=0.0, 
    max_tokens=100
)

print(completion.choices[0].message.content)