import os
from dotenv import load_dotenv

# 1. Load variables securely from your local .env file
load_dotenv()

# 2. Centralize your Groq configurations
# Fetch the API key safely from the environment
GROQ_API_KEY = os.getenv("Paste_your_key_here_for_testing")

# 3. Streamlined Model parameters
# In Groq, "greedy" decoding is achieved by setting temperature to 0.0
PARAMETERS = {
    "temperature": 0.0,
    "max_tokens": 256,
}

# 4. Active, supported Groq Model IDs
LLAMA_MODEL_ID = "llama-3.3-70b-versatile"    # Active high-performance model
MISTRAL_MODEL_ID = "mixtral-8x7b-32768"       # Active high-speed Mixtral model
GEMMA_MODEL_ID = "llama-3.1-8b-instant"               # Lightweight Google fallback model