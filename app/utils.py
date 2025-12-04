import io
import json
import yaml
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


def load_configuration(config_file: str) -> dict:
    """Load configuration from yaml file"""

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config
