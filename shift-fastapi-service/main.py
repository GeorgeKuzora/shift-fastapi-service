import logging

from fastapi import FastAPI, status

logging.basicConfig(filename="logs/main.log", level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/404", status_code=status.HTTP_404_NOT_FOUND)
def not_found() -> dict[str, str]:
    return {"message": "Resource Not Found"}


@app.get("/")
def read_root():
    return {"Hello": "World"}
