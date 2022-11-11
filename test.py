#%%
from app.main import is_uniform_row
import random
import requests
import numpy as np

#%%
def test_is_uniform_row(n = 20):
  def generate_uniform_row(row_length = random.randint(2,10)):
      return [ [random.randint(0,99) for _ in range(row_length)] for _ in range(random.randint(2,10)) ]
    
  def generate_non_uniform_row(row_length = random.randint(2,10)):
      return [ [random.randint(0,99) for _ in range(row_length+i)] for i in range(random.randint(2,10)) ]

  uniform_rows = [
    generate_uniform_row() for _ in range(n//2)
  ]

  non_uniform_rows = [
    generate_non_uniform_row() for _ in range(n//2)
  ]

  assert all(map(lambda x : is_uniform_row(x), uniform_rows)), "uniforms not true"
  assert not any(map(lambda x : is_uniform_row(x), non_uniform_rows)), "non uniforms not true"
  print("is_uniform_row PASS")

#%% 
def test_matrix_multiplication(n = 20):
  url = "http://localhost:3000/api/multiply_matrix"
  randint = lambda : random.randint(1,3)

  def one_test():
    common_dim = randint()

    matrix1_np = np.ndarray((randint(),common_dim), dtype=np.int8) 
    matrix1 = matrix1_np.tolist()

    matrix2_np = np.ndarray((common_dim, randint()), dtype=np.int8) 
    matrix2 = matrix2_np.tolist()

    res_np = matrix1_np.dot(matrix2_np).tolist()

    payload = {
      "m1": {
        "data": matrix1
      },
      "m2": {
        "data": matrix2
      }
    }

    res = requests.post(url, json = payload).json()["data"]
    passed = res == res_np
    if not passed:
      print(res)
      print(matrix1_np, matrix2_np, sep = "\n\n")
    return passed

  test_res = [one_test() for _ in range(n)]

  assert all(test_res), "matrix mult FAIL"
  print("matrix mult PASS")
    
def run_tests():
  test_is_uniform_row()
  test_matrix_multiplication(n=1)

if __name__ == "__main__":
  run_tests()