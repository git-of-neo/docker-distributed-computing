from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from jinja2 import Environment, FileSystemLoader

app = FastAPI()
environment = Environment(loader = FileSystemLoader("templates/"))

class Row(BaseModel):
    data : List[int]

class Col(BaseModel):
    data : List[int]

# result of multiplication
class Point(BaseModel):
    value : int

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

# @app.get("/something")
# async def something():
#     return {
#         "Loaded" : True
#     }

