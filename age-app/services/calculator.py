from datetime import date
from fastapi import HTTPException
from core.constants import ErrorMessages

def hitung_umur_detail(tahun: int, bulan: int, tanggal: int):
    today = date.today()
    try:
        birth_date = date(tahun, bulan, tanggal)
    except ValueError:
        raise HTTPException(status_code=400, detail=ErrorMessages.INVALID_DATE)

    if birth_date > today:
        raise HTTPException(status_code=400, detail=ErrorMessages.FUTURE_DATE)

    umur_tahun = today.year - birth_date.year
    umur_bulan = today.month - birth_date.month

    if today.day < birth_date.day:
        umur_bulan -= 1
        

    if umur_bulan < 0:
        umur_tahun -= 1
        umur_bulan += 12

    return umur_tahun, umur_bulan
