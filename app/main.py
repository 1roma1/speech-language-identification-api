from fastapi import FastAPI, UploadFile

from app.utils import read_file, json_load
from app.model import model


app = FastAPI()


@app.post("/predict")
def predict(file: UploadFile):
    langs = json_load("static/langs.json")
    lang_symb = list(langs.keys())

    data, _ = read_file(file)
    pred = model.predict(data)
    return {"language": langs[lang_symb[pred]]}
