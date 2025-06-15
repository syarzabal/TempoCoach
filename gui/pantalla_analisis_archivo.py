import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from backend.analizador_archivos import AnalizadorArchivos

class PantallaAnalisisArchivo(tk.Frame):

    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller
        self.analizador = None
        self.archivo_seleccionado = None

        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Button(self, text="⬅", command=lambda: self.controller.mostrar_pantalla("PantallaInicio")).place(x=5, y=5)
        ttk.Label(self, text="Analizar desde archivo", font=("Segoe UI", 16)).pack(pady=20)
        ttk.Label(self, text="Para resultados más precisos se recomienda usar archivos .wav", foreground="gray").pack(pady=5)

        self.btn_elegir_archivo = ttk.Button(self, text="Seleccionar archivo", command=lambda: self._seleccionar_archivo())
        self.btn_elegir_archivo.pack(pady=5)

        self.label_archivo_seleccionado = ttk.Label(self, text="")
        self.label_archivo_seleccionado.pack(pady=5)

    def _seleccionar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            filetypes=[("MP3 y WAV", ("*.mp3", "*.wav"))]
        )
        if ruta_archivo:
            self.archivo_seleccionado = ruta_archivo
            self.label_archivo_seleccionado.config(text=f"Archivo seleccionado: {ruta_archivo}")
            self.analizador = AnalizadorArchivos(ruta_archivo)
