from fastapi import APIRouter, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from services.calculator import hitung_umur_detail
from core.constants import ErrorMessages, AppConstants

router = APIRouter()
limiter = Limiter(key_func=get_remote_address, storage_uri="redis://redis:6379/")

class UmurRequest(BaseModel):
    tahun: int
    bulan: int
    tanggal: int

@router.get("/hitung")
@limiter.limit("5/minute")
def hitung_umur_get(request: Request, tahun: int, bulan: int, tanggal: int):
    # Menggunakan fungsi terpisah dari services
    umur_tahun, umur_bulan = hitung_umur_detail(tahun, bulan, tanggal)
    
    return {
        "status": ErrorMessages.API_SUCCESS_STATUS,
        "hasil": AppConstants.AGE_RESULT_FORMAT.format(tahun=umur_tahun, bulan=umur_bulan),
        "umur_tahun": umur_tahun
    }
