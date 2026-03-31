from fastapi import FastAPI
from datetime import datetime


app = FastAPI()


@app.get("/")
async def index():
    return {"status": "ok", "time": datetime.now()}
