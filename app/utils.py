import io
import json
import soundfile as sf

from fastapi import UploadFile


def json_load(filename: str):
    """Load json data from file"""

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def read_file(file: UploadFile):
    contents = io.BytesIO(file.file.read())
    data, sr = sf.read(contents)
    return data, sr
