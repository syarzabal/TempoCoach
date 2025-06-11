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

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Diccionario para almacenar las pantallas
        self.frames = {}

        # Crear las pantallas y guardarlas con nombre
        for clase, nombre in pantallas:
            frame = clase(self.container, self)
            self.frames[nombre] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_pantalla("PantallaInicio")

    def mostrar_pantalla(self, pantalla):
        frame = self.frames[pantalla]
        frame.tkraise() # Poner pantalla en primer plano y hacerla visible