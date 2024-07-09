import serial
import csv
from datetime import datetime
import numpy as np
from scipy.fftpack import fft

# Definir variables para la FFT
sampleRate = 100  # Frecuencia de muestreo en Hz
samples = 256      # Número de muestras para FFT

# Inicializar la señal con un valor inicial arbitrario (puedes ajustar según sea necesario)
initial_value = 100
signal = np.full(samples, initial_value)

# Configuración del puerto serie
try:
    ser = serial.Serial('COM3', 115200)  # Reemplaza 'COM3' con el puerto serie correcto
except serial.SerialException as e:
    print(f"Error al abrir el puerto serie: {e}")
    exit(1)

# Crear un archivo CSV para almacenar los datos
csv_file_path = 'datos_pulsometro_fft.csv'

with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['IR Value', 'Timestamp', 'Elapsed Time', 'Dominant Frequency'])  # Escribir encabezados

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

                # Realiza la Transformada Rápida de Fourier (FFT)
                signal = np.append(signal[1:], ir_value)

                # Imprime los datos actuales en el monitor serial
                print(f"IR Value: {ir_value}, Timestamp: {timestamp}, Elapsed Time: {elapsed_time} s")

                # Escribe los datos en el archivo CSV
                csv_writer.writerow([ir_value, timestamp, elapsed_time])

    except KeyboardInterrupt:
        print("Interrupción del usuario. Realizando la Transformada Rápida de Fourier (FFT).")

        # Cierra el archivo CSV antes de realizar la FFT
        csv_file.close()

        # Realiza la Transformada Rápida de Fourier (FFT) después de cerrar el puerto serie
        fft_result = fft(signal)
        fft_magnitude = np.abs(fft_result)
        dominant_frequency = np.argmax(fft_magnitude) * sampleRate / samples

        # Imprime los resultados finales
        print(f"Dominant Frequency: {dominant_frequency} Hz")

        # Vuelve a abrir el archivo CSV para agregar los resultados de la FFT
        with open(csv_file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Lee la fila de encabezados

            # Abre un nuevo archivo CSV para almacenar los datos actualizados
            updated_csv_file_path = 'datos_pulsometro_fft_actualizado.csv'
            with open(updated_csv_file_path, 'w', newline='') as updated_csv_file:
                updated_csv_writer = csv.writer(updated_csv_file)

                # Copia los encabezados al nuevo archivo
                updated_csv_writer.writerow(header + ['Dominant Frequency'])

                # Copia los datos anteriores al nuevo archivo
                for row in csv_reader:
                    updated_csv_writer.writerow(row + [dominant_frequency])

            print(f"Se ha creado un nuevo archivo CSV con los resultados de la FFT: {updated_csv_file_path}")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        # Cierra el puerto serie al finalizar
        if ser.is_open:
            ser.close()
            print("Puerto serie cerrado.")
