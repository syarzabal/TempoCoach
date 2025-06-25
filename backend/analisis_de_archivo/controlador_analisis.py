import os
from datetime import datetime
from backend.analisis_de_archivo.analizador_archivo import AnalizadorArchivo
from backend.analisis_de_archivo.plotter import Plotter


class ControladorAnalisis:
    def __init__(self, archivo):
        self.archivo = archivo
        self.directorio_salida = self._crear_directorio_salida()
        self.analizador = AnalizadorArchivo(ruta_archivo=archivo)
        self.plotter = Plotter()

    def _crear_directorio_salida(self) -> str:
        ahora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_carpeta = f"analisis_{ahora}"
        ruta = os.path.join("resultados", nombre_carpeta)

        os.makedirs(ruta, exist_ok=True)  # Crea la carpeta si no existe
        print(ruta)
        return ruta

    def get_directorio_salida(self) -> str:
        return self.directorio_salida

    def generar_plot_audio(self):
        y =         self.analizador.get_y()
        sr =        self.analizador.get_sr()

        plots = {
            "audio": self.plotter.plot_audio(y=y, sr=sr)
        }

        return plots

    def generar_plots_basicos(self):
        y =         self.analizador.get_y()
        sr =        self.analizador.get_sr()
        stempo =    self.analizador.get_stempo()
        dtempo =    self.analizador.get_dtempo()
        stats =     self.analizador.get_stats_estabilidad()
        beats =     self.analizador.get_beats()
        onset_env = self.analizador.get_onset_env()


        # Generar y guardar los gráficos
        plots = {
            "audio": self.plotter.plot_audio(y=y, sr=sr),
            "dtempo" :      self.plotter.plot_dynamic_tempo(dynamic_tempo=dtempo),
            "stability_pie" :       self.plotter.plot_tempo_stability_pie(stats=stats),
            "rw_beats" :    self.plotter.plot_rw_beats(beats=beats, onset_env=onset_env),
        }

        return plots

    def generar_plots_peaks(self, height):
        self.analizador.set_peak_height(height)
        y =         self.analizador.get_y()
        sr =        self.analizador.get_sr()
        stempo =    self.analizador.get_stempo()
        peaks =     self.analizador.get_peaks()
        peak_intervals = self.analizador.get_peak_intervals()

        # Generar y guardar los gráficos
        plots = {
            "peaks" :       self.plotter.plot_peaks(y=y, sr=sr, peaks=peaks, height=height),
            "peak_spacing" : self.plotter.plot_peak_spacing(peak_spacing=peak_intervals, stempo=stempo)
        }

        return plots
