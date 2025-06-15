import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.signal import find_peaks


class Plotter:
    def __init__(self, directorio_salida):
        self.dir = directorio_salida

    def plot_audio(self, y, sr):
        tiempo = np.linspace(0, len(y) / sr, num=len(y))

        plt.figure(figsize=(10, 4))
        plt.plot(tiempo, y, linewidth=0.8)
        plt.title("Forma de onda del audio")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.grid(True)
        plt.tight_layout()
        plt.ylim(-1, 1)

        ruta = os.path.join(self.dir, "audio_wave.png")
        plt.savefig(ruta)
        plt.close()

    # TODO: resolver problema de valores de eje-X incorrectos
    def plot_dynamic_tempo(self, dynamic_tempo):
        tiempos = list(dynamic_tempo.keys())
        tempos = list(dynamic_tempo.values())

        plt.figure(figsize=(10, 4))
        plt.plot(tiempos, tempos)
        plt.ylim(0, 200)
        plt.title("Tempo dinámico suavizado a lo largo del tiempo")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("BPM")
        plt.grid(True)
        plt.tight_layout()

        ruta = os.path.join(self.dir, "dynamic_tempo.png")
        plt.savefig(ruta)
        plt.close()

    # TODO: reemplazar eje-X por tiempo
    def plot_rw_beats(self, beats, onset_env):
        tolerancia_frames = 1
        umbral=0.5
        onset_peaks, _ = find_peaks(onset_env, height=umbral)

        plt.figure(figsize=(12, 5))
        plt.plot(onset_env, label='Onset strength', color='blue', lw=2.5)

        for beat in beats:
            if np.any(np.abs(onset_peaks - beat) <= tolerancia_frames):
                color = 'green'  # Alineado
            else:
                color = 'red'  # Desalineado
            plt.axvline(x=beat, color=color, linewidth=1)

        plt.title('Beats vs Onset Peaks')
        plt.xlabel('Frame')
        plt.ylabel('Onset Strength')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        ruta = os.path.join(self.dir, "beats_vs_onsets.png")
        plt.savefig(ruta)
        plt.close()


    def plot_peaks(self, y, sr, peaks):
        tiempo_y = np.linspace(0, len(y) / sr, num=len(y))
        peak_times = peaks / sr  # Convertir índices de picos a segundos

        plt.figure(figsize=(10, 4))
        plt.plot(tiempo_y, y, label='Amplitud', lw=1)
        plt.plot(peak_times, y[peaks], 'x', color='orange', label='Picos')
        plt.vlines(peak_times, ymin=-1, ymax=1, color='orange', label='Picos', lw=0.2)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.title("Forma de onda con picos detectados")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.ylim(-1, 1)

        ruta = os.path.join(self.dir, "audio_peaks.png")
        plt.savefig(ruta)
        plt.close()

    def plot_peak_spacing(self, peak_spacing, stempo):
        redonda = 60.0 / (stempo/2.0)
        negra = 60.0 / stempo
        corchea = 60.0 / (2 * stempo)
        semicorchea = 60.0 / (4 * stempo)

        plt.figure(figsize=(10, 4))
        plt.plot(peak_spacing, lw=0.5, marker='x', color='orange', label='Picos')

        alpha_figuras = 0.3
        plt.axhline(y=redonda, color='blue', linestyle='-', label='Redondas', alpha=alpha_figuras)
        plt.axhline(y=negra, color='blue', linestyle='--', label='Negras', alpha=alpha_figuras)
        plt.axhline(y=corchea, color='blue', linestyle='-.', label='Corcheas', alpha=alpha_figuras)
        plt.axhline(y=semicorchea, color='blue', linestyle=':', label='Semicorcheas', alpha=alpha_figuras)

        plt.xlabel("Picos")
        plt.ylabel("Intervalo (s)")
        plt.title("Espaciado entre picos de la onda de audio")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.ylim(min(peak_spacing) -0.2 , max(peak_spacing) + 0.2)

        ruta = os.path.join(self.dir, "peak_spacing.png")
        plt.savefig(ruta)
        plt.close()
