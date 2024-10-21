def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    return lineas

def escribir_archivo(nombre_archivo, lineas):
    with open(nombre_archivo, 'w') as archivo:
        archivo.writelines(lineas)

def mostrar_lineas(lineas):
    print("\nContenido del archivo:")
    for idx, linea in enumerate(lineas, 1):
        print(f"{idx}. {linea.strip()}")

def seleccionar_linea(lineas):
    try:
        num_linea = int(input("\nIngresa el número de la línea que deseas eliminar: "))
        if num_linea < 1 or num_linea > len(lineas):
            print("Número de línea no válido. Intenta de nuevo.")
            return seleccionar_linea(lineas)
        return num_linea - 1  # Convertimos a índice de lista (0-index)
    except ValueError:
        print("Entrada no válida. Ingresa un número.")
        return seleccionar_linea(lineas)

def confirmar_eliminacion():
    confirmacion = input("\n¿Estás seguro de que deseas eliminar esta línea? (s/n): ").lower()
    return confirmacion == 's'

def eliminar_linea(archivo_txt):
    lineas = leer_archivo(archivo_txt)
    
    mostrar_lineas(lineas)
    
    num_linea = seleccionar_linea(lineas)
    print(f"\nLínea seleccionada: {lineas[num_linea].strip()}")
    
    if confirmar_eliminacion():
        del lineas[num_linea]  # Eliminar la línea seleccionada
        escribir_archivo(archivo_txt, lineas)  # Guardar los cambios en el archivo
        print("\nLínea eliminada exitosamente.")
    else:
        print("\nEliminación cancelada.")
    
    # Preguntar si desea continuar eliminando más líneas
    continuar = input("\n¿Deseas eliminar otra línea? (s/n): ").lower()
    if continuar == 's':
        eliminar_linea()
    else:
        print("\nProceso finalizado.")

if __name__ == "__main__":
    eliminar_linea('personal.txt')
