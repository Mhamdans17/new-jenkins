pipeline {
    agent any

    environment {
        // Nama image docker (bebas, asal nyambung aja)
        IMAGE_NAME = "hello-jenkins-api"
        // Port yang mau di-publish ke luaran:port internal docker
        PORT_MAPPING = "8000:8000"
    }

    stages {
        stage('Ambil Kode') {
            steps {
                echo "Mengambil kode dari GitHub..."
                // Karena kita akan set URL GitHub-nya di settingan Job nanti, 
                // Jenkins otomatis nge-pull kodenya di tahap awal ini tanpa perlu checkout manual lagi.
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Mulai proses build Docker Image..."
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Deploy (Jalankan Container)') {
            steps {
                echo "Menjalankan aplikasi di dalam Docker Container..."
                
                // Mencegah error kalau nama container yang sama sudah nyala dari nge-build sebelumnya
                sh "docker stop ${IMAGE_NAME} || true"
                sh "docker rm ${IMAGE_NAME} || true"
                
                // Jalanin containernya di background (-d)
                sh "docker run -d --name ${IMAGE_NAME} -p ${PORT_MAPPING} ${IMAGE_NAME}"
                
                echo "🚀 Deploy Selesai! API menyala di port 8000"
            }
        }
    }
}
