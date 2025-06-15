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
        return ruta

    def generar_plots(self):
        y = self.analizador.get_y()
        sr = self.analizador.get_sr()

        self.plotter.plotAudio(y=y, sr=sr)