import tkinter as tk
from tkinter import ttk
from backend.analizador_chunks import AnalizadorChunks
import sounddevice as sd
import threading
import tkinter.scrolledtext as ScrolledText
import logging
from text_handler import TextHandler


class PantallaAnalisisDirecto(tk.Frame):
    DURACION_CHUNK = 4  # en segundos
    SAMPLE_RATE = 44100

    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller
        self.running = False
        self.thread = None
        self.analizador = AnalizadorChunks()

        self._crear_widgets()
        self._configurar_logging()

    def _crear_widgets(self):
        ttk.Button(self, text="⬅", command=lambda: self.controller.mostrar_pantalla("PantallaInicio")).place(x=5, y=5)

        ttk.Label(self, text="Calcular tempo en directo", font=("Segoe UI", 16)).pack(pady=15)

        self.frame_container = tk.Frame(self, bg="grey", height=200)
        self.frame_container.pack(side="top", fill="x", expand=True, padx=5, pady=5)

        self.text_display = ScrolledText.ScrolledText(self.frame_container, state='disabled', height=15, font=('Helvetica', 18))
        self.text_display.pack(side="bottom", fill="x")

        self.label_status = tk.Label(self, text="Status: detenido", font=("Segoe UI", 10))
        self.label_status.pack(pady=5)

        self.btn_grabar = ttk.Button(self, text="Grabar", command=self._toggle_worker)
        self.btn_grabar.pack(pady=5)

    def _configurar_logging(self):
        text_handler = TextHandler(self.text_display)
        logging.basicConfig(filename='test.log',
                            filemode='w',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.getLogger().addHandler(text_handler)

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

    def _procesar_audio(self, audio):
        self._actualizar_label_status("Status: analizando tempo...")
        tempo = self.analizador.getTempo(audio_chunk=audio, sample_rate=self.SAMPLE_RATE)
        display_text = f'[{tempo:.1f} BPM] \t\t [{self._formatear_tempo(tempo)}]'
        logging.info(display_text)

    def _procesar_audio_loop(self):
        while self.running:
            audio = self._grabar_audio()
            self._procesar_audio(audio)
        self._actualizar_label_status("Status: detenido")

    def _formatear_tempo(self, tempo):
        escala = ""
        for i in range(60, 201):
            if i == int(tempo):
                escala += "!"
            elif i % 20 == 0:
                escala += ":"
            else:
                escala += "."
        return escala
