import requests
import concurrent.futures
import time

URL = "http://localhost:8000/buy_ticket"
TOTAL_REQUESTS = 1000
CONCURRENCY = 100

def buy_ticket(i):
    try:
        response = requests.post(URL)
        return response.status_code
    except Exception as e:
        return f"Error: {e}"
    
def main():
    print(f"Starting {TOTAL_REQUESTS} requests with {CONCURRENCY} concurrent workers...")
    time.sleep(2)

    start_time = time.time()
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers = CONCURRENCY) as executor:
        futures = [executor.submit(buy_ticket,i) for i in range(TOTAL_REQUESTS)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    duration = time.time() - start_time
    print(f"Finished in {duration:.2f} seconds.")

    success_count = results.count(200)
    sold_out_count = results.count(410)
    errors = [r for r in results if r!=200 and r!=410]

    print(f"Success (200 OK): {success_count}")
    print(f"Sold Out (410 GONE): {sold_out_count}")
    print(f"Other/Errors: {len(errors)}")

    if errors:
        print(f"Sample Errors: {errors[:5]}")
    if success_count == 100 and sold_out_count == (TOTAL_REQUESTS - 100):
        print("SUCCESS: Exactly 100 items sold.")
    else:
        print("FAILURE: Incorrect counts.")

if __name__ == "__main__":
    main()
    
