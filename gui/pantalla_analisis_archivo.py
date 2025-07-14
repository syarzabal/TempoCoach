import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from backend.analisis_de_archivo.controlador_analisis import ControladorAnalisis
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PantallaAnalisisArchivo(tk.Frame):

    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller
        self.archivo_seleccionado = None

        self.__crear_canvas_scrollable()
        self.__crear_widgets()



    def __crear_widgets(self):
        # Fuera de scroll frame
        ttk.Button(self, text="⬅", command=lambda: self.controller.mostrar_pantalla("PantallaInicio")).place(x=5, y=5)

        # Dentro de scroll frame
        ttk.Label(self.scroll_frame, text="Analizar desde archivo", font=("Segoe UI", 16)).pack(pady=20)
        ttk.Label(self.scroll_frame, text="Para resultados más precisos se recomienda usar archivos .wav", foreground="gray").pack(pady=5)

        self.btn_elegir_archivo = ttk.Button(self.scroll_frame, text="Seleccionar archivo", command=lambda: self._seleccionar_archivo())
        self.btn_elegir_archivo.pack(pady=5)

        self.label_archivo_seleccionado = ttk.Label(self.scroll_frame, text="")
        self.label_archivo_seleccionado.pack(pady=5)

        self.btn_analizar = ttk.Button(self.scroll_frame, text="Analizar archivo", command=self._analizar_archivo)
        self.btn_analizar.pack(pady=5)
        self.btn_analizar.config(state="disabled")

        self.controlador_analisis = None

        self.frame_resultados = tk.Frame(self.scroll_frame)
        self.frame_resultados.pack(fill="x")


    def __crear_canvas_scrollable(self):
        # Canvas y Scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="gray")

        self.scroll_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="n")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        def centrar_scroll_frame(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.scroll_window, width=canvas_width)

        self.canvas.bind("<Configure>", centrar_scroll_frame)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Scroll con ratón
        self.scroll_frame.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>",
                                                                         lambda e: self.canvas.yview_scroll(
                                                                             -1 * int(e.delta / 120), "units")))
        self.scroll_frame.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))


    def _seleccionar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            filetypes=[("MP3 y WAV", ("*.mp3", "*.wav"))]
        )
        if ruta_archivo:
            self.archivo_seleccionado = ruta_archivo
            self.label_archivo_seleccionado.config(text=f"Archivo seleccionado: {ruta_archivo}")

            self.btn_analizar.config(state="normal")

            self.controlador_analisis = ControladorAnalisis(self.archivo_seleccionado)

            # Eliminar figura anterior si existe
            if hasattr(self, "canvas_widget_audio") and self.canvas_widget_audio.winfo_exists():
                self.canvas_widget_audio.destroy()

            # Eliminar resultados anteriores
            self.frame_resultados.destroy()
            self.frame_resultados = tk.Frame(self.scroll_frame)
            self.frame_resultados.pack(fill="x")

            figura_audio = self.controlador_analisis.generar_plot_audio()
            fig = figura_audio["audio"]
            canvas = FigureCanvasTkAgg(fig, master=self.scroll_frame)
            canvas.draw()
            self.canvas_widget_audio = canvas.get_tk_widget()
            self.canvas_widget_audio.pack(pady=(5, 15), anchor="center")





    def _analizar_archivo(self):
        self.btn_analizar.config(state="disabled", text="Cargando...")

        # Generar gráficos en forma de objetos matplotlib
        self.figuras_basicas = self.controlador_analisis.generar_figuras_basicas()
        print("Plots generados")

        # Eliminar resultados anteriores
        self.frame_resultados.destroy()
        self.frame_resultados = tk.Frame(self.scroll_frame)
        self.frame_resultados.pack(fill="x")

        # Tempo y pulsos ------------------------
        ttk.Label(self.frame_resultados, text="Tempo y pulsos", font=("Segoe UI", 35)).pack(pady=(50, 25))
        for fig in self.figuras_basicas.values():
            canvas = FigureCanvasTkAgg(fig, master=self.frame_resultados)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(pady=(5, 15), anchor="center")

        # Picos de audio ----------------------
        ttk.Label(self.frame_resultados, text="Picos de audio", font=("Segoe UI", 35)).pack(pady=(50, 25))

        # Caja de texto para umbral
        ttk.Label(self.frame_resultados, text="Umbral (0.0 - 1.0):").pack()
        self.entry_umbral = ttk.Entry(self.frame_resultados)
        self.entry_umbral.insert(0, "0.5")  # Valor por defecto
        self.entry_umbral.pack(pady=(5, 10))

        #Boton de analisis de picos
        self.btn_peaks = ttk.Button(self.frame_resultados, text="Analizar picos de audio",
                   command=lambda: self._analizar_peaks())
        self.btn_peaks.pack(pady=(50, 30), anchor="center")

        self.btn_analizar.config(state="disabled", text="Analizar archivo")

    def _analizar_peaks(self):
        try:
            umbral = float(self.entry_umbral.get())
            if not (0 <= umbral <= 1):
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Valor inválido", "Por favor, introduce un número entre 0.0 y 1.0.")
            return

        self.figuras_peaks = self.controlador_analisis.generar_figuras_peaks(height=umbral)


        for fig in self.figuras_peaks.values():
            canvas = FigureCanvasTkAgg(fig, master=self.frame_resultados)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(pady=(5, 15), anchor="center")