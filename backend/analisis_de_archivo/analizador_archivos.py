import librosa
import numpy as np
from scipy.signal import find_peaks


class AnalizadorArchivos:
    def __init__(self, ruta_archivo):
        self.archivo_seleccionado = ruta_archivo
        self.__obtener_propiedades()

    def __obtener_propiedades(self):
        self.y, self.sr = librosa.load(self.archivo_seleccionado)
        self.onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        self.stempo, self.beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        self.peaks = self.__calcular_peaks()

    def __calcular_peaks(self):

        # Calcular distancias de semicorchea
        spm = self.sr * 60  # Samples por minuto
        sc = int(self.stempo * 4)  # Semicorcheas por minuto
        d: int = spm // sc + 256  # Distancia = n samples que abarca una semicorchea en el tempo actual

        h = np.percentile(np.abs(self.y), 95)  # Para que los peaks estén por encima del 95% de la señal
        peaks, _ = find_peaks(self.y, height=h, distance=d)

        return peaks

    def get_y(self):
        return self.y

    def get_sr(self):
        return self.sr

    def get_avg_tempo(self):
        return float(self.stempo[0])

    def get_dynamic_tempo(self):
        beat_times = librosa.frames_to_time(self.beats, sr=self.sr)

        # Diferencia de tiempos entre beats sucesivos
        intervals = np.round(np.diff(beat_times), 2)

        # Cada n_beats calcularemos su tempo promedio
        n_beats = 4  # En n beats hay n-1 intervalos
        dynamic_tempo = {}  # Diccionario: {tiempo_medio: bpm}

        for i in range(len(intervals) - n_beats + 1):
            chunk = intervals[i:i + n_beats - 1]
            mean_interval = np.mean(chunk)
            if mean_interval > 0:
                bpm = 60.0 / mean_interval
                time = np.mean(beat_times[i:i + n_beats])
                dynamic_tempo[time] = bpm  # key=tiempo medio, value=bpm

        return dynamic_tempo

    def get_beats(self):
        return self.beats

    def get_onset_env(self):
        return self.onset_env

    def get_peaks(self):
        return self.peaks

    def get_peak_intervals(self):
        peak_times = self.peaks / self.sr
        peak_intervals = np.diff(peak_times)
        print(f'Peak times: {peak_times}')
        print(f'Peak intervals: {peak_intervals}')
        return peak_intervals

    # TODO: borrar esta función
    def test_conexion(self) -> str:
        return "Conexión con analizador establecida"