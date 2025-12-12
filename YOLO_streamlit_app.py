import streamlit as st
from ultralytics import YOLO, FastSAM
from PIL import Image
import numpy as np
import pandas as pd

# --- CONFIGURATION & MOCK DB ---
# Thresholds for heuristic sizing based on image area percentage
SMALL_THRESHOLD = 0.05  # Less than 5% of image = Small
LARGE_THRESHOLD = 0.15  # More than 15% of image = Large

# MOCK Nutrition DB (Replace with API later)
# Using generic COCO classes for demonstration. Replace/Add your custom classes here.
NUTRITION_DB = {
    'apple': {'base_calories': 95, 'unit': '1 medium'},
    'banana': {'base_calories': 105, 'unit': '1 medium'},
    'orange': {'base_calories': 62, 'unit': '1 medium'},
    'broccoli': {'base_calories': 50, 'unit': '1 cup chopped'},
    'carrot': {'base_calories': 30, 'unit': '1 medium'},
    # Fallback for items not in DB
    'default': {'base_calories': 50, 'unit': 'estimated serving'}
}

# List of COCO food classes to filter for in the demo model
COCO_FOOD_CLASSES = ['apple', 'banana', 'orange', 'broccoli', 'carrot', 'pizza', 'donut', 'cake']

# --- FUNCTIONS ---

@st.cache_resource
def load_models(det_model_path, seg_model_name):
    """
    Loads the detection model and the segmentation model.
    Cached so it only runs once.
    """
    # 1. Load your Trained YOLO Detection Model
    # REPLACE 'yolov8n.pt' with your custom weights path later: e.g., 'runs/detect/train/weights/best.pt'
    det_model = YOLO(det_model_path) 
    
    # 2. Load FastSAM for Segmentation
    # Ultralytics will auto-download 'FastSAM-s.pt' on first run
    seg_model = FastSAM(seg_model_name)
    
    return det_model, seg_model

def calculate_heuristic_size(mask_area_pixels, total_image_pixels):
    """Determines size label and multiplier based on area ratio."""
    ratio = mask_area_pixels / total_image_pixels
    
    if ratio < SMALL_THRESHOLD:
        return "Small", 0.7
    elif ratio > LARGE_THRESHOLD:
        return "Large", 1.3
    else:
        return "Medium", 1.0

# --- MAIN STREAMLIT APP ---
st.set_page_config(page_title="AI Food Scanner (FastSAM)", page_icon="🥑")
st.title("🥑 Nutritional Estimator (FastSAM Pipeline)")
st.write("This pipeline uses YOLOv8 to detect objects, then uses FastSAM to segment them and estimate size heuristically.")

# Load Models (using standard yolov8n for demo purposes)
try:
    with st.spinner("Loading AI Models... (First run may take a minute to download weights)"):
        # We use yolov8n.pt for detection demo, and FastSAM-s.pt for segmentation
        detector, segmentor = load_models('runs/detect/FNV_model/weights/best.pt', 'FastSAM-s.pt')
        st.success("Models Loaded!")
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# File Uploader
uploaded_file = st.file_uploader("Upload a food image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Pre-process image
    image_pil = Image.open(uploaded_file).convert("RGB")
    img_width, img_height = image_pil.size
    total_pixels = img_width * img_height
    
    col1, col2 = st.columns(2)
    with col1:
         st.image(image_pil, caption="Uploaded Image", use_column_width=True)

    # Analyze Button
    if st.button("Analyze Nutrition"):
        with st.spinner("Running Detection & Segmentation pipeline..."):
            # --- STEP 1: DETECTION ---
            # Run YOLOv8 detection to get bounding boxes
            # conf=0.4 filters out weak detections
            det_results = detector(image_pil, conf=0.4)
            det_boxes = det_results[0].boxes
            
            if len(det_boxes) == 0:
                st.warning("No objects detected.")
                st.stop()

            # Filter detection boxes to only include food classes we care about (for COCO demo)
            food_boxes = []
            food_classes = []
            for box in det_boxes:
                cls_id = int(box.cls[0])
                cls_name = detector.names[cls_id]
                if cls_name in COCO_FOOD_CLASSES:
                    food_boxes.append(box.xyxy[0]) # Append coordinates
                    food_classes.append(cls_name)
            
            if not food_boxes:
                 st.warning("Objects detected, but no matching food items found in database.")
                 st.stop()
                 
            # Convert list of tensors to a single tensor for FastSAM prompt
            import torch
            food_boxes_tensor = torch.stack(food_boxes)

            # --- STEP 2: SEGMENTATION WITH FASTSAM ---
            # Run FastSAM using the detected bounding boxes as prompts
            # bboxes prompt tells FastSAM exactly where to look
            sam_results = segmentor(image_pil, bboxes=food_boxes_tensor, retina_masks=True)
            
            # --- STEP 3: HEURISTIC CALCULATIONS ---
            total_calories_est = 0
            table_data = []

            # Iterate through the resulting masks
            # sam_results[0].masks corresponds to the prompted boxes in order
            if sam_results[0].masks is not None:
                masks_data = sam_results[0].masks.data.cpu().numpy() # Get masks as numpy arrays

                for i, mask_np in enumerate(masks_data):
                    class_name = food_classes[i]
                    
                    # Calculate mask area (sum of boolean pixels)
                    mask_pixels = mask_np.sum()
                    
                    # Determine heuristic size
                    size_label, multiplier = calculate_heuristic_size(mask_pixels, total_pixels)
                    
                    # Look up base nutrition and apply multiplier
                    nutri_info = NUTRITION_DB.get(class_name, NUTRITION_DB['default'])
                    base_cals = nutri_info['base_calories']
                    estimated_cals = int(base_cals * multiplier)
                    total_calories_est += estimated_cals
                    
                    table_data.append({
                        "Food Item": class_name.capitalize(),
                        "Heuristic Size": size_label,
                        "Multiplier": f"{multiplier}x",
                        "Est. Calories": estimated_cals
                    })
            
            with col2:
                # Display the FastSAM result plot
                # We plot the SAM result, which contains the segmentation masks
                st.image(sam_results[0].plot(), caption="Segmentation Masks", use_column_width=True)

            # --- RESULTS DISPLAY ---
            st.divider()
            st.header(f"Total Estimated Calories: ~{total_calories_est} kcal")
            
            df = pd.DataFrame(table_data)
            st.table(df)
            st.caption("Note: 'Size' is estimated based on how much of the image the object fills. This is a heuristic approximation.")