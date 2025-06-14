import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class PantallaAnalisisArchivo(tk.Frame):

    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller
        self.archivo_seleccionado = None
        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Button(self, text="⬅", command=lambda: self.controller.mostrar_pantalla("PantallaInicio")).place(x=5, y=5)
        ttk.Label(self, text="Analizar desde archivo", font=("Segoe UI", 16)).pack(pady=20)

        self.btn_elegir_archivo = ttk.Button(self, text="Seleccionar archivo", command=lambda: self._seleccionar_archivo())
        self.btn_elegir_archivo.pack(pady=5)

        self.label_archivo_seleccionado = ttk.Label(self, text="Ningún archivo seleccionado")
        self.label_archivo_seleccionado.pack(pady=5)

    def _seleccionar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            filetypes=[("MP3 y WAV", ("*.mp3", "*.wav"))]
        )
        if ruta_archivo:
            self.archivo_seleccionado = ruta_archivo
            self.label_archivo_seleccionado.config(text=f"Archivo seleccionado: {ruta_archivo}")
