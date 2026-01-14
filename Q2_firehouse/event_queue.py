import asyncio
event_queue = asyncio.Queue(maxsize=30_000)

async def enqueue_event(event):
    try:
        event_queue.put_nowait(event)
    except asyncio.QueueFull:
        raise

async def get_batch(batch_size:int):
    items = []
    for _ in range(batch_size):
        try:
            item = event_queue.get_nowait()
            items.append(item)
        except asyncio.QueueEmpty:
            break
    return items