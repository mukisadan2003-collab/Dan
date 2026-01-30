# Dan - Work Smart Ai (Kivy Starter)

Overview

Dan is an AI-powered mobile app (Kivy) targeting Ugandan business owners and local users. This starter branch provides a Kivy app skeleton, Ollama-local integration hooks, and feature stubs for:

- Local Business Opportunity Finder
- Ugandan Market Analysis & Insights
- AI-Powered Business Plan Generator
- Competitor Analysis & Comparison
- Business Registration Guide for Uganda
- AI-Powered Revenue Prediction Tool
- Supplier/Vendor Finder
- AI Business Assistant Chatbot

Prerequisites

- Python 3.10+
- Pip
- Ollama running locally and accessible at http://localhost:11434 (recommended)
  - Recommended model name: "local-llm" (adjust in ai/ollama_client.py)

Setup (local development)

1. Clone the repo and checkout the branch:

   git clone https://github.com/mukisadan2003-collab/Dan.git
   cd Dan
   git checkout feature/kivy-starter

2. Create a virtual environment and install dependencies:

   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate    # Windows
   pip install -r requirements.txt

3. Run the app:

   python main.py

Ollama

This starter expects Ollama to be running locally. Example installation & running is outside scope; see https://ollama.com/docs for details.

Mobile builds

- Android: Use Buildozer to package the Kivy app (see Buildozer docs).
- iOS: Packaging Kivy apps for iOS is more involved; refer to Kivy and BeeWare docs.

What is included

- Kivy app skeleton (main.py, main.kv)
- Ollama client wrapper (ai/ollama_client.py)
- Feature modules with stubs you can extend
- SQLite helper (models/db.py)

Next steps

- Replace stubs with real data integration (UBOS APIs, supplier directories)
- Improve UI and UX
- Add tests and CI
