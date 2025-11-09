import librosa
import numpy as np
import onnxruntime


class Model:
    def __init__(self):
        self.model = onnxruntime.InferenceSession(
            "static/model.onnx", providers=["CPUExecutionProvider"]
        )

    def _preprocess(self, wav_data, sr=16000, win_len=512, hop_len=128, n_mels=80):
        mel = librosa.feature.melspectrogram(
            y=wav_data, sr=sr, n_fft=win_len, hop_length=hop_len, n_mels=n_mels
        )
        return np.expand_dims(mel, axis=0).repeat(3, axis=0).astype(np.float32)

    def predict(self, wav_data: np.ndarray):
        input = self._preprocess(wav_data)
        preds = self.model.run(
            None, {self.model.get_inputs()[0].name: np.expand_dims(input, axis=0)}
        )
        return np.argmax(preds[0][0])


model = Model()
