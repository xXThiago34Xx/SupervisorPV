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

def ver_horario(nombre_archivo):
    personal = leer_archivo(nombre_archivo)
    
    while True:
        # Mostrar personal enumerado
        mostrar_personal_enumerado(personal)
        
        # Seleccionar personal
        num_personal = int(input("\nSelecciona el número del personal que deseas ver su horario: ")) - 1
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
        
        # Preguntar si se desea continuar
        continuar = input("\n¿Deseas ver otro horario? (1/0): ").lower()
        if continuar != '1':
            break

# Nombre del archivo de texto
archivo_txt = 'horario.txt'

# Ejecutar el script
ver_horario(archivo_txt)
