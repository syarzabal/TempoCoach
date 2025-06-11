import tkinter as tk
from gui.pantalla_inicio import PantallaInicio
from gui.pantalla_analisis import PantallaAnalisis
from gui.pantalla_ajustes import PantallaAjustes

# Lista de pantallas (clase, "nombre")
pantallas = [
    (PantallaInicio, "PantallaInicio"),
    (PantallaAnalisis, "PantallaAnalisis"),
    (PantallaAjustes, "PantallaAjustes")
]

class VentanaPrograma(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        self.geometry("500x300")

        self.frame_container = tk.Frame(self, bg="black")
        self.frame_container.pack(side="top", fill="both", expand=True)

        # Diccionario para almacenar las pantallas
        self.frames = {}

        # Crear las pantallas y guardarlas con nombre
        for clase, nombre in pantallas:
            frame = clase(parent_widget=self.frame_container, controller=self)
            self.frames[nombre] = frame
            frame.place(in_=self.frame_container, x=0, y=0, relwidth=1, relheight=1)

        self.mostrar_pantalla("PantallaInicio")

    def mostrar_pantalla(self, pantalla):
        frame = self.frames[pantalla]
        frame.tkraise() # Poner pantalla en primer plano y hacerla visible