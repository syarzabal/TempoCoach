import tkinter as tk
from tkinter import ttk
from backend.analizador_chunks import AnalizadorChunks
import sounddevice as sd
import threading

class PantallaAnalisisDirecto(tk.Frame):
    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller

        self.duracion_chunk = 4 # Duracion en segundos de un chunk de audio
        self.sample_rate = 44100
        self.AnalizadorChunks = AnalizadorChunks()

        self.btn_volver = ttk.Button(self, text="⬅",
                                     command=lambda: controller.mostrar_pantalla("PantallaInicio"))
        self.btn_volver.place(x=5, y=5)

        self.label_test_conexion = ttk.Label(self, text="Conexion NO establecida", foreground="gray")
        self.label_test_conexion.config(text=self.AnalizadorChunks.testConexion())
        self.label_test_conexion.pack(pady=5)

        self.label = ttk.Label(self, text="Calcular tempo en directo", font=("Segoe UI", 16))
        self.label.pack(pady=20)



        self.display_tempo = ttk.Label(self, text="Tempo en directo")
        self.display_tempo.pack(pady=20)

        self.btn_grabar = ttk.Button(self, text="Grabar",
                                     command=lambda: threading.Thread(target=self.grabar,
                                                                      args=(self.duracion_chunk, self.sample_rate),
                                                                      daemon=True).start())
        self.btn_grabar.pack(pady=20)




    def grabar(self, duracion, sr):
        self.actualizar_display("Grabando...")

        audio = sd.rec(
            int(duracion * sr),
            samplerate=sr,
            channels=1,
            dtype='float32'
        )
        sd.wait()
        audio = audio.flatten()

        # tempo = self.AnalizadorChunks.getTempo(audio, sr)
        # self.actualizar_display(f"Tempo estimado: {tempo:.2f} BPM")
        self.actualizar_display("Tempo estimado: ... BPM")

    def actualizar_display(self, texto):
        # Esto asegura que actualizamos la GUI desde el hilo principal
        self.display_tempo.after(0, lambda: self.display_tempo.config(text=texto))