import tkinter as tk
from tkinter import ttk

class PantallaAnalisisArchivo(tk.Frame):
    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller

        self.btn_volver = ttk.Button(self, text="⬅",
                                     command=lambda: controller.mostrar_pantalla("PantallaInicio"))
        self.btn_volver.place(x=5, y=5)

        label = ttk.Label(self, text="Analizar desde archivo", font=("Segoe UI", 16))
        label.pack(pady=20)
