# from model_loader.{file_name} import {model_name} as model
import os
import shutil

def run_all_models(image_path):
    os.makedirs("categorized_images", exist_ok=True)

    filename = os.path.basename(image_path)
    categorized_path = f"categorized_images/categorized_{filename}"

    # TEMP: just copy original image
    shutil.copy(image_path, categorized_path)
    #do something like this if you already have the image
    # cv2.imwrite(categorized_path, result_image)
    
    detected_items = "1 apple, 2 banana" # prob the result of prediction

    nutrition = [
        {"name": "carbohydrate", "value": "12g"},
        {"name": "vitamin A", "value": "30%"},
        {"name": "vitamin C", "value": "15%"}
    ]

    return {
        "image": categorized_path,
        "items": detected_items,
        "nutrition": nutrition
    }

