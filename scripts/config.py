# --- CONFIGURACIÓN GENERAL DEL JUEGO: IA HUNTER ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003

TITULO_JUEGO = "IA HUNTER - Evasión Algorítmica"

# Dimensiones de la pantalla (en píxeles)
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 800

# Configuración de la Cuadrícula (Grid)
# El mapa es una matriz donde cada celda representa un estado del entorno
TAMAÑO_CELDA = 40  # Cada celda del mapa mide 40x40 píxeles

# Calculamos cuántas celdas caben (800/40 = 20 columnas, 600/40 = 15 filas)
COLUMNAS = ANCHO_PANTALLA // TAMAÑO_CELDA
FILAS = ALTO_PANTALLA // TAMAÑO_CELDA

# --- SISTEMA DE TURNOS ---
# El juego es por turnos: Jugador mueve -> IA calcula -> IA mueve
# No necesitamos FPS alto, solo suficiente para animaciones fluidas
FPS = 30

# --- COLORES (Formato RGB) ---

# Entorno / Tablero
COLOR_FONDO = (30, 30, 30)         # Gris oscuro (fondo general)
COLOR_GRID = (50, 50, 50)          # Líneas de la cuadrícula
COLOR_SUELO = (40, 40, 45)         # Celda transitable (0)
COLOR_PARED = (100, 100, 100)      # Obstáculo/Pared (1)
COLOR_META = (0, 255, 100)         # Punto de destino (E)

# Jugador (El Intruso)
COLOR_JUGADOR = (0, 200, 255)      # Azul cián

# Enemigos (Programas de Seguridad) - Cada uno con color distinto
COLOR_ENEMIGO_ASTAR = (255, 50, 50)      # Rojo - "El Sabueso" (A*)
COLOR_ENEMIGO_BFS = (255, 165, 0)        # Naranja - "El Patrullero" (BFS)
COLOR_ENEMIGO_DFS = (180, 0, 255)        # Púrpura - "El Errático" (DFS)

# --- MODO DEBUG (Tecla D) ---
# Colores para la visualización de algoritmos
COLOR_CAMINO_ASTAR = (255, 80, 80)       # Línea roja: ruta calculada por A*
COLOR_EXPLORACION_BFS = (80, 255, 80)    # Cuadros verdes: nodos explorados por BFS
COLOR_EXPLORACION_DFS = (200, 100, 255)  # Cuadros morados: nodos explorados por DFS
COLOR_DEBUG_TEXTO = (255, 255, 255)      # Blanco para texto de debug

# --- VALORES DE LA MATRIZ (MAPA) ---
# Estos valores representan qué hay en cada celda del grid
CELDA_SUELO = 0     # Transitable
CELDA_PARED = 1     # Obstáculo
CELDA_JUGADOR = 2   # Posición del jugador (S - Start)
CELDA_META = 3      # Objetivo (E - End)

# --- POSICIONES INICIALES ---
POS_INICIAL_JUGADOR = (1, 1)                   # Esquina superior izquierda
POS_INICIAL_META = (COLUMNAS - 2, FILAS - 2)   # Esquina inferior derecha

# --- PORCENTAJE DE PAREDES ---
# Qué porcentaje del mapa se llenará de paredes aleatorias
PORCENTAJE_PAREDES = 0.25  # 25% del mapa serán obstáculos

# --- PUNTOS DE PATRULLA PARA EL ENEMIGO BFS ---
# El Patrullero va de punto A a punto B y viceversa
PATRULLA_PUNTO_A = (1, FILAS - 2)        # Esquina inferior izquierda
PATRULLA_PUNTO_B = (COLUMNAS - 2, 1)     # Esquina superior derecha