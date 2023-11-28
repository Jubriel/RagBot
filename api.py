from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
from test_3 import moto

class Query(BaseModel):
    query: str

app = FastAPI(title= "Ask-Moto Chatbot API",
    description= "Motopay assistant",
    version= "0.1.0",)

@app.get("/")
def read_root():
    """
    Root endpoint of the Ask-Moto API.

    Returns:
        dict: A welcome message.
    """
    return {"Hello": "Welcome to the Ask-Moto API!"}

@app.post("/chatbot/")
def ask_moto(Query = Body(...)):
    """
    Chat with the Ask-Moto chatbot.

    Args:
        Query (str): The input query.

    Returns:
       str: The response from the chatbot.
    """
    try:
        response = moto(Query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)