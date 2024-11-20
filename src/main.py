from typing import Union

from fastapi import FastAPI

import json
import extract

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items")
def read_root():
#def read_  read_item():
    file_path = "/opt/app/mnt/data/temp.json"
    food2 = extract.pull_food_cache(file_path)
    return {"items": food2}

@app.get("/items/{item_id}")
def read_item(item_id: str, q: Union[str, None] = None):
    file_path = "/opt/app/mnt/data/temp.json"
    food2 = extract.pull_food_cache(file_path)
    return {"item_id": item_id, "q": food2[item_id]}
