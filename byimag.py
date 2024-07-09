import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos desde el archivo Excel
datos = pd.read_excel('cnn.xlsx')

# Ordenar los datos por Elapsed Time si no están ordenados
datos = datos.sort_values(by='Elapsed Time')

# Definir el tamaño de la imagen (en píxeles)
ancho_imagen = 800
alto_imagen = 600

# Escalar los datos para que se ajusten a las dimensiones de la imagen
max_valor = datos['IR Value'].max()
min_valor = datos['IR Value'].min()
datos['IR Value'] = (datos['IR Value'] - min_valor) / (max_valor - min_valor)

# Crear una matriz de unos (imagen en blanco)
imagen = [[1 for _ in range(ancho_imagen)] for _ in range(alto_imagen)]

# Rellenar la imagen con los datos de IR Value
for indice, fila in datos.iterrows():
    x = int(fila['Elapsed Time'] / datos['Elapsed Time'].max() * (ancho_imagen - 1))
    y = int(fila['IR Value'] * (alto_imagen - 1))
    imagen[y][x] = 0

# Mostrar la imagen
plt.imshow(imagen, cmap='binary')
plt.show()
