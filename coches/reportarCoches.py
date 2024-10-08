import csv
import os
import datetime

# Variable global para el idUsuario (definido como 1 en este caso)
USUARIO_ACTUAL = 1

# Definir los nombres de los archivos para cada tabla y sus campos
TABLAS = {
    "Coche": ("coche.txt", ["id", "idTipoCoche"]),
    "Ubicacion": ("ubicacion.txt", ["id", "Nombre"]),
    "Registros": ("registros.txt", ["id", "Fecha", "Hora", "idUsuario", "IdCoche", "IdUbicacionReportada", "Observacion"]),
}

# Función para cargar los datos de una tabla
def cargar_tabla(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return []
    with open(nombre_archivo, mode='r', newline='') as archivo:
        return list(csv.reader(archivo))

# Función para guardar los datos en una tabla
def guardar_tabla(nombre_archivo, datos):
    with open(nombre_archivo, mode='w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(datos)

# Función para obtener el siguiente ID de una tabla (incremental)
def obtener_siguiente_id(datos):
    if not datos:
        return 1
    else:
        ultimo_id = int(datos[-1][0])
        return ultimo_id + 1

# Función para reportar un coche
def reportar_coche():
    # Cargar la tabla de coches y ubicaciones
    coches = cargar_tabla(TABLAS["Coche"][0])
    ubicaciones = cargar_tabla(TABLAS["Ubicacion"][0])
    registros = cargar_tabla(TABLAS["Registros"][0])

    # Si no hay coches o ubicaciones, no podemos proceder
    if not coches:
        print("No hay coches registrados. No se puede proceder.")
        return

    if not ubicaciones:
        print("No hay ubicaciones registradas. No se puede proceder.")
        return

    # Lista para almacenar los coches seleccionados
    coches_seleccionados = []

    # Bucle para permitir la selección de coches
    while True:
        id_coche = input("Introduce el ID del coche a reportar o escribe 'x' para finalizar: ")
        if id_coche.lower() == 'x':
            break

        # Verificar si el coche existe
        coche_encontrado = next((coche for coche in coches if coche[0] == id_coche), None)
        if coche_encontrado:
            coches_seleccionados.append(id_coche)
            print(f"Coche con ID {id_coche} añadido.")
        else:
            print(f"El coche con ID {id_coche} no existe. Intenta nuevamente.")

    # Si no se seleccionaron coches, salir
    if not coches_seleccionados:
        print("No se seleccionó ningún coche.")
        return

    # Mostrar ubicaciones disponibles
    print("\nOpciones disponibles para Ubicaciones:")
    for ubicacion in ubicaciones:
        print(f"ID: {ubicacion[0]}, Nombre: {ubicacion[1]}")

    # Solicitar la ubicación
    id_ubicacion = input("\nSelecciona el ID para la ubicación reportada: ")

    # Verificar si la ubicación existe
    ubicacion_encontrada = next((ubicacion for ubicacion in ubicaciones if ubicacion[0] == id_ubicacion), None)
    if not ubicacion_encontrada:
        print(f"La ubicación con ID {id_ubicacion} no existe. Operación cancelada.")
        return

    # Pedir observación
    observacion = input("Ingresa una observación para los registros (dejar vacío si no se desea agregar): ")

    # Confirmar la operación mostrando los IDs de coches seleccionados
    print(f"\nCoches a reportar: {', '.join(coches_seleccionados)}")
    confirmacion = input(f"¿Estás seguro de que quieres reportar los coches seleccionados en la ubicación '{ubicacion_encontrada[1]}'? (s/n): ")
    if confirmacion.lower() != 's':
        print("Operación cancelada.")
        return

    # Agregar los registros con fecha y hora actual
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

    for id_coche in coches_seleccionados:
        nuevo_registro = [
            str(obtener_siguiente_id(registros)),  # ID automático para el registro
            fecha_actual,  # Fecha actual
            hora_actual,  # Hora actual
            str(USUARIO_ACTUAL),  # ID del usuario actual
            id_coche,  # ID del coche
            id_ubicacion,  # ID de la ubicación reportada
            observacion  # Observación
        ]
        registros.append(nuevo_registro)

    # Guardar los nuevos registros en la tabla de registros
    guardar_tabla(TABLAS["Registros"][0], registros)
    print(f"Registros añadidos exitosamente para {len(coches_seleccionados)} coche(s).")

if __name__ == "__main__":
    # Crear archivos si no existen
    for archivo, _ in TABLAS.values():
        if not os.path.exists(archivo):
            with open(archivo, mode='w') as f:
                pass

    # Ejecutar la función para reportar coches
    reportar_coche()
