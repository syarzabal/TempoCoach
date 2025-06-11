import tkinter as tk
from tkinter import ttk

class PantallaAnalisis(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Pantalla de Análisis", font=("Segoe UI", 16))
        label.pack(pady=20)

        btn_volver = ttk.Button(self, text="Volver al inicio",
                                command=lambda: controller.mostrar_pantalla("PantallaInicio"))
        btn_volver.pack()