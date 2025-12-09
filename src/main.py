from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv

from src.utils import read_file, json_load, load_configuration
from src.model import Model

load_dotenv()

app = FastAPI(root_path="/speech-lang-id-api")
model = Model(config=load_configuration("config.yaml"))
model.load()


@app.get("/health")
def check_health():
    return {"status": "ok"}


@app.post("/predict")
def predict(file: UploadFile):
    langs = json_load("static/langs.json")
    lang_symb = list(langs.keys())

    data, _ = read_file(file)
    pred = model.predict(data)
    return {"language": langs[lang_symb[pred]]}
