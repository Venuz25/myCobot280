import time
from inputs import get_gamepad
from pymycobot.mycobot import MyCobot
from pymycobot import MyCobotSocket

IP = "192.168.1.64" 
PORT = 9000

# Conectarse al robot
print(f"Conectando a myCobot en {IP}...")
try:
    mc = MyCobotSocket(IP, PORT) 
    mc.power_on()
    mc.send_angles([0, 0, 0, 0, 0, 0], 50)
    print("¡Robot conectado! Mueve el joystick.")
except Exception as e:
    print(f"Error al conectar con el robot: {e}")
    exit()

def map_range(value, from_min, from_max, to_min, to_max):
    if from_max == from_min:
        return to_min
    normalized = (value - from_min) / (from_max - from_min)
    return (normalized * (to_max - to_min)) + to_min

# Configuración de Articulaciones
JOINT_CONFIG = {
    'BTN_PINKIE': {'id': 1, 'min': -150, 'max': 150}, # BTN 6
    'BTN_BASE':   {'id': 2, 'min': -135, 'max': 135}, # BTN 7
    'BTN_BASE2':  {'id': 3, 'min': -150, 'max': 150}, # BTN 8
    'BTN_BASE3':  {'id': 4, 'min': -130, 'max': 130}, # BTN 9
    'BTN_BASE4':  {'id': 5, 'min': -160, 'max': 160}, # BTN 10
    'BTN_BASE5':  {'id': 6, 'min': -160, 'max': 160}, # BTN 11
}

speed = 50
joint_id = 1
angMin = JOINT_CONFIG['BTN_PINKIE']['min']
angMax = JOINT_CONFIG['BTN_PINKIE']['max']

angle = 0 

print(f"Modo inicial: Servo {joint_id}, Velocidad {speed}")

try:
    while True:
        events = get_gamepad()
        for event in events:

            if event.ev_type == 'Absolute':
                
                # Joystick: establecer angulo
                if event.code == 'ABS_Y': 
                    angle = int(map_range(event.state, 0, 255, angMin, angMax))
                    angle = angle
                    
                    print(f"Ángulo fijado: {angle}°   ", end="\r")

                # Acelerador: establecer velocidad
                elif event.code == 'ABS_Z': 
                    speed = int(map_range(event.state, 0, 255, 1, 100))
                    print(f"Velocidad fijada: {speed}        ", end="\r")

            elif event.ev_type == 'Key':
                
                # Gatillo: enviar instruccion de moverse
                if event.code == 'BTN_TRIGGER':
                    if event.state == 1:
                        print(f"\nEnviando: J{joint_id}, {angle}° @ Vel {speed}")
                        mc.send_angle(joint_id, angle, speed)

                # BTN3: relaja servos
                elif event.code == 'BTN_THUMB2':
                    if event.state == 1: 
                        print("\nRelajando servos")
                        mc.release_all_servos() 

                # BTN 2: regresa servos a posicion 0
                elif event.code == 'BTN_THUMB': 
                    if event.state == 1: 
                        print("\nRegresando a posicion inicial")
                        mc.send_angles([0,0,0,0,0,0], 80)
                
                # Cambios de servos
                elif event.code in JOINT_CONFIG:
                    if event.state == 1:
                        config = JOINT_CONFIG[event.code]
                        joint_id = config['id']
                        angMin = config['min']
                        angMax = config['max']
                        print(f"\nServo {joint_id} seleccionado (Rango: {angMin}° a {angMax}°)")

except KeyboardInterrupt:
    print("\nSaliendo...")
    mc.power_off()