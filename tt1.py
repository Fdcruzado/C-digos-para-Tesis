import serial
import csv
from datetime import datetime

# Configuración del puerto serie
try:
    ser = serial.Serial('COM3', 115200)  # Reemplaza 'COM3' con el puerto serie correcto
except serial.SerialException as e:
    print(f"Error al abrir el puerto serie: {e}")
    exit(1)

# Crear un archivo CSV para almacenar los datos
csv_file_path = 'datos_pulsometro.csv'

with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['IR Value', 'Timestamp', 'Elapsed Time'])  # Escribir encabezados

    # Bucle principal
    start_time = datetime.now()  # Registro del tiempo de inicio
    try:
        while True:
            # Lee datos desde el puerto serie
            line = ser.readline().decode('utf-8').strip()
            if line:
                ir_value = int(line)

                # Obtiene la marca de tiempo
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Calcula el tiempo transcurrido desde el inicio
                elapsed_time = (datetime.now() - start_time).total_seconds()

                # Escribe los datos en el archivo CSV
                csv_writer.writerow([ir_value, timestamp, elapsed_time])

                # Imprime los datos en la consola para verificar
                print(f"IR Value: {ir_value}, Timestamp: {timestamp}, Elapsed Time: {elapsed_time} s")

    except KeyboardInterrupt:
        print("Interrupción del usuario. Cerrando el programa.")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        # Cierra el puerto serie al finalizar
        if ser.is_open:
            ser.close()
            print("Puerto serie cerrado.")
