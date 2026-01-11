This project trains a YOLOv8 object detection model to detect and classify fruits and vegetables.
The model was trained on roboflow dataset and evaluated using standard object detection metrics.

Roboflow Link: https://universe.roboflow.com/fvd-v4-with-split/fruits-and-vegetables-pufaj/dataset/2 VERSION 2 (Version 3 is classless, used for detection instead of classification)

The goal of this project is to demonstrate dataset preparation, model training, evaluation, inference using Ultralytics YOLO, along with Streamlit deployment to calculate the estimated total nutritional value of the submitted image of Fruits and Vegetables.

All available classes (fruits & vegetables) are as such:
names:
  0: apricot
  1: apple
  2: cauliflower
  3: corn
  4: cucumber
  5: custard_apple
  6: durian
  7: eggplant
  8: fig
  9: garlic
  10: grape
  11: hot_pepper
  12: avocado
  13: kiwi
  14: lemon
  15: mango
  16: melon
  17: onion
  18: orange
  19: papaya
  20: peach
  21: pear
  22: persimmon
  23: banana
  24: pineapple
  25: plum
  26: pomegranate
  27: potato
  28: pumpkin
  29: radish
  30: strawberry
  31: tomato
  32: turnip
  33: watermelon
  34: beetroot
  35: zucchini
  36: bell_pepper
  37: bitter_gourd
  38: broccoli
  39: cabbage
  40: carrot

This order is not random, could be a mistake from the authors or just impractical:
{0: '0', 1: '1', 2: '10', 3: '11', 4: '12', 5: '13', 6: '14', 7: '15', 8: '16', 9: '17', 10: '18', 11: '19', 12: '2', 13: '20', 14: '21', 15: '22', 16: '23', 17: '24', 18: '25', 19: '26', 20: '27', 21: '28', 22: '29', 23: '3', 24: '30', 25: '31', 26: '32', 27: '33', 28: '34', 29: '35', 30: '36', 31: '37', 32: '38', 33: '39', 34: '4', 35: '40', 36: '5', 37: '6', 38: '7', 39: '8', 40: '9'}