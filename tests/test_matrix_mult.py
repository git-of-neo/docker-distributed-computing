#%%
import requests
import random
import numpy as np

randint = lambda : random.randint(1,3)

def send_request(matrix1, matrix2):
    url = "http://localhost:3000/api/multiply_matrix"
    payload = {
      "m1": {
        "data": matrix1
      },
      "m2": {
        "data": matrix2
      }
    }
    res = requests.post(url, json = payload).json()["data"]
    return res

def generate_matrix(row, col):
    return [
        [random.randint(-10,10) for _ in range(col)] for _ in range(row)
    ]

def test_matrix_multiplication(n = 20):
    for i in range(n):
        common_dim = randint()
        matrix1 = generate_matrix(randint(), common_dim)
        matrix2 = generate_matrix(common_dim, randint())
        res = send_request(matrix1, matrix2)
        ans = (np.array(matrix1).dot(np.array(matrix2))).tolist()
        if res != ans:
            print({
                "test case" : {
                    "m1" : matrix1,
                    "m2" : matrix2,
                    "given answer" : res,
                    "correct answer" : ans
                }
            })
            print("matrix mult FAILED")

    print("matrix mult PASS")

#%%
def run_tests():
    test_matrix_multiplication()

if __name__ == "__main__":
    run_tests()

#%%