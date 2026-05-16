# GenAI-Flask-chatbot
arvam Maya is a premium, high-performance conversational AI assistant built with a Flask backend, a modern Gemini-inspired glassmorphism frontend, and an intelligent multi-LLM engine powered by LangChain and Groq.
# 🌟 Sarvam Maya AI Assistant

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-black.svg)](https://flask.palletsprojects.com/)
[![AI Engine](https://img.shields.io/badge/orchestration-LangChain-orange.svg)](https://www.langchain.com/)
[![Inference Platform](https://img.shields.io/badge/inference-Groq-red.svg)](https://groq.com/)

**Sarvam Maya** is a high-performance, intelligent conversational AI assistant engineered for a fluid, ultra-low-latency chat experience. It pairs a robust Python Flask backend with a minimal, responsive Google Gemini-inspired glassmorphism user interface. Using LangChain orchestration, the system streams user queries to cutting-edge open-weight model architectures via Groq's high-speed inference engine.

The architecture includes a dynamic **Intent-Length Orchestrator** to regulate response lengths and a persistent SQLite storage layer to capture individual conversational histories across browser sessions.

---

## ✨ Core Features

* **🎭 Gemini-Inspired Interface:** Implements a modern, distraction-free viewport centered around a floating, auto-expanding capsule input box, clean micro-interactions, smooth fade transitions, and sleek typography.
* **🧠 Intent-Based Length Orchestration:** Instead of outputting rigid, uniform paragraphs, the assistant automatically analyzes user intent to dynamically format responses:
  * **Short Mode (1–2 sentences):** Activated for casual greetings, basic calculations, single definitions, and binary lookups.
  * **Medium Mode (1–3 structured blocks):** Leveraged for multi-step "how-to" tasks, conceptual summaries, and explanations.
  * **Long Mode (Rich Layout):** Automatically triggered for deep-dive roadmaps, code generation scripts, system architectures, or extensive troubleshooting logs.
* **💾 Persistent Chat History database:** Built-in SQLite database engines record individual message logs mapped to distinct workflow threads, ensuring data is never lost when you close your browser.
* **🗑️ Granular Lifecycle Manipulation:** A sliding left-side historical manager panel allows users to quickly cycle through previous conversation logs or wipe out unwanted chat entries one by one using inline deletion mechanics.
* **⚡ Blazing Fast Compiler Execution:** Incorporates client-side `Marked.js` to parse raw incoming markdown text instantly into beautifully spaced headers, indented bullet trees, and clear bold tags.

---

## 📂 Project Directory Layout

```text
genai_flask_app/
│
├── app.py                 # Main Flask runtime engine, endpoints, and SQLite ORM
├── model.py               # LangChain inference pipelines and Groq SDK bindings
├── llm_test.py            # Isolated backend hardware connectivity utility
├── chat_history.db        # Automatically generated local SQLite database file
├── .gitignore             # Environment and private dependency exclusion manifest
└── README.md              # Production-grade project documentation
│
├── templates/
│   └── index.html         # Gemini flex-grid user viewport layout structure
│
└── static/
    ├── styles.css         # UI color palettes, glassmorphism layers, and typography rules
    └── script.js          # Asynchronous DOM manipulation, keystroke monitoring, & API hooks

---
# Create the local Python environment directory
python -m venv venv

# Activation on Windows (Command Prompt)
venv\Scripts\activate

# Activation on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activation on macOS / Linux
source venv/bin/activate
---
pip install flask langchain-groq langchain-core pydantic
python llm_test.py
python app.py
