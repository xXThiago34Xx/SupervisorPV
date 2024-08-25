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

def interpretar_salida(salida, entrada):
    if salida.lower() == "p":
        return sumar_duracion(entrada, (3, 45))  
    elif salida.lower() == "f":
        return sumar_duracion(entrada, (9, 0))  
    else:
        return formatear_hora(salida) 

def registrar_horario(personal):
    with open("horario.txt", "a") as archivo:  
        for persona in personal:
            apellidos, nombres, cargo = persona
            if (apellidos, nombres) in horarios_existentes:
                print(f"{nombres} {apellidos} ya tiene horario registrado. Saltando.")
                continue
            
            horario = [apellidos, nombres, cargo]
            tipo_jornada = None

            for dia in ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]:
                entrada = input(f"Ingrese la hora de entrada para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'd'): ")
                
                if entrada.lower() == "d":
                    horario.extend(["DESCANSO", "DESCANSO"])
                else:
                    entrada_formateada = formatear_hora(entrada)
                    
                    if tipo_jornada:
                        salida_formateada = sumar_duracion(entrada_formateada, (9, 0)) if tipo_jornada == "ft" else sumar_duracion(entrada_formateada, (3, 45))
                    else:
                        salida = input(f"Ingrese la hora de salida para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'p', 'f', 'pt', 'ft'): ")
                        
                        if salida.lower() in ['ft', 'pt']:
                            tipo_jornada = salida.lower()
                            salida_formateada = sumar_duracion(entrada_formateada, (9, 0)) if tipo_jornada == "ft" else sumar_duracion(entrada_formateada, (3, 45))
                        else:
                            salida_formateada = interpretar_salida(salida, entrada_formateada)
                    
                    horario.extend([entrada_formateada, salida_formateada])
            
            linea = ",".join(horario) + "\n"
            archivo.write(linea)
            print(f"Horario registrado para {nombres} {apellidos}.")

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
                
                horario = [apellidos, nombres, cargo]
                tipo_jornada = None

                for dia in ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]:
                    entrada = input(f"Ingrese la hora de entrada para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'd'): ")
                    
                    if entrada.lower() == "d":
                        horario.extend(["DESCANSO", "DESCANSO"])
                    else:
                        entrada_formateada = formatear_hora(entrada)
                        
                        if tipo_jornada:
                            salida_formateada = sumar_duracion(entrada_formateada, (9, 0)) if tipo_jornada == "ft" else sumar_duracion(entrada_formateada, (3, 45))
                        else:
                            salida = input(f"Ingrese la hora de salida para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, 'p', 'f', 'pt', 'ft'): ")
                            
                            if salida.lower() in ['ft', 'pt']:
                                tipo_jornada = salida.lower()
                                salida_formateada = sumar_duracion(entrada_formateada, (9, 0)) if tipo_jornada == "ft" else sumar_duracion(entrada_formateada, (3, 45))
                            else:
                                salida_formateada = interpretar_salida(salida, entrada_formateada)
                        
                        horario.extend([entrada_formateada, salida_formateada])
                
                with open("horario.txt", "a") as archivo:
                    linea = ",".join(horario) + "\n"
                    archivo.write(linea)
                print(f"Horario registrado para {nombres} {apellidos}.")
                encontrado = True
                return
        
        if not encontrado:
            print("No se encontró ninguna persona con ese apellido. Intente de nuevo.")

def registrar_horario_por_categoria(categoria, personal):
    personal_categoria = [p for p in personal if p[2].lower() == categoria.lower()]
    if not personal_categoria:
        print(f"No se encontró personal en la categoría '{categoria}'.")
        return
    registrar_horario(personal_categoria)

def mostrar_menu():
    while True:
        print("\nSeleccione el tipo de personal para ingresar horarios:")
        print("1. Asistente de Self Checkout")
        print("2. Representante de Servicio")
        print("3. Cajer@")
        print("4. Ecommerce")
        print("5. Manual (Ingresar apellido específico)")
        print("x. Salir")
        
        opcion = input("Ingrese su opción: ").strip().lower()
        
        if opcion == '1':
            registrar_horario_por_categoria("Asistente de Self Checkout", personal)
        elif opcion == '2':
            registrar_horario_por_categoria("Representante de Servicio", personal)
        elif opcion == '3':
            registrar_horario_por_categoria("Cajer@", personal)
        elif opcion == '4':
            registrar_horario_por_categoria("Ecommerce", personal)
        elif opcion == '5':
            registrar_horario_manualmente(personal)
        elif opcion == 'x':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Cargar la lista de personal desde el archivo 'personal.txt'
personal = cargar_personal("personal.txt")

# Cargar los horarios ya existentes desde el archivo 'horario.txt'
horarios_existentes = cargar_horarios("horario.txt")

# Mostrar el menú de opciones
mostrar_menu()
