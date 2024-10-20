import openpyxl

# Cargar la plantilla
plantilla = 'plantilla.xlsx'
wb = openpyxl.load_workbook(plantilla)
hoja = wb.active

# Definir el array de cajeros
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

# Mapeo de posiciones para las cajas
def obtener_posiciones(caja_num):
    if 1 <= caja_num <= 18:
        fila_base = 4 + (caja_num - 1) * 2
    elif caja_num == 20:
        fila_base = 41
    else:
        return None  # Cajas fuera del rango

    posiciones = [
        f'B{fila_base}', f'B{fila_base + 1}',  # Primer par
        f'F{fila_base}', f'F{fila_base + 1}'   # Segundo par
    ]
    return posiciones

# Crear una función para asignar cajeros a posiciones
def asignar_cajeros(cajeros, hoja):
    cajeros_por_caja = {}
    
    # Organizar cajeros por caja
    for cajero in cajeros:
        num_caja = cajero[0]
        if num_caja not in cajeros_por_caja:
            cajeros_por_caja[num_caja] = []
        cajeros_por_caja[num_caja].append(cajero[1])  # Solo nombre
    
    # Asignar los cajeros a las posiciones correctas en la plantilla
    for num_caja, nombres in cajeros_por_caja.items():
        posiciones = obtener_posiciones(num_caja)
        if posiciones:
            for idx, nombre in enumerate(nombres[:4]):  # Limitar a 4 cajeros por caja
                hoja[posiciones[idx]] = nombre

# Llamar la función de asignación
asignar_cajeros(Cajeros, hoja)

# Guardar el nuevo archivo
wb.save('Plantilla_Exportada.xlsx')
