import librosa
from librosa import feature
import numpy as np

class AnalizadorChunks:
    def __init__(self):
        pass

    def getTempo(self, audio_chunk: np.ndarray, sample_rate: int) -> float:
        if audio_chunk is None or len(audio_chunk) == 0:
            raise ValueError('Audio chunk vacío')

        tempo = librosa.feature.tempo(y=audio_chunk, sr=sample_rate)

        return float(tempo[0])
