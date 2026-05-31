from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import uuid

from scraper import scrape_product_info
from pipeline import download_image
from processor import process_gear_image
from aligner import align_and_composite

app = FastAPI(title="MotoKombin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("final_outputs", exist_ok=True)
os.makedirs("temp_downloads", exist_ok=True)
app.mount("/images", StaticFiles(directory="final_outputs"), name="images")

class GearRequest(BaseModel):
    url: str
    type: str 

@app.post("/api/process-gear")
async def process_gear(request: GearRequest):
    print(f"\n[API İSTEĞİ] URL: {request.url} | TİP: {request.type}")
    
    data = scrape_product_info(request.url)
    if not data or not data.get("image_url"):
        raise HTTPException(status_code=400, detail="Görsel çekilemedi.")
    
    unique_id = str(uuid.uuid4())[:8]
    raw_path = f"temp_downloads/raw_{unique_id}.webp"
    clean_path = f"temp_downloads/clean_{unique_id}.png"
    final_path = f"final_outputs/aligned_{unique_id}.png" 
    
    success = download_image(data["image_url"], raw_path)
    if not success:
        raise HTTPException(status_code=500, detail="Görsel indirilemedi.")
        
    # Rembg ile arkaplanı sil
    process_gear_image(raw_path, clean_path)

    # Hizala
    align_and_composite(clean_path, final_path, request.type)
    
    return {
        "success": True,
        "price": data.get("price"),
        "image_url": f"http://127.0.0.1:8000/images/aligned_{unique_id}.png"
    }