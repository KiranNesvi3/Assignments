import sqlite3
import asyncio
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class TransactionRequest(BaseModel):
    user_id: int
    amount: float

def init_db():
    conn = sqlite3.connect('ledger.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, balance REAL, role TEXT)''')
    
    c.execute("SELECT count(*) FROM users")
    if c.fetchone()[0] == 0:
        users = [
            (1, 'alice', 100.0, 'user'),
            (2, 'bob', 50.0, 'user'),
            (3, 'admin', 9999.0, 'admin'),
            (4, 'charlie', 10.0, 'user')
        ]
        c.executemany("INSERT OR IGNORE INTO users (id, username, balance, role) VALUES (?, ?, ?, ?)", users)
        conn.commit()
    conn.close()

init_db()

@app.get('/search')
async def search_users(q: str):
    """
    Search for a user by username.
    Usage: GET /search?q=alice
    """
    if not q:
        raise HTTPException(status_code=400, detail="Missing query parameter")

    query_sql = "SELECT id, username, role FROM users WHERE username = ?"
    
    try:
        conn = sqlite3.connect('ledger.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query_sql, (q,))
        results = cursor.fetchall()
        
        data = [{"id": r["id"], "username": r["username"], "role": r["role"]} for r in results]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post('/transaction')
async def process_transaction(transaction: TransactionRequest):
    """
    Deducts money from a user's balance.
    Body: {"user_id": 1, "amount": 25.0}
    """
    await asyncio.sleep(3)
    
    try:
        conn = sqlite3.connect('ledger.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT balance FROM users WHERE id = ?", (transaction.user_id,))
        row = cursor.fetchone()
        
        if not row:
             raise HTTPException(status_code=404, detail="User not found")
        
        cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", 
                       (transaction.amount, transaction.user_id))
        
        if cursor.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=400, detail="Transaction failed")
            
        conn.commit()
        return {"status": "processed", "deducted": transaction.amount}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
