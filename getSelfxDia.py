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

def printSelf(horarios_dia):
    Self = []
    print("\nOrden de Entradas:")
    entradas = []
    for entrada, registros in horarios_dia.items():
        if entrada != 'DESCANSO':
            for registro in registros:
                if len(registro) == 4:
                    apellidos, nombres, entrada, salida = registro
                    entradas.append((entrada, salida, apellidos, nombres))
    #Limpiar Duplicados
    entradas = list(set(entradas))

    #Imprimir Lista
    for entrada, salida, apellidos, nombres in sorted(entradas, key=lambda x: x[0]):
        print(f"{entrada} - {salida} - {apellidos} {nombres}")
        Self.append([f"{apellidos}, {nombres}", f"{entrada}-{salida}"])

    return Self
    


def main():
    archivo_horarios = "horario.txt"
    horarios = cargar_horarios(archivo_horarios)
    
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    print("\nSeleccionar Día:")
    for i, dia in enumerate(dias, 1):
        print(f"{i}. {dia.capitalize()}")
    dia_opcion = int(input("Ingrese el número de opción: ")) - 1
    dia = dias[dia_opcion]        
    horarios_dia = obtener_horarios_por_dia(horarios, dia, "Self Checkout")
    ASelf = printSelf(horarios_dia)
    for e in ASelf:
        print(e)

if __name__ == "__main__":
    main()