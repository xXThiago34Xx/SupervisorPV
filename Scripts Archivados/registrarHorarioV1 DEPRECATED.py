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
    
    if len(hora_str) == 1 or len(hora_str) == 2:
        hora_str = hora_str.zfill(2) + ":00"
    elif len(hora_str) == 3:
        hora_str = "0" + hora_str[0] + ":" + hora_str[1:]
    elif len(hora_str) == 4:
        hora_str = hora_str[:2] + ":" + hora_str[2:]
    
    return hora_str

def sumar_duracion(entrada, duracion):
    formato = "%H:%M"
    entrada_dt = datetime.strptime(entrada, formato)
    duracion_td = timedelta(hours=duracion[0], minutes=duracion[1])
    salida_dt = entrada_dt + duracion_td
    return salida_dt.strftime(formato)

def interpretar_salida(salida, entrada, tipo_jornada):
    if salida.lower() == "p":
        return sumar_duracion(entrada, (3, 45)) if tipo_jornada == "pt" else sumar_duracion(entrada, (9, 0)) 
    elif salida.lower() == "f":
        return sumar_duracion(entrada, (9, 0)) if tipo_jornada == "ft" else sumar_duracion(entrada, (3, 45))
    else:
        return formatear_hora(salida) 

def registrar_horario(personal, tipo_personal):
    personal_filtrado = [p for p in personal if p[2].lower() == tipo_personal.lower()]
    
    with open("horario.txt", "a") as archivo:
        for persona in personal_filtrado:
            apellidos, nombres, cargo = persona
            if (apellidos, nombres) in horarios_existentes:
                print(f"{nombres} {apellidos} ya tiene horario registrado. Saltando.")
                continue
            
            tipo_jornada = None
            while True:
                horario = [apellidos, nombres, cargo]
                dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
                i = 0  # Índice del día actual
                
                while i < len(dias):
                    dia = dias[i]
                    entrada = input(f"Ingrese la hora de entrada para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'd', 'v', 'x'): ")
                    
                    if entrada.lower() == "x":
                        print(f"Reiniciando el ingreso de horario para {nombres} {apellidos}.")
                        i = 0  # Reinicia desde el primer día
                        horario = [apellidos, nombres, cargo]  # Reinicia el horario
                        continue
                    
                    if entrada.lower() == "v":
                        if i > 0:
                            i -= 1  # Retrocede al día anterior
                            horario = horario[:-2]  # Elimina el horario del día actual
                            continue
                        else:
                            print("Ya estás en el primer día de la semana.")
                            continue
                    
                    if entrada.lower() == "d":
                        horario.extend(["DESCANSO", "DESCANSO"])
                    else:
                        entrada_formateada = formatear_hora(entrada)
                        
                        if tipo_jornada:
                            salida_formateada = sumar_duracion(entrada_formateada, (9, 0)) if tipo_jornada == "ft" else sumar_duracion(entrada_formateada, (3, 45))
                        else:
                            salida = input(f"Ingrese la hora de salida para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'p', 'f', 'pt', 'ft', 'v', 'x'): ")
                            
                            if salida.lower() == "x":
                                print(f"Reiniciando el ingreso de horario para {nombres} {apellidos}.")
                                i = 0  # Reinicia desde el primer día
                                horario = [apellidos, nombres, cargo]  # Reinicia el horario
                                continue
                            
                            if salida.lower() == "v":
                                if i > 0:
                                    i -= 1  # Retrocede al día anterior
                                    horario = horario[:-2]  # Elimina el horario del día actual
                                    continue
                                else:
                                    print("Ya estás en el primer día de la semana.")
                                    continue
                            
                            if salida.lower() in ['ft', 'pt']:
                                tipo_jornada = salida.lower()
                                salida_formateada = sumar_duracion(entrada_formateada, (9, 0)) if tipo_jornada == "ft" else sumar_duracion(entrada_formateada, (3, 45))
                            else:
                                salida_formateada = interpretar_salida(salida, entrada_formateada, tipo_jornada)
                        
                        horario.extend([entrada_formateada, salida_formateada])
                    
                    i += 1  # Avanza al siguiente día
                
                if i == len(dias):  # Si todos los días fueron ingresados correctamente
                    linea = ",".join(horario) + "\n"
                    archivo.write(linea)
                    print(f"Horario registrado para {nombres} {apellidos}.")
                    break

