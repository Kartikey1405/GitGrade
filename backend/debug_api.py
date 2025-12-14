import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"DEBUG: API Key Loaded? {'YES' if api_key else 'NO'}")
if api_key:
    print(f"DEBUG: Key starts with: {api_key[:5]}...")

genai.configure(api_key=api_key)

print("\n--- QUERYING AVAILABLE MODELS ---")
try:
    # We list ALL models to see what you have access to
    count = 0
    for m in genai.list_models():
        count += 1
        print(f"FOUND: {m.name}")
        # Check if it supports content generation (text)
        if 'generateContent' in m.supported_generation_methods:
            print(f"   -> Supports generateContent (OK to use)")
    
    if count == 0:
        print("\n[ERROR] Connection successful, but NO models returned.")
        print("POSSIBLE CAUSE: 'Google Generative Language API' is not enabled in your Google Cloud Console.")

except Exception as e:
    print(f"\n[CRITICAL ERROR] Connection Failed: {e}")