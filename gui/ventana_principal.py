import tkinter as tk
from tkinter import ttk

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Tempo Coach")
        self.root.geometry("800x400")

        self.label = ttk.Label(root, text="Te damos la bienvenida a Tempo Coach")
        self.label.pack(pady=20)

        self.boton_livebpm = ttk.Button(root, text="Live Tempo", command=self.haz_algo)
        self.boton_livebpm.pack()

        self.boton_analisis_archivo = ttk.Button(root, text="Analizar archivo de audio", command=self.haz_algo)
        self.boton_analisis_archivo.pack()

    def haz_algo(self):
        print("¡Botón pulsado!")
