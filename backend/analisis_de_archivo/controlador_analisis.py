import os
from datetime import datetime
from backend.analisis_de_archivo.analizador_archivos import AnalizadorArchivos
from backend.analisis_de_archivo.plotter import Plotter


class ControladorAnalisis:
    def __init__(self, archivo):
        self.archivo = archivo
        self.directorio_salida = self._crear_directorio_salida()
        self.analizador = AnalizadorArchivos(ruta_archivo=archivo)
        self.plotter = Plotter(directorio_salida=self.directorio_salida)

    def _crear_directorio_salida(self) -> str:
        ahora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_carpeta = f"analisis_{ahora}"
        ruta = os.path.join("resultados", nombre_carpeta)

        os.makedirs(ruta, exist_ok=True)  # Crea la carpeta si no existe
        print(ruta)
        return ruta

    def get_directorio_salida(self) -> str:
        return self.directorio_salida

    def generar_plots(self):
        y = self.analizador.get_y()
        sr = self.analizador.get_sr()
        stempo = self.analizador.get_avg_tempo()
        dynamic_tempo = self.analizador.get_dynamic_tempo()
        beats = self.analizador.get_beats()
        onset_env = self.analizador.get_onset_env()
        peaks = self.analizador.get_peaks()
        peak_intervals = self.analizador.get_peak_intervals()

        # Generar y guardar los gráficos
        self.plotter.plot_audio(y=y, sr=sr)
        self.plotter.plot_dynamic_tempo(dynamic_tempo=dynamic_tempo)
        self.plotter.plot_rw_beats(beats=beats, onset_env=onset_env)
        self.plotter.plot_peaks(y=y, sr=sr, peaks=peaks)
        self.plotter.plot_peak_spacing(peak_spacing=peak_intervals, stempo=stempo)
