import os
from dotenv import load_dotenv

load_dotenv("api.env")   # For local development

API_KEY = os.getenv("GROQ_API_KEY")

BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "llama-3.3-70b-versatile"