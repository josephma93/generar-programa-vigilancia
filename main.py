import pandas as pd
import json
import random

# Cargar datos de congregaciones desde JSON
with open('congregaciones.json', 'r') as file:
    congregaciones_data = json.load(file)

df_congregaciones = pd.DataFrame(congregaciones_data)

# Cargar datos de turnos de vigilancia desde JSON
with open('turnos_asignados_y_por_asignar.json', 'r') as file:
    turnos_data = json.load(file)

df_vigilancia = pd.DataFrame(turnos_data)

# Identificar congregaciones congeladas
congeladas = df_vigilancia['congregacion'].dropna().unique()

# Crear un diccionario para contar las asignaciones
asignaciones = {congregacion: 0 for congregacion in df_congregaciones['congregacion'] if congregacion not in congeladas}


# Función para verificar si una congregación tiene restricción en un día específico
def tiene_restriccion(congregacion, dia, fecha):
    fila = df_congregaciones[df_congregaciones['congregacion'] == congregacion].iloc[0]
    if dia in fila['dias_no_asignar'] or fecha in fila['fechas_no_asignar']:
        return True
    return False


# Asignar las congregaciones de manera manual para equilibrar las asignaciones
for idx, row in df_vigilancia.iterrows():
    if pd.isna(row['congregacion']):
        dia = row['dia']
        fecha = pd.to_datetime(row['fecha'])
        posibles_congregaciones = [congregacion for congregacion in asignaciones if
                                   not tiene_restriccion(congregacion, dia, fecha)]

        # Ordenar las congregaciones por el número de asignaciones actuales (ascendente)
        posibles_congregaciones.sort(key=lambda x: asignaciones[x])

        # Aleatorizar las congregaciones con el mismo número de asignaciones
        min_asignaciones = asignaciones[posibles_congregaciones[0]]
        min_congregaciones = [c for c in posibles_congregaciones if asignaciones[c] == min_asignaciones]
        random.shuffle(min_congregaciones)

        # Asignar la congregación aleatoria con menos asignaciones actuales
        congregacion_asignada = min_congregaciones[0]
        df_vigilancia.at[idx, 'congregacion'] = congregacion_asignada
        asignaciones[congregacion_asignada] += 1

# Verificar la distribución de asignaciones por congregación
distribucion_asignaciones_final = df_vigilancia['congregacion'].value_counts()
print(distribucion_asignaciones_final)

# Exportar el DataFrame a un archivo JSON para descargar
df_vigilancia.to_csv("programa_de_vigilancia_optimizado.csv", index=False)
