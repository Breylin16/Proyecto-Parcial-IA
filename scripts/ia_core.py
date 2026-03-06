# --- IA CORE: Algoritmos de Búsqueda y Árbol de Comportamiento ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
# Basado en el Lab-4 (búsqueda) y Lab-5 (Behavior Tree) del curso de IA
# Contiene: Nodo, Mapa, BFS, DFS, A*, generador de mundo, Arbol de Comportamiento

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


# =============================================================
# BUSQUEDA EN ANCHURA (BFS)
# Usa Cola FIFO (deque con popleft)
# Garantiza camino mas corto en grafos sin pesos
# Retorna: (camino, nodos_explorados)
# =============================================================
def BusquedaEnAnchura(estado_inicial, estado_final):
    nodoactual = Nodo(estado_inicial, None)
    nodosgenerado = deque()
    nodosvisitados = set()
    nodos_explorados = []  # Para el modo debug

    # Busqueda
    while nodoactual.dato != estado_final:
        sucesores = nodoactual.GenerarSucesores()

        for sucesor in sucesores:
            temp = Nodo(sucesor, nodoactual)
            if temp not in nodosvisitados:
                nodosgenerado.append(temp)

        nodosvisitados.add(nodoactual)
        nodos_explorados.append(nodoactual.dato.cordenadas[:])

        # Si no hay mas nodos por explorar, no hay solucion
        if not nodosgenerado:
            return [], nodos_explorados

        while nodoactual in nodosvisitados:
            if not nodosgenerado:
                return [], nodos_explorados
            nodoactual = nodosgenerado.popleft()  # FIFO: Cola

    # Reconstruir camino subiendo por los padres
    camino = []
    while nodoactual:
        camino.append(nodoactual.dato.cordenadas[:])
        nodoactual = nodoactual.padre
    camino.reverse()
    return camino, nodos_explorados


# =============================================================
# BUSQUEDA EN PROFUNDIDAD (DFS)
# Usa Pila LIFO (deque con pop)
# NO garantiza camino optimo
# Retorna: (camino, nodos_explorados)
# =============================================================
def BusquedaEnProfundidad(estado_inicial, estado_final):
    nodoactual = Nodo(estado_inicial, None)
    nodosgenerado = deque()
    nodosvisitados = set()
    nodos_explorados = []  # Para el modo debug

    # Busqueda
    while nodoactual.dato != estado_final:
        sucesores = nodoactual.GenerarSucesores()

        for sucesor in sucesores:
            temp = Nodo(sucesor, nodoactual)
            if temp not in nodosvisitados:
                nodosgenerado.append(temp)

        nodosvisitados.add(nodoactual)
        nodos_explorados.append(nodoactual.dato.cordenadas[:])

        if not nodosgenerado:
            return [], nodos_explorados

        while nodoactual in nodosvisitados:
            if not nodosgenerado:
                return [], nodos_explorados
            nodoactual = nodosgenerado.pop()  # LIFO: Pila

    # Reconstruir camino
    camino = []
    while nodoactual:
        camino.append(nodoactual.dato.cordenadas[:])
        nodoactual = nodoactual.padre
    camino.reverse()
    return camino, nodos_explorados


# =============================================================
# ALGORITMO A* (A-STAR)
# Usa Cola de Prioridad (heapq)
# f(n) = g(n) + h(n) donde h = Distancia Manhattan
# Garantiza camino optimo con heuristica admisible
# Retorna: (camino, nodos_explorados)
# =============================================================
def Astar(estado_inicial, estado_final):
    nodoactual = Nodo(estado_inicial, None, estado_inicial.Costo(estado_final))
    nodosgenerado = []
    nodosvisitados = set()
    nodos_explorados = []  # Para el modo debug

    heapq.heapify(nodosgenerado)

    # Busqueda
    while nodoactual.dato != estado_final:
        sucesores = nodoactual.GenerarSucesores()

        for sucesor in sucesores:
            temp = Nodo(sucesor, nodoactual, sucesor.Costo(estado_final))
            if temp not in nodosvisitados:
                heapq.heappush(nodosgenerado, temp)

        nodosvisitados.add(nodoactual)
        nodos_explorados.append(nodoactual.dato.cordenadas[:])

        if not nodosgenerado:
            return [], nodos_explorados

        while nodoactual in nodosvisitados:
            if not nodosgenerado:
                return [], nodos_explorados
            nodoactual = heapq.heappop(nodosgenerado)

    # Reconstruir camino
    camino = []
    while nodoactual:
        camino.append(nodoactual.dato.cordenadas[:])
        nodoactual = nodoactual.padre
    camino.reverse()
    return camino, nodos_explorados


