import csv
import os

# Definir los nombres de los archivos para cada tabla y sus campos
TABLAS = {
    "Coche": ("coche.txt", ["id", "idTipoCoche"]),
    "TipoCoche": ("tipocoche.txt", ["id", "Nombre"])  # Añadida la tabla TipoCoche
}

# Función para cargar los datos de una tabla
def cargar_tabla(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return []  # Retorna una lista vacía si el archivo no existe
    with open(nombre_archivo, mode='r', newline='') as archivo:
        return list(csv.reader(archivo))

# Función para guardar los datos en una tabla
def guardar_tabla(nombre_archivo, datos):
    with open(nombre_archivo, mode='w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(datos)

# Función para mostrar las opciones disponibles de una llave foránea
def mostrar_opciones_llave_foranea(tabla_foranea):
    archivo, campos = TABLAS[tabla_foranea]
    datos = cargar_tabla(archivo)
    if not datos:
        print(f"No hay datos disponibles para {tabla_foranea}.")
        return []
    
    print(f"\nOpciones disponibles para {tabla_foranea}:")
    for fila in datos:
        print(f"ID: {fila[0]}, Nombre: {fila[1]}")  # Se asume que el segundo campo es 'Nombre'
    return datos

# Función para obtener el valor de una llave foránea
def obtener_llave_foranea():
    tabla_foranea = "TipoCoche"
    opciones = mostrar_opciones_llave_foranea(tabla_foranea)
    if not opciones:
        return None
    id_seleccionado = input(f"Selecciona el ID para idTipoCoche: ")
    return id_seleccionado

# Función para obtener el siguiente ID de una tabla (incremental)
def obtener_siguiente_id(datos):
    if not datos:
        return 1
    else:
        ultimo_id = int(datos[-1][0])
        return ultimo_id + 1

# Función para agregar masivamente coches por tipo
def agregar_coches_masivamente():
    # Cargar la tabla de coches
    nombre_archivo, campos = TABLAS["Coche"]
    datos = cargar_tabla(nombre_archivo)

    # Mostrar opciones de TipoCoche
    idTipoCoche = obtener_llave_foranea()
    if idTipoCoche is None:
        print("Operación cancelada. No se puede proceder sin un tipo de coche.")
        return

    # Solicitar cantidad de coches a agregar
    try:
        cantidad = int(input("Cantidad de coches a agregar: "))
    except ValueError:
        print("La cantidad debe ser un número entero.")
        return

    # Agregar coches masivamente
    for i in range(cantidad):
        nueva_fila = []
        
        # Asignar automáticamente el siguiente ID
        siguiente_id = obtener_siguiente_id(datos)
        nueva_fila.append(str(siguiente_id))
        
        # Asignar el idTipoCoche seleccionado
        nueva_fila.append(idTipoCoche)
        
        datos.append(nueva_fila)
        print(f"Coche agregado con ID: {siguiente_id}, idTipoCoche: {idTipoCoche}")

    # Guardar los cambios en la tabla de coches
    guardar_tabla(nombre_archivo, datos)
    print(f"{cantidad} coches agregados exitosamente.")

if __name__ == "__main__":
    # Crear archivos si no existen
    for archivo, _ in TABLAS.values():
        if not os.path.exists(archivo):
            with open(archivo, mode='w') as f:
                pass
    
    # Ejecutar la función para agregar coches masivamente
    agregar_coches_masivamente()
