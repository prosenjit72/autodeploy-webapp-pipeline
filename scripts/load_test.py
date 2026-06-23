import requests
import threading
import time

# minikube service taskmanager-service --url থেকে পাওয়া URL দাও
URL = "http://127.0.0.1:26093"  # তোমার actual URL দাও

def send_requests():
    while True:
        try:
            requests.get(URL)
        except:
            pass

# ১০টা thread একসাথে request পাঠাবে
threads = []
for i in range(10):
    t = threading.Thread(target=send_requests)
    t.daemon = True
    threads.append(t)
    t.start()

print("Load test started! Press Ctrl+C to stop")
time.sleep(120)  # ২ মিনিট চলবে
print("Load test finished!")