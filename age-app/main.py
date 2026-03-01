from fastapi import FastAPI
from routers import api, web
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from core.config import get_redis_client

# Inisialisasi Rate Limiter dengan SlowAPI & Redis
redis_client = get_redis_client()
limiter = Limiter(key_func=get_remote_address, storage_uri="redis://redis:6379/")

app = FastAPI(title="API Kalkulator Umur Modern")

# Daftarkan penanganan Exception otomatis pas kena Limit
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Daftarkan Router (MVC Approach)
app.include_router(web.router)
app.include_router(api.router)
