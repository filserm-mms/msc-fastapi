from fastapi import FastAPI, Depends
from fastapi.param_functions import Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey
from dependencies import get_api_key
from routers import articles

app = FastAPI()

app.include_router(articles.router)

@app.get("/")
def read_root():
    return {"key": "value"}
