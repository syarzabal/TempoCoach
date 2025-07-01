import tkinter as tk
from tkinter import ttk

from numba.core.types import Boolean

from backend.analisis_en_vivo.analizador_chunks import AnalizadorChunks
import sounddevice as sd
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class PantallaAnalisisDirecto(tk.Frame):
    DURACION_CHUNK = 4  # en segundos
    SAMPLE_RATE = 44100 # Hz (samples/seg)

    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller
        self.running: bool = False
        self.thread: threading.Thread = None
        self.analizador: AnalizadorChunks = AnalizadorChunks()

        # Campos para graficar el tempo en directo
        plt.style.use('dark_background')
        self.tempos = []
        self.tiempos = []
        self.fig, self.ax = plt.subplots()
        self.linea, = self.ax.plot([], [], 'o-', color='blue', lw=3)
        self.tiempo_total = 0  # acumulador de tiempo en segundos

        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Button(self, text="⬅", command=lambda: self.controller.mostrar_pantalla("PantallaInicio")).place(x=5, y=5)

        ttk.Label(self, text="Calcular tempo en directo", font=("Segoe UI", 16)).pack(pady=15)

        self.label_current_tempo = ttk.Label(self, text="0 BPM", font=("Segoe UI", 25))
        self.label_current_tempo.pack(pady=15)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

        self.ax.set_title("Tempo en tiempo real")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylim(60, 200)
        self.ax.set_xlim(0, 30)
        self.ax.set_ylabel("BPM")
        self.ax.grid(True)

        self.label_status = tk.Label(self, text="Status: detenido", font=("Segoe UI", 10))
        self.label_status.pack(pady=5)

        self.btn_grabar = ttk.Button(self, text="Grabar", command=self._toggle_worker)
        self.btn_grabar.pack(pady=5)


    def _toggle_worker(self):
        self.running = not self.running
        self.btn_grabar.config(text="Detener" if self.running else "Grabar")

        if self.running:
            threading.Thread(target=self._procesar_audio_loop, daemon=True).start()
        else:
            self._actualizar_label_status("Status: deteniendo...")

    def _actualizar_label_status(self, texto):
        self.label_status.after(0, lambda: self.label_status.config(text=texto))

    def _grabar_audio(self):
        self._actualizar_label_status("Status: grabando...")
        audio = sd.rec(int(self.DURACION_CHUNK * self.SAMPLE_RATE),
                       samplerate=self.SAMPLE_RATE,
                       channels=1,
                       dtype='float32')
        sd.wait()
        return audio.flatten()

    def _actualizar_grafico(self):
        self.linea.set_data(self.tiempos, self.tempos)
        self.label_current_tempo.config(text=f"{self.tempos[-1]:.2f} BPM")

        # Aumentar límite del eje X en bloques de 30 s
        if self.tiempo_total > self.ax.get_xlim()[1]:
            nuevo_limite = self.ax.get_xlim()[1] + 30
            self.ax.set_xlim(self.ax.get_xlim()[0], nuevo_limite)
        elif self.tiempo_total == self.DURACION_CHUNK:  # al primer dato
            self.ax.set_xlim(0, 30)

        self.canvas.draw()

    def _procesar_audio(self, audio):
        self._actualizar_label_status("Status: analizando tempo...")
        tempo = self.analizador.getTempo(audio_chunk=audio, sample_rate=self.SAMPLE_RATE)
        self.tiempo_total += self.DURACION_CHUNK
        self.tempos.append(tempo)
        self.tiempos.append(self.tiempo_total)
        self._actualizar_grafico()

    def _procesar_audio_loop(self):
        while self.running:
            audio = self._grabar_audio()
            self._procesar_audio(audio)
        self._actualizar_label_status("Status: detenido")
