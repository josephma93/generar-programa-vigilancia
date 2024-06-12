# User Guide

## Introduction

This user guide explains in detail the implementation of the solution for assigning surveillance shifts to
congregations. The solution ensures that no congregation is overloaded with assignments and that assignments do not
interfere with the congregations' meeting days. This guide includes an overview of the solution's features,
pre-conditions, assumptions, and relevant details. It also provides representative examples of the data used.

## Features

1. **Balanced Assignments**: Ensures that assignments are distributed equitably among available congregations.
2. **Restrictions Handling**: Considers days of the week and specific dates when a congregation should not receive
   assignments.
3. **Congregation Freezing**: Assignments made manually (frozen assignments) are respected and not altered by the
   algorithm.
4. **Variety in Assignments**: Introduces randomization to prevent repetitive assignment patterns.

## Pre-conditions

1. **Congregations Data**: Requires a JSON file containing congregations' restrictions.
2. **Surveillance Shifts Data**: Requires a JSON file with surveillance shifts and current assignments.

## Assumptions

1. **Available Congregations**: All congregations are available for assignment unless specified as frozen.
2. **Manual Assignments**: Manually assigned shifts are final and will not be modified by the script.
3. **Balanced Assignments**: The solution strives to distribute shifts as evenly as possible among all congregations.

## Data Structure

### 1. congregaciones.json

This file contains information about the congregations and their restrictions.

**Structure**:

```json
[
  {
    "congregacion": "Congregation A",
    "dias_no_asignar": [
      "miercoles",
      "sabado"
    ],
    "fechas_no_asignar": []
  },
  {
    "congregacion": "Congregation B",
    "dias_no_asignar": [
      "martes",
      "domingo"
    ],
    "fechas_no_asignar": [
      "2024-08-06"
    ]
  },
  ...
]
```

### 2. turnos_asignados_y_por_asignar.json

This file contains the surveillance shifts and current assignments.

**Structure**:

```json
[
  {
    "dia": "jueves",
    "fecha": "2024-08-01",
    "turno": "nocturno",
    "horario": "17:00-07:00",
    "congregacion": ""
  },
  {
    "dia": "viernes",
    "fecha": "2024-08-02",
    "turno": "nocturno",
    "horario": "17:00-07:00",
    "congregacion": "Congregation A"
  },
  ...
]
```

## Implementation

The implementation involves reading the JSON files, processing the data, and assigning shifts based on the defined
restrictions. The output is saved as a CSV file.

## Conclusion

This guide provides a detailed explanation of the implementation for assigning surveillance shifts to congregations. By
following the steps and using the provided code, users can easily clone and reuse this solution. The use of JSON files
ensures the data is easy to read and manage, while the algorithm balances assignments effectively, respecting all
specified restrictions.