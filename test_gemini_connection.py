import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not found.")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)

print("Testing Gemini API connection...")

try:
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents="Reply with exactly: Gemini API connection successful."
    )

    if response.text:
        print("\nSUCCESS:")
        print(response.text)
    else:
        print("\nThe API responded, but the response was empty.")

except Exception as exc:
    print("\nGemini API request failed.")
    print(f"Error: {exc}")