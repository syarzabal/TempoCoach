from gui.ventana_principal import VentanaPrincipal
import tkinter as tk

def main():
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == '__main__':
    main()