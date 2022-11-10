from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Row(BaseModel):
    data : List[int]

class Col(BaseModel):
    data : List[int]

# result of multiplication
class Point(BaseModel):
    value : int

@app.get("/")
async def root():
    return {
        "Loaded" : True
    }

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
