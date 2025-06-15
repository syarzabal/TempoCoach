import matplotlib.pyplot as plt
import os
import numpy as np

class Plotter:
    def __init__(self, directorio_salida):
        self.dir = directorio_salida

    def plotAudio(self, y, sr):
        tiempo = np.linspace(0, len(y) / sr, num=len(y))

        plt.figure(figsize=(10, 4))
        plt.plot(tiempo, y, linewidth=0.8)
        plt.title("Forma de onda del audio")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.grid(True)
        plt.tight_layout()

        ruta = os.path.join(self.dir, "audio_wave.png")
        plt.savefig(ruta)
        plt.close()

    def plotDynamicTempo(self, dynamic_tempo):
        return None

    def plotRWBeats(self, beats, onset_env):
        return None

    def plotPeaks(self, y, sr, peak_times):
        return None