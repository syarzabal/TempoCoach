import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


class Plotter:
    def __init__(self):
        plt.style.use("dark_background")

    def plot_audio(self, y, sr):
        tiempo = np.linspace(0, len(y) / sr, num=len(y))
        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(tiempo, y, linewidth=0.8)
        ax.set_title("Forma de onda del audio")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.grid(True)
        ax.set_ylim(-1, 1)
        fig.tight_layout()

        return fig

    def plot_dynamic_tempo(self, dynamic_tempo):
        times = np.array(list(dynamic_tempo.keys()))
        tempi = np.array(list(dynamic_tempo.values()))
        tempo_medio = np.mean(tempi)

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.grid(True)

        ax.fill_between(times, tempo_medio - 15, tempo_medio + 15, color='red', alpha=0.1, label='±15 BPM')
        ax.fill_between(times, tempo_medio - 10, tempo_medio + 10, color='yellow', alpha=0.2, label='±10 BPM')
        ax.fill_between(times, tempo_medio - 5, tempo_medio + 5, color='green', alpha=0.2, label='±5 BPM')

        ax.axhline(tempo_medio, color='gray', linestyle='--', linewidth=1.5, label=f'Tempo medio: {tempo_medio:.2f} BPM')

        diffs = np.abs(tempi - tempo_medio)
        mask_green = diffs <= 5
        mask_yellow = (diffs > 5) & (diffs <= 10)
        mask_red = (diffs > 10) & (diffs <= 15)

        ax.plot(times, tempi, color='white', lw=1.5, label='Tempo dinámico')
        ax.scatter(times[mask_green], tempi[mask_green], color='green', s=20, label='Dentro de ±5 BPM')
        ax.scatter(times[mask_yellow], tempi[mask_yellow], color='orange', s=20, label='Dentro de ±10 BPM')
        ax.scatter(times[mask_red], tempi[mask_red], color='red', s=20, label='Dentro de ±15 BPM')

        ax.set_ylim(tempo_medio - 30, tempo_medio + 30)
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Tempo (BPM)')
        ax.set_title('Tempograma')
        fig.tight_layout()

        return fig

    def plot_tempo_stability_pie(self, stats):
        labels = ['±5 BPM', '±10 BPM', '±15 BPM']
        sizes = [
            stats['percent_in_5'] * 100,
            stats['percent_in_10'] * 100,
            stats['percent_in_15'] * 100
        ]
        colors = ['green', 'gold', 'red']

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'edgecolor': 'black'}
        )
        ax.set_title('Distribución de estabilidad del tempo')
        ax.axis('equal')  # Para que sea un círculo perfecto

        return fig

    def plot_rw_beats(self, beats, onset_env):
        tolerancia_frames = 1
        umbral = 0.5
        onset_peaks, _ = find_peaks(onset_env, height=umbral)

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(onset_env, label='Onset strength', color='blue', lw=2.5)

        for beat in beats:
            color = 'green' if np.any(np.abs(onset_peaks - beat) <= tolerancia_frames) else 'red'
            ax.axvline(x=beat, color=color, linewidth=1)

        ax.set_title('Beats vs Onset Peaks')
        ax.set_xlabel('Frame')
        ax.set_ylabel('Onset Strength')
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        return fig

    def plot_peaks(self, y, sr, peaks):
        tiempo_y = np.linspace(0, len(y) / sr, num=len(y))
        peak_times = peaks / sr

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(tiempo_y, y, label='Amplitud', lw=1)
        ax.plot(peak_times, y[peaks], 'x', color='orange', label='Picos')
        ax.vlines(peak_times, ymin=-1, ymax=1, color='orange', label='Picos', lw=0.2)

        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title("Forma de onda con picos detectados")
        ax.legend()
        ax.grid(True)
        ax.set_ylim(-1, 1)
        fig.tight_layout()

        return fig

    def plot_peak_spacing(self, peak_spacing, stempo):
        redonda = 60.0 / (stempo / 2.0)
        negra = 60.0 / stempo
        corchea = 60.0 / (2 * stempo)
        semicorchea = 60.0 / (4 * stempo)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(peak_spacing, lw=0.5, marker='x', color='orange', label='Picos')

        alpha_figuras = 0.3
        ax.axhline(y=redonda, color='blue', linestyle='-', label='Redondas', alpha=alpha_figuras)
        ax.axhline(y=negra, color='blue', linestyle='--', label='Negras', alpha=alpha_figuras)
        ax.axhline(y=corchea, color='blue', linestyle='-.', label='Corcheas', alpha=alpha_figuras)
        ax.axhline(y=semicorchea, color='blue', linestyle=':', label='Semicorcheas', alpha=alpha_figuras)

        ax.set_xlabel("Picos")
        ax.set_ylabel("Intervalo (s)")
        ax.set_title("Espaciado entre picos de la onda de audio")
        ax.legend()
        ax.grid(True)
        ax.set_ylim(min(peak_spacing) - 0.2, max(peak_spacing) + 0.2)
        fig.tight_layout()

        return fig
