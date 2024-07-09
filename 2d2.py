import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyts.image import RecurrencePlot

# Cargar los datos desde el archivo Excel
datos = pd.read_excel('cnn5.xlsx')

# Ordenar los datos por Elapsed Time si no están ordenados
datos = datos.sort_values(by='Elapsed Time')

# Tomar solo las primeras 1000 muestras de la serie temporal
datos = datos.iloc[:1000]

# Crear un objeto RecurrencePlot
rp = RecurrencePlot(threshold='point', percentage=20)

# Transformar los datos en un FRP
frp = rp.fit_transform(datos['IR Value'].values.reshape(1, -1))

# Visualizar el FRP
plt.figure(figsize=(6, 6))
plt.imshow(frp[0], cmap='binary', origin='lower')
plt.xlabel('Elapsed Time')
plt.ylabel('Elapsed Time')
plt.title('Fuzzy Recurrence Plot')
plt.show()
