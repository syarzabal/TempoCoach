import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


class AnalizadorArchivo:
    def __init__(self, ruta_archivo):
        self.archivo: str = ruta_archivo
        self.peak_height: float = 0.5
        self.y: list = None
        self.sr: int = None

        self.stempo: float = None
        self.beats: list = None

        self.onset_env: list = None

        self.peaks: list = None
        self.peak_intervals: list = None

        self.dtempo: list = None # Diccionario

        self.stats_estabilidad: dict = None


    """
    Todos las funciones de tipo __calcular_x están definidas de tal forma que no se calcule lo mismo dos veces.
     
    Por ejemplo, el cálculo de muchas cosas depende de self.y y self.sr. No conviene perder tiempo en calcularlo
    varias veces ya que el resultado va a ser el mismo.
    
    Otras como self.peaks pueden dar un resultado distinto en función de los parámetros definidos para su cálculo.
    """

    def __calcular_y_sr(self):
        # Solo se calcula una vez.
        if self.y is None or self.sr is None:
            self.y, self.sr = librosa.load(self.archivo)

    def __calcular_stempo_beats(self):
        # Solo se calcula una vez.
        if self.stempo is None or self.beats is None:
            # Aseguramos que tenemos los datos necesarios para este cálculo
            if self.y is None or self.sr is None:
                self.__calcular_y_sr()
            # Realizamos el cálculo
            self.stempo, self.beats = librosa.beat.beat_track(y=self.y, sr=self.sr)

    def __calcular_onset_env(self):
        # Solo se calcula una vez.
        if self.onset_env is None:
            # Aseguramos que tenemos los datos necesarios para este cálculo
            if self.y is None or self.sr is None:
                self.__calcular_y_sr()
            # Realizamos el cálculo
            self.onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)

    def __calcular_peaks(self):
        # Aseguramos que tenemos los datos necesarios para este cálculo
        if self.y is None or self.sr is None:
            self.__calcular_y_sr()

        # Se puede calcular varias veces si se ha cambiado self.height

        # Calcular distancias de semicorchea
        spm = self.sr * 60  # Samples por minuto
        sc = int(self.stempo * 4)  # Semicorcheas por minuto
        d: int = spm // sc + 256  # Distancia = n samples que abarca una semicorchea en el tempo actual

        self.peaks, _ = find_peaks(self.y, height=self.peak_height, distance=d)

    def __calcular_peak_intervals(self):
        # Se puede calcular varias veces si se ha cambiado self.height
        # Aseguramos que tenemos los datos necesarios para este cálculo
        if self.y is None or self.sr is None:
            self.__calcular_y_sr()
        if self.peaks is None:
            self.__calcular_peaks()
        # Realizamos el cálculo
        peak_times = self.peaks / self.sr
        self.peak_intervals = np.diff(peak_times)

    def __calcular_dtempo(self):
        # Solo se calcula una vez
        if self.dtempo is None:
            # Aseguramos que tenemos los datos necesarios para este cálculo
            if self.y is None or self.sr is None:
                self.__calcular_y_sr()
            if self.beats is None:
                self.__calcular_stempo_beats()

            # Realizamos el cálculo
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

            self.dtempo = dynamic_tempo


    def __calcular_stats_estabilidad(self):
        if self.stats_estabilidad is None:
            if self.dtempo is None:
                self.__calcular_dtempo()

            times = list(self.dtempo.keys())
            tempi = list(self.dtempo.values())

            tempi = np.array(tempi)
            times = np.array(times)
            duration = times[-1] - times[0]

            tempo_mean = np.mean(tempi)
            tempo_std = np.std(tempi)
            tempo_range = np.max(tempi) - np.min(tempi)

            times_in_5 = 0
            times_in_10 = 0
            times_in_15 = 0

            for t in tempi:
                if abs(t - tempo_mean) <= 5:
                    times_in_5 += 1
                elif abs(t - tempo_mean) <= 10:
                    times_in_10 += 1
                elif abs(t - tempo_mean) <= 15:
                    times_in_15 += 1

            percent_in_5 = times_in_5 / len(times)
            percent_in_10 = times_in_10 / len(times)
            percent_in_15 = times_in_15 / len(times)

            stability_score = percent_in_5 * 100  # limitar entre 0 y 100

            self.stats_estabilidad = {
                "tempo_medio": tempo_mean,
                "desviacion_estandar": tempo_std,
                "rango": tempo_range,
                "percent_in_5": percent_in_5,
                "percent_in_10": percent_in_10,
                "percent_in_15": percent_in_15,
                "score_estabilidad": stability_score
            }

    def set_peak_height(self, peak_height):
        self.peak_height = peak_height


    def get_y(self):
        if self.y is None or self.sr is None:
            self.__calcular_y_sr()
        return self.y
    def get_sr(self):
        if self.y is None or self.sr is None:
            self.__calcular_y_sr()
        return self.sr
    def get_stempo(self):
        if self.stempo is None:
            self.__calcular_stempo_beats()
        return self.stempo
    def get_beats(self):
        if self.stempo is None:
            self.__calcular_stempo_beats()
        return self.beats
    def get_onset_env(self):
        if self.onset_env is None:
            self.__calcular_onset_env()
        return self.onset_env
    def get_peaks(self):
        if self.peaks is None:
            self.__calcular_peaks()
        return self.peaks
    def get_peak_intervals(self):
        if self.peak_intervals is None:
            self.__calcular_peak_intervals()
        return self.peak_intervals
    def get_dtempo(self):
        if self.dtempo is None:
            self.__calcular_dtempo()
        return self.dtempo
    def get_stats_estabilidad(self):
        if self.stats_estabilidad is None:
            self.__calcular_stats_estabilidad()
        return self.stats_estabilidad