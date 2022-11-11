"""
Not full tester, only to check interaction from within the containers
"""
import httpx
import requests
import json

url = f"http://node2:3001/api/compute"
data1 = {
  "row": {
    "data": [
      0
    ]
  },
  "col": {
    "data": [
      0
    ]
  }
}
data1 = json.dumps(data1)

# res = requests.post(url, json = data)
# print(res)
r = httpx.post(url, data = data1)
print(r.text)
print(r.headers)
print(r.json()["value"])
# print(httpx.get(url.strip("/api/compute")))