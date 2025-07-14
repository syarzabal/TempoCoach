import tkinter as tk
from tkinter import ttk, PhotoImage


class PantallaInicio(tk.Frame):
    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller

        label = ttk.Label(self, text="Tempo Coach", font=("Segoe UI", 32))
        label.pack(pady=30)

        btn_analisis_directo = ttk.Button(self, text="Ver tempo en directo",
                                  command=lambda: controller.mostrar_pantalla("PantallaAnalisisDirecto"))
        btn_analisis_directo.pack(pady=20)

        bton_analisis_archivo = ttk.Button(self, text="Analizar desde un archivo",
                                 command=lambda: controller.mostrar_pantalla("PantallaAnalisisArchivo"))
        bton_analisis_archivo.pack(pady=20)