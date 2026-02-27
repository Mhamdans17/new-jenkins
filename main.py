import os
import redis
from fastapi import FastAPI

app = FastAPI()

# Koneksi ke Redis. Nama host 'redis' akan di-resolve oleh Docker Compose
# ke container yang menjalankan service bernama 'redis'.
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.get("/")
def read_root():
    try:
        # Menaikkan angka hit (kunjungan) sebesar 1 setiap kali website dibuka
        kunjungan = cache.incr('hits')
    except redis.exceptions.ConnectionError:
        kunjungan = "<i>(Redis belum menyala)</i>"

    # Ambil pesan dari environment variable
    pesan = os.getenv("MESSAGE", "Hello World! Message default nih dari Python.")
    
    return {
        "message": pesan,
        "pengunjung_ke": kunjungan,
        "info": "Refresh halaman ini untuk melihat angkanya bertambah terus berkat Database Redis!"
    }
