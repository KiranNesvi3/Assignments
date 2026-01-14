
# Inventory System

Welcome! This project is a simple yet powerful demonstration of handling **high concurrency** in web applications. We set out to solve a classic problem: **preventing overselling** when thousands of users try to buy the last few items simultaneously. 

##  The Problem
Imagine a flash sale. You have 100 items, but 1,000 customers hit "Buy" at the exact same millisecond. In a standard system, race conditions would cause you to sell more items than you actually have. Chaos, right?

##  The Solution
We built a robust API using **FastAPI** and **PostgreSQL** that guarantees data consistency. 

By implementing **Row-Level Locking** (using `with_for_update` in SQLAlchemy), we ensure that the database locks the specific inventory row during a transaction. This forces requests to queue up for that split second, ensuring that **1 item implies 1 sale**—no matter the traffic load.

##  Tech Stack
- **FastAPI**: For a lightning-fast web server.
- **PostgreSQL**: For reliable, ACID-compliant storage.
- **SQLAlchemy**: For elegant database interactions.
- **Python**: Because it's awesome.

##  What's Inside?
- `app.py`: The core API with the safely locked `/buy_ticket` endpoint.
- `proof_of_correctness.py`: A stress-testing script. It fires **1,000 concurrent requests** at our server to prove that exactly 100 items are sold, and not a single one more.

##  How to Run It

1.  **Start the Database**: Ensure you have PostgreSQL running and the `DATABASE_URL` set in `database.py`.
2.  **Run the App**:
    ```bash
    uvicorn app:app --reload
    ```
3.  **Witness the Magic**: Run the proof script to stress test the system:
    ```bash
    python proof_of_correctness.py
    ```

You'll see it process all requests and finish with exactly **100 Success** and **900 Sold Out**. Perfection. 
