import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from backend.analisis_de_archivo.controlador_analisis import ControladorAnalisis
import os


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

        self.btn_analizar = None
        self.controlador_analisis = None


    def _seleccionar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            filetypes=[("MP3 y WAV", ("*.mp3", "*.wav"))]
        )
        if ruta_archivo:
            self.archivo_seleccionado = ruta_archivo
            self.label_archivo_seleccionado.config(text=f"Archivo seleccionado: {ruta_archivo}")
            self.btn_analizar = ttk.Button(self, text="Analizar archivo", command=lambda: self._analizar_archivo())
            self.btn_analizar.pack(pady=5)

    # TODO: añadir visualización de tiempo de carga
    def _analizar_archivo(self):
        self.controlador_analisis = ControladorAnalisis(self.archivo_seleccionado)
        self.controlador_analisis.generar_plots()
        print("Plots generados")
        self._cargar_imagenes()

    def _cargar_imagenes(self) -> None:
        if self.controlador_analisis is None:
            return

        # Container scrolleable
        canvas = tk.Canvas(self, height=400)  # Puedes ajustar la altura
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        dir_salida = self.controlador_analisis.get_directorio_salida()

        self.img_dtempo = tk.PhotoImage(file=os.path.join(dir_salida, "dynamic_tempo.png"))
        self.img_beats = tk.PhotoImage(file=os.path.join(dir_salida, "beats_vs_onsets.png"))
        self.img_peaks = tk.PhotoImage(file=os.path.join(dir_salida, "audio_peaks.png"))
        self.img_peak_spacing = tk.PhotoImage(file=os.path.join(dir_salida, "peak_spacing.png"))

        ttk.Label(scroll_frame, image=self.img_dtempo).pack(pady=5)
        ttk.Label(scroll_frame, image=self.img_beats).pack(pady=5)
        ttk.Label(scroll_frame, image=self.img_peaks).pack(pady=5)
        ttk.Label(scroll_frame, image=self.img_peak_spacing).pack(pady=5)

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units"))
