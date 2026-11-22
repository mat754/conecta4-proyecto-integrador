# juego.py
# Programa principal de Conecta 4. Se ejecuta con:  python juego.py

import tkinter as tk
from tkinter import simpledialog

from interfaz import Interfaz

ventana = tk.Tk()
ventana.withdraw()          # esconde la ventana mientras se piden los nombres

nombre1 = simpledialog.askstring("Conecta 4", "Nombre del jugador 1:", parent=ventana)
nombre2 = simpledialog.askstring("Conecta 4", "Nombre del jugador 2:", parent=ventana)

ventana.deiconify()         # muestra la ventana
juego = Interfaz(ventana, nombre1, nombre2)
ventana.mainloop()