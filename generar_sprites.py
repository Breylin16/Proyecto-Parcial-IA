# --- GENERAR SPRITES: Crea imagenes PNG pixel art para IA HUNTER ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
# Ejecutar una sola vez para generar los sprites del juego

import pygame
import os

pygame.init()

TAMANO = 64  # Tamano de cada sprite en pixeles
carpeta = os.path.join(os.path.dirname(__file__), "assets", "images")
os.makedirs(carpeta, exist_ok=True)


def crear_superficie():
    """Crea una superficie transparente del tamano estandar."""
    return pygame.Surface((TAMANO, TAMANO), pygame.SRCALPHA)


def guardar(superficie, nombre):
    """Guarda la superficie como PNG."""
    ruta = os.path.join(carpeta, nombre)
    pygame.image.save(superficie, ruta)
    print(f"Sprite generado: {ruta}")


def generar_jugador():
    """Sprite del jugador: hacker/intruso con visor cian."""
    s = crear_superficie()
    c = TAMANO  # 64

    # Cuerpo (capucha oscura)
    pygame.draw.rect(s, (20, 30, 50), (16, 8, 32, 48))
    # Cabeza
    pygame.draw.rect(s, (30, 45, 70), (18, 10, 28, 24))
    # Visor (linea brillante cian)
    pygame.draw.rect(s, (0, 255, 220), (20, 20, 24, 4))
    # Resplandor del visor
    pygame.draw.rect(s, (0, 200, 180, 80), (18, 18, 28, 8))
    # Hombros
    pygame.draw.rect(s, (15, 25, 45), (12, 32, 40, 12))
    # Piernas
    pygame.draw.rect(s, (10, 18, 35), (20, 46, 10, 14))
    pygame.draw.rect(s, (10, 18, 35), (34, 46, 10, 14))
    # Detalles de circuitos en el pecho
    pygame.draw.rect(s, (0, 180, 160, 120), (24, 36, 2, 8))
    pygame.draw.rect(s, (0, 180, 160, 120), (30, 34, 6, 2))
    pygame.draw.rect(s, (0, 180, 160, 120), (38, 36, 2, 6))

    guardar(s, "jugador.png")


def generar_enemigo_astar():
    """Sprite del Sabueso (A*): robot rojo agresivo."""
    s = crear_superficie()

    # Cuerpo principal (rojo oscuro)
    pygame.draw.rect(s, (120, 15, 15), (14, 12, 36, 44))
    # Cabeza angular
    pygame.draw.polygon(s, (150, 20, 20), [
        (18, 12), (46, 12), (50, 28), (14, 28)
    ])
    # Ojos rojos brillantes
    pygame.draw.rect(s, (255, 50, 50), (20, 16, 8, 6))
    pygame.draw.rect(s, (255, 50, 50), (36, 16, 8, 6))
    # Pupilas
    pygame.draw.rect(s, (255, 200, 200), (22, 18, 3, 3))
    pygame.draw.rect(s, (255, 200, 200), (38, 18, 3, 3))
    # Pecho con indicador
    pygame.draw.rect(s, (200, 30, 30), (26, 32, 12, 4))
    # Brazos mecanicos
    pygame.draw.rect(s, (100, 10, 10), (8, 28, 8, 20))
    pygame.draw.rect(s, (100, 10, 10), (48, 28, 8, 20))
    # Piernas
    pygame.draw.rect(s, (90, 8, 8), (18, 50, 10, 12))
    pygame.draw.rect(s, (90, 8, 8), (36, 50, 10, 12))
    # Resplandor
    pygame.draw.rect(s, (255, 0, 0, 40), (12, 10, 40, 48))

    guardar(s, "enemigo_astar.png")


def generar_enemigo_bfs():
    """Sprite del Patrullero (BFS): dron naranja/amarillo."""
    s = crear_superficie()

    # Cuerpo circular (dron)
    pygame.draw.ellipse(s, (180, 100, 20), (10, 16, 44, 32))
    # Cupula superior
    pygame.draw.ellipse(s, (200, 120, 30), (16, 10, 32, 20))
    # Ojo central (sensor)
    pygame.draw.circle(s, (255, 180, 0), (32, 28), 8)
    pygame.draw.circle(s, (255, 255, 100), (32, 28), 4)
    # Antena
    pygame.draw.rect(s, (180, 100, 20), (30, 4, 4, 10))
    pygame.draw.circle(s, (255, 200, 0), (32, 4), 4)
    # Propulsores inferiores
    pygame.draw.rect(s, (150, 80, 10), (14, 44, 8, 8))
    pygame.draw.rect(s, (150, 80, 10), (42, 44, 8, 8))
    # Destellos de propulsores
    pygame.draw.rect(s, (255, 200, 0, 100), (16, 50, 4, 6))
    pygame.draw.rect(s, (255, 200, 0, 100), (44, 50, 4, 6))
    # Resplandor
    pygame.draw.ellipse(s, (255, 150, 0, 30), (8, 14, 48, 36))

    guardar(s, "enemigo_bfs.png")


