import time

from groq import Groq

from app.core.config import GROQ_API_KEY
from app.modules.chat.models import ChatMessage

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are a helpful AI assistant.

Instructions:
- Answer clearly and accurately.
- Be polite and professional.
- Maintain conversation context.
- If you don't know the answer, say so instead of guessing.
"""


def build_messages(history: list[ChatMessage]) -> list[dict]:
    """
    Convert chat history into LLM message format.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for msg in history:
        messages.append(
            {
                "role": msg.role,
                "content": msg.content
            }
        )

    return messages


def generate_response(messages: list[dict]) -> str:
    """
    Generate AI response using Groq.
    """

    for attempt in range(3):

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

            usage = response.usage

            print("=" * 50)
            print("Prompt Tokens:", usage.prompt_tokens)
            print("Completion Tokens:", usage.completion_tokens)
            print("Total Tokens:", usage.total_tokens)
            print("=" * 50)

            return response.choices[0].message.content

        except Exception as e:

            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return (
                    "Sorry, the AI service is temporarily unavailable. "
                    "Please try again later."
                )