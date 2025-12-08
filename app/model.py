import os
import base64
import tempfile
import requests
import librosa
import numpy as np
import onnxruntime

from pathlib import Path


class Model:
    def __init__(self, config: dict) -> None:
        self.config = config

    def _preprocess(self, wav_data):
        if self.config["feature"] == "mel":
            return librosa.feature.melspectrogram(
                y=wav_data, **self.config["feature_params"]
            )
        elif self.config["feature"] == "mfcc":
            return librosa.feature.mfcc(
                y=wav_data, **self.config["feature_params"]
            )
        else:
            raise ValueError(f"Unknown feature name: {self.config["feautre"]}")

    def _download_model(self, url, path, params):
        username = os.getenv("MLFLOW_TRACKING_USERNAME")
        password = os.getenv("MLFLOW_TRACKING_PASSWORD")
        basic_auth_str = f"{username}:{password}".encode()
        auth_str = "Basic " + base64.standard_b64encode(basic_auth_str).decode(
            "utf-8"
        )
        headers = {
            "Authorization": auth_str,
            "User-Agent": "mlflow-python-client/2.22.2",
        }
        resp = requests.get(url, headers=headers, params=params)
        if resp.ok:
            with open(path, "wb") as f:
                f.write(resp.content)

    def load(self):
        url = os.getenv("MLFLOW_URL")
        with tempfile.TemporaryDirectory() as tmp_dir:
            params = {
                "path": (
                    f"{self.config["artifact_name"]}/"
                    f"{self.config["model_name"]}"
                ),
                "run_uuid": f"{self.config["run_id"]}",
            }
            self._download_model(
                url, Path(tmp_dir, self.config["model_name"]), params
            )

            self.model = onnxruntime.InferenceSession(
                Path(tmp_dir, self.config["model_name"]),
                providers=["CPUExecutionProvider"],
            )
        return self

    def predict(self, wav_data: np.ndarray):
        input = self._preprocess(wav_data)
        preds = self.model.run(
            None,
            {
                self.model.get_inputs()[0].name: np.expand_dims(
                    input.astype(np.float32), axis=0
                )
            },
        )
        return np.argmax(preds[0][0])
