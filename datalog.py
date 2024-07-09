import serial
import csv
from datetime import datetime
from tkinter import Tk, filedialog
import matplotlib.pyplot as plt

# Configuración del puerto serie
try:
    ser = serial.Serial('COM3', 115200)  # Reemplaza 'COM3' con el puerto serie correcto
except serial.SerialException as e:
    print(f"Error al abrir el puerto serie: {e}")
    exit(1)

# Crear una ventana emergente para que el usuario elija el directorio donde guardar el archivo CSV
root = Tk()
root.withdraw()  # Ocultar la ventana principal

csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

# Preparar el gráfico
plt.ion()  # Modo interactivo de matplotlib
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot(x_data, y_data)
ax.set_title('Sensor Data')
ax.set_xlabel('Time')
ax.set_ylabel('IR Value')

with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['IR Value', 'Elapsed Time', 'Timestamp'])  # Escribir encabezados

    # Bucle principal
    start_time = datetime.now()  # Registro del tiempo de inicio
    try:
        first_line = True
        while True:
            # Lee datos desde el puerto serie
            serial_data = ser.readline().decode('utf-8').strip()
            if serial_data:
                if first_line:
                    first_line = False
                    continue  # Saltar la primera línea, que es un encabezado

                ir_value = int(serial_data)

                # Calcula el tiempo transcurrido desde el inicio
                elapsed_time = (datetime.now() - start_time).total_seconds()

                # Obtiene la marca de tiempo
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Escribe los datos en el archivo CSV
                csv_writer.writerow([ir_value, elapsed_time, timestamp])

                # Actualizar los datos del gráfico
                x_data.append(elapsed_time)
                y_data.append(ir_value)
                line.set_xdata(x_data)
                line.set_ydata(y_data)
                ax.relim()
                ax.autoscale_view()

                # Redibujar el gráfico
                fig.canvas.draw()
                fig.canvas.flush_events()

                # Imprime los datos en la consola para verificar
                print(f"IR Value: {ir_value}, Elapsed Time: {elapsed_time} s, Timestamp: {timestamp}")

    except KeyboardInterrupt:
        print("Interrupción del usuario. Cerrando el programa.")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        # Cierra el puerto serie al finalizar
        if ser.is_open:
            ser.close()
            print("Puerto serie cerrado.")
