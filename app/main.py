from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv

from app.utils import read_file, json_load, load_configuration
from app.model import Model

load_dotenv()

app = FastAPI()
model = Model(config=load_configuration("config.yaml"))
model.load()


@app.post("/predict")
def predict(file: UploadFile):
    langs = json_load("static/langs.json")
    lang_symb = list(langs.keys())

    data, _ = read_file(file)
    pred = model.predict(data)
    return {"language": langs[lang_symb[pred]]}
