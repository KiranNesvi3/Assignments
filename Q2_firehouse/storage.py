import asyncio
import sqlite3
import json
from event_queue import get_batch

DB_FILE = "events.db"
BATCH_SIZE = 200


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TEXT,
            metadata TEXT
        )
    """)
    conn.commit()
    conn.close()


def write_batch_to_db(batch):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for event in batch:
        cursor.execute(
            "INSERT INTO events (user_id, timestamp, metadata) VALUES (?, ?, ?)",
            (
                event["user_id"],
                event["timestamp"],
                json.dumps(event["metadata"])
            )
        )

    conn.commit()
    conn.close()


async def batch_writer():
    print("Batch writer started")

    while True:
        try:
            batch = await get_batch(BATCH_SIZE)

            if not batch:
                await asyncio.sleep(0.1)
                continue

            await asyncio.to_thread(write_batch_to_db, batch)

            print(f"Wrote {len(batch)} events to DB")

        except Exception as e:
            print("DB error:", e)
            await asyncio.sleep(1)
