#include "nodo.h"
#include <iostream>
using namespace std;

int main(int argc, char* argv[]) {
    string ruta = "../python_juego/historial.csv";
    if (argc > 1) {
        ruta = argv[1];            
    }

    NodoPartida* partidas = leerHistorial(ruta);
    if (partidas == NULL) {
        cout << "No hay partidas para mostrar." << endl;
        return 0;
    }
    cout << "Partidas leidas: " << contarPartidas(partidas) << endl << endl;

    NodoJugador* jugadores = calcularEstadisticas(partidas);

    ordenarBurbuja(jugadores);
    mostrarRanking(jugadores);

    liberarJugadores(jugadores);
    liberarPartidas(partidas);
    return 0;
}
