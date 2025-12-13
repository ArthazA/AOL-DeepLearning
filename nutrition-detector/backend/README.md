YOU LOAD THE AI MODEL AT backend/model_loader.py
then arrange the output in backend/inference/predict.py:
    wich is for now is like image after categorize,
    the category found in string, (can make the )
    and the nutrition value wich is in{name: , value:}

to run the backend go to /backend and run this : uvicorn main:app --reload
but yeah u need to download this fest if u dont have : pip install fastapi uvicorn python-multipart (add it in README in the main page please thank yu)

