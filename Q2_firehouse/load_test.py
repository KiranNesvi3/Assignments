import asyncio
import httpx
import time

URL = "http://127.0.0.1:8000/event"
TOTAL_REQUESTS = 1000
CONCURRENCY = 200

async def send_event(client,i):
    data = {
        "user_id":i,
        "timestamp":"2026-01-10T10:30:00Z",
        "metadata":{
            "page":"/home",
            "seq":i
        }
    }

    try:
        r = await client.post(URL,json=data,timeout=5)
        return r.status_code
    except Exception:
        return None
    
async def main():
    start = time.time()
    success = 0
    failed = 0

    async with httpx.AsyncClient() as client:
        tasks =[]

        for i in range(TOTAL_REQUESTS):
            tasks.append(send_event(client,i))
            if len(tasks)>=CONCURRENCY:
                results = await asyncio.gather(*tasks)
                for r in results:
                    if r == 202:
                        success+=1
                    else:
                        failed+=1
                tasks = []

        if tasks:
            results = await asyncio.gather(*tasks)
            for r in results:
                if r  == 202:
                    success+=1
                else:
                    failed+=1

    end = time.time()

    print("sent:",TOTAL_REQUESTS)
    print("Accepted:", success)
    print("Failed:",failed)
    print("Time:", round(end-start,2),"seconds")

if __name__ =="__main__":
    asyncio.run(main())      