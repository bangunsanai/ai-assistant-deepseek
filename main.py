#!/usr/bin/env python3
"""
Backend AI Server dengan FastAPI
Terintegrasi dengan KoboiLLM API (DeepSeek V3.2)
"""

import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv

# Load API Key dari .env
load_dotenv()

API_KEY = os.getenv("KOBOILLM_API_KEY")
BASE_URL = "https://api.koboillm.com/v1"
DEFAULT_MODEL = "vertex_ai/deepseek-ai/deepseek-v3.2-maas"

# Expert bawaan
BUILTIN_EXPERTS = {
    "default": {
        "name": "Asisten Umum",
        "icon": "🤖",
        "system_prompt": "Kamu adalah asisten AI yang ramah dan membantu. Jawab pertanyaan dengan jelas dan akurat."
    },
    "programmer": {
        "name": "Expert Programmer",
        "icon": "💻",
        "system_prompt": "Kamu adalah expert programmer berpengalaman. Fokus pada kode, algoritma, dan best practices. Berikan contoh kode jika memungkinkan."
    },
    "writer": {
        "name": "Asisten Penulis",
        "icon": "✍️",
        "system_prompt": "Kamu adalah asisten penulis kreatif. Bantu dengan ide cerita, gaya bahasa, editing, dan struktur tulisan."
    },
    "doctor": {
        "name": "Konsultan Medis",
        "icon": "🏥",
        "system_prompt": "Kamu adalah asisten medis yang membantu. Ingat: ini hanya saran umum, bukan diagnosis medis."
    }
}

# Inisialisasi FastAPI
app = FastAPI(title="AI Assistant API", description="Backend AI dengan KoboiLLM (DeepSeek V3.2)")

# CORS - izinkan akses dari browser mana pun
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models untuk request/response
class ChatRequest(BaseModel):
    message: str
    expert: Optional[str] = "default"
    history: Optional[List[dict]] = []
    model: Optional[str] = DEFAULT_MODEL

class ChatResponse(BaseModel):
    response: str
    expert_name: str
    expert_icon: str

# ==================== ENDPOINTS API ====================

@app.get("/health")
def health():
    """Cek status backend"""
    return {"status": "healthy", "api_key_loaded": bool(API_KEY)}

@app.get("/experts")
def get_experts():
    """Dapatkan daftar semua expert"""
    return BUILTIN_EXPERTS

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint chat dengan expert system"""
    
    # Ambil expert yang diminta
    expert = BUILTIN_EXPERTS.get(request.expert, BUILTIN_EXPERTS["default"])
    
    # Siapkan messages dengan system prompt
    messages = [
        {"role": "system", "content": expert["system_prompt"]}
    ]
    
    # Tambahkan history jika ada
    if request.history:
        messages.extend(request.history)
    
    # Tambahkan pesan user
    messages.append({"role": "user", "content": request.message})
    
    # Panggil API KoboiLLM
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": request.model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
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
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"API Error: {response.text}"
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/simple")
async def chat_simple(request: ChatRequest):
    """Endpoint chat sederhana tanpa expert system"""
    
    messages = [{"role": "user", "content": request.message}]
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": request.model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
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
                return {"response": result["choices"][0]["message"]["content"]}
            else:
                raise HTTPException(status_code=response.status_code, detail="API Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== SERVING FRONTEND ====================
# Mount static files (harus di paling bawah agar tidak bentrok dengan endpoint API)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# ==================== MAIN ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
