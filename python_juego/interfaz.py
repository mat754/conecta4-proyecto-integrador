# interfaz.py
# Ventana del juego con Tkinter: dibuja la matriz y recibe los clics.

import tkinter as tk
from tkinter import messagebox

from logica import Juego, FILAS, COLUMNAS, limpiar_nombre

TAM = 80                   # tamaño de cada casilla en pixeles
COLOR_VACIO = "white"
COLOR_J1 = "yellow"
COLOR_J2 = "red"


class Interfaz:
    def __init__(self, ventana, nombre1, nombre2):
        self.ventana = ventana
        ventana.title("Conecta 4")

        # Limpiar nombres; si están vacíos se usa Jugador 1 / Jugador 2
        n1 = limpiar_nombre(nombre1, "Jugador 1")
        n2 = limpiar_nombre(nombre2, "Jugador 2")
        self.juego = Juego(n1, n2)

        # Texto que indica de quién es el turno
        self.etiqueta = tk.Label(ventana, font=("Arial", 14))
        self.etiqueta.pack(pady=5)

        # Zona donde se dibuja el tablero
        self.canvas = tk.Canvas(ventana, width=COLUMNAS * TAM,
                                height=FILAS * TAM, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clic)

        # Botones
        self.boton_deshacer = tk.Button(ventana, text="Deshacer",
                                        command=self.deshacer)
        self.boton_deshacer.pack(side="left", padx=20, pady=5)

        self.boton_nueva = tk.Button(ventana, text="Nueva partida",
                                     command=self.nueva_partida)
        self.boton_nueva.pack(side="right", padx=20, pady=5)

        self.dibujar()

    def dibujar(self):
        # Dibuja las 42 casillas según los valores de la matriz T
        self.canvas.delete("all")
        for i in range(FILAS):
            for j in range(COLUMNAS):
                valor = self.juego.T[i][j]
                if valor == 1:
                    color = COLOR_J1
                elif valor == 2:
                    color = COLOR_J2
                else:
                    color = COLOR_VACIO
                x1 = j * TAM + 5
                y1 = i * TAM + 5
                x2 = (j + 1) * TAM - 5
                y2 = (i + 1) * TAM - 5
                self.canvas.create_oval(x1, y1, x2, y2, fill=color)

        # Actualizar el texto del turno
        if self.juego.terminada:
            self.etiqueta.config(text="Partida terminada")
        else:
            turno = self.juego.turno_actual()
            if turno == 1:
                texto = "Turno de " + self.juego.nombre1 + " (amarillo)"
            else:
                texto = "Turno de " + self.juego.nombre2 + " (rojo)"
            self.etiqueta.config(text=texto)

    def clic(self, evento):
        # La columna se calcula con la posición x del clic
        columna = evento.x // TAM
        fila = self.juego.colocar_ficha(columna)

        if fila == -1:
            if self.juego.terminada:
                messagebox.showinfo("Aviso", "La partida ya terminó.")
            else:
                messagebox.showinfo("Aviso", "Esa columna está llena.")
            return

        self.dibujar()
        if self.juego.terminada:
            self.terminar_partida()

    def deshacer(self):
        if self.juego.deshacer():
            self.dibujar()
        else:
            messagebox.showinfo("Aviso", "No hay jugadas para deshacer")

    def nueva_partida(self):
        self.juego.nueva_partida()
        self.boton_deshacer.config(state="normal")
        self.dibujar()

    def terminar_partida(self):
        # Figura 2: desactivar Deshacer, guardar en el historial y mostrar resultado
        self.boton_deshacer.config(state="disabled")

        try:
            self.juego.guardar_resultado()
        except OSError:
            messagebox.showerror("Error", "No se pudo guardar en historial.csv")

        if self.juego.resultado == "gana_1":
            mensaje = "Ganó " + self.juego.nombre1
        elif self.juego.resultado == "gana_2":
            mensaje = "Ganó " + self.juego.nombre2
        else:
            mensaje = "Empate"
        messagebox.showinfo("Fin de la partida", mensaje)