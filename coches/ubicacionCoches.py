import csv
import os
from collections import defaultdict

# Definición de constantes
TABLA_COCHES = "coche.txt"
TABLA_REGISTROS = "registros.txt"
TABLA_UBICACIONES = "ubicacion.txt"
TABLA_USUARIOS = "user.txt"  # Archivo de usuarios para obtener los nombres

# Función para cargar los coches desde el archivo
def cargar_coches(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return []
    with open(nombre_archivo, mode='r', newline='') as archivo:
        return list(csv.reader(archivo))

# Función para cargar ubicaciones desde el archivo
def cargar_ubicaciones(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return []
    with open(nombre_archivo, mode='r', newline='') as archivo:
        return list(csv.reader(archivo))

# Función para cargar usuarios desde el archivo
def cargar_usuarios(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return []
    with open(nombre_archivo, mode='r', newline='') as archivo:
        return list(csv.reader(archivo))

# Función para filtrar los últimos reportes de cada coche
def obtener_ultimos_reportes(registros):
    ultimos_reportes = {}
    
    for registro in registros:
        id_coche = registro[4]  # Suponiendo que el idCoche está en la quinta columna
        fecha_hora = f"{registro[1]} {registro[2]}"  # Suponiendo que la fecha y hora están en las columnas 2 y 3

        # Solo guardar el último reporte
        if id_coche not in ultimos_reportes or ultimos_reportes[id_coche][0] < fecha_hora:
            ultimos_reportes[id_coche] = (fecha_hora, registro[5], registro[3], registro[6])  # (fecha_hora, idUbicacion, idUsuario, observacion)
    
    return ultimos_reportes

# Función para mostrar las ubicaciones y la cantidad de coches en cada una
def mostrar_ubicaciones_y_cantidad(ultimos_reportes, ubicaciones):
    conteo_ubicaciones = defaultdict(int)

    for _, (fecha_hora, id_ubicacion, _, _) in ultimos_reportes.items():
        conteo_ubicaciones[id_ubicacion] += 1

    print("Ubicaciones y cantidad de coches:")
    for ubicacion in ubicaciones:
        id_ubicacion = ubicacion[0]
        nombre_ubicacion = ubicacion[1]
        cantidad_coches = conteo_ubicaciones.get(id_ubicacion, 0)
        print(f"ID: {id_ubicacion}, Nombre: {nombre_ubicacion}, Cantidad de coches: {cantidad_coches}")

# Función para mostrar coches en una ubicación específica
def mostrar_coches_en_ubicacion(ubicacion_id, ultimos_reportes, usuarios):
    print(f"\nCoches en la ubicación ID = {ubicacion_id}:")
    for id_coche, (fecha_hora, id_ubicacion, id_usuario, observacion) in ultimos_reportes.items():
        if id_ubicacion == ubicacion_id:  # Comparar con idUbicacionReportada
            # Obtener el nombre del usuario que hizo el reporte
            nombre_usuario = next((user[3] for user in usuarios if user[0] == id_usuario), "Desconocido")
            print(f"ID Coche: {id_coche}, Observación: {observacion}, Reportado por: {nombre_usuario}, Fecha y Hora: {fecha_hora}")

def main():
    coches = cargar_coches(TABLA_COCHES)
    registros = cargar_coches(TABLA_REGISTROS)
    ubicaciones = cargar_ubicaciones(TABLA_UBICACIONES)
    usuarios = cargar_usuarios(TABLA_USUARIOS)

    if not ubicaciones:
        print("No hay ubicaciones registradas.")
        return

    ultimos_reportes = obtener_ultimos_reportes(registros)

    mostrar_ubicaciones_y_cantidad(ultimos_reportes, ubicaciones)

    # Selección de ubicación
    id_ubicacion_seleccionada = input("\nSelecciona la ID de la ubicación para ver los coches: ")
    mostrar_coches_en_ubicacion(id_ubicacion_seleccionada, ultimos_reportes, usuarios)

if __name__ == "__main__":
    main()
