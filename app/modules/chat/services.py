from google import genai
from google.genai.errors import ServerError

from app.core.config import GEMINI_API_KEY
from app.modules.chat.models import ChatMessage


client = genai.Client(api_key=GEMINI_API_KEY)


def build_messages(history: list[ChatMessage]) -> list[dict]:
    """
    Convert chat history into LLM message format.
    """

    messages = []

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
    Generate AI response using Gemini.
    """

    prompt = (
        "You are a helpful AI assistant.\n\n"
    )

    for message in messages:
        prompt += f"{message['role']}: {message['content']}\n"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except ServerError:
        return (
            "Sorry, the AI service is temporarily unavailable. "
            "Please try again later."
        )