def generar_enemigo_dfs():
    """Sprite del Erratico (DFS): virus/glitch purpura."""
    s = crear_superficie()

    # Forma irregular (glitch)
    pygame.draw.polygon(s, (100, 20, 140), [
        (32, 6), (48, 16), (54, 32), (48, 50),
        (32, 56), (16, 50), (10, 32), (16, 16)
    ])
    # Capa mas clara interior
    pygame.draw.polygon(s, (130, 40, 170), [
        (32, 12), (44, 20), (48, 32), (44, 46),
        (32, 50), (20, 46), (16, 32), (20, 20)
    ])
    # Ojo central
    pygame.draw.circle(s, (200, 100, 255), (32, 30), 10)
    pygame.draw.circle(s, (255, 180, 255), (32, 30), 5)
    pygame.draw.circle(s, (255, 255, 255), (32, 30), 2)
    # Tentaculos/extensiones glitch
    pygame.draw.rect(s, (150, 50, 180, 150), (6, 24, 6, 4))
    pygame.draw.rect(s, (150, 50, 180, 150), (52, 28, 6, 4))
    pygame.draw.rect(s, (150, 50, 180, 150), (12, 50, 4, 6))
    pygame.draw.rect(s, (150, 50, 180, 150), (48, 48, 4, 6))
    # Particulas de glitch
    pygame.draw.rect(s, (200, 100, 255, 80), (8, 14, 3, 3))
    pygame.draw.rect(s, (200, 100, 255, 80), (50, 12, 3, 3))
    pygame.draw.rect(s, (200, 100, 255, 80), (54, 40, 3, 3))
    pygame.draw.rect(s, (200, 100, 255, 80), (4, 38, 3, 3))

    guardar(s, "enemigo_dfs.png")


def generar_meta():
    """Sprite de la meta: portal de extraccion verde."""
    s = crear_superficie()

    # Anillo exterior
    pygame.draw.circle(s, (0, 180, 80), (32, 32), 26, 4)
    # Anillo interior
    pygame.draw.circle(s, (0, 255, 120), (32, 32), 18, 3)
    # Centro brillante
    pygame.draw.circle(s, (100, 255, 150), (32, 32), 10)
    pygame.draw.circle(s, (200, 255, 220), (32, 32), 5)
    # Flecha hacia arriba (extraccion)
    pygame.draw.polygon(s, (255, 255, 255), [
        (32, 18), (40, 30), (36, 30), (36, 42),
        (28, 42), (28, 30), (24, 30)
    ])
    # Resplandor
    pygame.draw.circle(s, (0, 255, 100, 30), (32, 32), 28)

    guardar(s, "meta.png")


def generar_pared():
    """Sprite de pared: bloque solido con borde."""
    s = crear_superficie()

    # Fondo de pared
    pygame.draw.rect(s, (40, 45, 55), (0, 0, 64, 64))
    # Bordes mas claros (efecto 3D)
    pygame.draw.rect(s, (55, 60, 70), (0, 0, 64, 2))
    pygame.draw.rect(s, (55, 60, 70), (0, 0, 2, 64))
    pygame.draw.rect(s, (25, 30, 40), (0, 62, 64, 2))
    pygame.draw.rect(s, (25, 30, 40), (62, 0, 2, 64))
    # Detalle de ladrillos
    pygame.draw.line(s, (50, 55, 65), (0, 16), (64, 16), 1)
    pygame.draw.line(s, (50, 55, 65), (0, 32), (64, 32), 1)
    pygame.draw.line(s, (50, 55, 65), (0, 48), (64, 48), 1)
    pygame.draw.line(s, (50, 55, 65), (32, 0), (32, 16), 1)
    pygame.draw.line(s, (50, 55, 65), (16, 16), (16, 32), 1)
    pygame.draw.line(s, (50, 55, 65), (48, 16), (48, 32), 1)
    pygame.draw.line(s, (50, 55, 65), (32, 32), (32, 48), 1)
    pygame.draw.line(s, (50, 55, 65), (16, 48), (16, 64), 1)
    pygame.draw.line(s, (50, 55, 65), (48, 48), (48, 64), 1)

    guardar(s, "pared.png")


def generar_suelo():
    """Sprite de suelo: piso oscuro con grid sutil."""
    s = crear_superficie()

    pygame.draw.rect(s, (18, 20, 28), (0, 0, 64, 64))
    # Grid sutil
    pygame.draw.rect(s, (22, 25, 33), (0, 0, 64, 1))
    pygame.draw.rect(s, (22, 25, 33), (0, 0, 1, 64))
    pygame.draw.rect(s, (22, 25, 33), (0, 63, 64, 1))
    pygame.draw.rect(s, (22, 25, 33), (63, 0, 1, 64))

    guardar(s, "suelo.png")


if __name__ == "__main__":
    generar_jugador()
    generar_enemigo_astar()
    generar_enemigo_bfs()
    generar_enemigo_dfs()
    generar_meta()
    generar_pared()
    generar_suelo()
    print("\n¡Todos los sprites generados en assets/images/!")
    pygame.quit()
