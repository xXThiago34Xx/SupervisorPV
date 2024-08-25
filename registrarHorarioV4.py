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
    comandos_duracion = {"*": (3, 45), "**": (8, 0), "***": (9, 0)}
    if salida in comandos_duracion:
        return sumar_duracion(entrada, comandos_duracion[salida])
    elif salida == ".":
        return "DESCANSO"
    else:
        return formatear_hora(salida)

def limpiar_archivo(archivo):
    with open(archivo, "w") as archivo:
        pass

def registrar_horario(personal):
    horarios_completos = []
    dia_index = 0
    actual_persona = None
    while dia_index < 7:
        if actual_persona is None:
            print("\nSeleccione una persona para registrar horarios:")
            for i, persona in enumerate(personal):
                apellidos, nombres, cargo = persona
                print(f"{i+1}. {nombres} {apellidos} ({cargo})")
            print(f"{len(personal) + 1}. Volver al menú principal")
            seleccion = input("Ingrese el número de la opción deseada: ")
            if seleccion.isdigit() and 1 <= int(seleccion) <= len(personal):
                actual_persona = personal[int(seleccion) - 1]
                apellidos, nombres, cargo = actual_persona
                if (apellidos, nombres) in horarios_existentes:
                    print(f"{nombres} {apellidos} ya tiene horario registrado. Saltando.")
                    actual_persona = None
                    continue
                horario = [apellidos, nombres, cargo]
                jornada_duracion = None
                completo = True
            elif seleccion == str(len(personal) + 1):
                print("Volviendo al menú principal.")
                return
            else:
                print("Opción no válida.")
                continue

        if actual_persona is not None:
            apellidos, nombres, cargo = actual_persona
            dia = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"][dia_index]
            entrada = input(f"Ingrese la hora de entrada para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, ., /, //, ..): ")

            if entrada.lower() == "/":
                if dia_index > 0:
                    dia_index -= 1
                    horario = horario[:-2]  # Elimina la entrada y salida del día anterior
                    continue
                else:
                    print("No se puede retroceder más.")
                    continue
            elif entrada.lower() == "//":
                print("Reiniciando desde el lunes.")
                return "reiniciar_semana"
            elif entrada.lower() == "..":
                print("Volviendo al menú principal.")
                completo = False
                actual_persona = None
                dia_index = 0
                continue
            elif entrada == ".":
                horario.extend(["DESCANSO", "DESCANSO"])
            else:
                entrada_formateada = formatear_hora(entrada)
                
                if not jornada_duracion:
                    salida = input(f"Ingrese la hora de salida para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, *, **, ***, +, ++, .): ")

                    if salida == "+":
                        jornada_duracion = (3, 45)  # Part-time
                        salida_formateada = sumar_duracion(entrada_formateada, jornada_duracion)
                    elif salida == "++":
                        jornada_duracion = (9, 0)  # Full-time
                        salida_formateada = sumar_duracion(entrada_formateada, jornada_duracion)
                    else:
                        salida_formateada = interpretar_salida(salida, entrada_formateada)
                else:
                    salida_formateada = sumar_duracion(entrada_formateada, jornada_duracion)

                horario.extend([entrada_formateada, salida_formateada])
            
            dia_index += 1
            if dia_index >= 7:
                if completo:
                    horarios_completos.append(horario)
                    print(f"Horario registrado para {nombres} {apellidos}.")
                else:
                    print(f"El horario para {nombres} {apellidos} no se completó. No se guardará.")
                    actual_persona = None
                    dia_index = 0
                    continue

        if dia_index >= 7 and actual_persona:
            for h in horarios_completos:
                with open("horario.txt", "a") as archivo:
                    linea = ",".join(h) + "\n"
                    archivo.write(linea)
            horarios_completos = []
            actual_persona = None
            dia_index = 0

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
                jornada_duracion = None
                completo = True

                dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
                dia_index = 0
                
                while dia_index < len(dias):
                    dia = dias[dia_index]
                    
                    entrada = input(f"Ingrese la hora de entrada para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, ., /, //, ..): ")

                    if entrada.lower() == "/":
                        if dia_index > 0:
                            dia_index -= 1
                            horario = horario[:-2]  # Elimina la entrada y salida del día anterior
                            continue
                        else:
                            print("No se puede retroceder más.")
                            continue
                    elif entrada.lower() == "//":
                        print("Reiniciando desde el lunes.")
                        return "reiniciar_semana"
                    elif entrada.lower() == "..":
                        print("Volviendo al menú principal.")
                        completo = False
                        break
                    elif entrada == ".":
                        horario.extend(["DESCANSO", "DESCANSO"])
                    else:
                        entrada_formateada = formatear_hora(entrada)
                        
                        if not jornada_duracion:
                            salida = input(f"Ingrese la hora de salida para {nombres} {apellidos} el {dia} (ej. 645, 9, 16, *, **, ***, +, ++, .): ")

                            if salida == "+":
                                jornada_duracion = (3, 45)  # Part-time
                                salida_formateada = sumar_duracion(entrada_formateada, jornada_duracion)
                            elif salida == "++":
                                jornada_duracion = (9, 0)  # Full-time
                                salida_formateada = sumar_duracion(entrada_formateada, jornada_duracion)
                            else:
                                salida_formateada = interpretar_salida(salida, entrada_formateada)
                        else:
                            salida_formateada = sumar_duracion(entrada_formateada, jornada_duracion)

                        horario.extend([entrada_formateada, salida_formateada])
                    
                    dia_index += 1
                    if dia_index >= 7:
                        if completo:
                            horarios_completos.append(horario)
                            print(f"Horario registrado para {nombres} {apellidos}.")
                        else:
                            print(f"El horario para {nombres} {apellidos} no se completó. No se guardará.")
                            break

                if completo:
                    with open("horario.txt", "a") as archivo:
                        linea = ",".join(horario) + "\n"
                        archivo.write(linea)
                encontrado = True
                break
        
        if not encontrado:
            print("No se encontró la persona.")

def main():
    archivo_personal = "personal.txt"
    archivo_horarios = "horarios.txt"
    
    personal = cargar_personal(archivo_personal)
    global horarios_existentes
    horarios_existentes = cargar_horarios(archivo_horarios)

    while True:
        print("\nMenú principal:")
        print("1. Registrar horario")
        print("2. Registrar horario manualmente")
        print("3. Salir")
        
        opcion = input("Ingrese el número de la opción deseada: ")
        
        if opcion == "1":
            resultado = registrar_horario(personal)
            if resultado == "reiniciar_semana":
                continue
        elif opcion == "2":
            resultado = registrar_horario_manualmente(personal)
            if resultado == "reiniciar_semana":
                continue
        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
