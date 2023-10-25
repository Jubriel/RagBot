from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from test import moto

class Query(BaseModel):
    query: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Ask-Moto API!"}

@app.post("/chatbot/")
def ask_moto(query:str):
    try:
        response = moto(query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)