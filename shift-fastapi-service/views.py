import logging
from datetime import date

from app import app
from exceptions import DataNotFoundException
from fastapi import HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from repository import get_user_by_id

logger = logging.getLogger(__name__)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return RedirectResponse(url="/404")


@app.get("/404", status_code=status.HTTP_404_NOT_FOUND)
async def not_found() -> dict[str, str]:
    return {"message": "Resource Not Found"}




