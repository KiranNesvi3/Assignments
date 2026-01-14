# Firehouse Collector 

> **A high-performance, async event ingestion system built for speed and reliability.**

Welcome to the **Firehouse Collector** project! This repository showcases a robust solution for handling high-throughput data streams without breaking a sweat. It demonstrates how to decouple data ingestion from storage to achieve maximize performance.

##  What does it do?

Imagine thousands of sensors or users sending data to your server at the exact same millisecond. A traditional server might freeze or crash trying to save everything to the database at once.

**Firehouse Collector** solves this by acting like a smart buffer:
1.  **Catch**: It instantly accepts the data via a fast API.
2.  **Queue**: It drops the data into a memory safe-zone (Queue).
3.  **Batch**: A background worker picks up the data in chunks and saves it efficiently to the database.

It's like having a dedicated receptionist who takes all the calls and a separate team filing the paperwork—so the phone line is never busy!

##  Key Features

-   **High Concurrency**: Built on **FastAPI** and **Asyncio** to handle thousands of requests per second.
-   **Non-Blocking I/O**: The API never waits for the database. It responds "Accepted" immediately.
-   **Batch Processing**: Writes to **SQLite** in batches (default: 200 events) to drastically reduce disk operations.
-   **Backpressure Handling**: Includes a queue limit (30k) to prevent memory overflows if the system gets overwhelmed.

##  The Tech Stack

-   **Language**: Python 3.10+
-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Database**: SQLite (built-in, efficient for embedded use)
-   **Testing**: HTTPX (for async load testing)

##  Project Structure

-   `app.py`: The main entry point. Defines the API endpoints.
-   `event_queue.py`: Manages the async queue (the buffer).
-   `storage.py`: Handles database connections and batch writing logic.
-   `load_test.py`: A custom script to stress-test the system with concurrent traffic.

##  Getting Started

Follow these simple steps to get Firehouse running on your machine.

### 1. Prerequisites
Make sure you have Python installed.

### 2. Install Dependencies
You'll need `fastapi`, `uvicorn` (to run the server), and `httpx` (for testing).

```bash
pip install fastapi uvicorn httpx
```

### 3. Run the Server
Start the Firehouse collector:

```bash
uvicorn app:app --reload
```
You should see: `Starting Firehose...` in your terminal.

##  heavy_check_mark Performance Testing

We've proved the concept with a load tester. 

Open a new terminal and run:

```bash
python load_test.py
```

This script fires **1000 requests** with **200 concurrent users** to simulate a traffic spike.  
Watch how the server accepts them all instantly, while the background writer quietly saves them to `events.db`.
