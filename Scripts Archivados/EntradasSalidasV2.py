import csv
from collections import defaultdict

def cargar_horarios(archivo):
    horarios = []
    with open(archivo, "r") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            horarios.append(fila)
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

def obtener_horarios_por_dia(horarios, dia, tipo_personal):
    dia_index = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"].index(dia.lower())
    horarios_dia = defaultdict(list)
    
    for registro in horarios:
        apellidos, nombres, cargo, *dias = registro
        if cargo.lower() == tipo_personal.lower():
            entrada = dias[dia_index * 2]
            salida = dias[dia_index * 2 + 1]
            entrada_formateada = formatear_hora(entrada)
            salida_formateada = formatear_hora(salida)
            if entrada_formateada == "DESCANSO" and salida_formateada == "DESCANSO":
                horarios_dia['DESCANSO'].append((apellidos, nombres))
            else:
                horarios_dia[entrada_formateada].append((apellidos, nombres, entrada_formateada, salida_formateada))
                horarios_dia[salida_formateada].append((apellidos, nombres, entrada_formateada, salida_formateada))
    
    return horarios_dia

def mostrar_horarios(horarios_dia, ver_por):
    if ver_por == "1":
        print("\nEntradas y Salidas:")
        horarios_entradas = defaultdict(list)
        horarios_salidas = defaultdict(list)

        for hora, registros in horarios_dia.items():
            if hora == 'DESCANSO':
                continue
            for apellidos, nombres, entrada, salida in registros:
                if hora == entrada:
                    horarios_entradas[hora].append((apellidos, nombres, entrada, salida))
                elif hora == salida:
                    horarios_salidas[hora].append((apellidos, nombres, entrada, salida))

        for hora in sorted(set(horarios_entradas.keys()).union(horarios_salidas.keys())):
            print(f"\n{hora}")
            if hora in horarios_entradas:
                print("Entradas:")
                for apellidos, nombres, entrada, salida in sorted(horarios_entradas[hora], key=lambda x: x[1]):
                    print(f"{apellidos} {nombres} - {entrada} - {salida}")
            if hora in horarios_salidas:
                print("Salidas:")
                for apellidos, nombres, entrada, salida in sorted(horarios_salidas[hora], key=lambda x: x[1]):
                    print(f"{apellidos} {nombres} - {entrada} - {salida}")
        if 'DESCANSO' in horarios_dia:
            print("\nDescansos:")
            for apellidos, nombres in horarios_dia['DESCANSO']:
                print(f"{apellidos} {nombres} - DESCANSO")
    
    elif ver_por == "2":
        print("\nOrden de Entradas:")
        entradas = [(entrada, salida, apellidos, nombres) for entrada, registros in horarios_dia.items() for apellidos, nombres, entrada, salida in registros if entrada != 'DESCANSO']
        for entrada, salida, apellidos, nombres in sorted(entradas, key=lambda x: x[0]):
            print(f"{entrada} - {salida} - {apellidos} {nombres}")
    
    elif ver_por == "3":
        print("\nOrden de Salidas:")
        salidas = [(entrada, salida, apellidos, nombres) for salida, registros in horarios_dia.items() for apellidos, nombres, entrada, salida in registros if salida != 'DESCANSO']
        for entrada, salida, apellidos, nombres in sorted(salidas, key=lambda x: x[1]):
            print(f"{entrada} - {salida} - {apellidos} {nombres}")

    elif ver_por == "11":
        print("\nMostrar Gráfico:")
        # Crear intervalos de 15 minutos desde las 06:00 hasta las 24:00
        intervalos = [f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(6, 24) for m in [0, 15, 30, 45]]
        intervalos.append("24:00")
        
        # Ancho para columnas
        ancho_columna = 20
        
        # Crear encabezados de columnas
        personal = {}
        for registros in horarios_dia.values():
            for registro in registros:
                if len(registro) == 2:
                    # Si el registro es de tipo DESCANSO, no lo agregamos al gráfico
                    continue
                apellidos = registro[0]
                entrada = registro[2]
                if apellidos not in personal:
                    personal[apellidos] = entrada
        personal_ordenado = sorted(personal.keys(), key=lambda x: personal[x])
        
        # Imprimir encabezados de columna
        print(f"{'Hora':<{ancho_columna}}", end="")
        for p in personal_ordenado:
            print(f"{p:<{ancho_columna}}", end="")  # Espacio adicional en el encabezado
        print()

        # Imprimir horarios por intervalos
        for intervalo in intervalos:
            print(f"{intervalo:<{ancho_columna}}", end="")
            for p in personal_ordenado:
                ocupado = False
                for registros in horarios_dia.values():
                    for registro in registros:
                        if len(registro) == 2:
                            # Si el registro es de tipo DESCANSO, no se considera para las "X"
                            if registro[0] == p:
                                ocupado = False
                                break
                        else:
                            apellidos, nombres, entrada, salida = registro
                            if apellidos == p:
                                # Convertir intervalo y tiempos de entrada/salida a minutos para comparación
                                intervalo_min = int(intervalo[:2]) * 60 + int(intervalo[3:])
                                entrada_min = int(entrada[:2]) * 60 + int(entrada[3:])
                                salida_min = int(salida[:2]) * 60 + int(salida[3:])
                                
                                if entrada_min <= intervalo_min < salida_min:
                                    ocupado = True
                                    break
                    if ocupado:
                        break
                if ocupado:
                    print(f"{'X':^{ancho_columna}}", end="")  # Espacio adicional para las "X"
                else:
                    print(f"{'':^{ancho_columna}}", end="")  # Espacio adicional para columnas vacías
            print()

def main():
    archivo_horarios = "horario.txt"
    horarios = cargar_horarios(archivo_horarios)
    
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    tipos_personal = ["Asistente de Self Checkout", "Representante de Servicio", "Cajer@", "Ecommerce"]
    
    while True:
        print("\nSeleccionar Día:")
        for i, dia in enumerate(dias, 1):
            print(f"{i}. {dia.capitalize()}")
        dia_opcion = int(input("Ingrese el número de opción: ")) - 1
        dia = dias[dia_opcion]
        
        print("\nVer Horarios De:")
        for i, tipo in enumerate(tipos_personal, 1):
            print(f"{i}. {tipo}")
        tipo_personal_opcion = int(input("Ingrese el número de opción: ")) - 1
        tipo_personal = tipos_personal[tipo_personal_opcion]
        
        print("\nVer Por:")
        print("1. Ver Horarios Entradas y Salidas")
        print("2. Ver Horarios Por Orden de Entrada")
        print("3. Ver Horarios Por Orden de Salida")
        print("11. Mostrar Gráfico")
        ver_por_opcion = input("Ingrese el número de opción: ")
        
        horarios_dia = obtener_horarios_por_dia(horarios, dia, tipo_personal)
        mostrar_horarios(horarios_dia, ver_por_opcion)
        
        salir = input("\n¿Desea salir? (s/n): ").strip().lower()
        if salir == "s":
            break

if __name__ == "__main__":
    main()
