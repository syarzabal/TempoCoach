import tkinter as tk
from tkinter import ttk

class PantallaInicio(tk.Frame):
    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller

        label = ttk.Label(self, text="Pantalla de Inicio", font=("Segoe UI", 16), background="red")
        label.pack(pady=20)

        btn_analisis = ttk.Button(self, text="Ver tempo en directo",
                                  command=lambda: controller.mostrar_pantalla("PantallaAnalisisDirecto"))
        btn_analisis.pack(pady=10)

        btn_ajustes = ttk.Button(self, text="Analizar desde un archivo",
                                 command=lambda: controller.mostrar_pantalla("PantallaAnalisisArchivo"))
        btn_ajustes.pack(pady=10)