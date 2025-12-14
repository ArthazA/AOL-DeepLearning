import streamlit as st
import numpy as np
import cv2
import json
import pandas as pd
from ultralytics import YOLO
from pathlib import Path

st.set_page_config(
    page_title="Fruit & Vegetable Nutrition Estimator",
    layout="wide"
)

st.title("Fruit & Vegetable Nutrition Estimator")
st.write(
    "Upload an image containing fruits and vegetables. "
    "The app detects each item and estimates the total nutritional value."
)

ROOT = Path.cwd().parent
MODEL_PATH = ROOT / "runs" / "yolov11_fnv_correct_p1" / "weights" / "best.pt"
NUTRITION_100G_PATH = ROOT / "nutrition" / "nutrition_per_100g.json"
AVG_WEIGHTS_PATH = ROOT / "nutrition" / "avg_weights.json"

@st.cache_resource
def load_model():
    return YOLO(str(MODEL_PATH))

@st.cache_data
def load_nutrition_data():
    with open(NUTRITION_100G_PATH) as f:
        nutrition_100g = json.load(f)
    with open(AVG_WEIGHTS_PATH) as f:
        avg_weights = json.load(f)
    return nutrition_100g, avg_weights


model = load_model()
nutrition_100g, avg_weights = load_nutrition_data()

st.subheader("DEBUG — YOLO class names")
st.write(model.names)
st.stop()


def get_color(conf):
    if conf >= 0.8:
        return (0, 255, 0)
    elif conf >= 0.5:
        return (0, 255, 255)
    return (0, 0, 255)


def run_detection(image, conf_thresh=0.4):
    results = model(image, conf=conf_thresh)[0]
    detections = []

    for box in results.boxes:
        cls_id = int(box.cls.item())
        detections.append({
            "class_id": cls_id,
            "class_name": results.names[cls_id],
            "confidence": float(box.conf.item()),
            "bbox": box.xyxy.cpu().numpy().astype(int)[0]
        })

    return detections


def draw_boxes(image, detections):
    img = image.copy()

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        conf = det["confidence"]
        label = f'{det["class_name"]} {conf:.2f}'
        color = get_color(conf)

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            img, label, (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
        )

    return img


def count_items(detections, conf_thresh=0.4):
    counts = {}
    for det in detections:
        if det["confidence"] >= conf_thresh:
            name = det["class_name"]
            counts[name] = counts.get(name, 0) + 1
    return counts


def compute_nutrition(counts):
    rows = []
    totals = {"Calories": 0, "Carbs (g)": 0, "Protein (g)": 0, "Fat (g)": 0, "Fiber (g)": 0}

    for item, count in counts.items():
        if item not in nutrition_100g or item not in avg_weights:
            continue

        weight = avg_weights[item] * count
        factor = weight / 100.0
        per100 = nutrition_100g[item]

        calories = per100["calories"] * factor
        carbs = per100["carbs"] * factor
        protein = per100["protein"] * factor
        fat = per100["fat"] * factor
        # fiber = per100["fiber"] * factor
        fiber = per100.get("fiber", 0) * factor

        rows.append({
            "Item": item,
            "Count": count,
            "Estimated Weight (g)": weight,
            "Calories": calories,
            "Carbs (g)": carbs,
            "Protein (g)": protein,
            "Fat (g)": fat,
            "Fiber (g)": fiber
        })

        totals["Calories"] += calories
        totals["Carbs (g)"] += carbs
        totals["Protein (g)"] += protein
        totals["Fat (g)"] += fat
        totals["Fiber (g)"] += fiber

    return pd.DataFrame(rows), totals


uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

conf_threshold = st.slider(
    "Confidence Threshold",
    min_value=0.1,
    max_value=0.9,
    value=0.4,
    step=0.05
)

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    detections = run_detection(image_rgb, conf_threshold)
    counts = count_items(detections, conf_threshold)
    annotated_img = draw_boxes(image_rgb, detections)

    # st.subheader("🔍 DEBUG: Raw detections")
    # st.write(detections)
    # st.write(counts)
    # st.stop()
    # st.write("DEBUG — counts dictionary:", counts) # why class name not show plz PLZLPLPZ
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Detected Items")
        st.image(annotated_img, use_container_width=True)

    with col2:
        st.subheader("Item Counts")
        if counts:
            counts_df = (
            pd.DataFrame.from_dict(counts, orient="index", columns=["Count"])
                .reset_index()
                .rename(columns={"index": "Item"})
            )
            st.dataframe(counts_df)

        else:
            st.info("No items detected above the confidence threshold.")

    if counts:
        nutrition_df, totals = compute_nutrition(counts)

        st.subheader("Nutritional Breakdown")
        st.dataframe(nutrition_df)

        st.subheader("Total Estimated Nutrition")
        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Calories", f"{totals['Calories']:.1f} kcal")
        c2.metric("Carbs", f"{totals['Carbs (g)']:.1f} g")
        c3.metric("Protein", f"{totals['Protein (g)']:.1f} g")
        c4.metric("Fat", f"{totals['Fat (g)']:.1f} g")
        c5.metric("Fiber", f"{totals['Fiber (g)']:.1f} g")
