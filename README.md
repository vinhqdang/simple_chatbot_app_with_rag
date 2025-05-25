# Chatbot Application

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/vinhqdang/simple_chatbot_app_with_rag.git
   cd simple_chatbot_app_with_rag
   ```

2. Install Conda (if not already installed). You can install Miniconda by
   following the instructions at <https://docs.conda.io/en/latest/miniconda.html>.

3. Create a conda environment:
   ```bash
   conda create -n chatbot python=3.10 -y
   conda activate chatbot
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure API key:
   - Copy `config.json.example` to `config.json`
   - Edit `config.json` and set your OpenAI API key.
   - Optionally adjust `system_prompt` in the config to change the assistant behaviour.
   - If you don't have an OpenAI key, leave it blank and select the HuggingFace provider when chatting.

6. Run the application:
   ```bash
   python app.py
   ```

7. Access in browser at http://127.0.0.1:5000

## Features

- User registration and login
- Chatbot with GPT-4o multi-modal support (text and image)
- Session management: create and delete chat sessions
