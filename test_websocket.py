import asyncio
import json
import os
import urllib.parse
import urllib.request

import websockets
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def websocket_base_url(http_base_url: str) -> str:
    if http_base_url.startswith("https://"):
        return "wss://" + http_base_url[len("https://"):]

    if http_base_url.startswith("http://"):
        return "ws://" + http_base_url[len("http://"):]

    return http_base_url


def get_access_token() -> str:
    token = os.getenv("ACCESS_TOKEN")

    if token:
        return token

    email = os.getenv("TEST_EMAIL")
    password = os.getenv("TEST_PASSWORD")

    if not email or not password:
        raise RuntimeError(
            "Set ACCESS_TOKEN or both TEST_EMAIL and TEST_PASSWORD to run "
            "the WebSocket smoke test."
        )

    payload = json.dumps(
        {
            "email": email,
            "password": password
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        f"{BASE_URL}/login",
        data=payload,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["access_token"]


async def test():
    token = get_access_token()
    ws_base_url = websocket_base_url(BASE_URL)
    uri = f"{ws_base_url}/ws?token={urllib.parse.quote(token)}"

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")

        history_message = await websocket.recv()
        print("Initial response:", history_message)

        await websocket.send(
            json.dumps(
                {
                    "type": "message",
                    "content": "Hello Server"
                }
            )
        )

        response = await websocket.recv()
        print("Server response:", response)


asyncio.run(test())
