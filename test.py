import requests

url = "http://localhost:3002/api/compute"
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
print(res.json()["value"])

#%%
# from app.main import is_uniform_row
# import random

# def test_is_uniform_row(n = 20):
#   def generate_uniform_row(row_length = random.randint(2,10)):
#       return [ [random.randint(0,99) for _ in range(row_length)] for _ in range(random.randint(2,10)) ]
    
#   def generate_non_uniform_row(row_length = random.randint(2,10)):
#       return [ [random.randint(0,99) for _ in range(row_length+i)] for i in range(random.randint(2,10)) ]

#   uniform_rows = [
#     generate_uniform_row() for _ in range(n//2)
#   ]

#   non_uniform_rows = [
#     generate_non_uniform_row() for _ in range(n//2)
#   ]

#   assert all(map(lambda x : is_uniform_row(x), uniform_rows)), "uniforms not true"
#   assert not any(map(lambda x : is_uniform_row(x), non_uniform_rows)), "non uniforms not true"
#   print("is_uniform_row PASS")

# if __name__ == "__main__":
#   test_is_uniform_row()