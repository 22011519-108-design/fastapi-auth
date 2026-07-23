from app.modules.rag.services import search_documents
from app.modules.chat.services import generate_response


def run_policy_agent(query: str):
    """
    Policy Agent.

    Answers library policy and knowledge-base questions
    using RAG + Groq.
    """

    results = search_documents(
        query=query,
        k=5,
        retrieval="hybrid"
    )

    if not results:
        return "I couldn't find any relevant information in the library knowledge base."

    context = ""

    for item in results:
        metadata = item["metadata"]

        context += (
            f"Title: {metadata['title']}\n"
            f"Content: {metadata['text']}\n\n"
        )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful library assistant.\n"
                "Answer ONLY from the provided context.\n"
                "If the answer is not in the context, say you don't know."
            ),
        },
        {
            "role": "system",
            "content": context,
        },
        {
            "role": "user",
            "content": query,
        },
    ]

    return generate_response(messages)