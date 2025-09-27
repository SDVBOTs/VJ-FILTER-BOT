from fastapi import FastAPI
from pydantic import BaseModel
import secrets
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware add karein
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for file mappings
file_mappings = {}

class FileRequest(BaseModel):
    file_id: str

@app.post("/generate_temp_url")
async def generate_temp_url(request: FileRequest):
    # Generate unique temporary ID
    temp_id = secrets.token_urlsafe(16)
    
    # Store mapping
    file_mappings[temp_id] = {
        "original_id": request.file_id,
        "created_at": datetime.now(),
        "used": False
    }
    
    # Cleanup old entries
    cleanup_expired_mappings()
    
    # Bot username yahan set karein
    bot_username = "SDV_PW_Token_gen_bot"  # 👈 APNA BOT USERNAME DALEN
    temp_url = f"https://t.me/{bot_username}?start={temp_id}"
    
    return {
        "temp_url": temp_url,
        "temp_id": temp_id
    }

@app.get("/get_original_id/{temp_id}")
async def get_original_id(temp_id: str):
    """Get original file ID and mark as used"""
    if temp_id in file_mappings:
        if not file_mappings[temp_id]["used"]:
            file_mappings[temp_id]["used"] = True
            return {"original_id": file_mappings[temp_id]["original_id"], "status": "success"}
        else:
            return {"original_id": None, "status": "already_used"}
    return {"original_id": None, "status": "not_found"}

@app.get("/")
async def root():
    return {"message": "Temporary URL API is running"}

def cleanup_expired_mappings():
    """Remove mappings older than 24 hours"""
    current_time = datetime.now()
    expired_keys = []
    
    for temp_id, mapping in file_mappings.items():
        if current_time - mapping["created_at"] > timedelta(hours=24):
            expired_keys.append(temp_id)
    
    for key in expired_keys:
        del file_mappings[key]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)