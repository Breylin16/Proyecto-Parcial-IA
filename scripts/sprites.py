# --- SPRITES: Entidades del Juego IA HUNTER ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
# Contiene las clases Jugador y Enemigo
# El Enemigo usa el Arbol de Comportamiento (Lab-5) para decidir
# y los algoritmos de busqueda (Lab-4) para calcular rutas

import pygame
import os
from scripts.config import *
from scripts.ia_core import (
    Mapa, BusquedaEnAnchura, BusquedaEnProfundidad, Astar,
    NodoBT, Selector, Secuencia, AccionBT, Invertir, Timer
)

# Ruta base para cargar sprites PNG
_CARPETA_BASE = os.path.dirname(os.path.dirname(__file__))
_CARPETA_IMAGENES = os.path.join(_CARPETA_BASE, "assets", "images")


def cargar_sprite(nombre_archivo):
    """Carga un sprite PNG desde assets/images/."""
    ruta = os.path.join(_CARPETA_IMAGENES, nombre_archivo)
    if os.path.exists(ruta):
        return pygame.image.load(ruta).convert_alpha()
    return None


# =============================================================
# CLASE JUGADOR
# El "Intruso" que controla el usuario con las flechas
# Se mueve 1 celda por turno
# =============================================================
class Jugador:
    def __init__(self, x, y):
        # Posicion en celdas (no pixeles)
        self.x = x
        self.y = y
        # Cargar sprite PNG
        self.imagen_original = cargar_sprite("jugador.png")
        self._imagen_escalada = None
        self._tamano_cache = 0

    def mover(self, dx, dy, mapa):
        """Intenta mover al jugador en la direccion (dx, dy).
        Retorna True si se movio, False si habia pared o limite."""
        nueva_x = self.x + dx
        nueva_y = self.y + dy

        # Verificar limites del mapa
        if nueva_x < 0 or nueva_x >= len(mapa):
            return False
        if nueva_y < 0 or nueva_y >= len(mapa[0]):
            return False

        # Verificar que no sea pared
        if mapa[nueva_x][nueva_y] == 1:
            return False

        # Mover
        self.x = nueva_x
        self.y = nueva_y
        return True

    def dibujar(self, pantalla, tamano_celda, offset_x=0, offset_y=0):
        """Dibuja al jugador usando su sprite PNG."""
        px = offset_x + self.y * tamano_celda
        py = offset_y + self.x * tamano_celda

        if self.imagen_original:
            # Escalar sprite al tamano de celda (cache para rendimiento)
            if self._tamano_cache != tamano_celda:
                self._imagen_escalada = pygame.transform.scale(
                    self.imagen_original, (tamano_celda, tamano_celda)
                )
                self._tamano_cache = tamano_celda
            pantalla.blit(self._imagen_escalada, (px, py))
        else:
            # Fallback: rectangulo si no hay sprite
            rect = pygame.Rect(px, py, tamano_celda, tamano_celda)
            pygame.draw.rect(pantalla, COLOR_JUGADOR, rect)
            centro_x = px + tamano_celda // 2
            centro_y = py + tamano_celda // 2
            pygame.draw.circle(pantalla, (255, 255, 255),
                               (centro_x, centro_y), tamano_celda // 4)


# =============================================================
# CLASE ENEMIGO
# Programa de Seguridad que persigue al jugador
# Utiliza un Arbol de Comportamiento (Lab-5) para decidir
# que accion tomar en cada turno:
#   Selector (raiz)
#   ├── Secuencia: "Perseguir"
#   │   ├── Condicion: jugador_cerca()
#   │   └── Accion: perseguir_con_algoritmo()
#   └── Accion: patrullar()
#
# Una vez decidida la accion, usa A*, BFS o DFS (Lab-4)
# para calcular la ruta optima.
# =============================================================
class Enemigo:
    def __init__(self, x, y, algoritmo, color, nombre=""):
        # Posicion en celdas
        self.x = x
        self.y = y
        self.algoritmo = algoritmo  # "Astar", "BFS", "DFS"
        self.color = color
        self.nombre = nombre

        # Cargar sprite PNG segun el tipo de algoritmo
        sprites_por_tipo = {
            "Astar": "enemigo_astar.png",
            "BFS": "enemigo_bfs.png",
            "DFS": "enemigo_dfs.png"
        }
        self.imagen_original = cargar_sprite(sprites_por_tipo.get(algoritmo, ""))
        self._imagen_escalada = None
        self._tamano_cache = 0

        # Resultado del ultimo calculo
        self.camino = []             # Ruta calculada
        self.nodos_explorados = []   # Para el modo debug

        # Referencia al mapa y al jugador (se actualizan cada turno)
        self.mapa_ref = None
        self.jugador_x = 0
        self.jugador_y = 0

        # Para el Patrullero (BFS): puntos de patrulla
        self.patrulla_a = None
        self.patrulla_b = None
        self.objetivo_patrulla = None
        self.jugador_detectado = False

        # Radio de deteccion (distancia Manhattan)
        self.radio_deteccion = 8

        # =====================================================
        # ÁRBOL DE COMPORTAMIENTO (Behavior Tree)
        # Construido siguiendo el patron del Lab-5 del profesor
        # usando agregar_hijo() y clases Selector/Secuencia
        # =====================================================

        # Nodo raiz: Selector (prueba cada hijo hasta que uno tenga exito)
        self.comportamiento = Selector()

        # Rama 1: Secuencia de Persecucion
        # Si el jugador esta cerca -> perseguirlo con el algoritmo
        secuencia_persecucion = Secuencia()
        condicion_cerca = AccionBT(self.jugador_cerca)
        accion_perseguir = AccionBT(self.perseguir)
        secuencia_persecucion.agregar_hijo(condicion_cerca)
        secuencia_persecucion.agregar_hijo(accion_perseguir)

        # Rama 2: Accion de Patrulla (fallback si no esta cerca)
        accion_patrullar = AccionBT(self.patrullar)

        # Estructura final del arbol:
        # Selector
        # ├── Secuencia [jugador_cerca? -> perseguir]
        # └── Accion [patrullar]
        self.comportamiento.agregar_hijo(secuencia_persecucion)
        self.comportamiento.agregar_hijo(accion_patrullar)

    def configurar_patrulla(self, punto_a, punto_b):
        """Configura los puntos de patrulla para el enemigo BFS."""
        self.patrulla_a = punto_a
        self.patrulla_b = punto_b
        self.objetivo_patrulla = punto_b  # Empieza yendo a B

    # ==========================================================
    # FUNCIONES DEL ARBOL DE COMPORTAMIENTO
    # Estas funciones son llamadas por los nodos AccionBT
    # ==========================================================

    def jugador_cerca(self):
        """Condicion: verifica si el jugador esta dentro del radio.
        Retorna True/False (patron del Lab-5)."""
        distancia = abs(self.x - self.jugador_x) + abs(self.y - self.jugador_y)
        cerca = distancia <= self.radio_deteccion
        self.jugador_detectado = cerca
        return cerca

    def perseguir(self):
        """Accion: calcula ruta hacia el jugador usando el algoritmo asignado.
        Retorna True si encontro camino, False si no."""
        estado_inicio = Mapa(self.mapa_ref, [self.x, self.y])
        estado_fin = Mapa(self.mapa_ref, [self.jugador_x, self.jugador_y])

        if self.algoritmo == "Astar":
            self.camino, self.nodos_explorados = Astar(estado_inicio, estado_fin)
        elif self.algoritmo == "BFS":
            self.camino, self.nodos_explorados = BusquedaEnAnchura(estado_inicio, estado_fin)
        elif self.algoritmo == "DFS":
            self.camino, self.nodos_explorados = BusquedaEnProfundidad(estado_inicio, estado_fin)

        return len(self.camino) > 0

    def patrullar(self):
        """Accion: se mueve entre puntos de patrulla o hacia un objetivo fijo.
        Si no tiene patrulla configurada, persigue al jugador igualmente."""
        estado_inicio = Mapa(self.mapa_ref, [self.x, self.y])

        if self.patrulla_a and self.patrulla_b and self.objetivo_patrulla:
            if self.x == self.objetivo_patrulla[0] and self.y == self.objetivo_patrulla[1]:
                if self.objetivo_patrulla == self.patrulla_b:
                    self.objetivo_patrulla = self.patrulla_a
                else:
                    self.objetivo_patrulla = self.patrulla_b

            estado_fin = Mapa(self.mapa_ref, list(self.objetivo_patrulla))
        else:
            estado_fin = Mapa(self.mapa_ref, [self.jugador_x, self.jugador_y])

        if self.algoritmo == "BFS":
            self.camino, self.nodos_explorados = BusquedaEnAnchura(estado_inicio, estado_fin)
        elif self.algoritmo == "DFS":
            self.camino, self.nodos_explorados = BusquedaEnProfundidad(estado_inicio, estado_fin)
        else:
            self.camino, self.nodos_explorados = Astar(estado_inicio, estado_fin)

        return True

    # ==========================================================
    # METODOS PRINCIPALES
    # ==========================================================

    def calcular_movimiento(self, mapa, jugador_x, jugador_y):
        """Actualiza referencias y ejecuta el arbol de comportamiento.
        El arbol decide si perseguir o patrullar, y calcula la ruta."""
        # Actualizar referencias para que las funciones del BT las usen
        self.mapa_ref = mapa
        self.jugador_x = jugador_x
        self.jugador_y = jugador_y

        # Ejecutar el arbol de comportamiento
        # El Selector probara primero perseguir, si falla, patrullara
        self.comportamiento.ejecutar()

    def mover(self):
        """Avanza 1 paso por el camino calculado."""
        if self.camino and len(self.camino) > 1:
            siguiente = self.camino[1]
            self.x = siguiente[0]
            self.y = siguiente[1]

    def dibujar(self, pantalla, tamano_celda, offset_x=0, offset_y=0):
        """Dibuja al enemigo usando su sprite PNG."""
        px = offset_x + self.y * tamano_celda
        py = offset_y + self.x * tamano_celda

        if self.imagen_original:
            if self._tamano_cache != tamano_celda:
                self._imagen_escalada = pygame.transform.scale(
                    self.imagen_original, (tamano_celda, tamano_celda)
                )
                self._tamano_cache = tamano_celda
            pantalla.blit(self._imagen_escalada, (px, py))
        else:
            rect = pygame.Rect(px, py, tamano_celda, tamano_celda)
            pygame.draw.rect(pantalla, self.color, rect)
            margen = tamano_celda // 5
            x1, y1 = px + margen, py + margen
            x2, y2 = px + tamano_celda - margen, py + tamano_celda - margen
            pygame.draw.line(pantalla, (255, 255, 255), (x1, y1), (x2, y2), 2)
            pygame.draw.line(pantalla, (255, 255, 255), (x2, y1), (x1, y2), 2)

    def dibujar_debug(self, pantalla, color_camino, color_explorados, tamano_celda,
                       offset_x=0, offset_y=0):
        """Dibuja la visualizacion de debug del algoritmo."""
        superficie = pygame.Surface((tamano_celda, tamano_celda), pygame.SRCALPHA)
        superficie.fill((*color_explorados, 60))

        for coord in self.nodos_explorados:
            pantalla.blit(superficie, (offset_x + coord[1] * tamano_celda,
                                       offset_y + coord[0] * tamano_celda))

        if self.camino and len(self.camino) > 1:
            puntos = []
            for coord in self.camino:
                centro_x = offset_x + coord[1] * tamano_celda + tamano_celda // 2
                centro_y = offset_y + coord[0] * tamano_celda + tamano_celda // 2
                puntos.append((centro_x, centro_y))
            pygame.draw.lines(pantalla, color_camino, False, puntos, 3)
