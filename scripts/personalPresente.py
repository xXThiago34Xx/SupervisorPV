def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    return [linea.strip().split(',') for linea in lineas]

def obtener_personal_presente(personal, dia_semana, hora_actual):
    personal_presente_por_cargo = {}

    for persona in personal:
        apellidos = persona[0]
        nombres = persona[1]
        cargo = persona[2]

        # Índices en el archivo donde empiezan las horas para cada día (3 en adelante)
        idx_entrada = 3 + (dia_semana - 1) * 2
        idx_salida = idx_entrada + 1

        entrada = persona[idx_entrada]
        salida = persona[idx_salida]

        # Ignorar si es "DESCANSO" o si no tienen un horario válido
        if entrada == "DESCANSO" or salida == "DESCANSO":
            continue

        # Comparamos la hora actual con el rango de entrada y salida
        if entrada <= hora_actual <= salida:
            if cargo not in personal_presente_por_cargo:
                personal_presente_por_cargo[cargo] = []
            personal_presente_por_cargo[cargo].append({
                "nombre_completo": f"{apellidos} {nombres}",
                "entrada": entrada,
                "salida": salida
            })

    # Ordenar por hora de salida (de menor a mayor)
    for cargo in personal_presente_por_cargo:
        personal_presente_por_cargo[cargo].sort(key=lambda x: x['salida'])

    return personal_presente_por_cargo

def mostrar_personal_presente(personal_presente_por_cargo):
    if not personal_presente_por_cargo:
        print("\nNo hay personal presente en esa hora.")
    else:
        for cargo, personas in personal_presente_por_cargo.items():
            print(f"\n{cargo}:")
            for idx, persona in enumerate(personas, 1):
                print(f"{idx}. {persona['nombre_completo']} ({persona['entrada']}-{persona['salida']})")

def obtener_dia_semana():
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    print("\nSelecciona el día de la semana:")
    for idx, dia in enumerate(dias_semana, 1):
        print(f"{idx}. {dia}")

    num_dia = int(input("\nElige el número del día (1-7): "))
    if num_dia < 1 or num_dia > 7:
        print("Día no válido.")
        return obtener_dia_semana()  # Recursión para que elija un valor correcto
    return num_dia

def convertir_hora(hora):
    """ Convierte la hora de formato 1600 a 16:00. """
    if len(hora) == 4 and hora.isdigit():
        horas = hora[:2]
        minutos = hora[2:]
        return f"{horas}:{minutos}"
    else:
        print("Formato de hora incorrecto. Debes ingresar 4 dígitos (ej: 1600).")
        return obtener_hora_actual()

def obtener_hora_actual():
    hora_actual = input("\nIngresa la hora en formato 24h sin dos puntos (HHMM): ")

    # Validar formato de hora (HHMM)
    if len(hora_actual) == 4 and hora_actual.isdigit():
        hora_actual = convertir_hora(hora_actual)
        horas, minutos = map(int, hora_actual.split(":"))
        if horas < 0 or horas >= 24 or minutos < 0 or minutos >= 60:
            print("Hora no válida.")
            return obtener_hora_actual()
    else:
        print("Formato de hora no válido. Debes ingresar 4 dígitos (ej: 1600).")
        return obtener_hora_actual()
    
    return hora_actual

def main():
    archivo_txt = 'horario.txt'
    personal = leer_archivo(archivo_txt)
    
    while True:
        dia_semana = obtener_dia_semana()  # Elegir día de la semana
        hora_actual = obtener_hora_actual()  # Elegir hora en formato HHMM
        
        personal_presente_por_cargo = obtener_personal_presente(personal, dia_semana, hora_actual)
        
        print(f"\nPersonal presente el día {dia_semana} a las {hora_actual}:")
        mostrar_personal_presente(personal_presente_por_cargo)

        continuar = input("\n¿Deseas verificar otra hora? (1/0): ").lower()
        if continuar != '1':
            break

if __name__ == "__main__":
    main()
