from app.routers.tasks import router as task_router
from fastapi import FastAPI
from datetime import datetime, timezone


app = FastAPI()

app.include_router(task_router, prefix="/api/v1/tasks", tags=["Tasks"])

@app.get("/")
async def index():
    return {"status": "ok", "time": datetime.now(timezone.utc)}
