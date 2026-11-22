
#include "nodo.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <cstdlib>
using namespace std;

NodoPartida* crearNodoPartida(string fecha, string j1, string j2,
                              string resultado, string ganador, int total) {
    NodoPartida* nuevo = new NodoPartida;
    nuevo->fecha_hora = fecha;
    nuevo->jugador1 = j1;
    nuevo->jugador2 = j2;
    nuevo->resultado = resultado;
    nuevo->ganador = ganador;
    nuevo->total_jugadas = total;
    nuevo->siguiente = NULL;
    return nuevo;
}

NodoPartida* insertarAlFinal(NodoPartida* cabeza, NodoPartida* nuevo) {
    if (cabeza == NULL) {
        return nuevo;             
    }
    NodoPartida* actual = cabeza;
    while (actual->siguiente != NULL) {
        actual = actual->siguiente;
    }
    actual->siguiente = nuevo;
    return cabeza;
}

NodoPartida* leerHistorial(string ruta) {
    ifstream archivo(ruta.c_str());
    if (!archivo.is_open()) {
        cout << "No se pudo abrir el archivo: " << ruta << endl;
        return NULL;
    }

    NodoPartida* cabeza = NULL;
    string linea;

    getline(archivo, linea);       

    while (getline(archivo, linea)) {

        if (linea.size() > 0 && linea[linea.size() - 1] == '\r') {
            linea.erase(linea.size() - 1);
        }


        stringstream ss(linea);
        string campos[6];
        string campo;
        int cantidad = 0;
        while (getline(ss, campo, ',')) {
            if (cantidad < 6) {
                campos[cantidad] = campo;
            }
            cantidad++;
        }


        if (cantidad != 6) {
            continue;             
        }

        string res = campos[3];
        if (res != "gana_1" && res != "gana_2" && res != "empate") {
            continue;
        }

        int total = atoi(campos[5].c_str()); 
        NodoPartida* nuevo = crearNodoPartida(campos[0], campos[1], campos[2],
                                              campos[3], campos[4], total);
        cabeza = insertarAlFinal(cabeza, nuevo);
    }

    archivo.close();
    return cabeza;
}

int contarPartidas(NodoPartida* cabeza) {
    int total = 0;
    NodoPartida* actual = cabeza;
    while (actual != NULL) {
        total++;
        actual = actual->siguiente;
    }
    return total;
}

void liberarPartidas(NodoPartida* cabeza) {
    while (cabeza != NULL) {
        NodoPartida* siguiente = cabeza->siguiente;
        delete cabeza;
        cabeza = siguiente;
    }
}


bool esNombrePorDefecto(string nombre) {
    return (nombre == "Jugador 1" || nombre == "Jugador 2");
}


NodoJugador* buscarJugador(NodoJugador* cabeza, string nombre) {
    NodoJugador* actual = cabeza;
    while (actual != NULL) {
        if (actual->nombre == nombre) {
            return actual;
        }
        actual = actual->siguiente;
    }
    return NULL;
}


NodoJugador* registrarJugador(NodoJugador* cabeza, string nombre,
                              int numero, string resultado) {
    if (esNombrePorDefecto(nombre)) {
        return cabeza;            
    }

    NodoJugador* jugador = buscarJugador(cabeza, nombre);

    if (jugador == NULL) {

        jugador = new NodoJugador;
        jugador->nombre = nombre;
        jugador->partidas = 0;
        jugador->victorias = 0;
        jugador->derrotas = 0;
        jugador->empates = 0;
        jugador->siguiente = NULL;

        if (cabeza == NULL) {
            cabeza = jugador;
        } else {
            NodoJugador* ultimo = cabeza;
            while (ultimo->siguiente != NULL) {
                ultimo = ultimo->siguiente;
            }
            ultimo->siguiente = jugador;
        }
    }


    jugador->partidas++;
    if (resultado == "empate") {
        jugador->empates++;
    } else if (resultado == "gana_1" && numero == 1) {
        jugador->victorias++;
    } else if (resultado == "gana_2" && numero == 2) {
        jugador->victorias++;
    } else {
        jugador->derrotas++;
    }
    return cabeza;
}


NodoJugador* calcularEstadisticas(NodoPartida* partidas) {
    NodoJugador* cabeza = NULL;
    NodoPartida* actual = partidas;
    while (actual != NULL) {
        cabeza = registrarJugador(cabeza, actual->jugador1, 1, actual->resultado);
        cabeza = registrarJugador(cabeza, actual->jugador2, 2, actual->resultado);
        actual = actual->siguiente;
    }
    return cabeza;
}



bool ordenIncorrecto(NodoJugador* a, NodoJugador* b) {
    if (a->victorias < b->victorias) {
        return true;
    }
    if (a->victorias == b->victorias) {
        if (a->derrotas > b->derrotas) {
            return true;
        }
        if (a->derrotas == b->derrotas) {
            if (a->partidas < b->partidas) {
                return true;
            }
        }
    }
    return false;
}

void intercambiarDatos(NodoJugador* a, NodoJugador* b) {
    string nombreTemp = a->nombre;
    int partidasTemp = a->partidas;
    int victoriasTemp = a->victorias;
    int derrotasTemp = a->derrotas;
    int empatesTemp = a->empates;

    a->nombre = b->nombre;
    a->partidas = b->partidas;
    a->victorias = b->victorias;
    a->derrotas = b->derrotas;
    a->empates = b->empates;

    b->nombre = nombreTemp;
    b->partidas = partidasTemp;
    b->victorias = victoriasTemp;
    b->derrotas = derrotasTemp;
    b->empates = empatesTemp;
}

void ordenarBurbuja(NodoJugador* cabeza) {
    bool huboCambio = true;
    while (huboCambio) {
        huboCambio = false;
        NodoJugador* actual = cabeza;
        while (actual != NULL && actual->siguiente != NULL) {
            if (ordenIncorrecto(actual, actual->siguiente)) {
                intercambiarDatos(actual, actual->siguiente);
                huboCambio = true;
            }
            actual = actual->siguiente;
        }
    }
}


void mostrarRanking(NodoJugador* cabeza) {
    if (cabeza == NULL) {
        cout << "No hay jugadores con nombre en el historial." << endl;
        return;
    }

    cout << left << setw(6) << "Pos" << setw(20) << "Jugador"
         << setw(10) << "Partidas" << setw(11) << "Victorias"
         << setw(10) << "Derrotas" << "Empates" << endl;

    int posicion = 1;
    NodoJugador* actual = cabeza;
    while (actual != NULL) {
        cout << left << setw(6) << posicion << setw(20) << actual->nombre
             << setw(10) << actual->partidas << setw(11) << actual->victorias
             << setw(10) << actual->derrotas << actual->empates << endl;
        posicion++;
        actual = actual->siguiente;
    }
}

void liberarJugadores(NodoJugador* cabeza) {
    while (cabeza != NULL) {
        NodoJugador* siguiente = cabeza->siguiente;
        delete cabeza;
        cabeza = siguiente;
    }
}
