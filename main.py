import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    # Ambil pesan dari environment variable, kalau tidak ada pakai pesan default
    pesan = os.getenv("MESSAGE", "Hello World! Message default nih dari Python.")
    return {"message": pesan}
