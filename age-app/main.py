import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import date

app = FastAPI(title="API Kalkulator Umur Modern")

# Koneksi ke Redis
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

class UmurRequest(BaseModel):
    tahun: int
    bulan: int
    tanggal: int

def kalkulasi_umur(tahun: int, bulan: int, tanggal: int):
    today = date.today()
    try:
        birth_date = date(tahun, bulan, tanggal)
    except ValueError:
        raise HTTPException(status_code=400, detail="Tanggal tidak valid!")

    if birth_date > today:
        raise HTTPException(status_code=400, detail="Kok ngisi tanggal masa depan? Mesin waktu belum diciptakan! 🤖")

    umur_tahun = today.year - birth_date.year
    umur_bulan = today.month - birth_date.month

    if today.day < birth_date.day:
        umur_bulan -= 1

    if umur_bulan < 0:
        umur_tahun -= 1
        umur_bulan += 12

    return umur_tahun, umur_bulan

@app.get("/hitung")
def hitung_umur_get(tahun: int, bulan: int, tanggal: int):
    umur_tahun, umur_bulan = kalkulasi_umur(tahun, bulan, tanggal)
    return {
        "status": "Sukses",
        "hasil": f"{umur_tahun} Tahun, {umur_bulan} Bulan",
        "umur_tahun": umur_tahun
    }

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        kunjungan = cache.incr('hits_umur')
    except redis.exceptions.ConnectionError:
        kunjungan = "Error (Redis Mati)"

    html_content = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <!-- SEO Primary Meta Tags -->
        <title>Kalkulator Umur Online | Hitung Usia Akurat & Cepat</title>
        <meta name="title" content="Kalkulator Umur Online | Hitung Usia Akurat & Cepat">
        <meta name="description" content="Hitung umur kamu secara akurat berdasarkan tahun, bulan, dan tanggal lahir secara gratis dengan kalkulator umur online paling kekinian tahun ini. Cepat dan instan!">
        <meta name="keywords" content="hitung umur, kalkulator umur, hitung usia, umur saya berapa, umur berjalan, cek umur, kalkulator usia online, tahun lahir">
        <meta name="author" content="ImTokyoDev">
        <meta name="robots" content="index, follow">

        <!-- Open Graph / Facebook -->
        <meta property="og:type" content="website">
        <meta property="og:url" content="https://umur.imtokyodev.cloud/">
        <meta property="og:title" content="Kalkulator Umur Online Kekinian">
        <meta property="og:description" content="Hitung umur kamu secara akurat berdasarkan tahun, bulan, dan tanggal lahir. Gratis tanpa iklan!">
        
        <!-- JSON-LD Structured Data for Google -->
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "WebApplication",
          "name": "Kalkulator Umur Kekinian",
          "description": "Aplikasi Web untuk menghitung umur dengan akurasi tahun dan bulan berdasarkan tanggal lahir.",
          "applicationCategory": "UtilitiesApplication",
          "operatingSystem": "All"
        }
        </script>

        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #fff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0;
            }
            .glass-panel {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            .input-glass {
                background: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: white;
            }
            .input-glass:focus {
                outline: none;
                border-color: rgba(255, 255, 255, 0.5);
                background: rgba(0, 0, 0, 0.3);
            }
            ::-webkit-calendar-picker-indicator {
                filter: invert(1);
                cursor: pointer;
            }
        </style>
    </head>
    <body class="p-4">

        <main class="glass-panel p-8 md:p-10 max-w-lg w-full text-center" itemscope itemtype="https://schema.org/SoftwareApplication">
            <h1 itemprop="name" class="text-3xl font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-green-300 to-blue-400">
                ⏳ Kalkulator Umur
            </h1>
            <p itemprop="description" class="text-sm text-gray-300 mb-6 tracking-wide">Hitung usia pasti kamu di tahun berjalan, 100% Akurat!</p>

            <div class="mb-8 bg-black/20 rounded-full py-1.5 px-4 inline-block border border-white/10 shadow-inner">
                <span class="text-xs text-gray-300 flex items-center gap-2">
                    <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                    Telah diuji oleh <strong class="text-green-300 ml-1">{KUNJUNGAN_COUNT}</strong> orang
                </span>
            </div>

            <form id="ageForm" class="space-y-6">
                <div class="flex flex-col text-left">
                    <label for="tanggalLahir" class="text-sm font-semibold text-gray-200 mb-2">Pilih Tanggal Lahir Kamu</label>
                    <input type="date" id="tanggalLahir" required
                        class="input-glass rounded-xl px-4 py-3 w-full transition-all duration-300 focus:ring-2 focus:ring-blue-400">
                </div>
                
                <button type="submit" 
                    class="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-bold py-3 px-4 rounded-xl shadow-lg transform transition hover:scale-105 active:scale-95 duration-200">
                    Hitung Umur Saya! ✨
                </button>
            </form>

            <!-- Loading Spinner -->
            <div id="loading" class="mt-8 hidden">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto"></div>
            </div>

            <!-- Tempat Hasil -->
            <div id="resultBox" class="mt-8 hidden opacity-0 transition-opacity duration-500">
                <div class="p-6 bg-white/5 rounded-2xl border border-white/10">
                    <p class="text-sm text-gray-300 uppercase tracking-widest mb-1">Sekarang Umurmu Adalah:</p>
                    <div id="hasilTeks" class="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-orange-400 my-3">
                        -
                    </div>
                    <p id="pesanTambahan" class="text-xs text-gray-300 italic mt-2">Masih muda, semangat terus! 💪</p>
                </div>
            </div>
            
        </main>

        <script>
            document.getElementById('ageForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const dobInput = document.getElementById('tanggalLahir').value;
                if(!dobInput) return;

                const resultBox = document.getElementById('resultBox');
                resultBox.classList.add('hidden', 'opacity-0');
                
                const loading = document.getElementById('loading');
                loading.classList.remove('hidden');

                const dateObj = new Date(dobInput);
                const tahun = dateObj.getFullYear();
                const bulan = dateObj.getMonth() + 1;
                const tanggal = dateObj.getDate();

                try {
                    const response = await fetch(`/hitung?tahun=${tahun}&bulan=${bulan}&tanggal=${tanggal}`);
                    const data = await response.json();
                    
                    loading.classList.add('hidden');
                    
                    if(!response.ok) {
                        alert(data.detail || 'Terjadi kesalahan!');
                        return;
                    }

                    document.getElementById('hasilTeks').innerText = data.hasil;
                    
                    // Pemanis Berdasarkan Umur
                    let pesan = "Tetap semangat menikmati hidup! 🌟";
                    let warna = "text-gray-300";
                    if(data.umur_tahun < 17) {
                        pesan = "Masih di bawah umur! Fokus belajar ya biar pintar 📚";
                        warna = "text-green-300";
                    }
                    else if(data.umur_tahun >= 17 && data.umur_tahun < 30) {
                        pesan = "Lagi masa emas nih, Gas pol asah skill dan karier! 🚀";
                        warna = "text-blue-300";
                    }
                    else if(data.umur_tahun >= 30 && data.umur_tahun < 50) {
                        pesan = "Sudah matang! Jaga work-life balance dan kesehatan mental ya ☕";
                        warna = "text-purple-300";
                    }
                    else if(data.umur_tahun >= 50) {
                        pesan = "Wah udah senior nih, yang penting sehat-sehat selalu Mbah/Kek! 🍵";
                        warna = "text-yellow-300";
                    }
                    
                    const textEl = document.getElementById('pesanTambahan');
                    textEl.innerText = pesan;
                    textEl.className = `text-xs italic mt-2 ${warna}`;

                    resultBox.classList.remove('hidden');
                    setTimeout(() => resultBox.classList.remove('opacity-0'), 50);

                } catch (error) {
                    loading.classList.add('hidden');
                    alert("Gagal menghubungi server API. Koneksi terputus.");
                }
            });
        </script>
    </body>
    </html>
    """
    return html_content.replace("{KUNJUNGAN_COUNT}", str(kunjungan))
