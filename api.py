from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
import uvicorn
from test import moto
# import requests


class Query(BaseModel):
    query: str


app = FastAPI()


@app.get("/")
def read_root():
    """
    Root endpoint of the Ask-Moto API.

    Returns:
        dict: A welcome message.
    """
    return {"Hello": "Welcome to the Ask-Moto API!"}


@app.post("/chatbot/")
def ask_moto(query: Query):
    """
    Chat with the Ask-Moto chatbot.

    Args:
        query_data (Query): The input query and chat logs.

    Returns:
        dict: The response from the chatbot.
    """
    try:
        response = moto(query.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

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
        response = moto(data)  # user_id
        await websocket.send_text(response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)