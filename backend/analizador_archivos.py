import librosa
from librosa import feature
import numpy as np
from typing import List, Tuple
from scipy.signal import find_peaks

# TODO: completar right worng beats

"""
Esta clase proporcionará los siguientes datos sobre una interpretación musical
- AvgTempo: float. Tempo promedio que se ha mantenido durante la interpretación
- DynamicTempo: array[float]. Medida de un tempo que puede ir variando durante la interpretacion. 
- RWBeats: plot de Right-Wrong Beats. Un plot de los pulsos de la interpretación marcados en rojo cuando no coincide el
    onser_env con ellos.
- PeakSpacing: array[float]. Distancia en segundos entre los picos de cada golpe en la batería. 
- PeakIntensity: array[float]. Intensidad (-1, 1) de cada golpe en la batería.
"""
class AnalizadorArchivos:
    def __init__(self, ruta_archivo):
        self.archivo_seleccionado = ruta_archivo
        self.y, self.sr = librosa.load(self.archivo_seleccionado)
        self.onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)

    """  
    Calcula el tempo promedio en toda la interpretación
    @:returns bpm: float
    """
    def _getAvgTempo(self) -> float:
        tempo, _ = librosa.beat.beat_track(onset_envelope=self.onset_env)
        return float(tempo[0])

    """  
    Calcula el tempo en diferentes momentos de la interpretación
    @:returns dynamic_tempo: dict(key=time, value=bpm)
    """
    def _getDynamicTempo(self):
        _, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        beat_times = librosa.frames_to_time(beats, sr=self.sr)

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

    def _geatBeatsAndOnsets(self):
        _, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        return beats, self.onset_env

    """
    Devuelve los tiempos donde se produce un pico en la señal de audio
    """
    def _getPeakTimes(self):
        mean = np.mean(np.absolute(self.y)) * 1.3  # TODO: not working as expected

        # Calcular distancias de semicorchea
        spm = self.sr * 60  # Samples por minuto
        sc = int(self._getAvgTempo() * 4)  # Semicorcheas por minuto
        d: int = spm // sc + 256  # Distancia = n samples que abarca una semicorchea en el tempo actual

        print(f'Distance = {d}, Mean={mean}')
        peaks, _ = find_peaks(self.y, height=mean, distance=d)
        peak_times = librosa.frames_to_time(peaks, sr=self.sr)

        return peak_times

    """
    Devuelve los intervalos entre cada pico en la señal de audio
    """
    def _getPeakIntervals(self):
        peak_times = self._getPeakTimes()
        peak_intervals = np.diff(peak_times)
        return peak_intervals

    # TODO: borrar esta función
    def testConexion(self) -> str:
        return "Conexión establecida"