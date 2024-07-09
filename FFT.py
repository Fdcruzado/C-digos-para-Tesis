import pandas as pd
import numpy as np
from scipy.fftpack import fft
from scipy.interpolate import interp1d
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Cargar datos desde el archivo CSV
file_path = 'datos_pulsometro.csv'  # Ajusta el nombre del archivo según sea necesario
df = pd.read_csv(file_path)

# Extraer la columna 'IR Value' y 'Elapsed Time'
ir_values = df['IR Value'].values
elapsed_time_values = df['Elapsed Time'].values

# Interpolar la señal para tener una representación uniforme en el tiempo
interp_func = interp1d(elapsed_time_values, ir_values, kind='linear', fill_value='extrapolate')

# Crear un nuevo conjunto de tiempos equiespaciados
uniform_elapsed_time = np.linspace(elapsed_time_values[0], elapsed_time_values[-1], len(elapsed_time_values))

# Evaluar la función interpolada en los nuevos tiempos
uniform_ir_values = interp_func(uniform_elapsed_time)

# Calcular la frecuencia de muestreo y la frecuencia de Nyquist
total_data_points = len(uniform_ir_values)
total_time = uniform_elapsed_time[-1]  # Último valor de tiempo
sampling_frequency = total_data_points / total_time
nyquist_frequency = sampling_frequency / 2

print(f"Frecuencia de muestreo: {sampling_frequency} Hz")
print(f"Frecuencia de Nyquist: {nyquist_frequency} Hz")

# Realizar la FFT
fft_result = fft(uniform_ir_values)
fft_magnitude = np.abs(fft_result)

# Obtener las frecuencias y el espectro de frecuencia correspondiente
samples = len(uniform_ir_values)
frequencies = np.fft.fftfreq(samples, 1 / sampling_frequency)
positive_frequencies = frequencies[:samples//2]
positive_fft_magnitude = fft_magnitude[:samples//2]

# Filtrar las frecuencias y magnitudes para mostrar solo a partir de 0.5 Hz
threshold_frequency = 0.5
indices_above_threshold = np.where(positive_frequencies >= threshold_frequency)[0]
filtered_frequencies = positive_frequencies[indices_above_threshold]
filtered_fft_magnitude = positive_fft_magnitude[indices_above_threshold]

# Calcular la primera y segunda derivada
first_derivative = np.gradient(filtered_fft_magnitude, filtered_frequencies)
second_derivative = np.gradient(first_derivative, filtered_frequencies)

# Filtrar las derivadas para mostrar solo a partir de 0.5 Hz
filtered_first_derivative = first_derivative
filtered_second_derivative = second_derivative

# Crear subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

# Plot de la transformada de Fourier original
axs[0].plot(filtered_frequencies, filtered_fft_magnitude, label='Espectro de Frecuencia')
axs[0].set_title('Espectro de Frecuencia')
axs[0].set_ylabel('Magnitud')
axs[0].legend()

# Plot de la primera derivada
axs[1].plot(filtered_frequencies, filtered_first_derivative, label='Primera Derivada', linestyle='--')
axs[1].set_title('Primera Derivada')
axs[1].set_ylabel('Magnitud')
axs[1].legend()

# Plot de la segunda derivada
axs[2].plot(filtered_frequencies, filtered_second_derivative, label='Segunda Derivada', linestyle=':')
axs[2].set_title('Segunda Derivada')
axs[2].set_xlabel('Frecuencia (Hz)')
axs[2].set_ylabel('Magnitud')
axs[2].legend()

plt.tight_layout()
plt.show()

dominant_frequency = positive_frequencies[np.argmax(filtered_fft_magnitude)]
print(f'Dominant Frequency: {dominant_frequency} Hz')
