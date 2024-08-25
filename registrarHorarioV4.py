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
    horarios = {}
    with open(archivo, "r") as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            datos = linea.strip().split(",")
            apellidos_nombres = (datos[0], datos[1])
            horarios[apellidos_nombres] = datos[2:]
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

def registrar_horario_por_categoria(categoria, personal):
    personal_categoria = [p for p in personal if p[2].lower() == categoria.lower()]
    if not personal_categoria:
        print(f"No se encontró personal en la categoría '{categoria}'.")
        return
    
    horarios_completos = []
    with open("horario.txt", "a") as archivo:
        for persona in personal_categoria:
            apellidos, nombres, cargo = persona
            if (apellidos, nombres) in horarios_existentes:
                print(f"{nombres} {apellidos} ya tiene horario registrado. Saltando.")
                continue
            
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
                    return
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
            
            if completo:
                horarios_completos.append(horario)
                print(f"Horario registrado para {nombres} {apellidos}.")
            else:
                print(f"El horario para {nombres} {apellidos} no se completó. No se guardará.")
                break
        
        for h in horarios_completos:
            linea = ",".join(h) + "\n"
            archivo.write(linea)

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
                        return
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
                
                if completo:
                    with open("horario.txt", "a") as archivo:
                        linea = ",".join(horario) + "\n"
                        archivo.write(linea)
                    print(f"Horario registrado para {nombres} {apellidos}.")
                else:
                    print(f"El horario para {nombres} {apellidos} no se completó. No se guardará.")
                encontrado = True
                return

        if not encontrado:
            print("No se encontró ninguna persona con ese apellido. Intente de nuevo.")

def main():
    archivo_personal = "personal.txt"
    archivo_horarios = "horario.txt"
    
    personal = cargar_personal(archivo_personal)
    global horarios_existentes
    horarios_existentes = cargar_horarios(archivo_horarios)

    while True:
        print("\nSeleccione el tipo de personal para ingresar horarios:")
        print("1. Asistente de Self Checkout")
        print("2. Representante de Servicio")
        print("3. Cajer@")
        print("4. Ecommerce")
        print("5. Registrar Manualmente")
        print("6. Limpiar el archivo de horarios")
        print("0. Salir")
        
        opcion = input("Ingrese el número de la opción deseada: ")
        
        if opcion == "1":
            registrar_horario_por_categoria("Asistente de Self Checkout", personal)
        elif opcion == "2":
            registrar_horario_por_categoria("Representante de Servicio", personal)
        elif opcion == "3":
            registrar_horario_por_categoria("Cajer@", personal)
        elif opcion == "4":
            registrar_horario_por_categoria("Ecommerce", personal)
        elif opcion == "5":
            registrar_horario_manualmente(personal)
        elif opcion == "6":
            limpiar_archivo(archivo_horarios)
            print("Archivo de horarios limpiado.")
        elif opcion == "0":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
