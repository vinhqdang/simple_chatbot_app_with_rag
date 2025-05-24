import json
from pathlib import Path

config_path = Path(__file__).parent / 'config.json'
if not config_path.exists():
    raise FileNotFoundError("Config file not found. Please create config.json based on config.json.example.")
with open(config_path) as f:
    data = json.load(f)
API_KEY = data.get("api_key")
MODEL = data.get("model", "gpt-4o")
HF_MODEL = "distilgpt2"
