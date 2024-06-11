# websocket_manager.py
from fastapi import WebSocket
from typing import List

clients: List[WebSocket] = []

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"Client disconnected: {e}")
    finally:
        clients.remove(websocket)

async def notify_clients(message: str):
    for client in clients:
        await client.send_text(message)
