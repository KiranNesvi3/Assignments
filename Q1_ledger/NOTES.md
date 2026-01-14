# Refactoring Notes

Here's a breakdown of the issues I found in the legacy codebase and how I fixed them to meet production standards.

## 1. Security Vulnerabilities
**The Problem:**
The original search endpoint was extremely vulnerable to **SQL Injection**. The query was built using f-strings (`f"SELECT ... WHERE username = '{query}'"`), which meant anyone could manipulate the database by injecting malicious SQL code into the `q` parameter.

**The Fix:**
I switched to **parameterized queries** (using `?` placeholders). This ensures the database treats the input strictly as data, not executable code, completely neutralizing the vulnerability.

## 2. Performance Issues
**The Problem:**
The application was suffering from severe blocking. The `process_transaction` endpoint used `time.sleep(3)` to simulate banking delays. In a synchronous framework like Flask (as it was used), this freezes the entire worker process for 3 seconds, making the API unresponsive to other distinct requests during that time.

**The Solution:**
I migrated the application to **FastAPI**, which supports asynchronous request handling out of the box. By replacing `time.sleep(3)` with `await asyncio.sleep(3)`, the server can now "pause" the specific request without blocking the main event loop. This allows it to handle thousands of other incoming requests while waiting for the "banking core" to respond, massively improving throughput.

## 3. Data Integrity
**The Problem:**
The original update logic was "blind"—it didn't check if the user actually existed or had enough funds before trying to deduct money.

**The Fix:**
I added a check to verify the user exists and has a sufficient balance before processing the transaction. The update is now performed transactionally, ensuring that we don't end up with inconsistent states.
