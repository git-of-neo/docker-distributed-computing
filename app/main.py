from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from jinja2 import Environment, FileSystemLoader
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import requests
import os

app = FastAPI()
environment = Environment(loader = FileSystemLoader("templates/"))

# hard-corded list of nodes in network
nodes = [
    "node1",
    "node2",
    "node3",
]
ports = ["3000", "3001", "3002"]

# list of allowed origins
origins = [f"http://{x}" for x in nodes]
origins.append("http://localhost")

# allow cross origin access
# reference : https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # allow cookies
    allow_methods=["*"], # allow all methods
    allow_headers=["*"], # allow all headers
)

class Row(BaseModel):
    data : List[int]

class Col(BaseModel):
    data : List[int]

# result of multiplication
class Point(BaseModel):
    value : int

class Matrix(BaseModel):
    data : List[List[int]]

class AliveResponse(BaseModel):
    alive : bool

@app.get("/", response_class = HTMLResponse)
async def root():
    template = environment.get_template("index.html")
    return template.render()

@app.post("/api/compute", response_model = Point)
async def compute(row: Row, col: Col):
    if len(row.data) != len(col.data):
        raise HTTPException(status_code = 400, detail = "row and column dimensions must match")
    res = sum([row.data[i] * col.data[i] for i in range(len(row.data))])
    return {"value" : res}

def is_uniform_row(matrix):
    row_size = lambda row : len(row)
    x = list(map(row_size, matrix))
    for i in range(len(x) - 1):
        if x[i]!=x[i+1]:
            return False
    return True

@app.post("/api/alive", response_model = AliveResponse)
async def is_alive():
    return {"alive" : True}

@app.post("/api/ping_neighbours", response_model = AliveResponse)
async def ping_neighbours():
    res = []
    for node_name, port in zip(nodes, ports):
        if node_name != os.environ["NODE_NAME"]: # skip self-check
            url = f"http://{node_name}:{port}/api/alive"
            res.append(requests.post(url).status_code==200)
    return {"alive" : all(res)}

# TODO : fix distribution
# referenced : https://stackoverflow.com/questions/63872924/how-can-i-send-an-http-request-from-my-fastapi-app-to-another-site-api
# for asynchronous requests
async def get_compute(client, url, json):
    res = await client.post(url, data = json)
    return res.json().value

async def distribute(matrix1, matrix2):
    # distribute workload (point based workload distribution, there are faster algorithms like fox algo but stick to basic for now)
    async with httpx.AsyncClient() as client:
        res = [[0] * len(matrix1)] * len(matrix2[0]) # collection to store results
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                flattened_index = i*len(matrix2[0]) + j 
                res[i][j] = get_compute(client, json = {
                    "row" : {
                        "data" : matrix1[i]
                    },
                    "col" : {
                        "data" : list(map(lambda x : x[j], matrix2))
                    }
                }, url = f"{origins[flattened_index % len(origins) ]}/compute")
        res = await asyncio.gather(*res)
    return res

@app.post("/api/multiply_matrix", response_model = Matrix)
# dot product
async def multiply_matrix(m1 : Matrix, m2 : Matrix):
    matrix1 = m1.data
    matrix2 = m2.data
    # validate matrices 
    if not (is_uniform_row(matrix1) and is_uniform_row(matrix2) and ( len(matrix1[0]) == len(matrix2) ) ):
        raise HTTPException(status_code = 400, detail = "matrix dimensions must match")
    
    res = await distribute(matrix1, matrix2)

    return {
        "data" : res
    }

# testing if hot reload is working as aspected
# @app.get("/something")
# async def something():
#     return {
#         "Loaded" : True
#     }