def registrar_horario_manualmente(personal):
    while True:
        apellido = input("Ingrese el apellido de la persona a registrar (o 'x' para regresar): ").strip()
        if apellido.lower() == 'x':
            return
        encontrado = False
        for persona in personal:
            apellidos, nombres, cargo = persona
            if apellidos.lower() == apellido.lower():
                if (apellidos, nombres) in horarios_existentes:
                    print(f"{nombres} {apellidos} ya tiene horario registrado. Saltando.")
                    return
                
                tipo_jornada = None
                while True:
                    horario = [apellidos, nombres, cargo]
                    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
                    i = 0  # Índice del día actual
                    
                    while i < len(dias):
                        dia = dias[i]
                        entrada = input(f"Ingrese la hora de entrada para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'd', 'v', 'x'): ")
                        
                        if entrada.lower() == "x":
                            print(f"Reiniciando el ingreso de horario para {nombres} {apellidos}.")
                            i = 0  # Reinicia desde el primer día
                            horario = [apellidos, nombres, cargo]  # Reinicia el horario
                            continue
                        
                        if entrada.lower() == "v":
                            if i > 0:
                                i -= 1  # Retrocede al día anterior
                                horario = horario[:-2]  # Elimina el horario del día actual
                                continue
                            else:
                                print("Ya estás en el primer día de la semana.")
                                continue
                        
                        if entrada.lower() == "d":
                            horario.extend(["DESCANSO", "DESCANSO"])
                        else:
                            entrada_formateada = formatear_hora(entrada)
                            
                            if tipo_jornada:
                                salida_formateada = sumar_duracion(entrada_formateada, (9, 0)) if tipo_jornada == "ft" else sumar_duracion(entrada_formateada, (3, 45))
                            else:
                                salida = input(f"Ingrese la hora de salida para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'p', 'f', 'pt', 'ft', 'v', 'x'): ")
                                
                                if salida.lower() == "x":
                                    print(f"Reiniciando el ingreso de horario para {nombres} {apellidos}.")
                                    i = 0  # Reinicia desde el primer día
                                    horario = [apellidos, nombres, cargo]  # Reinicia el horario
                                    continue
                                
                                if salida.lower() == "v":
                                    if i > 0:
                                        i -= 1  # Retrocede al día anterior
                                        horario = horario[:-2]  # Elimina el horario del día actual
                                        continue
                                    else:
                                        print("Ya estás en el primer día de la semana.")
                                        continue
                                
                                if salida.lower() in ['ft', 'pt']:
                                    tipo_jornada = salida.lower()
                                    salida_formateada = sumar_duracion(entrada_formateada, (9, 0)) if tipo_jornada == "ft" else sumar_duracion(entrada_formateada, (3, 45))
                                else:
                                    salida_formateada = interpretar_salida(salida, entrada_formateada, tipo_jornada)
                            
                            horario.extend([entrada_formateada, salida_formateada])
                        
                        i += 1  # Avanza al siguiente día
                    
                    if i == len(dias):  # Si todos los días fueron ingresados correctamente
                        linea = ",".join(horario) + "\n"
                        with open("horario.txt", "a") as archivo:
                            archivo.write(linea)
                        print(f"Horario registrado para {nombres} {apellidos}.")
                        break

                encontrado = True
                break
        
        if not encontrado:
            print("Apellido no encontrado. Inténtelo de nuevo.")

personal = cargar_personal("personal.txt")
horarios_existentes = cargar_horarios("horario.txt")

while True:
    print("\nMenu:")
    print("1. Registrar horario automáticamente por categoría de personal")
    print("2. Registrar horario manualmente")
    print("3. Salir")
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        print("Seleccione el tipo de personal:")
        print("1. Asistente de Self Checkout")
        print("2. Representante de Servicio")
        print("3. Cajer@")
        print("4. Ecommerce")
        tipo_personal_opcion = input("Ingrese el número de opción: ")
        
        tipo_personal = {
            "1": "Asistente de Self Checkout",
            "2": "Representante de Servicio",
            "3": "Cajer@",
            "4": "Ecommerce"
        }.get(tipo_personal_opcion, "Otro")

        registrar_horario(personal, tipo_personal)
    elif opcion == "2":
        registrar_horario_manualmente(personal)
    elif opcion == "3":
        break
    else:
        print("Opción no válida. Intente nuevamente.")
