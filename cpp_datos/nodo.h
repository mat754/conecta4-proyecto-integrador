
#ifndef NODO_H
#define NODO_H

#include <string>
using namespace std;


struct NodoPartida {
    string fecha_hora;
    string jugador1;
    string jugador2;
    string resultado;      
    string ganador;        
    int total_jugadas;
    NodoPartida* siguiente;   
};

struct NodoJugador {
    string nombre;
    int partidas;
    int victorias;
    int derrotas;
    int empates;
    NodoJugador* siguiente;
};


NodoPartida* crearNodoPartida(string fecha, string j1, string j2,
                              string resultado, string ganador, int total);
NodoPartida* insertarAlFinal(NodoPartida* cabeza, NodoPartida* nuevo);
NodoPartida* leerHistorial(string ruta);
int contarPartidas(NodoPartida* cabeza);
void liberarPartidas(NodoPartida* cabeza);


NodoJugador* calcularEstadisticas(NodoPartida* partidas);
void ordenarBurbuja(NodoJugador* cabeza);
void mostrarRanking(NodoJugador* cabeza);
void liberarJugadores(NodoJugador* cabeza);

#endif
