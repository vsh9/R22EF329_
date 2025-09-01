import requests

class Logger:
    def __init__(self):
        self.log_api_url = "http://20.244.56.144/evaluation-service/logs"

    def log(self, stack, level, package, message):
        payload = {
            "stack": "backend",
            "level": "error",
            "package": "handler",
            "message": "received string, expected bool",
        }

        try:
            res = requests.post(self.log_api_url, json=payload, timeout=5)
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            print(f"[Logger] Logging failed: {e}")
            return None
