import pandas as pd
import pulp

# Cargar los datos desde los archivos CSV
df_guardias = pd.read_csv('schedule.csv')
df_congregaciones = pd.read_csv('congregations.csv')

# Normalizar los nombres de los días a minúsculas para comparación
df_guardias['dia'] = df_guardias['dia'].str.lower()
df_congregaciones['Dia entre semana'] = df_congregaciones['Dia entre semana'].str.lower()
df_congregaciones['Dia fin de semana'] = df_congregaciones['Dia fin de semana'].str.lower()

# Ordenar las congregaciones por los kilómetros de viaje en ascendente
df_congregaciones = df_congregaciones.sort_values(by='kms de viaje')

# Crear el problema de optimización
prob = pulp.LpProblem("AsignacionGuardias", pulp.LpMinimize)

# Variables de decisión
x = pulp.LpVariable.dicts("x", [(i, j) for i in df_congregaciones.index for j in df_guardias.index], cat='Binary')

# Restricciones

# Evitar asignaciones en días de reunión
for i in df_congregaciones.index:
    meeting_day_week = df_congregaciones.loc[i, 'Dia entre semana']
    meeting_day_weekend = df_congregaciones.loc[i, 'Dia fin de semana']

    for j in df_guardias.index:
        guard_day = df_guardias.loc[j, 'dia']

        if guard_day == meeting_day_week or guard_day == meeting_day_weekend:
            prob += x[(i, j)] == 0

# Cada guardia debe ser asignada a una congregación
for j in df_guardias.index:
    prob += pulp.lpSum(x[(i, j)] for i in df_congregaciones.index) == 1

# Añadir restricciones para balancear las asignaciones
# Calcular el número promedio de asignaciones
avg_assignments = len(df_guardias) / len(df_congregaciones)

# Añadir restricciones para evitar la sobrecarga
for i in df_congregaciones.index:
    num_assignments = pulp.lpSum(x[(i, j)] for j in df_guardias.index)
    prob += num_assignments <= avg_assignments + 1

# Función objetivo: minimizar el número máximo de asignaciones por congregación
max_assignments = pulp.LpVariable("max_assignments", lowBound=0, cat='Continuous')
for i in df_congregaciones.index:
    prob += pulp.lpSum(x[(i, j)] for j in df_guardias.index) <= max_assignments
prob += max_assignments

# Resolver el problema
prob.solve()

# Resultado
assignments = []
for i in df_congregaciones.index:
    for j in df_guardias.index:
        if pulp.value(x[(i, j)]) == 1:
            assignments.append({
                "Dia": df_guardias.loc[j, 'dia'].capitalize(),
                "Fecha": df_guardias.loc[j, 'fecha'],
                "Congregación": df_congregaciones.loc[i, 'Nombre congregación'],
                "Turno": df_guardias.loc[j, 'turno'],
                "Horario": df_guardias.loc[j, 'Horario'],
                "Coordinador": "",
                "Celular": ""
            })

df_result = pd.DataFrame(assignments)

# Guardar el resultado en un archivo CSV
df_result.to_csv('asignaciones_vigilancia.csv', index=False)

# Mostrar el resultado en formato de cadena
print(df_result.to_string(index=False))
