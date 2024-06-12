import pandas as pd
import json
import random

with open('congregaciones.json', 'r') as file:
    congregations_data = json.load(file)

df_congregations = pd.DataFrame(congregations_data)

with open('turnos_asignados_y_por_asignar.json', 'r') as file:
    shifts_data = json.load(file)

df_shifts = pd.DataFrame(shifts_data)

frozen_congregations = df_shifts['congregacion'].dropna().unique()

assignments = {congregation: 0 for congregation in df_congregations['congregacion'] if
               congregation not in frozen_congregations}


def has_restriction(congregation, day, date):
    row = df_congregations[df_congregations['congregacion'] == congregation].iloc[0]
    if day in row['dias_no_asignar'] or date in row['fechas_no_asignar']:
        return True
    return False


for idx, row in df_shifts.iterrows():
    if pd.isna(row['congregacion']):
        day = row['dia']
        date = pd.to_datetime(row['fecha'])
        possible_congregations = [congregation for congregation in assignments if
                                  not has_restriction(congregation, day, date)]

        possible_congregations.sort(key=lambda x: assignments[x])

        min_assignments = assignments[possible_congregations[0]]
        min_congregations = [c for c in possible_congregations if assignments[c] == min_assignments]
        random.shuffle(min_congregations)

        assigned_congregation = min_congregations[0]
        df_shifts.at[idx, 'congregacion'] = assigned_congregation
        assignments[assigned_congregation] += 1

assignments_distribution = df_shifts['congregacion'].value_counts()
print(assignments_distribution)

df_shifts.to_csv("programa_de_vigilancia_optimizado.csv", index=False)
