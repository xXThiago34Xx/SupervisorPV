from datetime import datetime, timedelta

def cargar_personal(archivo):
    personal = []
    with open(archivo, "r") as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            datos = linea.strip().split(",")
            personal.append(datos)
    return personal

def cargar_horarios(archivo):
    horarios = set()
    with open(archivo, "r") as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            datos = linea.strip().split(",")
            apellidos_nombres = (datos[0], datos[1])
            horarios.add(apellidos_nombres)
    return horarios

def formatear_hora(hora):
    hora_str = str(hora)
    
    # Si la longitud es 1 o 2, es una hora sin minutos
    if len(hora_str) == 1 or len(hora_str) == 2:
        hora_str = hora_str.zfill(2) + ":00"
    
    # Si la longitud es 3, debemos interpretar como 'h:mm'
    elif len(hora_str) == 3:
        hora_str = "0" + hora_str[0] + ":" + hora_str[1:]
    
    # Si la longitud es 4, es en formato 'hhmm' -> 'hh:mm'
    elif len(hora_str) == 4:
        hora_str = hora_str[:2] + ":" + hora_str[2:]
    
    return hora_str

def sumar_duracion(entrada, duracion):
    formato = "%H:%M"
    entrada_dt = datetime.strptime(entrada, formato)
    duracion_td = timedelta(hours=duracion[0], minutes=duracion[1])
    salida_dt = entrada_dt + duracion_td
    return salida_dt.strftime(formato)

def interpretar_salida(salida, entrada):
    if salida.lower() == "p":
        return sumar_duracion(entrada, (3, 45))  # Tiempo para part-time
    elif salida.lower() == "f":
        return sumar_duracion(entrada, (9, 0))  # Tiempo para full-time
    else:
        return formatear_hora(salida)  # Hora exacta en formato hh:mm

def registrar_horario(personal):
    with open("horario.txt", "a") as archivo:  # Abrir en modo de añadir (append)
        for persona in personal:
            apellidos, nombres, cargo = persona
            if (apellidos, nombres) in horarios_existentes:
                print(f"{nombres} {apellidos} ya tiene horario registrado. Saltando.")
                continue
            
            horario = [apellidos, nombres, cargo]
            
            # Solicitar las horas de entrada y salida para cada día de la semana
            for dia in ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]:
                entrada = input(f"Ingrese la hora de entrada para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'd'): ")
                
                if entrada.lower() == "d":
                    horario.extend(["DESCANSO", "DESCANSO"])
                else:
                    # Formatear la hora de entrada
                    entrada_formateada = formatear_hora(entrada)
                    
                    salida = input(f"Ingrese la hora de salida para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'p', 'f'): ")
                    
                    # Interpretar la hora de salida
                    salida_formateada = interpretar_salida(salida, entrada_formateada)
                    
                    horario.extend([entrada_formateada, salida_formateada])
            
            # Escribir la línea en el archivo
            linea = ",".join(horario) + "\n"
            archivo.write(linea)
            print(f"Horario registrado para {nombres} {apellidos}.")

# Cargar la lista de personal desde el archivo 'personal.txt'
personal = cargar_personal("personal.txt")

# Cargar los horarios ya existentes desde el archivo 'horario.txt'
horarios_existentes = cargar_horarios("horario.txt")

# Registrar horarios para el personal que no tiene horarios registrados
registrar_horario(personal)
