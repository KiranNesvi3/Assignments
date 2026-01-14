from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import Any,Dict
from datetime import datetime
import asyncio
from storage import init_db, batch_writer
from event_queue import enqueue_event

app = FastAPI(title = "Firehouse Collector")

@app.on_event("startup")
async def startup_event():
    print("Starting Firehose...")
    init_db()
    asyncio.create_task(batch_writer())

class Event(BaseModel):
    user_id: int
    timestamp: datetime
    metadata: Dict[str,Any]

@app.post("/event",status_code= 202)
async def collect_event(event:Event):
    try:
        await enqueue_event(event.model_dump())
    except Exception:
        raise HTTPException(status_code=503,detail="Queue is full,Try again later")
    return {"status":"accepted"}  