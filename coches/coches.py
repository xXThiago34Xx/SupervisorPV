import csv
import os

# Definir los nombres de los archivos para cada tabla y sus campos
TABLAS = {
    "Coche": ("coche.txt", ["id", "idTipoCoche"]),
    "User": ("user.txt", ["id", "Usuario", "Clave", "Nombre Completo", "idCargo"]),
    "Empresa": ("empresa.txt", ["id", "Nombre"]),
    "Cargo": ("cargo.txt", ["id", "idEmpresa", "NombreCargo"]),
    "Ubicacion": ("ubicacion.txt", ["id", "Nombre"]),
    "Registros": ("registros.txt", ["id", "Fecha", "Hora", "idUsuario", "IdCoche", "IdUbicacionReportada", "Observacion"]),
    "TipoCoche": ("tipocoche.txt", ["id", "Nombre"])  # Añadida la tabla TipoCoche
}

# Llaves foráneas: campo -> (tabla, campo_nombre)
LLAVES_FORANEAS = {
    "idCargo": ("Cargo", "NombreCargo"),
    "idEmpresa": ("Empresa", "Nombre"),
    "idUsuario": ("User", "Usuario"),
    "IdCoche": ("Coche", "idTipoCoche"),
    "IdUbicacionReportada": ("Ubicacion", "Nombre"),
    "idTipoCoche": ("TipoCoche", "Nombre")  # Nueva llave foránea para el tipo de coche
}

# Función para cargar los datos de una tabla
def cargar_tabla(nombre_archivo):
    with open(nombre_archivo, mode='r', newline='') as archivo:
        return list(csv.reader(archivo))

# Función para guardar los datos en una tabla
def guardar_tabla(nombre_archivo, datos):
    with open(nombre_archivo, mode='w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(datos)

# Función para mostrar todos los elementos de una tabla
def mostrar_todos(nombre_archivo):
    datos = cargar_tabla(nombre_archivo)
    for fila in datos:
        print(", ".join(fila))

# Función para mostrar las opciones disponibles de una llave foránea
def mostrar_opciones_llave_foranea(tabla_foranea, campo_nombre):
    archivo, campos = TABLAS[tabla_foranea]
    datos = cargar_tabla(archivo)
    print(f"\nOpciones disponibles para {tabla_foranea}:")
    for fila in datos:
        print(f"ID: {fila[0]}, {campo_nombre}: {fila[campos.index(campo_nombre)]}")
    return datos

# Función para obtener el valor de una llave foránea
def obtener_llave_foranea(campo):
    tabla_foranea, campo_nombre = LLAVES_FORANEAS[campo]
    opciones = mostrar_opciones_llave_foranea(tabla_foranea, campo_nombre)
    id_seleccionado = input(f"Selecciona el ID para {campo}: ")
    return id_seleccionado

# Función para obtener el siguiente ID de una tabla (incremental)
def obtener_siguiente_id(datos):
    if not datos:
        return 1
    else:
        ultimo_id = int(datos[-1][0])
        return ultimo_id + 1

# Función para agregar un nuevo elemento a una tabla
def agregar(nombre_archivo, campos):
    datos = cargar_tabla(nombre_archivo)
    nueva_fila = []
    
    # Asignar automáticamente el siguiente ID
    siguiente_id = obtener_siguiente_id(datos)
    nueva_fila.append(str(siguiente_id))
    
    print(f"ID asignado automáticamente: {siguiente_id}")
    
    # Pide los valores de los campos restantes
    for campo in campos[1:]:  # Excluye el campo "id"
        if campo in LLAVES_FORANEAS:
            valor = obtener_llave_foranea(campo)
        else:
            valor = input(f"{campo}: ")
        nueva_fila.append(valor)
    
    datos.append(nueva_fila)
    guardar_tabla(nombre_archivo, datos)
    print("Elemento agregado.")

# Función para actualizar un elemento de una tabla
def actualizar(nombre_archivo, campos):
    datos = cargar_tabla(nombre_archivo)
    id_a_actualizar = input("Ingresa el ID del elemento a actualizar: ")
    
    for fila in datos:
        if fila[0] == id_a_actualizar:
            nueva_fila = []
            print("Ingresa los nuevos valores (déjalo en blanco para no cambiarlo):")
            
            for i, campo in enumerate(campos):
                if i == 0:
                    nueva_fila.append(fila[i])  # No cambiar el ID
                else:
                    if campo in LLAVES_FORANEAS:
                        valor = obtener_llave_foranea(campo)
                    else:
                        valor = input(f"{campo} (actual: {fila[i]}): ")
                    nueva_fila.append(valor if valor else fila[i])
            
            datos[datos.index(fila)] = nueva_fila
            guardar_tabla(nombre_archivo, datos)
            print("Elemento actualizado.")
            return
    print("ID no encontrado.")

# Función para eliminar un elemento de una tabla
def eliminar(nombre_archivo):
    datos = cargar_tabla(nombre_archivo)
    id_a_eliminar = input("Ingresa el ID del elemento a eliminar: ")
    datos = [fila for fila in datos if fila[0] != id_a_eliminar]
    guardar_tabla(nombre_archivo, datos)
    print("Elemento eliminado.")

# Menú para seleccionar tabla y operación CRUD
def menu_crud():
    while True:
        print("\n--- Menú CRUD ---")
        print("1. Crear")
        print("2. Leer (Mostrar todos)")
        print("3. Actualizar")
        print("4. Eliminar")
        print("5. Salir")
        opcion_crud = input("Elige una opción: ")

        if opcion_crud == "5":
            break
        
        print("\nTablas disponibles:")
        for idx, tabla in enumerate(TABLAS.keys(), 1):
            print(f"{idx}. {tabla}")
        opcion_tabla = input("Elige una tabla: ")

        try:
            nombre_archivo, campos = list(TABLAS.values())[int(opcion_tabla) - 1]
        except (IndexError, ValueError):
            print("Opción no válida.")
            continue

        if opcion_crud == "1":
            agregar(nombre_archivo, campos)
        elif opcion_crud == "2":
            mostrar_todos(nombre_archivo)
        elif opcion_crud == "3":
            actualizar(nombre_archivo, campos)
        elif opcion_crud == "4":
            eliminar(nombre_archivo)
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    # Crear archivos si no existen
    for archivo, _ in TABLAS.values():
        if not os.path.exists(archivo):
            with open(archivo, mode='w') as f:
                pass
    
    # Ejecutar el menú CRUD
    menu_crud()
