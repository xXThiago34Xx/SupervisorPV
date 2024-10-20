import openpyxl
from openpyxl import load_workbook
from ubicacionv3 import cargar_horarios, dia_menu, inhabilitados_menu, get_ubicaciones_exportados
from getSelfxDia import get_self_exportados

# Función para obtener las posiciones de nombres y horas según el número de caja
def obtener_posiciones_caja(caja_num):
    if 1 <= caja_num <= 18:
        fila_base = 4 + (caja_num - 1) * 2
    elif caja_num == 20:
        fila_base = 41
    elif caja_num == 21:
        fila_base = 43
    elif caja_num == 22:
        fila_base = 45
    elif caja_num == 23:
        fila_base = 47
    elif caja_num == 24:
        fila_base = 49
    elif caja_num == 25:
        fila_base = 52
    else:
        return None  # Cajas fuera del rango

    posiciones = [
        f'B{fila_base}', f'B{fila_base + 1}',  # Nombres en columna B
        f'F{fila_base}', f'F{fila_base + 1}'   # Nombres en columna F
    ]
    
    horas_posiciones = [
        f'C{fila_base}', f'C{fila_base + 1}',  # Horas en columna C
        f'G{fila_base}', f'G{fila_base + 1}'   # Horas en columna G
    ]

    if (caja_num == 25):
        posiciones.insert(2, f'B{fila_base+2}')
        posiciones.append(f'F{fila_base+2}')
        horas_posiciones.insert(2, f'C{fila_base+2}')
        horas_posiciones.append(f'G{fila_base+2}')
    
    return posiciones, horas_posiciones

# Función para asignar cajeros a sus posiciones en el Excel evitando duplicados de nombres en la misma caja
def asignar_cajeros(cajeros, hoja):
    cajeros_asignados = {caja: [] for caja in range(1, 25)}  # Diccionario para rastrear cajeros asignados por caja

    for cajero in cajeros:
        num_caja, nombre_completo, hora_entrada, hora_salida = cajero

        # Validar que la caja sea válida
        if num_caja not in cajeros_asignados:
            print(f"Error: Caja {num_caja} fuera de rango o no válida.")
            continue

        # Verificar si el cajero ya ha sido asignado a esta caja
        if nombre_completo in cajeros_asignados[num_caja]:
            print(f"Advertencia: {nombre_completo} ya asignado a la caja {num_caja}. Evitando duplicado.")
            continue

        # Obtener las posiciones correspondientes
        posiciones, horas_posiciones = obtener_posiciones_caja(num_caja)
        if posiciones is None:
            print(f"Error: Caja {num_caja} fuera de rango o no válida.")
            continue

        # Verificar si ya se han asignado 4 cajeros a la caja; si es así, saltar
        if len(cajeros_asignados[num_caja]) >= 4:
            print(f"Advertencia: Caja {num_caja} ya tiene los 4 cajeros asignados. Saltando.")
            continue

        # Asignar cajero en la primera o segunda fila de la caja según cuántos hayan sido asignados
        idx = len(cajeros_asignados[num_caja])  # índice basado en la cantidad de cajeros asignados
        hoja[posiciones[idx]] = nombre_completo
        hoja[horas_posiciones[idx]] = f'{hora_entrada}-{hora_salida}'  # Asignar el turno en formato solicitado

        # Añadir cajero a la lista de asignados en esa caja
        cajeros_asignados[num_caja].append(nombre_completo)

def asignar_selfs(selfs, hoja):
    cajeros_asignados = []  # Para evitar duplicados de nombres en la caja 25
    for self in selfs:
        nombre_completo, horas = self
        num_caja = 25  # Caja destinada para self-service

        # Verificar si el cajero ya ha sido asignado
        if nombre_completo in cajeros_asignados:
            print(f"Advertencia: {nombre_completo} ya asignado a la caja {num_caja}. Evitando duplicado.")
            continue

        # Obtener las posiciones correspondientes
        posiciones, horas_posiciones = obtener_posiciones_caja(num_caja)
        if posiciones is None:
            print(f"Error: Caja {num_caja} fuera de rango o no válida.")
            continue

        # Verificar si ya se han asignado 4 cajeros a la caja; si es así, saltar
        if len(cajeros_asignados) >= 6:
            print(f"Advertencia: Caja {num_caja} ya tiene los 4 cajeros asignados. Saltando.")
            continue

        # Asignar cajero en la primera o segunda fila de la caja según cuántos hayan sido asignados
        idx = len(cajeros_asignados)  # índice basado en la cantidad de cajeros asignados
        hoja[posiciones[idx]] = nombre_completo
        hoja[horas_posiciones[idx]] = horas  # Asignar las horas directamente en el formato correspondiente

        # Añadir cajero a la lista de asignados
        cajeros_asignados.append(nombre_completo)


if (__name__ == '__main__'):
    # Cargar el archivo Excel y la hoja de trabajo
    archivo_origen = 'Plantilla.xlsx'
    archivo_destino = 'Plantilla_Exportada.xlsx'

    wb = load_workbook(archivo_origen)
    hoja = wb.active

    horarios = cargar_horarios("horario.txt")
    inhabilitados_indices = inhabilitados_menu(horarios)
    dia_seleccionado = dia_menu()

    cajeros = get_ubicaciones_exportados(horarios, dia_seleccionado, inhabilitados_indices)
    selfs = get_self_exportados(horarios, dia_seleccionado)

    # Llamar a la función para asignar los cajeros
    asignar_cajeros(cajeros, hoja)
    asignar_selfs(selfs, hoja)

    # Guardar el nuevo archivo
    wb.save(archivo_destino)

    print("Asignación completada y archivo guardado como", archivo_destino)
