import tkinter as tk
from tkinter import ttk
from backend.analizador_chunks import AnalizadorChunks
import sounddevice as sd

class PantallaAnalisisDirecto(tk.Frame):
    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller

        self.duracion_chunk = 4 # Duracion en segundos de un chunk de audio
        self.sample_rate = 44100
        self.AnalizadorChunks = AnalizadorChunks()

        self.label_test_conexion = ttk.Label(self, text="Conexion NO establecida")
        self.label_test_conexion.config(text=self.AnalizadorChunks.testConexion())
        self.label_test_conexion.pack(pady=20)

        self.label = ttk.Label(self, text="Calcular tempo en directo", font=("Segoe UI", 16), background="orange")
        self.label.pack(pady=20)

        self.btn_volver = ttk.Button(self, text="Volver al inicio",
                                command=lambda: controller.mostrar_pantalla("PantallaInicio"))
        self.btn_volver.pack()


    def grabar(self, duracion, sr):
        audio = sd.rec(
            int(duracion * sr),
            samplerate=sr,
            channels=1,
            dtype='float32'
        )
        sd.wait()
        audio = audio.flatten()
        return audio