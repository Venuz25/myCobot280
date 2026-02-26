from inputs import get_gamepad

def main():
    """
    Función principal para leer los eventos del joystick.
    """
    print("Conecta tu Logitech Attack 3 y presiona un botón o mueve el joystick...")
    
    try:
        while True:
            # get_gamepad() espera hasta que detecta un gamepad (joystick)
            # y luego empieza a capturar sus eventos.
            events = get_gamepad()
            
            for event in events:
                # event.code -> El nombre del eje o botón (ej: 'ABS_X', 'BTN_TRIGGER')
                # event.state -> El valor (ej: 0-255 para ejes, 0 o 1 para botones)
                # event.ev_type -> El tipo de evento (ej: 'Absolute' para ejes, 'Key' para botones)

                # Filtramos para mostrar solo los eventos que nos interesan
                if event.ev_type == 'Absolute':
                    # Los ejes (X, Y, Acelerador)
                    print(f"Eje: {event.code}, Valor: {event.state}")
                elif event.ev_type == 'Key':
                    # Los botones
                    print(f"Botón: {event.code}, Estado: {event.state}")

    except KeyboardInterrupt:
        # Permite salir del bucle presionando Ctrl+C en la terminal
        print("\nSaliendo del programa.")
    except Exception as e:
        print(f"No se detectó ningún joystick o gamepad. Asegúrate de que esté conectado.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()