import logging

from fastapi import FastAPI

logging.basicConfig(filename="logs/main.log", level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
