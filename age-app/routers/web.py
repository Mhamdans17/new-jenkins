import os
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.config import get_redis_client
from core.constants import AppConstants
import redis

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def read_root(request: Request):
    cache = get_redis_client()
    try:
        kunjungan = cache.incr(AppConstants.REDIS_HIT_KEY)
    except redis.exceptions.ConnectionError:
        kunjungan = AppConstants.REDIS_ERROR_MSG

    # Me-render template HTML menggunakan Jinja2
    return templates.TemplateResponse("index.html", {"request": request, "kunjungan": kunjungan})
