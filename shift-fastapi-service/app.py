from fastapi import FastAPI
from logs import init_logging

init_logging()

app = FastAPI()
