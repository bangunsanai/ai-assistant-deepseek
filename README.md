# 🤖 AI Assistant - Personal AI Chatbot

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/bangunsanai/ai-assistant-deepseek/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)](https://www.python.org/)

**AI Assistant** adalah aplikasi chatbot pribadi yang dapat berjalan di **Windows (WSL)**, **Linux**, maupun **Android (Termux)**. Dilengkapi dengan **web interface** modern, **expert system**, dan **riwayat percakapan**.

> 🔑 **Mendukung Virtual API Key yang kompatibel dengan OpenAI API format.**

---

## ✨ Fitur

| Fitur | Keterangan |
| :--- | :--- |
| 💬 **Real-time Chat** | Web UI modern dengan dark mode |
| 🧠 **Expert System** | Pilih expert: Umum, Programmer, Penulis, Dokter |
| 📱 **Responsive Design** | Nyaman di HP maupun desktop |
| 🔄 **Multi Session** | History chat tersimpan (database) |
| 🎨 **Dark Mode** | Mata nyaman saat malam hari |
| 🚀 **Ringan & Cepat** | Bisa jalan di laptop RAM 4GB |

---

## 🛠️ Tech Stack

| Komponen | Teknologi |
| :--- | :--- |
| **Backend** | Python + Flask / FastAPI |
| **Frontend** | HTML, CSS, JavaScript (Vanilla) |
| **API** | OpenAI-compatible (Virtual API Key) |
| **Database** | SQLite (history chat) |

---

## 📦 Instalasi

### Prasyarat
- Python 3.10 atau lebih baru
- Virtual API Key (OpenAI-compatible format)

### Langkah-langkah

```bash
# 1. Clone repository
git clone https://github.com/bangunsanai/ai-assistant-deepseek.git
cd ai-assistant-deepseek

# 2. Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac/Termux
# atau
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Konfigurasi API Key
cp .env.example .env
nano .env  # isi API_KEY, BASE_URL, MODEL_NAME

# 5. Jalankan server
python main.py

# 6. Buka browser
# http://localhost:8000

================
Konfigurasi .env
================
# Virtual API Key (OpenAI-compatible)
API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# Base URL endpoint (dari penyedia layanan)
BASE_URL=https://api.your-provider.com/v1

# Nama model (default: deepseek-chat)
MODEL_NAME=deepseek-chat

##Struktur Proyek

ai-assistant-deepseek/
├── main.py              # Backend server
├── requirements.txt     # Dependencies
├── .env.example         # Template konfigurasi
├── .gitignore           # File yang diabaikan Git
├── static/
│   └── index.html       # Frontend web
└── README.md            # Dokumentasi ini


🎯 Endpoint API
Method	Endpoint	Deskripsi
GET	/	Halaman utama (frontend)
GET	/health	Cek status server
GET	/experts	Daftar expert yang tersedia
POST	/chat	Kirim pesan ke AI


📜 Lisensi

MIT License - Silakan digunakan, dimodifikasi, dan didistribusikan.

🙏 Credits

    API Gateway: [Virtual API Key Provider]

    AI Model: [DeepSeek V3.2 / sesuai provider]

📧 Kontak

    GitHub: @bangunsanai

    Email: bangunsan@gmail.com


⭐ Jangan lupa star repository ini jika bermanfaat!
