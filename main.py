# --- MAIN: Bucle Principal de IA HUNTER ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
# Evasion Algoritmica - Juego por turnos en cuadricula
# Flechas/Gamepad: moverse, D: debug, M: musica, R/Start: reiniciar, ESC: salir

import pygame
import sys
import os
from scripts.config import *
from scripts.ia_core import generar_mundo
from scripts.sprites import Jugador, Enemigo, cargar_sprite


# =============================================================
# FUNCIONES DE DIBUJO
# =============================================================

def dibujar_tablero(pantalla, mapa, tamano_celda, img_pared, img_suelo, offset_x, offset_y):
    """Dibuja la cuadricula usando sprites de pared y suelo."""
    for fila in range(len(mapa)):
        for col in range(len(mapa[0])):
            px = offset_x + col * tamano_celda
            py = offset_y + fila * tamano_celda
            if mapa[fila][col] == 1:
                if img_pared:
                    pantalla.blit(img_pared, (px, py))
                else:
                    rect = pygame.Rect(px, py, tamano_celda, tamano_celda)
                    pygame.draw.rect(pantalla, COLOR_PARED, rect)
            else:
                if img_suelo:
                    pantalla.blit(img_suelo, (px, py))
                else:
                    rect = pygame.Rect(px, py, tamano_celda, tamano_celda)
                    pygame.draw.rect(pantalla, COLOR_SUELO, rect)


def dibujar_meta(pantalla, meta_x, meta_y, tamano_celda, img_meta, offset_x, offset_y):
    """Dibuja el punto de destino usando sprite de meta."""
    px = offset_x + meta_y * tamano_celda
    py = offset_y + meta_x * tamano_celda
    if img_meta:
        pantalla.blit(img_meta, (px, py))
    else:
        rect = pygame.Rect(px, py, tamano_celda, tamano_celda)
        pygame.draw.rect(pantalla, COLOR_META, rect)
        cx = px + tamano_celda // 2
        cy = py + tamano_celda // 2
        s = tamano_celda // 5
        pygame.draw.polygon(pantalla, (255, 255, 255), [
            (cx - s, cy - s * 2), (cx + s * 2, cy - s), (cx - s, cy)
        ])


def dibujar_texto(pantalla, texto, x, y, tamano=20, color=(255, 255, 255)):
    """Dibuja texto en la pantalla."""
    fuente = pygame.font.SysFont("consolas", tamano)
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, (x, y))


def dibujar_texto_centrado(pantalla, texto, y, tamano=20, color=(255, 255, 255)):
    """Dibuja texto centrado horizontalmente."""
    fuente = pygame.font.SysFont("consolas", tamano)
    superficie = fuente.render(texto, True, color)
    x = (pantalla.get_width() - superficie.get_width()) // 2
    pantalla.blit(superficie, (x, y))


