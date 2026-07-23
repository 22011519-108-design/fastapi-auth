from sqlalchemy.orm import Session

from app.modules.agents.catalog_agent import run_catalog_agent
from app.modules.agents.policy_agent import run_policy_agent


MAX_HOPS = 3
ORCHESTRATOR_PROMPT = """
You are a routing agent.

Your job is ONLY to decide which specialist should handle a request.

Available specialists:
1. Catalog Agent:
   - searching books
   - availability
   - borrowing
   - returning
   - borrowed books

2. Policy Agent:
   - library rules
   - policies
   - general library knowledge

Never answer the user directly.
Only route the request.
"""

def call_catalog_agent(
    tool_name: str,
    arguments,
    db: Session
):
    """
    Tool wrapper for Catalog Agent.
    """

    return run_catalog_agent(
        tool_name=tool_name,
        arguments=arguments,
        db=db
    )


def call_policy_agent(
    query: str
):
    """
    Tool wrapper for Policy Agent.
    """

    return run_policy_agent(
        query=query
    )


def run_orchestrator(
    agent_type: str,
    payload,
    db: Session | None = None,
):
    """
    Main router.

    Decides which specialist should handle the request.
    """

    if agent_type == "catalog":

        return call_catalog_agent(
            tool_name=payload["tool"],
            arguments=payload["arguments"],
            db=db
        )

    if agent_type == "policy":

        return call_policy_agent(
            query=payload["query"]
        )

    return {
        "success": False,
        "message": "Unable to route request."
    }

def classify_request(message: str) -> str:
    """
    Decide which agent should handle the request.
    """

    catalog_keywords = [
        "book",
        "search",
        "find",
        "borrow",
        "return",
        "available",
        "availability",
        "my books",
        "borrowed",
    ]

    policy_keywords = [
        "policy",
        "rule",
        "limit",
        "library timing",
        "fine",
        "late",
        "membership",
    ]

    text = message.lower()

    for keyword in catalog_keywords:
        if keyword in text:
            return "catalog"

    for keyword in policy_keywords:
        if keyword in text:
            return "policy"

    return "policy"