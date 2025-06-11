# main.py
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from core import StoryTeller
import uvicorn

# -------------------- Logging Config --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("hermex-assistant")

# -------------------- FastAPI Setup --------------------
app = FastAPI(title="Hermex Assistant API",
              description= "Hermex Assistant API for real-time chat",
              version="0.1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

herssa = StoryTeller()

# -------------------- WebSocket Endpoint --------------------


@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await websocket.accept()
    logger.info(f"✅ WebSocket connection opened for user: {user_id}")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"📩 Received from [{user_id}]: {data}")

            response = herssa.chat(user_id, data)

            logger.info(f"💬 Response to [{user_id}]: {response}")
            await websocket.send_text(response)
    except WebSocketDisconnect:
        logger.warning(f"🔌 WebSocket disconnected: {user_id}")
        # herssa.clear_chat_history(user_id)
        # logger.info(f"🗑️ Cleared chat history for user: {user_id}")
    except Exception as e:
        logger.error(f"❌ Error for user {user_id}: {e}", exc_info=True)
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, port=8000)