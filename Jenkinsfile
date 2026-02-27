pipeline {
    agent any

    // 1. Definisikan parameter yang bisa diisi manual oleh user saat nge-klik "Build with Parameters"
    parameters {
        string(name: 'PESAN_BEBAS', defaultValue: 'Halo dari Jenkins pakai Docker Compose!', description: 'Ketik pesan apa saja yang mau ditampilkan di web API')
    }

    environment {
        // 2. Hubungkan Parameter Jenkins ke Environment Variable system
        MESSAGE = "${params.PESAN_BEBAS}"
    }

    stages {
        stage('Ambil Kode') {
            steps {
                echo "Source Code ditarik otomatis oleh Jenkins dari GitHub..."
                sh 'ls -la'
            }
        }

        stage('Build & Deploy with Docker Compose') {
            steps {
                echo "Bikin Image dan Langsung Jalanin Container pakai Compose!"
                
                // Matikan service lama kalau ada, lalu build ulang dan jalankan (-d)
                sh 'docker-compose down'
                sh 'docker-compose up -d --build'
                                
                echo "🚀 Aplikasi berhasil dijalankan dengan pesan kustom: ${MESSAGE}"
            }
        }
    }
}
