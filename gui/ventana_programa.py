import ttkbootstrap as tb
from ttkbootstrap.constants import *
from gui.pantalla_inicio import PantallaInicio
from gui.pantalla_analisis_en_directo import PantallaAnalisisDirecto
from gui.pantalla_analisis_archivo import PantallaAnalisisArchivo
import sys

# Lista de pantallas (clase, "nombre")
pantallas = [
    (PantallaInicio, "PantallaInicio"),
    (PantallaAnalisisDirecto, "PantallaAnalisisDirecto"),
    (PantallaAnalisisArchivo, "PantallaAnalisisArchivo")
]

class VentanaPrograma(tb.Window):
    def __init__(self):
        super().__init__(themename="cyborg") #litera #darkly #cyborg
        self.title("Tempo Coach")
        self.geometry("1600x800")
        self.state("zoomed")

        # Dentro de __init__ de VentanaPrograma
        self.protocol("WM_DELETE_WINDOW", self.on_closing)



        self.frame_container = tb.Frame(self)
        self.frame_container.pack(side="top", fill="both", expand=True)

        # Diccionario para almacenar las pantallas
        self.frames = {}

        # Crear las pantallas y guardarlas con nombre
        for clase, nombre in pantallas:
            frame = clase(parent_widget=self.frame_container, controller=self)
            self.frames[nombre] = frame
            frame.place(in_=self.frame_container, x=0, y=0, relwidth=1, relheight=1)

        self.mostrar_pantalla("PantallaInicio")

    def on_closing(self):
        self.destroy()
        sys.exit()

    def mostrar_pantalla(self, pantalla):
        frame = self.frames[pantalla]
        frame.tkraise() # Poner pantalla en primer plano y hacerla visible
