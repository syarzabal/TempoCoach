import tkinter as tk
from tkinter import ttk

class PantallaAjustes(tk.Frame):
    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller

        label = ttk.Label(self, text="Pantalla de Ajustes", font=("Segoe UI", 16))
        label.pack(pady=20)

        btn_volver = ttk.Button(self, text="Volver al inicio",
                                command=lambda: controller.mostrar_pantalla("PantallaInicio"))
        btn_volver.pack()
