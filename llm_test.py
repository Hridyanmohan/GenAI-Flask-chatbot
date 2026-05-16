from model import llama_response, mistral_response
import json

def call_active_models(system_prompt, user_prompt):
    print("🚀 Firing queries to active Groq endpoints...\n")
    
    # Run inference on our two chosen active configurations
    llama_heavy_result = llama_response(system_prompt, user_prompt)
    llama_fast_result = mistral_response(system_prompt, user_prompt)

    print("=========================================")
    print("1. Llama 3.3 (70B) JSON Response:")
    print("=========================================")
    print(json.dumps(llama_heavy_result, indent=2))
    
    print("\n=========================================")
    print("2. Llama 3.1 (8B) JSON Response:")
    print("=========================================")
    print(json.dumps(llama_fast_result, indent=2))

# Run the dual-model diagnostic test
call_active_models(
    "You are an AI customer support assistant. Analyze the user message.", 
    "My screen goes completely black whenever I try to open the settings menu. Please help!"
)