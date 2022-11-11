from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from jinja2 import Environment, FileSystemLoader
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
environment = Environment(loader = FileSystemLoader("templates/"))

# list of allowed origins
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
]

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

@app.post("/api/multiply_matrix", response_model = Matrix)
# dot product
async def multiply_matrix(m1 : Matrix, m2 : Matrix):
    matrix1 = m1.data
    matrix2 = m2.data
    # validate matrices 
    if not (is_uniform_row(matrix1) and is_uniform_row(matrix2) and ( len(matrix1[0]) == len(matrix2) ) ):
        raise HTTPException(status_code = 400, detail = "matrix dimensions must match")
    
    # distribute workload (point based workload distribution, there are faster algorithms like fox algo but stick to basic for now)
    

    pass

# testing if hot reload is working as aspected
# @app.get("/something")
# async def something():
#     return {
#         "Loaded" : True
#     }

