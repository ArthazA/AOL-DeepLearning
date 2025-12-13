from fastapi import FastAPI
from router.predict_router import router as predict_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers = ["*"],
)

os.makedirs("saved_images", exist_ok=True)
os.makedirs("categorized_images", exist_ok=True)

app.mount("/saved_images", StaticFiles(directory="saved_images"), name="saved_images")
app.mount("/categorized_images", StaticFiles(directory="categorized_images"), name="categorized_images")

app.include_router(predict_router, prefix="")

@app.get("/")
def home():
    return {"message": "FastAPI backend is running"}

