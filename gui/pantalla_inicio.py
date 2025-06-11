import tkinter as tk
from tkinter import ttk

class PantallaInicio(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Pantalla de Inicio", font=("Segoe UI", 16))
        label.pack(pady=20)

        btn_analisis = ttk.Button(self, text="Ir a análisis",
                                  command=lambda: controller.mostrar_pantalla("PantallaAnalisis"))
        btn_analisis.pack(pady=10)

        btn_ajustes = ttk.Button(self, text="Ir a ajustes",
                                 command=lambda: controller.mostrar_pantalla("PantallaAjustes"))
        btn_ajustes.pack(pady=10)