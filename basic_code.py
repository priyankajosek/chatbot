import time

from google import genai
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

client = genai.Client()

conversation = []
def chat(user_message):

    conversation.append({"role": "user", "parts": [{"text": user_message}]})
   
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=conversation
            )
            if not getattr(response, "text", None):
                raise RuntimeError("The model returned an empty response.")
            reply =  response.text
        except Exception as error:
            is_service_unavailable = (
                getattr(error, "status_code", None) == 503
                or "503" in str(error)
                or "high demand" in str(error).lower()
            )
            if not is_service_unavailable:
                raise
            if attempt == 2:
                raise RuntimeError(
                    "Gemini is still unavailable due to high demand. "
                    "Please try again later."
                ) from error
            time.sleep(2 ** attempt)
    conversation.append({"role": "assistant", "parts": [{"text": reply}]})
    return reply
print(chat("What is the capital of France?"))
print(chat("What is the capital I asked for?"))