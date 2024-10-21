def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    return [linea.strip().split(',') for linea in lineas]

def mostrar_personal_enumerado(personal):
    print("\nLista de personal:")
    for idx, persona in enumerate(personal, 1):
        print(f"{idx}. {persona[0]} {persona[1]} ({persona[2]})")

def guardar_archivo(nombre_archivo, personal):
    with open(nombre_archivo, 'w') as archivo:
        for persona in personal:
            archivo.write(','.join(persona) + '\n')

def modificar_horario(nombre_archivo):
    personal = leer_archivo(nombre_archivo)
    
    while True:
        # Mostrar personal enumerado
        mostrar_personal_enumerado(personal)
        
        # Seleccionar personal
        num_personal = int(input("\nSelecciona el número del personal que deseas modificar: ")) - 1
        if num_personal < 0 or num_personal >= len(personal):
            print("Número de personal no válido.")
            continue
        
        persona = personal[num_personal]
        print(f"\nHas seleccionado: {persona[0]} {persona[1]}")
        
        # Seleccionar el día de la semana
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        print("\nDías de la semana:")
        for idx, dia in enumerate(dias_semana, 1):
            entrada = persona[3 + (idx - 1) * 2]
            salida = persona[4 + (idx - 1) * 2]
            print(f"{idx}. {dia} ({entrada} - {salida})")
        
        num_dia = int(input("\nSelecciona el número del día que deseas modificar (1-7): ")) - 1
        if num_dia < 0 or num_dia >= len(dias_semana):
            print("Número de día no válido.")
            continue
        
        # Obtener las horas de entrada y salida del día seleccionado
        entrada = persona[3 + num_dia * 2]
        salida = persona[4 + num_dia * 2]
        
        print(f"\nPara {dias_semana[num_dia]}:")
        print(f"1. Hora de entrada: {entrada}")
        print(f"2. Hora de salida: {salida}")
        
        # Seleccionar si se quiere modificar la entrada o la salida
        num_modificar = int(input("\n¿Qué deseas modificar? (1 para entrada, 2 para salida): "))
        if num_modificar == 1:
            nueva_entrada = input(f"\nIngresa la nueva hora de entrada para {dias_semana[num_dia]}: ")
            persona[3 + num_dia * 2] = nueva_entrada
        elif num_modificar == 2:
            nueva_salida = input(f"\nIngresa la nueva hora de salida para {dias_semana[num_dia]}: ")
            persona[4 + num_dia * 2] = nueva_salida
        else:
            print("Selección no válida.")
            continue

        # Preguntar si se desea modificar la otra hora
        modificar_otra = input("\n¿Deseas modificar la otra hora (entrada/salida) para este mismo día? (1/0): ").lower()
        if modificar_otra == '1':
            if num_modificar == 1:
                nueva_salida = input(f"\nIngresa la nueva hora de salida para {dias_semana[num_dia]}: ")
                persona[4 + num_dia * 2] = nueva_salida
            else:
                nueva_entrada = input(f"\nIngresa la nueva hora de entrada para {dias_semana[num_dia]}: ")
                persona[3 + num_dia * 2] = nueva_entrada
        
        # Confirmar si se desean guardar los cambios
        confirmar = input("\n¿Deseas guardar los cambios? (1/0): ").lower()
        if confirmar == '1':
            personal[num_personal] = persona
            guardar_archivo(nombre_archivo, personal)
            print("\nCambios guardados con éxito.")
        else:
            print("\nCambios no guardados.")
        
        # Preguntar si se desea continuar
        continuar = input("\n¿Deseas modificar otra hora? (1/0): ").lower()
        if continuar != '1':
            break

# Nombre del archivo de texto
archivo_txt = 'horario.txt'

# Ejecutar el script
modificar_horario(archivo_txt)
