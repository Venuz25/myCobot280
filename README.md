# Control del Brazo Robótico MyCobot 280 mediante Controlador PS4

El presente proyecto proporciona scripts en Python para el control del brazo robótico MyCobot 280 utilizando un controlador de PlayStation 4 (u otros gamepads compatibles, como el Logitech Attack 3). El sistema permite la manipulación precisa de las articulaciones y movimientos del robot a través de entradas intuitivas de control.

---

## Acerca del Proyecto

Este repositorio contiene programas en Python diseñados para interactuar con el brazo robótico MyCobot 280. El objetivo principal es habilitar el control de los movimientos y ángulos de las articulaciones del robot mediante mandos de videojuegos, específicamente un controlador de PS4 (a través de la biblioteca `dualsense-controller`) y un joystick Logitech Attack 3 (mediante la biblioteca `inputs`).

---

## Características Principales

- **Control por Gamepad:** Manipulación individual de las articulaciones y ángulos del robot utilizando un controlador de PS4 o un joystick Logitech Attack 3.
- **Retroalimentación en Tiempo Real:** Visualización de los cambios en los ángulos de las articulaciones y la velocidad en la terminal mientras se interactúa con el controlador.
- **Rangos Personalizables:** Definición de rangos de ángulos específicos para cada articulación, accesibles mediante los botones del controlador.
- **Control de Velocidad:** Ajuste dinámico de la velocidad de movimiento del robot utilizando el acelerador del joystick.
- **Funciones de Seguridad:** Inclusión de funciones para liberar los servomotores y retornar el robot a su posición inicial (home).
- **Lectura de Eventos del Joystick:** Script de utilidad para monitorear y mostrar los eventos de entrada brutos del joystick.

---

## Tecnologías Utilizadas

- **Python:** Lenguaje de programación principal utilizado en todos los scripts.
- **`pymycobot`:** Biblioteca oficial para la interacción con el brazo robótico MyCobot.
- **`inputs`:** Biblioteca para la lectura de entradas de gamepads y joysticks (utilizada para el Logitech Attack 3).
- **`dualsense-controller`:** Biblioteca para el manejo de las entradas del controlador de PS4 (DualSense).

---

## Estructura del Proyecto

```text
myCobot280/
├── attack3/
│   ├── attack3.py     # Script para leer eventos genéricos del joystick
│   └── brazoAttack.py # Script para controlar el MyCobot con el Logitech Attack 3
├── mando/
│   └── mando.py       # Script para controlar el MyCobot con el controlador PS4 DualSense
├── README.md          # Archivo de documentación del proyecto
└── tests.ipynb        # Jupyter Notebook para pruebas
```

---

## Enlaces de Interés

* **Sitio Oficial de MyCobot:** [https://www.elephantrobotics.com/en/mycobot/](https://www.elephantrobotics.com/en/mycobot/)

---

<div align="center">
  <strong>© 2025 | <a href="https://github.com/Venuz25">Areli Guevara</a></strong>
</div>
