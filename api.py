from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
import uvicorn
from hermex import HermexAssistant
# import requests


# class Query(BaseModel):
#     query: str


app = FastAPI()
hera = HermexAssistant()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat with the Ask-Moto chatbot.

    Args:
        websocket (WebSocket): The WebSocket connection.

    Returns:
        None
    """
    # user_id = websocket.query_params.get("user_id")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = hera.chat(query=data)  # user_id
        await websocket.send_text(response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)