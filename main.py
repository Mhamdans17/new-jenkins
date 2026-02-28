import os
import redis
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Koneksi ke Redis
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        kunjungan = cache.incr('hits')
    except redis.exceptions.ConnectionError:
        kunjungan = "Error (Redis Mati)"

    # Ambil pesan dari Jenkins
    pesan = os.getenv("MESSAGE", "Default: Halo dari Python!")
    
    # Template HTML dengan Tailwind CSS dan gaya Glassmorphism
    html_content = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard Jenkins & Docker</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
            body {{
                font-family: 'Outfit', sans-serif;
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: #ffffff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0;
            }}
            .glass {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 1.5rem;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            }}
            .counter-text {{
                background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
        </style>
    </head>
    <body class="p-4">
        <div class="glass max-w-2xl w-full p-10 text-center transition-transform transform hover:scale-105 duration-300">
            <h1 class="text-4xl font-extrabold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
                🚀 Misi Selesai!
            </h1>
            <p class="text-lg text-gray-300 mb-8 tracking-wide">Jenkins CI/CD + Docker + Redis + FastAPI</p>
            
            <!-- Box Pesan Jenkins -->
            <div class="bg-black/30 rounded-xl p-6 mb-8 border border-white/10">
                <span class="text-sm uppercase tracking-widest text-gray-400 font-semibold mb-2 block">Pesan dari Jenkins Parameter</span>
                <p class="text-2xl font-bold text-yellow-300">"{pesan}"</p>
            </div>
            
            <!-- Hit Counter -->
            <div class="mb-8">
                <h2 class="text-xl text-gray-300 font-semibold">Total Pengunjung Web</h2>
                <div class="text-8xl font-black counter-text my-4 drop-shadow-lg">
                    {kunjungan}
                </div>
                <p class="text-sm text-gray-400 italic">Refresh browser-mu (F5) untuk melihat angkanya naik!</p>
            </div>
            
            <div class="mt-10 pt-6 border-t border-white/10 flex justify-between items-center text-sm text-gray-400">
                <span>Dideploy otomatis via Github Push</span>
                <span class="flex items-center gap-2">
                    <span class="animate-pulse h-2 w-2 bg-green-500 rounded-full"></span>
                    Server Online
                </span>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content
