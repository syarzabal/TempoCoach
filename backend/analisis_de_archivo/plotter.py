import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import lineStyles
from scipy.signal import find_peaks


class Plotter:
    def __init__(self):
        plt.style.use("dark_background")

    def plot_audio(self, y, sr):
        tiempo = np.linspace(0, len(y) / sr, num=len(y))
        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(tiempo, y, linewidth=0.8, alpha=0.9)
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

        ax.fill_between(times, tempo_medio - 15, tempo_medio + 15, color='red', alpha=0.1)
        ax.fill_between(times, tempo_medio - 10, tempo_medio + 10, color='yellow', alpha=0.2)
        ax.fill_between(times, tempo_medio - 5, tempo_medio + 5, color='green', alpha=0.2)

        ax.axhline(tempo_medio, color='yellow', linestyle='--', linewidth=1, alpha=0.5, label=f'Tempo medio: {tempo_medio:.2f} BPM')

        diffs = np.abs(tempi - tempo_medio)
        mask_green = diffs <= 5
        mask_yellow = (diffs > 5) & (diffs <= 10)
        mask_red = (diffs > 10) & (diffs <= 15)

        ax.plot(times, tempi, color='white', lw=1, label='Tempo dinámico', alpha=0.5)
        ax.scatter(times[mask_green], tempi[mask_green], color='green', s=20)
        ax.scatter(times[mask_yellow], tempi[mask_yellow], color='orange', s=20)
        ax.scatter(times[mask_red], tempi[mask_red], color='red', s=20)

        ax.set_ylim(tempo_medio - 30, tempo_medio + 30)
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Tempo (BPM)')
        ax.set_title('Tempograma')
        ax.legend(loc='best')
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

    def plot_rw_beats(self, beats, y, sr, hop_length=512):
        import librosa

        tolerancia_segundos = 0.1  # 100 ms
        umbral = 0.05

        tiempo_y = np.linspace(0, len(y) / sr, num=len(y))
        beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=hop_length)
        tolerancia_muestras = int(tolerancia_segundos * sr)

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(tiempo_y, y, label='Forma de onda', lw=1) # color='blue'

        for beat_sec in beat_times:
            idx = int(beat_sec * sr)

            # Crear ventana alrededor del beat
            start = max(0, idx - tolerancia_muestras // 2)
            end = min(len(y), idx + tolerancia_muestras // 2)
            ventana = y[start:end]

            # Comprobar si hay amplitud significativa en la ventana
            tiene_audio = np.max(np.abs(ventana)) > umbral
            color = 'green' if tiene_audio else 'red'

            ax.axvline(x=beat_sec, color=color, linewidth=1)

        ax.set_title('Forma de onda con pulsos detectados')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Amplitud')
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        return fig

    # Plots para picos de audio -----------------------------------------------------------------------------------

    def plot_peaks(self, y, sr, peaks, height):
        tiempo_y = np.linspace(0, len(y) / sr, num=len(y))
        peak_times = peaks / sr

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(tiempo_y, y, label='Amplitud', lw=1)
        ax.plot(peak_times, y[peaks], 'x', color='orange', label='Picos')
        ax.vlines(peak_times, ymin=-1, ymax=1, color='orange', label='Picos', lw=0.2)

        plt.axhline(1, color='green', linestyle='--', linewidth=1, label='Upper limit')
        plt.axhline(-1, color='green', linestyle='--', linewidth=1, label='Lower limit')
        plt.axhline(height, color='yellow', linestyle='-', linewidth=1, label='Threshold')

        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title("Forma de onda con picos detectados")
        ax.legend()
        ax.grid(True)
        ax.set_ylim(-1.5, 1.5)
        fig.tight_layout()

        return fig

    def plot_peaks_closeup(self, y, sr, peaks, height):
        tiempo_y = np.linspace(0, len(y) / sr, num=len(y))
        peak_times = peaks / sr

        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot(tiempo_y, y, label='Amplitud', lw=2)
        ax.plot(peak_times, y[peaks], 'x', color='orange', label='Picos')
        ax.vlines(peak_times, ymin=-1, ymax=1, color='orange', lw=0.2, label='Picos')
        ax.axhline(1, color='green', linestyle='--', linewidth=3, alpha=0.8, label='Upper limit')
        ax.axhline(-1, color='green', linestyle='--', linewidth=3, alpha=0.8, label='Lower limit')
        ax.axhline(height, color='yellow', linestyle='-', linewidth=1, label='Threshold')

        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title("Zoom en forma de onda con picos detectados")
        ax.grid(True)
        ax.set_ylim(height - 0.2, 1.5)
        ax.legend()
        fig.tight_layout()
        return fig

    def plot_peaks_timeline(self, y, sr, peaks):
        density_threshold = 8
        bin_size = 0.06

        peak_times = peaks / sr
        deltas = np.diff(peak_times)
        bin_edges = np.arange(0, max(deltas) + bin_size, bin_size)
        hist, _ = np.histogram(deltas, bins=bin_edges)
        dense_bins = bin_edges[:-1][hist >= density_threshold]

        cmap = plt.colormaps.get_cmap('Set1')
        color_map = {db: cmap(i % cmap.N) for i, db in enumerate(dense_bins)}

        def get_zone_color(delta):
            for db in dense_bins:
                if db <= delta < db + bin_size:
                    return color_map[db]
            return (0.9, 0.9, 0.9, 0.2)

        fig, ax = plt.subplots(figsize=(15, 2))

        for i in range(len(deltas)):
            x_start = peak_times[i]
            x_end = peak_times[i + 1]
            delta = deltas[i]
            color = get_zone_color(delta)
            ax.axvspan(x_start, x_end, color=color, alpha=0.3)

        ax.eventplot(peak_times, orientation='horizontal', colors='orange', lineoffsets=1, linelengths=0.9)
        ax.axhline(y=1, color='black', linewidth=0.5, linestyle='-')

        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel(" ")
        ax.set_yticks([])
        ax.set_title("Línea temporal de picos detectados\nCategorizados por intervalo")
        ax.grid(True, axis='x')
        fig.tight_layout()
        return fig

    def plot_peak_intervals(self, peaks, sr):
        density_threshold = 8
        bin_size = 0.06

        peak_times = peaks / sr
        deltas = np.diff(peak_times)
        mid_times = (peak_times[:-1] + peak_times[1:]) / 2

        hist, bin_edges = np.histogram(deltas, bins=np.arange(0, max(deltas) + bin_size, bin_size))
        dense_bins = bin_edges[:-1][hist >= density_threshold]

        cmap = plt.colormaps.get_cmap('Set1')
        color_map = {db: cmap(i % cmap.N) for i, db in enumerate(dense_bins)}

        def get_zone_color(delta):
            for db in dense_bins:
                if db <= delta < db + bin_size:
                    return color_map[db]
            return (0.6, 0.6, 0.6)

        fig, ax = plt.subplots(figsize=(15, 5))

        for db in dense_bins:
            color = color_map[db]
            ax.axhspan(db, db + bin_size, color=color, alpha=0.2,
                       label=f"Zona densa ({round(db, 2)}–{round(db + bin_size, 2)}s)")

        ax.plot(mid_times, deltas, linestyle='-', color='orange', linewidth=1, zorder=1)

        for i in range(len(deltas)):
            ax.plot(mid_times[i], deltas[i], marker='o', linestyle='None', color=get_zone_color(deltas[i]))

        ax.set_xlabel("Tiempo medio entre picos (s)")
        ax.set_ylabel("Diferencia de tiempo (s)")
        ax.set_title("Diferencias de tiempo entre picos")
        ax.grid(True)
        fig.tight_layout()

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())
        return fig
