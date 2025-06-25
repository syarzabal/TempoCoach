import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from backend.analisis_de_archivo.controlador_analisis import ControladorAnalisis
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PantallaAnalisisArchivo(tk.Frame):

    def __init__(self, parent_widget, controller):
        super().__init__(parent_widget)
        self.controller = controller
        self.analizador = None
        self.archivo_seleccionado = None

        self.__crear_widgets()
        self.__crear_canvas_scrollable()


    def __crear_widgets(self):
        ttk.Button(self, text="⬅", command=lambda: self.controller.mostrar_pantalla("PantallaInicio")).place(x=5, y=5)
        ttk.Label(self, text="Analizar desde archivo", font=("Segoe UI", 16)).pack(pady=20)
        ttk.Label(self, text="Para resultados más precisos se recomienda usar archivos .wav", foreground="gray").pack(pady=5)

        self.btn_elegir_archivo = ttk.Button(self, text="Seleccionar archivo", command=lambda: self._seleccionar_archivo())
        self.btn_elegir_archivo.pack(pady=5)

        self.label_archivo_seleccionado = ttk.Label(self, text="")
        self.label_archivo_seleccionado.pack(pady=5)

        self.btn_analizar = ttk.Button(self, text="Analizar archivo", command=self._analizar_archivo)
        self.btn_analizar.pack(pady=5)
        self.btn_analizar.config(state="disabled")

        self.controlador_analisis = None


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

            figura_audio = self.controlador_analisis.generar_plot_audio()
            fig = figura_audio["audio"]
            canvas = FigureCanvasTkAgg(fig, master=self.scroll_frame)
            canvas.draw()
            self.canvas_widget_audio = canvas.get_tk_widget()
            self.canvas_widget_audio.pack(pady=(5, 15), anchor="center")






    # TODO: añadir visualización de tiempo de carga
    def _analizar_archivo(self):
        self.btn_analizar.config(state="disabled", text="Cargando...")

        # Generar gráficos en forma de objetos matplotlib
        self.figuras_basicas = self.controlador_analisis.generar_plots_basicos()
        self.figuras_peaks = self.controlador_analisis.generar_plots_peaks()
        print("Plots generados")
        self._cargar_imagenes()
        self.btn_analizar.config(state="disabled", text="Analizar archivo")


    def _cargar_imagenes(self) -> None:
        if self.controlador_analisis is None:
            return

        # Limpiar contenido anterior
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        figuras = {
            "Audio": self.figuras_basicas["audio"],
            "Tempograma": self.figuras_basicas["dtempo"],
            "Porcentaje de estabilidad" : self.figuras_basicas["stability_pie"],
            "Beats vs Onsets": self.figuras_basicas["rw_beats"],
            "Forma de onda con picos": self.figuras_peaks["peaks"],
            "Espaciado entre picos": self.figuras_peaks["peak_spacing"],
        }

        for titulo, fig in figuras.items():
            ttk.Label(self.scroll_frame, text=titulo, font=("Segoe UI", 12, "bold")).pack(pady=(15, 5))
            canvas = FigureCanvasTkAgg(fig, master=self.scroll_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(pady=(5, 15), anchor="center")

        ttk.Button(self.scroll_frame, text="Boton de prueba", command=None).pack(pady=(5, 15), anchor="center")

