# --- IA CORE: Algoritmos de Búsqueda y Árbol de Comportamiento ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
# Basado en el Lab-4 (búsqueda) y Lab-5 (Behavior Tree) del curso de IA
# Contiene: Nodo, Mapa (clases base para los algoritmos de busqueda)

from collections import deque
import heapq
import random


# =============================================================
# CLASE NODO
# Estructura base para representar estados en los algoritmos.
# Tomada directamente del Lab-4 con la misma interfaz.
# =============================================================
class Nodo:
    def __init__(self, dato, padre=None, distancia=0):
        self.dato = dato
        self.padre = padre
        self.H = distancia
        if padre == None:
            self.profundidad = 0
        else:
            self.profundidad = padre.profundidad + 1

    def GenerarSucesores(self):
        return self.dato.GenerarSucesores()

    def __eq__(self, __o) -> bool:
        if isinstance(__o, Nodo):
            return self.dato == __o.dato
        if isinstance(__o, type(self.dato)):
            return self.dato == __o
        return False

    # < override (necesario para heapq en A*)
    def __lt__(self, __o) -> bool:
        if isinstance(__o, Nodo):
            return self.Heuristica() < __o.Heuristica()
        return False

    # > override
    def __gt__(self, __o) -> bool:
        if isinstance(__o, Nodo):
            return self.Heuristica() > __o.Heuristica()
        return False

    # f(n) = g(n) + h(n)
    # g(n) = profundidad (costo real acumulado)
    # h(n) = H (heuristica, distancia estimada)
    def Heuristica(self):
        return self.H + self.profundidad

    def __hash__(self) -> int:
        return hash(str(self.dato))

    def __str__(self):
        return str(self.dato.__str__())


# =============================================================
# CLASE MAPA
# Representa un estado en la cuadrícula del juego.
# Adaptada del Lab-4: la configuracion es compartida (referencia)
# para no copiar la matriz entera en cada nodo.
# =============================================================
class Mapa:
    def __init__(self, configuracion, cordenadas) -> None:
        self.configuracion = configuracion
        self.cordenadas = cordenadas
        self.filas = len(configuracion)
        self.columnas = len(configuracion[0])

    def GenerarSucesores(self):
        sucesores = []
        # Movimientos: derecha, abajo, izquierda, arriba
        movimientos_validos = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        for movimiento in movimientos_validos:
            x = self.cordenadas[0] + movimiento[0]
            y = self.cordenadas[1] + movimiento[1]

            # Verificar que no se salga de los limites
            if x >= 0 and x < self.filas and y >= 0 and y < self.columnas:
                # Verificar que no sea pared (1)
                if self.configuracion[x][y] != 1:
                    # Compartimos la misma configuracion (referencia)
                    sucesores.append(Mapa(self.configuracion, [x, y]))

        return sucesores

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Mapa):
            return self.cordenadas == __o.cordenadas
        return self.cordenadas == __o

    def __hash__(self) -> int:
        # Usamos las coordenadas para el hash (mas eficiente)
        return hash(str(self.cordenadas))

    def __str__(self):
        return f"({self.cordenadas[0]}, {self.cordenadas[1]})"

    # Distancia Manhattan: |x1-x2| + |y1-y2|
    # Esta es la heuristica h(n) para A*
    def Costo(self, estado_final):
        return (abs(self.cordenadas[0] - estado_final.cordenadas[0])
                + abs(self.cordenadas[1] - estado_final.cordenadas[1]))
