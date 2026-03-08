# 🎯 IA HUNTER — Evasión Algorítmica

**Nombre:** Breylin Gabriel Sanchez Santana
**Matrícula:** 23-EISN-2-003
**Asignatura:** Inteligencia Artificial — 10mo Semestre
**Universidad:** O&M

---

## ¿De qué trata?

IA HUNTER es un juego por turnos en una cuadrícula donde controlas a un "intruso digital" que debe llegar a un punto de extracción (la meta) sin ser atrapado por 3 enemigos controlados por inteligencia artificial.

Cada enemigo usa un algoritmo de búsqueda diferente:

| Enemigo | Algoritmo | Comportamiento |
|---|---|---|
| **El Sabueso** (rojo) | A* | Siempre encuentra la ruta más corta hacia ti |
| **El Patrullero** (naranja) | BFS | Patrulla entre dos puntos. Si te ve cerca, te persigue |
| **El Errático** (morado) | DFS | Toma rutas impredecibles |

Cada enemigo decide su acción usando un **Árbol de Comportamiento** (Behavior Tree) que evalúa si el jugador está dentro de su radio de detección de 8 celdas.

---

## Cómo ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el juego
```bash
python main.py
```

El juego arranca en pantalla completa automáticamente.

---

## Controles

| Tecla | Acción |
|---|---|
| Flechas / D-pad | Mover al jugador |
| D | Activar modo debug (ver rutas de la IA) |
| M | Activar/desactivar música |
| ESC | Volver al menú |
| Enter / Botón A | Confirmar |
| Stick analógico | Movimiento con gamepad |

---

## Algoritmos implementados

Todos los algoritmos fueron implementados **desde cero**, sin librerías externas de IA. Basados en el Lab-4 (búsqueda) y Lab-5 (Behavior Tree) del curso.

- **BFS** — Búsqueda en Anchura (cola FIFO, garantiza camino óptimo)
- **DFS** — Búsqueda en Profundidad (pila LIFO, caminos impredecibles)
- **A*** — A-Estrella con heurística Manhattan (cola de prioridad, óptimo y eficiente)
- **Árbol de Comportamiento** — Selector, Secuencia, AccionBT, Invertir, Timer

---

## Estructura del proyecto

```
├── main.py              ← Bucle principal, menú, dibujo
├── generar_sprites.py   ← Script para generar los sprites PNG
├── scripts/
│   ├── __init__.py      ← Paquete de Python
│   ├── config.py        ← Constantes y colores
│   ├── ia_core.py       ← Algoritmos de IA (BFS, DFS, A*, BT, generador de mundo)
│   └── sprites.py       ← Clases Jugador y Enemigo
├── assets/
│   ├── images/          ← Sprites PNG
│   ├── music/           ← Música de fondo (generada con Suno AI)
│   └── sounds/          ← Efectos de sonido WAV
├── requirements.txt
└── README.md
```

---

## Modo Debug

Presiona **D** durante el juego para ver la visualización de los algoritmos:
- Cuadros de colores = nodos explorados por cada algoritmo
- Líneas = camino calculado hacia el jugador

Esto permite ver cómo BFS explora uniformemente, DFS va profundo, y A* va directo al objetivo gracias a la heurística.

---

## Video

*(Link del video de YouTube aquí)*

---

## Tecnologías

- Python 3.12
- Pygame 2.6.1
