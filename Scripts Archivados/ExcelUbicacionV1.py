import openpyxl
from openpyxl import load_workbook

# Función para obtener las posiciones de nombres y horas según el número de caja
def obtener_posiciones(caja_num):
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
        posiciones, horas_posiciones = obtener_posiciones(num_caja)
        if posiciones is None:
            print(f"Error: Caja {num_caja} fuera de rango o no válida.")
            continue

        # Verificar si ya se han asignado 2 cajeros a la caja; si es así, saltar
        if len(cajeros_asignados[num_caja]) >= 2:
            print(f"Advertencia: Caja {num_caja} ya tiene los 2 cajeros asignados. Saltando.")
            continue

        # Asignar cajero en la primera o segunda fila de la caja según cuántos hayan sido asignados
        idx = len(cajeros_asignados[num_caja]) * 2  # 0 o 2 para las posiciones y horas
        hoja[posiciones[idx]] = nombre_completo
        hoja[horas_posiciones[idx]] = f'{hora_entrada}-{hora_salida}'

        # Añadir cajero a la lista de asignados en esa caja
        cajeros_asignados[num_caja].append(nombre_completo)

# Cargar el archivo Excel y la hoja de trabajo
archivo_origen = 'Plantilla.xlsx'
archivo_destino = 'Plantilla_Exportada.xlsx'

wb = load_workbook(archivo_origen)
hoja = wb.active

# Datos de cajeros (array con el formato dado)
Cajeros = [
    [1, 'HUAMAN HUAMANI, ALEXIS JAVIER', '06:30', '10:15'],
    [1, '(T) BRANCACHO RAMIREZ, BRINDY', '10:00', '13:45'],
    [1, '(T) JIMENEZ TORERO, ASTRID GERALDINE', '13:30', '22:15'],
    [1, '(T) AYQUIPA MONTENEGRO, VALERIA ESTEFANY', '22:00', '22:45'],
    [2, 'LOPEZ SANCHEZ, NELLY ANDREA', '07:00', '16:00'],
    [2, 'LIZARME HUINCHO, BRIYITH JASUMI', '16:00', '19:45'],
    [3, 'QUISPE MONDRAGON, JUAN ALFONSO', '08:15', '12:00'],
    [3, 'YANQUI BRAVO, MIRIAN LUZ', '12:00', '15:45'],
    [3, 'ERIQUE CALLE, MARIA ANTONIETA', '15:45', '19:15'],
    [3, 'VILCAPOMA CHILIN, JULISSA JAZMIN', '19:15', '22:00'],
    [4, 'VEGA CARDENAS, ANGELICA LOURDES', '08:45', '12:30'],
    [4, 'QUISPE MENDOZA, ANTONY MAURICIO', '12:45', '21:45'],
    [5, 'ROA ZARATE, ELIZABETH LUCY', '09:30', '13:15'],
    [5, 'HEREDIA CAHUAYA, SUSAN NAYELLI', '13:45', '22:45'],
    [6, 'HUAYANAY VELASCO, ATHINA', '10:00', '13:45'],
    [6, 'HURTADO SAMPLINI, JACK FERNANDO', '14:00', '21:30'],
    [7, 'BRANCACHO RAMIREZ, BRINDY', '10:00', '10:00'],
    [7, 'CASAPAICO RIVERA, ENZO MANUEL', '10:15', '14:00'],
    [7, 'RAMOS TINOCO, JORDAN JAVIER', '14:15', '22:45'],
    [8, 'SOTO VELAZCO, EMIR ALESSANDRO', '10:45', '14:30'],
    [8, 'SICHA JORGE, JOSE ANGELO', '14:30', '18:15'],
    [8, 'LA ROSA EUSEBIO, SHADIA SHAMIRA', '18:15', '22:00'],
    [9, 'RUIZ SANTOS, CIELO CRISTHINA', '10:45', '14:30'],
    [9, 'PEREZ GORMAS, ANTHONY', '16:00', '19:45'],
    [10, 'CUSI QUISPE, ANDREA ESTEFANY', '11:00', '14:45'],
    [10, 'GARRIDO SOTO, VICTORIA CELESTE', '16:45', '20:30'],
    [11, 'QUIQUIA MALLQUI, CYNTHIA ANGELLINE', '11:15', '15:00'],
    [11, 'LEON TICONA, MARIA FERNANDA', '17:00', '20:45'],
    [12, 'DEL AGUILA MURAYARI, DARLA', '12:00', '21:00'],
    [13, 'IDELFONSO MOTTA, JHOSSEP ANGELO', '17:30', '21:15'],
    [14, 'INGA DELGADO, CARLOS DANIEL', '17:30', '21:15'],
    [15, 'BRENIS LARTIGA, SEBASTIAN', '18:00', '21:45'],
    [21, 'MARTINEZ PAZ, ROCIO ESPERANZA', '09:00', '18:00'],
    [22, 'JIMENEZ TORERO, ASTRID GERALDINE', '13:15', '13:30'],
    [22, 'AYQUIPA MONTENEGRO, VALERIA ESTEFANY', '13:45', '22:00']
]

# Asignar los cajeros a las posiciones correspondientes en la hoja de Excel
asignar_cajeros(Cajeros, hoja)

# Guardar la nueva plantilla
wb.save(archivo_destino)

print(f"Archivo guardado como {archivo_destino}")