def dibujar_panel_info(pantalla, turno, debug_activo, estado_juego,
                       enemigos, jugador, meta_x, meta_y,
                       panel_x, panel_y, panel_ancho, panel_alto,
                       nivel=1, puntaje=0):
    """Dibuja el panel de informacion lateral con datos del juego."""
    # Fondo del panel (semitransparente)
    panel_surface = pygame.Surface((panel_ancho, panel_alto), pygame.SRCALPHA)
    panel_surface.fill((10, 12, 20, 200))
    pantalla.blit(panel_surface, (panel_x, panel_y))

    # Borde del panel
    pygame.draw.rect(pantalla, (0, 200, 180, 80),
                     (panel_x, panel_y, panel_ancho, panel_alto), 1)

    # Margen interno
    mx = panel_x + 15
    y = panel_y + 15
    espacio = 24

    # Titulo del panel
    dibujar_texto(pantalla, "IA HUNTER", mx, y, 22, (0, 255, 220))
    y += espacio + 5
    pygame.draw.line(pantalla, (0, 200, 180, 100),
                     (mx, y), (panel_x + panel_ancho - 15, y), 1)
    y += 12

    # Estado del juego
    if estado_juego == "jugando":
        dibujar_texto(pantalla, "Estado: EN JUEGO", mx, y, 16, (100, 255, 100))
    elif estado_juego == "ganaste":
        dibujar_texto(pantalla, "DATOS EXTRAIDOS!", mx, y, 16, COLOR_META)
    elif estado_juego == "perdiste":
        dibujar_texto(pantalla, "INTRUSO DETECTADO!", mx, y, 16, COLOR_ENEMIGO_ASTAR)
    y += espacio

    # Nivel y puntaje
    dibujar_texto(pantalla, f"Nivel: {nivel} / 3", mx, y, 16, (255, 220, 100))
    y += espacio
    dibujar_texto(pantalla, f"Puntaje: {puntaje}", mx, y, 16, (255, 220, 100))
    y += espacio

    # Turno
    dibujar_texto(pantalla, f"Turno: {turno}", mx, y, 16)
    y += espacio

    # Distancia a la meta
    dist_meta = abs(jugador.x - meta_x) + abs(jugador.y - meta_y)
    dibujar_texto(pantalla, f"Dist. a meta: {dist_meta}", mx, y, 16, (100, 255, 150))
    y += espacio + 10

    # Separator
    pygame.draw.line(pantalla, (0, 200, 180, 100),
                     (mx, y), (panel_x + panel_ancho - 15, y), 1)
    y += 12

    # Informacion de enemigos
    dibujar_texto(pantalla, "PROGRAMAS DE SEGURIDAD", mx, y, 14, (200, 200, 200))
    y += espacio

    for enemigo in enemigos:
        # Nombre y algoritmo
        dibujar_texto(pantalla, f"{enemigo.nombre}", mx, y, 15, enemigo.color)

        # Distancia al jugador
        dist = abs(enemigo.x - jugador.x) + abs(enemigo.y - jugador.y)
        estado_txt = "PERSIGUIENDO" if enemigo.jugador_detectado else "Patrullando"
        color_estado = (255, 100, 100) if enemigo.jugador_detectado else (150, 150, 150)
        dibujar_texto(pantalla, f"  Dist: {dist} | {estado_txt}", mx, y + 18, 12, color_estado)
        y += espacio + 18

    y += 5
    pygame.draw.line(pantalla, (0, 200, 180, 100),
                     (mx, y), (panel_x + panel_ancho - 15, y), 1)
    y += 12

    # Controles
    dibujar_texto(pantalla, "CONTROLES", mx, y, 14, (200, 200, 200))
    y += espacio
    controles = [
        ("Flechas / D-pad", "Mover"),
        ("D", "Debug mode"),
        ("M", "Musica ON/OFF"),
        ("ESC", "Menu"),
    ]
    for tecla, accion in controles:
        dibujar_texto(pantalla, f"{tecla}: {accion}", mx, y, 13, (140, 140, 140))
        y += 18

    # Debug indicator
    if debug_activo:
        y += 10
        dibujar_texto(pantalla, "DEBUG: ON", mx, y, 14, (255, 255, 0))


