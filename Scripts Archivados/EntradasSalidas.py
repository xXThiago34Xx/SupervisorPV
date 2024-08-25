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
            horarios_dia['entrada'].append((formatear_hora(entrada), formatear_hora(salida), f"{nombres} {apellidos}"))
    
    return horarios_dia

def mostrar_horarios(horarios_dia, ver_por):
    if ver_por == "1":
        print("\nEntradas y Salidas:")
        for entrada, salida, persona in sorted(horarios_dia['entrada']):
            print(f"{entrada} - {salida} - {persona}")
    
    elif ver_por == "2":
        print("\nOrden de Entradas:")
        for entrada, salida, persona in sorted(horarios_dia['entrada'], key=lambda x: x[0]):
            print(f"{entrada} - {salida} - {persona}")
    
    elif ver_por == "3":
        print("\nOrden de Salidas:")
        for entrada, salida, persona in sorted(horarios_dia['entrada'], key=lambda x: x[1]):
            print(f"{entrada} - {salida} - {persona}")

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
        ver_por_opcion = input("Ingrese el número de opción: ")
        
        horarios_dia = obtener_horarios_por_dia(horarios, dia, tipo_personal)
        mostrar_horarios(horarios_dia, ver_por_opcion)
        
        salir = input("\n¿Desea salir? (s/n): ").strip().lower()
        if salir == "s":
            break

if __name__ == "__main__":
    main()
