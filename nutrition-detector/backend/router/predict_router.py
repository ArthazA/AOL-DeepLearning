from fastapi import APIRouter, UploadFile, File
from inference.predict import run_all_models
from utils.timestamp import get_timestamp
import shutil, os

router = APIRouter()

@router.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):

    os.makedirs("saved_images", exist_ok=True)

    timestamp = get_timestamp()
    filename = f"{timestamp}_{file.filename}"
    img_path = f"saved_images/{filename}"

    with open(img_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = run_all_models(img_path)

    return {
        "timestamp": timestamp,
        "original_image": img_path,
        "categorized_image": results["image"],
        "items": results["items"],
        "nutrition": results["nutrition"]
    }

