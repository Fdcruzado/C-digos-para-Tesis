import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Paso 1: Cargar datos desde Excel
df = pd.read_excel('cnn3.xlsx')

# Paso 2: Extraer columnas relevantes
ir_values = df['IR Value'].values
elapsed_time = df['Elapsed Time'].values

# Paso 3: Combinar los valores IR Value y Elapsed Time en una secuencia binaria
binary_data = ['{0:08b}{1:08b}'.format(int(ir), int(elapsed)) for ir, elapsed in zip(ir_values, elapsed_time)]
binary_length = len(binary_data[0])

# Paso 4: Calcular la resolución para una imagen cuadrada de 168x168
resolution = 120

# Paso 5: Calcular el número de datos que podemos mostrar por fila y por columna
data_per_row = resolution // binary_length
data_per_column = resolution

# Paso 6: Calcular el número total de datos que podemos mostrar
total_data = data_per_row * data_per_column

# Paso 7: Crear una matriz de ceros para la imagen con la nueva resolución
image_matrix = np.zeros((resolution, resolution))

# Paso 8: Llenar la imagen con los datos concatenados
for i in range(data_per_column):
    for j in range(data_per_row):
        index = i * data_per_row + j
        if index < len(binary_data):
            binary_pair = binary_data[index]
            # Usar el bit menos significativo para determinar el valor del píxel
            for k, bit in enumerate(binary_pair):
                image_matrix[i, j * binary_length + k] = int(bit)

# Paso 9: Mostrar la imagen
plt.figure(figsize=(7.5, 7.5))  # Ajustar el tamaño de la figura para mantener la relación de aspecto
plt.imshow(image_matrix, cmap='gray', origin='lower', interpolation='nearest')
plt.axis('off')
plt.title('Imagen codificada de IR Value y Elapsed Time en binario (Estilo TV Estática)')
plt.show()
