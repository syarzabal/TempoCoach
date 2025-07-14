import os
from datetime import datetime
from backend.analisis_de_archivo.analizador_archivo import AnalizadorArchivo
from backend.analisis_de_archivo.plotter import Plotter


class ControladorAnalisis:
    def __init__(self, ruta_archivo):
        self.archivo = ruta_archivo
        self.analizador = AnalizadorArchivo(ruta_archivo=ruta_archivo)
        self.plotter = Plotter()

    def generar_plot_audio(self):
        y =         self.analizador.get_y()
        sr =        self.analizador.get_sr()

        plots = {
            "audio": self.plotter.plot_audio(y=y, sr=sr)
        }

        return plots

    def generar_figuras_basicas(self):
        y =         self.analizador.get_y()
        sr =        self.analizador.get_sr()
        stempo =    self.analizador.get_stempo()
        dtempo =    self.analizador.get_dtempo()
        stats =     self.analizador.get_stats_estabilidad()
        beats =     self.analizador.get_beats()
        onset_env = self.analizador.get_onset_env()


        # Generar y guardar los gráficos
        figuras = {
            "audio": self.plotter.plot_audio(y=y, sr=sr),
            "dtempo" :      self.plotter.plot_dynamic_tempo(dynamic_tempo=dtempo),
            "stability_pie" :       self.plotter.plot_tempo_stability_pie(stats=stats),
            "rw_beats" :    self.plotter.plot_rw_beats(y=y, sr=sr, beats=beats)
        }

        return figuras

    def generar_figuras_peaks(self, height):
        self.analizador.set_peak_height(height)
        y =         self.analizador.get_y()
        sr =        self.analizador.get_sr()
        stempo =    self.analizador.get_stempo()
        peaks =     self.analizador.get_peaks()
        peak_intervals = self.analizador.get_peak_intervals()

        # Generar y guardar los gráficos
        figuras = {
            "peaks" :       self.plotter.plot_peaks(y=y, sr=sr, peaks=peaks, height=height),
            "peaks_closeup" : self.plotter.plot_peaks_closeup(y=y, sr=sr, peaks=peaks, height=height),
            "peaks_timeline" : self.plotter.plot_peaks_timeline(y=y, sr=sr, peaks=peaks, tempo_bpm=stempo),
            "peak_spacing": self.plotter.plot_peak_intervals(peaks=peaks, sr=sr, tempo_bpm=stempo)
        }

        return figuras
