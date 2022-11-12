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
import json

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
# origins = [f"http://{x}" for x in nodes]
# origins.append("http://localhost")
origins = ["*"] # HOTFIX : allow from all origins, never do this in production environment

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

async def compute_point(client, node_no : int, row : List[int], col : List[int]):
    payload = {
        "row" : {
            "data" : row
        }, 
        "col" : {
            "data" : col
        }, 
    }
    payload = json.dumps(payload)
    port = ports[node_no]
    response = await client.post(f"http://{nodes[node_no]}:{port}/api/compute", data = payload)
    return response.json()["value"]

async def distribute(m1 : List[List[int]], m2 : List[List[int]]):
    row = len(m1)
    col = len(m2[0])
    n = row * col
    unflatten_index = lambda x : (x//col, x % col)
    get_col = lambda x, j : list(map(lambda row : row[j], x))
    
    task_per_node = max(n // len(nodes), 1)
    
    async with httpx.AsyncClient() as client:
        tasks = []
        for task_no in range(n):
            node_no = min(task_no // task_per_node, len(nodes)-1)
            i, j = unflatten_index(task_no)
            tasks.append(compute_point(client, node_no, m1[i], get_col(m2, j)))
        res = await asyncio.gather(*tasks)

    # format into matrix
    return [ res[(i * col) : (i * col + col)] for i in range(row)] # <-- format error]

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
