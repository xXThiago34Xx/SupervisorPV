def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    return lineas

def mostrar_lineas_enumeradas(lineas):
    for idx, linea in enumerate(lineas, 1):
        print(f"{idx}: {linea.strip()}")

def guardar_archivo(nombre_archivo, lineas):
    with open(nombre_archivo, 'w') as archivo:
        archivo.writelines(lineas)

def modificar_orden(nombre_archivo):
    # Leer el archivo
    lineas = leer_archivo(nombre_archivo)
    
    # Mostrar las líneas enumeradas
    print("\nLíneas actuales del archivo:")
    mostrar_lineas_enumeradas(lineas)
    
    # Preguntar cuál línea se desea mover
    num_linea_mover = int(input("\n¿Cuál línea deseas mover? (ingresa el número): ")) - 1
    
    if num_linea_mover < 0 or num_linea_mover >= len(lineas):
        print("Número de línea no válido.")
        return
    
    # Preguntar a qué posición se desea mover la línea
    num_linea_destino = int(input(f"¿Encima de cuál línea deseas mover la línea {num_linea_mover + 1}? (ingresa el número): ")) - 1
    
    if num_linea_destino < 0 or num_linea_destino > len(lineas):
        print("Número de línea destino no válido.")
        return

    # Extraer la línea que se va a mover
    linea_mover = lineas.pop(num_linea_mover)
    
    # Insertar la línea en la nueva posición
    lineas.insert(num_linea_destino, linea_mover)
    
    # Guardar el archivo con las modificaciones
    guardar_archivo(nombre_archivo, lineas)
    
    print("\nArchivo modificado con éxito.")
    mostrar_lineas_enumeradas(lineas)

# Nombre del archivo de texto
archivo_txt = 'personal.txt'

# Ejecutar el script
modificar_orden(archivo_txt)