# =============================================================
# GENERADOR DE MUNDO
# Crea la matriz del mapa con paredes aleatorias
# Garantiza que inicio, meta y posiciones de enemigos esten libres
# =============================================================
def generar_mundo(filas, columnas, porcentaje_paredes=0.25):
    # Crear matriz vacia (todo suelo = 0)
    mapa = [[0 for _ in range(columnas)] for _ in range(filas)]

    # Colocar paredes aleatorias
    for i in range(filas):
        for j in range(columnas):
            if random.random() < porcentaje_paredes:
                mapa[i][j] = 1  # Pared

    # Asegurar que las esquinas y bordes esten libres
    # (para el jugador, la meta y los enemigos)
    posiciones_libres = [
        (1, 1),                    # Jugador
        (filas - 2, columnas - 2), # Meta
        (1, columnas - 2),         # Enemigo A*
        (filas - 2, 1),            # Enemigo BFS (Patrulla punto A)
        (filas // 2, columnas // 2), # Enemigo DFS (centro)
    ]

    # Limpiar las posiciones reservadas y sus alrededores
    for pos in posiciones_libres:
        fila, col = pos
        for di in range(-1, 2):
            for dj in range(-1, 2):
                fi = fila + di
                fj = col + dj
                if 0 <= fi < filas and 0 <= fj < columnas:
                    mapa[fi][fj] = 0

    # Bordes del mapa como paredes
    for i in range(filas):
        mapa[i][0] = 1
        mapa[i][columnas - 1] = 1
    for j in range(columnas):
        mapa[0][j] = 1
        mapa[filas - 1][j] = 1

    return mapa


# =============================================================
# ÁRBOL DE COMPORTAMIENTO (BEHAVIOR TREE)
# Basado en el Lab-5 del curso de Inteligencia Artificial
# Patron del profesor: Nodo base con agregar_hijo(),
# Selector (OR), Secuencia (AND), Accion, Invertir, Timer
# Retorna True/False (no strings)
# =============================================================

class NodoBT:
    """Clase base para todos los nodos del arbol de comportamiento.
    Cada nodo tiene una lista de hijos y un metodo ejecutar().
    Tomada directamente del Lab-5."""
    def __init__(self):
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def ejecutar(self):
        pass


class Selector(NodoBT):
    """OR logico: ejecuta hijos en orden hasta que uno retorne True.
    Si todos retornan False, retorna False.
    Ejemplo: 'O persigue O patrulla'."""
    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False


class Secuencia(NodoBT):
    """AND logico: ejecuta hijos en orden hasta que uno retorne False.
    Si todos retornan True, retorna True.
    Ejemplo: 'SI esta cerca Y ENTONCES perseguir'."""
    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True


class AccionBT(NodoBT):
    """Nodo hoja que ejecuta una funcion (lambda o metodo).
    La funcion debe retornar True o False.
    Basado en la clase Accion del Lab-5."""
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

    def ejecutar(self):
        return self.accion()


class Invertir(NodoBT):
    """Decorador que invierte el resultado de su hijo.
    Si el hijo retorna True, retorna False y viceversa.
    Util para condiciones negadas: 'NO hay objetivo'."""
    def __init__(self, accion):
        super().__init__()
        self.agregar_hijo(accion)

    def ejecutar(self):
        return not self.hijos[0].ejecutar()


class Timer(NodoBT):
    """Decorador que espera N turnos antes de ejecutar su hijo.
    Cuenta regresiva: mientras tiempo_restante > 0, retorna False.
    Cuando llega a 0, ejecuta el hijo y reinicia el contador."""
    def __init__(self, tiempo):
        super().__init__()
        self.tiempo = tiempo
        self.tiempo_restante = tiempo

    def ejecutar(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            return False
        else:
            self.tiempo_restante = self.tiempo
            self.hijos[0].ejecutar()
            return True
