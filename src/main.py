import json
import extract
from typing import Union
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

CACHE_PATH = '/opt/app/mnt/data/temp.json'

class SessionManager:
    def __init__(self):
        self._session = {}

    def set(self, key: str, value: any):
        self._session[key] = value

    def get(self, key: str, default: any = None):
        return self._session.get(key, default)

    def clear(self):
        self._session.clear()

session_manager = SessionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.set("data", extract.pull_food_cache(CACHE_PATH))
    print("Application is starting...")
    yield
    session_manager.clear()
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)

def get_session():
    return session_manager

@app.get("/items/")
async def read_root(session: SessionManager = Depends(get_session)):
    return {"message": "Hello, World!", "session": session.get("data")}

@app.get("/items/{item_id}")
async def read_root( item_id: str , q: Union[str, None] = None 
                    , session: SessionManager = Depends(get_session)):
    return {"message": item_id, "q": session.get("data")[item_id]}


@app.post("/items/")
async def update_session(new_data: dict, session: SessionManager = Depends(get_session)):
    session.set("data", new_data)
    return {"message": "Session updated", "session": session.get("data")}