from fastapi import FastAPI
from pydantic import BaseModel
import secrets
from datetime import datetime, timedelta
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Temporary storage for file mappings
file_mappings = {}

# GET method bhi add karein for easy testing
@app.get("/generate_temp_url")
async def generate_temp_url_get(file_id: str = None):
    if not file_id:
        return {"error": "file_id parameter required"}
    
    # Generate unique temporary ID
    temp_id = secrets.token_urlsafe(16)
    
    # Store mapping
    file_mappings[temp_id] = {
        "original_id": file_id,
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
        "temp_id": temp_id,
        "original_id": file_id
    }

@app.post("/generate_temp_url")
async def generate_temp_url_post(request: dict = None):
    if not request or 'file_id' not in request:
        return {"error": "file_id required in JSON body"}
    
    file_id = request['file_id']
    
    # Generate unique temporary ID
    temp_id = secrets.token_urlsafe(16)
    
    # Store mapping
    file_mappings[temp_id] = {
        "original_id": file_id,
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
        "temp_id": temp_id,
        "original_id": file_id
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

@app.get("/test")
async def test():
    return {"status": "working", "timestamp": datetime.now().isoformat()}

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
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)