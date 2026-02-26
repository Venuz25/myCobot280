import sys
import time
from pymycobot import MyCobotSocket
from dualsense_controller import DualSenseController

# Variables de conexion
ROBOT_IP = "192.168.1.64"
ROBOT_PORT = 9000
ROBOT_SPEED = 80

STICK_DRIFT_OFFSET = 0.06  # Valor para compensar el drift del stick
STICK_DEADZONE = 0.2     # Umbral para ignorar el movimiento
MIN_ANGLE_OUT = -100.0   # Ángulo mínimo al que escalar
MAX_ANGLE_OUT = 100.0    # Ángulo máximo al que escalar


class CobotController:
    def __init__(self):
        print("Iniciando controlador del Cobot...")
        # Estado inicial
        self.actual_servo = 1
        self.actual_angle = 0.0
        
        # Conectar dispositivos
        try:
            self.mc = self.connect_robot()
            self.controller = self.connect_controller()
        except Exception as e:
            print(f"Error fatal al inicializar: {e}", file=sys.stderr)
            sys.exit(1)
            
        self.register_callbacks()
        print(f"Controlador listo. Servo inicial: {self.actual_servo}")

    def connect_robot(self):
        print(f"Conectando al robot en {ROBOT_IP}:{ROBOT_PORT}...")
        mc = MyCobotSocket(ROBOT_IP, ROBOT_PORT)
        
        if not mc.is_controller_connected():
            raise Exception(f"No se pudo conectar al robot en {ROBOT_IP}")
        print("Robot conectado.")
        mc.release_all_servos()
        return mc

    def connect_controller(self):
        print("Buscando control DualSense...")
        device_infos = DualSenseController.enumerate_devices()
        if not device_infos:
            raise Exception('No se encontró ningún control DualSense.')
        
        controller = DualSenseController(device_infos[0].path)
        controller.lightbar.set_color_red()
        print("Control DualSense conectado.")
        return controller

    def map_value(self, in_val, in_min, in_max, out_min, out_max):
        return (in_val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    # --- Callbacks (Eventos del Mando) ---

    def register_callbacks(self):        
        # Stick Izquierdo (X) para seleccionar ángulo
        self.controller.left_stick_x.on_change(self.on_left_stick_x_changed)
        
        # Botones de acción
        self.controller.btn_cross.on_down(self.send_home_position)
        self.controller.btn_circle.on_down(self.release_servos)
        self.controller.btn_square.on_down(self.send_current_angle)

        # Selección de Servo (D-Pad y Hombros)
        # Usamos 'lambda' para pasar el número de servo a nuestra función.
        self.controller.btn_up.on_down(lambda: self.set_servo(1))
        self.controller.btn_left.on_down(lambda: self.set_servo(2))
        self.controller.btn_down.on_down(lambda: self.set_servo(3))
        self.controller.btn_right.on_down(lambda: self.set_servo(4))
        self.controller.btn_l1.on_down(lambda: self.set_servo(5))
        self.controller.btn_r1.on_down(lambda: self.set_servo(6))

    def set_servo(self, servo_id):
        """Actualiza el servo que se está controlando."""
        self.actual_servo = servo_id
        print(f"Servo seleccionado: {self.actual_servo}")

    def on_left_stick_x_changed(self, stick_x):
        """
        Calcula el ángulo basado en la posición del stick,
        aplicando la lógica de drift y deadzone.
        """
        # 1. Aplicar compensación de drift
        if stick_x >= 0:
            no_drift = stick_x - STICK_DRIFT_OFFSET
        else:
            no_drift = stick_x + STICK_DRIFT_OFFSET

        # 2. Aplicar deadzone
        if abs(no_drift) <= STICK_DEADZONE:
            return 
            
        # 3. Calcular nuevo ángulo (fuera del deadzone)
        self.actual_angle = self.map_value(
            no_drift, 
            -1.0, 
            1.0, 
            MIN_ANGLE_OUT, 
            MAX_ANGLE_OUT
        )

    def send_current_angle(self):
        print(f"Enviando [Ángulo: {self.actual_angle:.2f}] a [Servo: {self.actual_servo}] a [Vel: {ROBOT_SPEED}]")
        self.mc.send_angle(self.actual_servo, self.actual_angle, ROBOT_SPEED)

    def send_home_position(self):
        print("Enviando a posición HOME [0,0,0,0,0,0]")
        self.mc.send_angles([0, 0, 0, 0, 0, 0], ROBOT_SPEED)

    def release_servos(self):
        print("Liberando todos los servos.")
        self.mc.release_all_servos()

    def run(self):
        print("Activando listeners del mando. Presiona Ctrl+C para salir.")
        self.controller.activate()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nCerrando conexiones...")
        except Exception as ex:
            print(f"\nError inesperado: {ex}")
        finally:
            self.controller.deactivate()
            self.release_servos()
            print("Controlador desactivado y servos liberados. Adiós.")

if __name__ == "__main__":
    control = CobotController()
    control.run()