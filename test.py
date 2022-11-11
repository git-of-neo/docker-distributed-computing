import requests

url = "http://127.0.0.1:3000/api/compute"
json = {
  "row": {
    "data": [
      0,1
    ]
  },
  "col": {
    "data": [
      0,1
    ]
  }
}

res = requests.post(url, json = json)
print(res.text)