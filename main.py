#!/usr/bin/env python3
"""
AI Assistant Backend - Provider Agnostic
Mendukung Virtual API Key yang kompatibel dengan OpenAI API format.
"""

import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

# ==================== KONFIGURASI API (SEMUA DARI .env) ====================
# Tidak ada hardcoded provider! Semua dari environment variable.
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")  # User harus mengisi sendiri
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat")

# Validasi konfigurasi (opsional)
if not API_KEY:
    print("⚠️ PERINGATAN: API_KEY tidak ditemukan di file .env")
if not BASE_URL:
    print("⚠️ PERINGATAN: BASE_URL tidak ditemukan di file .env")

# ==================== EXPERT SYSTEM ====================
BUILTIN_EXPERTS = {
    "default": {
        "name": "Asisten Umum",
        "icon": "🤖",
        "system_prompt": "Kamu adalah asisten AI yang ramah dan membantu."
    },
    "programmer": {
        "name": "Programmer",
        "icon": "💻",
        "system_prompt": "Kamu adalah expert programmer. Fokus pada kode dan algoritma."
    },
    "writer": {
        "name": "Penulis",
        "icon": "✍️",
        "system_prompt": "Kamu adalah asisten penulis kreatif."
    },
    "doctor": {
        "name": "Dokter",
        "icon": "🏥",
        "system_prompt": "Kamu adalah asisten medis. Ini hanya saran umum."
    }
}

# ==================== FASTAPI APP ====================
app = FastAPI(title="AI Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    expert: Optional[str] = "default"
    history: Optional[List[dict]] = []
    model: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    expert_name: str
    expert_icon: str

# ==================== ENDPOINTS ====================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "api_configured": bool(API_KEY and BASE_URL)
    }

@app.get("/experts")
def get_experts():
    return BUILTIN_EXPERTS

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not API_KEY or not BASE_URL:
        raise HTTPException(status_code=500, detail="API not configured. Check .env file.")
    
    expert = BUILTIN_EXPERTS.get(request.expert, BUILTIN_EXPERTS["default"])
    
    messages = [{"role": "system", "content": expert["system_prompt"]}]
    if request.history:
        messages.extend(request.history)
    messages.append({"role": "user", "content": request.message})
    
    model = request.model or MODEL_NAME
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 8000
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                jawaban = result["choices"][0]["message"]["content"]
                return ChatResponse(
                    response=jawaban,
                    expert_name=expert["name"],
                    expert_icon=expert["icon"]
                )
            else:
                raise HTTPException(status_code=response.status_code, detail="API Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
