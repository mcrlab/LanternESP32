import requests
import time

try:
    while True:
        r = requests.post("http://localhost/lights", json={"color":"FF0000", "time":1000})
        time.sleep(0.5)
        print(r.status_code)
        r = requests.post("http://localhost/lights", json={"color":"00FF00", "time":1000})
        time.sleep(0.5)
        print(r.status_code)
        r = requests.post("http://localhost/lights", json={"color":"0000FF", "time":1000})
        time.sleep(0.5)
        print(r.status_code)
except KeyboardInterrupt:
    print("ending")
