import csv
from collections import defaultdict
from ubicacionv3 import dia_menu, cargar_horarios

def formatear_hora(hora):
    hora_str = str(hora)
    if len(hora_str) == 1 or len(hora_str) == 2:
        hora_str = hora_str.zfill(2) + ":00"
    elif len(hora_str) == 3:
        hora_str = "0" + hora_str[0] + ":" + hora_str[1:]
    elif len(hora_str) == 4:
        hora_str = hora_str[:2] + ":" + hora_str[2:]
    return hora_str

def obtener_horarios_por_dia(horarios, diaI, tipo_personal):
    horarios_dia = defaultdict(list)
    
    for registro in horarios:
        apellidos, nombres, cargo, *dias = registro
        if cargo.lower() == tipo_personal.lower():
            entrada = dias[(diaI-1) * 2]
            salida = dias[(diaI-1) * 2 + 1]
            entrada_formateada = formatear_hora(entrada)
            salida_formateada = formatear_hora(salida)
            if entrada_formateada == "DESCANSO" and salida_formateada == "DESCANSO":
                horarios_dia['DESCANSO'].append((apellidos, nombres))
            else:
                horarios_dia[entrada_formateada].append((apellidos, nombres, entrada_formateada, salida_formateada))
                horarios_dia[salida_formateada].append((apellidos, nombres, entrada_formateada, salida_formateada))
    
    return horarios_dia


def procesar_registros(horarios_dia):
    entradas = []
    for entrada, registros in horarios_dia.items():
        if entrada != 'DESCANSO':
            for registro in registros:
                if len(registro) == 4:
                    apellidos, nombres, entrada, salida = registro
                    entradas.append((entrada, salida, apellidos, nombres))
    # Limpiar duplicados
    entradas = list(set(entradas))
    
    # Ordenar por la hora de entrada
    entradas_ordenadas = sorted(entradas, key=lambda x: x[0])
    
    # Formatear la lista para retornar
    return [[f"{apellidos}, {nombres}", f"{entrada}-{salida}"] for entrada, salida, apellidos, nombres in entradas_ordenadas]

def imprimir_entradas(entradas):
    print("\nOrden de Entradas:")
    for entrada, salida, apellidos, nombres in entradas:
        print(f"{entrada} - {salida} - {apellidos} {nombres}")

def get_self_exportados(horarios, diaI):
    horarios_dia = obtener_horarios_por_dia(horarios, diaI, "Self Checkout")
    entradas = procesar_registros(horarios_dia)
    return entradas

def main():
    archivo_horarios = "horario.txt"
    horarios = cargar_horarios(archivo_horarios)
    diaI = dia_menu()

    horarios_dia = obtener_horarios_por_dia(horarios, diaI, "Self Checkout")
    entradas = procesar_registros(horarios_dia)
    imprimir_entradas(entradas)

if __name__ == "__main__":
    main()