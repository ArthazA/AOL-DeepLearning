This project trains a YOLOv8 object detection model to detect and classify fruits and vegetables.
The model was trained on roboflow dataset and evaluated using standard object detection metrics.

Roboflow Link: https://universe.roboflow.com/fvd-v4-with-split/fruits-and-vegetables-pufaj VERSION 2 (VERSION 3 IS FAULTY)

The goal of this project is to demonstrate dataset preparation, model training, evaluation, inference using Ultralytics YOLO, along with Streamlit deployment to calculate the estimated total nutritional value of the submitted image of Fruits and Vegetables.

All available classes (fruits & vegetables) are as such:
names:
  0: apricot
  1: apple
  2: avocado
  3: banana
  4: beetroot
  5: bell_pepper
  6: bitter_gourd
  7: broccoli
  8: cabbage
  9: carrot
  10: cauliflower
  11: corn
  12: cucumber
  13: custard_apple
  14: durian
  15: eggplant
  16: fig
  17: garlic
  18: grape
  19: hot_pepper
  20: kiwi
  21: lemon
  22: mango
  23: melon
  24: onion
  25: orange
  26: papaya
  27: peach
  28: pear
  29: persimmon
  30: pineapple
  31: plum
  32: pomegranate
  33: potato
  34: pumpkin
  35: radish
  36: strawberry
  37: tomato
  38: turnip
  39: watermelon
  40: zucchini

*these are obtained and altered from the `data.yaml` file and rewritten anew into the same file