def dibujar_nombres_enemigos(pantalla, enemigos, tamano_celda, alto, offset_x, offset_y):
    """Dibuja el nombre del algoritmo debajo de cada enemigo."""
    fuente = pygame.font.SysFont("consolas", max(10, tamano_celda // 4))
    for enemigo in enemigos:
        texto = fuente.render(enemigo.nombre, True, enemigo.color)
        x = offset_x + enemigo.y * tamano_celda + tamano_celda // 2 - texto.get_width() // 2
        y = offset_y + enemigo.x * tamano_celda + tamano_celda + 2
        if y < alto - 10:
            pantalla.blit(texto, (x, y))


def pantalla_game_over(pantalla, gano, ancho, alto, puntaje=0, nivel=1, victoria_total=False):
    """Muestra mensaje de victoria, derrota o victoria total."""
    # Fondo semitransparente
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    pantalla.blit(overlay, (0, 0))

    if victoria_total:
        dibujar_texto_centrado(pantalla, "VICTORIA TOTAL", alto // 2 - 50,
                               42, (255, 220, 100))
        dibujar_texto_centrado(pantalla, "Has completado los 3 niveles!",
                               alto // 2, 22, COLOR_META)
        dibujar_texto_centrado(pantalla, f"Puntaje final: {puntaje}",
                               alto // 2 + 35, 24, (255, 255, 255))
    elif gano:
        dibujar_texto_centrado(pantalla, "DATOS EXTRAIDOS CON EXITO", alto // 2 - 40,
                               36, COLOR_META)
        dibujar_texto_centrado(pantalla, f"Nivel {nivel} completado!",
                               alto // 2 + 5, 20, (200, 200, 200))
        dibujar_texto_centrado(pantalla, f"Puntaje: {puntaje}",
                               alto // 2 + 35, 22, (255, 220, 100))
        dibujar_texto_centrado(pantalla, "Preparando siguiente nivel...",
                               alto // 2 + 65, 16, (150, 255, 150))
    else:
        dibujar_texto_centrado(pantalla, "INTRUSO DETECTADO", alto // 2 - 40,
                               36, COLOR_ENEMIGO_ASTAR)
        dibujar_texto_centrado(pantalla, f"Llegaste al nivel {nivel}",
                               alto // 2 + 5, 20, (200, 200, 200))
        dibujar_texto_centrado(pantalla, f"Puntaje final: {puntaje}",
                               alto // 2 + 35, 22, (255, 220, 100))

    dibujar_texto_centrado(pantalla, "Enter / Boton A: Continuar",
                           alto // 2 + 85, 18, (150, 150, 150))


# =============================================================
# MENÚ PRINCIPAL
# =============================================================

def pantalla_menu(pantalla, ancho, alto):
    """Muestra el menu principal con opciones de Jugar y Salir.
    Soporta teclado y gamepad."""
    reloj = pygame.time.Clock()

    # Inicializar joystick para el menu
    joystick = None
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    opcion = 0  # 0 = Jugar, 1 = Salir
    opciones = ["INICIAR JUEGO", "SALIR"]

    while True:
        reloj.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcion = (opcion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    opcion = (opcion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opcion == 0:
                        return "jugar"
                    else:
                        return "salir"
                elif evento.key == pygame.K_ESCAPE:
                    return "salir"

            # Soporte de Gamepad
            if evento.type == pygame.JOYBUTTONDOWN:
                if evento.button == 0:  # Boton A / X
                    if opcion == 0:
                        return "jugar"
                    else:
                        return "salir"
                if evento.button == 7:  # Start
                    return "jugar"

            if evento.type == pygame.JOYHATMOTION:
                if evento.value[1] == 1:  # D-pad arriba
                    opcion = (opcion - 1) % len(opciones)
                elif evento.value[1] == -1:  # D-pad abajo
                    opcion = (opcion + 1) % len(opciones)

        # Dibujar menu
        pantalla.fill((15, 15, 25))

        # Titulo
        dibujar_texto_centrado(pantalla, "IA  HUNTER", alto // 4 - 40, 56, COLOR_JUGADOR)
        dibujar_texto_centrado(pantalla, "Evasion Algoritmica", alto // 4 + 20, 22,
                               (150, 150, 150))

        # Linea decorativa
        pygame.draw.line(pantalla, COLOR_JUGADOR,
                         (ancho // 4, alto // 4 + 55),
                         (3 * ancho // 4, alto // 4 + 55), 2)

        # Opciones del menu
        for i, texto in enumerate(opciones):
            color = (255, 255, 255) if i == opcion else (100, 100, 100)
            prefijo = "> " if i == opcion else "  "
            dibujar_texto_centrado(pantalla, prefijo + texto,
                                   alto // 2 + i * 50, 28, color)

        # Info de controles
        dibujar_texto_centrado(pantalla, "Flechas / D-pad: Navegar | Enter / A: Seleccionar",
                               alto - 80, 16, (80, 80, 80))
        dibujar_texto_centrado(pantalla, "D: Debug | M: Musica | ESC: Menu",
                               alto - 55, 16, (80, 80, 80))

        # Info del gamepad
        if joystick:
            dibujar_texto_centrado(pantalla, f"Gamepad: {joystick.get_name()}",
                                   alto - 30, 14, (0, 200, 100))

        pygame.display.flip()


# =============================================================
# INICIALIZAR JUEGO
# =============================================================

def inicializar_juego(filas, columnas, porcentaje_paredes=None):
    """Crea el mapa, jugador y enemigos. Retorna todo listo para jugar.
    generar_mundo() se llama UNA SOLA VEZ aqui — el mapa se guarda en RAM."""
    if porcentaje_paredes is None:
        porcentaje_paredes = PORCENTAJE_PAREDES
    mapa = generar_mundo(filas, columnas, porcentaje_paredes)

    jugador = Jugador(POS_INICIAL_JUGADOR[1], POS_INICIAL_JUGADOR[0])
    meta_x = POS_INICIAL_META[1]
    meta_y = POS_INICIAL_META[0]

    enemigos = []

    # Enemigo 1: "El Sabueso" - A* (esquina superior derecha)
    sabueso = Enemigo(1, columnas - 2, "Astar", COLOR_ENEMIGO_ASTAR, "A*")
    sabueso.radio_deteccion = 12
    enemigos.append(sabueso)

    # Enemigo 2: "El Patrullero" - BFS (esquina inferior izquierda)
    patrullero = Enemigo(filas - 2, 1, "BFS", COLOR_ENEMIGO_BFS, "BFS")
    patrullero.radio_deteccion = 12
    patrullero.configurar_patrulla(PATRULLA_PUNTO_A, PATRULLA_PUNTO_B)
    enemigos.append(patrullero)

    # Enemigo 3: "El Erratico" - DFS (centro del mapa)
    erratico = Enemigo(filas // 2, columnas // 2, "DFS", COLOR_ENEMIGO_DFS, "DFS")
    erratico.radio_deteccion = 12
    enemigos.append(erratico)

    # Enemigo 4: "El Centinela" - A* (esquina inferior derecha)
    centinela = Enemigo(filas - 2, columnas - 2, "Astar", COLOR_ENEMIGO_ASTAR2, "A*-2")
    centinela.radio_deteccion = 10
    enemigos.append(centinela)

    # Enemigo 5: "El Rastreador" - BFS (centro izquierda)
    rastreador = Enemigo(filas // 2, 1, "BFS", COLOR_ENEMIGO_BFS2, "BFS-2")
    rastreador.radio_deteccion = 14
    rastreador.configurar_patrulla(PATRULLA2_PUNTO_A, PATRULLA2_PUNTO_B)
    enemigos.append(rastreador)

    # Enemigo 6: "El Fantasma" - DFS (centro derecha)
    fantasma = Enemigo(filas // 2, columnas - 2, "DFS", COLOR_ENEMIGO_DFS2, "DFS-2")
    fantasma.radio_deteccion = 10
    enemigos.append(fantasma)

    return mapa, jugador, meta_x, meta_y, enemigos


# =============================================================
# PROCESAR MOVIMIENTO DEL JUGADOR
# =============================================================

def procesar_movimiento(dx, dy, jugador, mapa, enemigos, turno,
                        sonido_movimiento, sonido_victoria, sonido_derrota,
                        meta_x, meta_y, estado_juego):
    """Intenta mover al jugador y actualiza la IA.
    Los algoritmos de busqueda SOLO se ejecutan aqui (por turno),
    no en cada frame del bucle de dibujo.
    Retorna (nuevo_turno, nuevo_estado)."""
    if estado_juego != "jugando":
        return turno, estado_juego

    movido = jugador.mover(dx, dy, mapa)

    if movido:
        turno += 1
        if sonido_movimiento:
            sonido_movimiento.play()

        # Fase de Pensamiento: cada enemigo ejecuta su Arbol de Comportamiento
        # El BT decide si perseguir o patrullar, y calcula la ruta
        for enemigo in enemigos:
            enemigo.calcular_movimiento(mapa, jugador.x, jugador.y)

        # Turno de la IA: cada enemigo avanza 1 paso por su ruta
        for enemigo in enemigos:
            enemigo.mover()

        # Verificar captura (enemigo alcanzo al jugador)
        for enemigo in enemigos:
            if enemigo.x == jugador.x and enemigo.y == jugador.y:
                estado_juego = "perdiste"
                if sonido_derrota:
                    sonido_derrota.play()

        # Verificar victoria (jugador llego a la meta)
        if jugador.x == meta_x and jugador.y == meta_y:
            estado_juego = "ganaste"
            if sonido_victoria:
                sonido_victoria.play()

    return turno, estado_juego


# =============================================================
# PAUSA INTELIGENTE (CONTROL DE FOCO)
# Cuando la ventana pierde el foco (Alt+Tab o minimizar),
# pausamos musica y calculos para no consumir recursos.
# =============================================================

def manejar_perdida_foco(musica_cargada, musica_activa):
    """Pausa el juego cuando la ventana pierde el foco.
    Espera hasta que el usuario vuelva a la ventana."""
    if musica_cargada:
        pygame.mixer.music.pause()

    # Esperar hasta que la ventana recupere el foco
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.ACTIVEEVENT:
                if evento.state == 2 and evento.gain == 1:
                    # Ventana recupero el foco
                    esperando = False
                    if musica_cargada and musica_activa:
                        pygame.mixer.music.unpause()
            if evento.type == pygame.QUIT:
                return False  # Señal de cerrar el juego
        pygame.time.wait(100)  # No saturar CPU mientras espera

    return True  # Señal de continuar


# =============================================================
# BUCLE PRINCIPAL
# =============================================================

def main():
    # Inicializar Pygame
    pygame.init()
    pygame.mixer.init()

    # Pantalla completa (requisito del examen)
    # Usamos la resolucion nativa del monitor
    info = pygame.display.Info()
    ancho = info.current_w
    alto = info.current_h
    pantalla = pygame.display.set_mode((ancho, alto), pygame.NOFRAME)
    pygame.display.set_caption(TITULO_JUEGO)
    reloj = pygame.time.Clock()

    # Calcular tamano de celda dinamicamente para la resolucion
    # Reservamos 280px a la derecha para el panel de informacion
    ancho_panel = 280
    ancho_juego = ancho - ancho_panel
    tamano_celda = min(ancho_juego // COLUMNAS, alto // FILAS)

    # Calcular offsets para centrar la cuadricula en la pantalla
    offset_x = (ancho_juego - COLUMNAS * tamano_celda) // 2
    offset_y = (alto - FILAS * tamano_celda) // 2

    # Posicion del panel lateral (a la derecha del tablero)
    panel_x = ancho_juego
    panel_y = 0
    panel_ancho = ancho_panel
    panel_alto = alto

    # Cargar musica de fondo (MP3 generado con Suno AI)
    # Usamos os.path.join para que funcione en cualquier PC
    carpeta = os.path.dirname(__file__)
    carpeta_musica = os.path.join(carpeta, "assets", "music")
    carpeta_sonidos = os.path.join(carpeta, "assets", "sounds")

    ruta_musica = os.path.join(carpeta_musica, "background.mp3")
    musica_cargada = False
    if os.path.exists(ruta_musica):
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.set_volume(0.4)
        musica_cargada = True

    # Cargar efectos de sonido (WAV)
    sonido_victoria = None
    sonido_derrota = None
    sonido_movimiento = None

    ruta_victoria = os.path.join(carpeta_sonidos, "sonido_victoria.wav")
    ruta_derrota = os.path.join(carpeta_sonidos, "sonido_derrota.wav")
    ruta_movimiento = os.path.join(carpeta_sonidos, "sonido_movimiento.wav")
    if os.path.exists(ruta_victoria):
        sonido_victoria = pygame.mixer.Sound(ruta_victoria)
    if os.path.exists(ruta_derrota):
        sonido_derrota = pygame.mixer.Sound(ruta_derrota)
    if os.path.exists(ruta_movimiento):
        sonido_movimiento = pygame.mixer.Sound(ruta_movimiento)

    # Cargar sprites de tablero (pared, suelo, meta)
    img_pared_orig = cargar_sprite("pared.png")
    img_suelo_orig = cargar_sprite("suelo.png")
    img_meta_orig = cargar_sprite("meta.png")
    img_pared = pygame.transform.scale(img_pared_orig, (tamano_celda, tamano_celda)) if img_pared_orig else None
    img_suelo = pygame.transform.scale(img_suelo_orig, (tamano_celda, tamano_celda)) if img_suelo_orig else None
    img_meta = pygame.transform.scale(img_meta_orig, (tamano_celda, tamano_celda)) if img_meta_orig else None

    # Inicializar joystick (soporte de gamepad = +3 puntos extra)
    joystick = None
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    musica_activa = True
    joy_cooldown = 0  # Evitar movimiento continuo con joystick

    # === SISTEMA DE NIVELES ===
    # 3 niveles progresivos: cada nivel tiene mas paredes
    NIVELES_PAREDES = [0.25, 0.30, 0.35]  # Nivel 1, 2, 3
    BONUS_POR_NIVEL = 50  # Puntos extra al completar un nivel

    # === BUCLE DE ESTADOS DEL JUEGO ===
    corriendo = True
    while corriendo:
        # --- MENU PRINCIPAL ---
        if musica_cargada:
            pygame.mixer.music.play(-1)
        resultado_menu = pantalla_menu(pantalla, ancho, alto)

        if resultado_menu == "salir":
            break

        # --- JUEGO CON NIVELES ---
        nivel = 1
        puntaje = 0
        debug_activo = False
        jugando_niveles = True

        while jugando_niveles and corriendo:
            # generar_mundo() se ejecuta UNA VEZ por nivel
            porcentaje = NIVELES_PAREDES[nivel - 1]
            mapa, jugador, meta_x, meta_y, enemigos = inicializar_juego(
                FILAS, COLUMNAS, porcentaje
            )
            turno = 0
            estado_juego = "jugando"

            jugando = True
            while jugando and corriendo:
                reloj.tick(FPS)
                if joy_cooldown > 0:
                    joy_cooldown -= 1

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        corriendo = False
                        jugando = False
                        jugando_niveles = False

                    # --- CONTROL DE FOCO (PAUSA INTELIGENTE) ---
                    if evento.type == pygame.ACTIVEEVENT:
                        if evento.state == 2 and evento.gain == 0:
                            sigue = manejar_perdida_foco(musica_cargada, musica_activa)
                            if not sigue:
                                corriendo = False
                                jugando = False
                                jugando_niveles = False

                    if evento.type == pygame.KEYDOWN:
                        # Tecla ESC: volver al menu
                        if evento.key == pygame.K_ESCAPE:
                            jugando = False
                            jugando_niveles = False

                        # Tecla D: Toggle debug mode
                        if evento.key == pygame.K_d:
                            debug_activo = not debug_activo

                        # Tecla M: Toggle musica
                        if evento.key == pygame.K_m:
                            if musica_activa:
                                if musica_cargada:
                                    pygame.mixer.music.pause()
                            else:
                                if musica_cargada:
                                    pygame.mixer.music.unpause()
                            musica_activa = not musica_activa

                        # ENTER en game over: continuar
                        if evento.key == pygame.K_RETURN and estado_juego != "jugando":
                            jugando = False

                        # Flechas: movimiento (solo durante el juego)
                        if estado_juego == "jugando":
                            dx, dy = 0, 0
                            if evento.key == pygame.K_UP:
                                dx, dy = -1, 0
                            elif evento.key == pygame.K_DOWN:
                                dx, dy = 1, 0
                            elif evento.key == pygame.K_LEFT:
                                dx, dy = 0, -1
                            elif evento.key == pygame.K_RIGHT:
                                dx, dy = 0, 1

                            if dx != 0 or dy != 0:
                                turno, estado_juego = procesar_movimiento(
                                    dx, dy, jugador, mapa, enemigos, turno,
                                    sonido_movimiento, sonido_victoria, sonido_derrota,
                                    meta_x, meta_y, estado_juego
                                )

                    # --- GAMEPAD ---
                    if evento.type == pygame.JOYBUTTONDOWN:
                        if evento.button == 0 and estado_juego != "jugando":
                            jugando = False
                        if evento.button == 7 and estado_juego != "jugando":
                            jugando = False

                    if evento.type == pygame.JOYHATMOTION and estado_juego == "jugando":
                        dx, dy = 0, 0
                        if evento.value == (0, 1):
                            dx, dy = -1, 0
                        elif evento.value == (0, -1):
                            dx, dy = 1, 0
                        elif evento.value == (-1, 0):
                            dx, dy = 0, -1
                        elif evento.value == (1, 0):
                            dx, dy = 0, 1

                        if dx != 0 or dy != 0:
                            turno, estado_juego = procesar_movimiento(
                                dx, dy, jugador, mapa, enemigos, turno,
                                sonido_movimiento, sonido_victoria, sonido_derrota,
                                meta_x, meta_y, estado_juego
                            )

                # Joystick analogico
                if joystick and estado_juego == "jugando" and joy_cooldown == 0:
                    eje_x = joystick.get_axis(0)
                    eje_y = joystick.get_axis(1)
                    dx, dy = 0, 0
                    if eje_y < -0.5:
                        dx, dy = -1, 0
                    elif eje_y > 0.5:
                        dx, dy = 1, 0
                    elif eje_x < -0.5:
                        dx, dy = 0, -1
                    elif eje_x > 0.5:
                        dx, dy = 0, 1

                    if dx != 0 or dy != 0:
                        turno, estado_juego = procesar_movimiento(
                            dx, dy, jugador, mapa, enemigos, turno,
                            sonido_movimiento, sonido_victoria, sonido_derrota,
                            meta_x, meta_y, estado_juego
                        )
                        joy_cooldown = 8

                # === DIBUJAR ===
                pantalla.fill(COLOR_FONDO)

                # 1. Tablero
                dibujar_tablero(pantalla, mapa, tamano_celda,
                                img_pared, img_suelo, offset_x, offset_y)

                # 2. Meta
                dibujar_meta(pantalla, meta_x, meta_y, tamano_celda,
                             img_meta, offset_x, offset_y)

                # 3. Debug
                if debug_activo:
                    for enemigo in enemigos:
                        if enemigo.algoritmo == "Astar":
                            enemigo.dibujar_debug(pantalla, COLOR_CAMINO_ASTAR,
                                                  COLOR_CAMINO_ASTAR, tamano_celda,
                                                  offset_x, offset_y)
                        elif enemigo.algoritmo == "BFS":
                            enemigo.dibujar_debug(pantalla, COLOR_EXPLORACION_BFS,
                                                  COLOR_EXPLORACION_BFS, tamano_celda,
                                                  offset_x, offset_y)
                        elif enemigo.algoritmo == "DFS":
                            enemigo.dibujar_debug(pantalla, COLOR_EXPLORACION_DFS,
                                                  COLOR_EXPLORACION_DFS, tamano_celda,
                                                  offset_x, offset_y)

                # 4. Jugador y Enemigos
                jugador.dibujar(pantalla, tamano_celda, offset_x, offset_y)
                for enemigo in enemigos:
                    enemigo.dibujar(pantalla, tamano_celda, offset_x, offset_y)

                # 5. Nombres de enemigos (en debug)
                if debug_activo:
                    dibujar_nombres_enemigos(pantalla, enemigos, tamano_celda,
                                             alto, offset_x, offset_y)

                # 6. Panel con nivel y puntaje
                puntaje_actual = puntaje + turno
                dibujar_panel_info(pantalla, turno, debug_activo, estado_juego,
                                   enemigos, jugador, meta_x, meta_y,
                                   panel_x, panel_y, panel_ancho, panel_alto,
                                   nivel, puntaje_actual)

                # 7. Game over / Victoria
                if estado_juego != "jugando":
                    victoria_total = (estado_juego == "ganaste" and nivel >= 3)
                    pantalla_game_over(pantalla, estado_juego == "ganaste",
                                       ancho, alto, puntaje_actual, nivel,
                                       victoria_total)

                pygame.display.flip()

            # --- Fin del nivel: calcular puntaje y decidir siguiente paso ---
            puntaje += turno  # Sumar turnos sobrevividos

            if estado_juego == "ganaste":
                puntaje += BONUS_POR_NIVEL  # Bonus por ganar el nivel
                if nivel >= 3:
                    # Victoria Total — volver al menu
                    jugando_niveles = False
                else:
                    # Siguiente nivel
                    nivel += 1
            else:
                # Perdio — volver al menu
                jugando_niveles = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
