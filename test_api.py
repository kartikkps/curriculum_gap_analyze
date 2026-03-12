import requests
import time

def test_api():
    print("Waiting for server to start...")
    time.sleep(2)
    
    url = "http://127.0.0.1:8000/analyze"
    payload = {
        "target_curriculum": "Python Basics\nData Types\nLoops\nFunctions\nClasses",
        "student_curriculum": "Python Basics\nData Types\nLoops",
        "seed": 42
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Analysis Result:")
        print(response.json())
        
        run_id = response.json().get("run_id")
        if run_id:
            print(f"\nFetching logs for run_id: {run_id}")
            log_url = f"http://127.0.0.1:8000/runs/{run_id}"
            log_response = requests.get(log_url)
            log_response.raise_for_status()
            logs = log_response.json().get("logs", [])
            print(f"Found {len(logs)} log entries.")
            for log in logs[:3]:
                print(log)
            print("...")
            
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    test_api()
