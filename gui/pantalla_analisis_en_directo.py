import tkinter as tk
from tkinter import ttk, Widget
from backend.analizador_chunks import AnalizadorChunks
import sounddevice as sd
import threading
from text_handler import TextHandler
import tkinter.scrolledtext as ScrolledText
import logging
import time

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

        # TODO: borrar este componente
        # self.label_test_conexion = ttk.Label(self, text="Conexion NO establecida", foreground="gray")
        # self.label_test_conexion.config(text=self.AnalizadorChunks.testConexion())
        # self.label_test_conexion.pack(pady=5)

        self.label_title = ttk.Label(self, text="Calcular tempo en directo", font=("Segoe UI", 16), background="yellow")
        self.label_title.pack(pady=5)

        self.frame_container = tk.Frame(self, bg="grey", height=200)
        self.frame_container.pack(side="top", fill="x", expand=True, padx=5, pady=5)

        # Add text widget to display logging info
        st = ScrolledText.ScrolledText(self.frame_container, state='disabled', height=15)
        st.configure(font='TkFixedFont')
        st.pack(side="bottom", fill="x")

        # Create textLogger
        text_handler = TextHandler(st)

        # Logging configuration
        logging.basicConfig(filename='test.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)

        # self.btn_grabar = ttk.Button(self, text="Grabar",
        #                              command=lambda: threading.Thread(target=self.grabar,
        #                                                               args=(self.duracion_chunk, self.sample_rate),
        #                                                               daemon=True).start())
        # self.btn_grabar.pack(pady=20)

        self.label_status = tk.Label(self, text="Status: detenido", font=("Segoe UI", 10), background="yellow")
        self.label_status.pack(pady=5)

        self.running: bool = False
        self.thread = None
        self.btn_grabar = ttk.Button(self, text="Grabar",
                                     command=self.toggle_thread)
        self.btn_grabar.pack(pady=5)


    def toggle_thread(self):
        if self.running:
            self.running = False
            self.btn_grabar.config(text="Iniciar")
            self.actualizar_label_status("Status: deteniendo...")
        else:
            self.running = True
            self.btn_grabar.config(text="Detener")
            self.thread = threading.Thread(target=self.worker)
            self.thread.start()

    def actualizar_label_status(self, texto):
        self.label_status.after(0, lambda: self.label_status.config(text=texto))

    def worker(self):
        d = self.duracion_chunk
        sr = self.sample_rate

        while self.running:

            print('Comenzando grabación')
            self.actualizar_label_status("Status: grabando...")

            audio = sd.rec(
                int(d * sr),
                samplerate=sr,
                channels=1,
                dtype='float32'
            )
            sd.wait()
            audio = audio.flatten()

            # tempo = self.AnalizadorChunks.getTempo(audio, sr)
            # self.actualizar_display(f"Tempo estimado: {tempo:.2f} BPM")
            print('Grabación finalizada')
            print('Analizando tempo')
            self.actualizar_label_status("Status: analizando tempo...")
            tempo = self.AnalizadorChunks.getTempo(audio_chunk=audio, sample_rate=sr)

            msg = f'Tempo estimado: {tempo:.2f} BPM'
            print(msg)
            logging.info(msg)

        if not self.running:
            self.actualizar_label_status("Status: detenido")