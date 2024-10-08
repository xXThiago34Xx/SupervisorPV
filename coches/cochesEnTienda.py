import csv
import os
from datetime import datetime

# Definición de constantes
TABLA_COCHES = "coche.txt"
TABLA_REGISTROS = "registros.txt"
ID_USUARIO = 1  # ID del usuario, se puede modificar si es necesario

# Función para cargar los coches desde el archivo
def cargar_coches(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return []
    with open(nombre_archivo, mode='r', newline='') as archivo:
        return list(csv.reader(archivo))

# Función para guardar registros en el archivo
def guardar_registros(nombre_archivo, registros):
    with open(nombre_archivo, mode='a', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(registros)

# Función para registrar todos los coches en la ubicación con id = 1
def ubicar_todos_los_coches():
    coches = cargar_coches(TABLA_COCHES)

    if not coches:
        print("No hay coches registrados.")
        return

    registros = []

    # Fecha y hora actuales
    fecha_hora = datetime.now()
    fecha = fecha_hora.strftime("%Y-%m-%d")
    hora = fecha_hora.strftime("%H:%M:%S")

    # Pedir observación general
    observacion = input("Observación para todos los coches: ")

    for coche in coches:
        id_coche = coche[0]  # Suponiendo que el ID está en la primera columna

        # Agregar registro para cada coche
        registros.append([len(registros) + 1, fecha, hora, ID_USUARIO, id_coche, '1', observacion])

    # Guardar registros
    if registros:
        guardar_registros(TABLA_REGISTROS, registros)
        print("Todos los coches han sido ubicados en la ubicación con id = 1.")
    else:
        print("No se agregaron registros.")

if __name__ == "__main__":
    ubicar_todos_los_coches()
