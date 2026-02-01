import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

a4f_api_key = os.getenv("A4F_API_KEY")
a4f_base_url = "https://api.a4f.co/v1"

client = OpenAI(base_url=a4f_base_url, api_key=a4f_api_key)

try:
    models = client.models.list()
    print("Available models:")
    for model in models.data:
        print(f"  - {model.id}")
except Exception as e:
    print(f"Error: {e}")
