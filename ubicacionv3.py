import csv
import random
from datetime import datetime

# Función para cargar los horarios desde el archivo
def cargar_horarios(archivo):
    cajeros = []
    with open(archivo, 'r') as file:
        reader = csv.reader(file)
        for fila in reader:
            cajeros.append(fila)
    return cajeros

# Función para convertir horas a objetos datetime
def hora_a_datetime(hora_str, dia):
    return datetime.strptime(f"{dia} {hora_str}", "%Y-%m-%d %H:%M") if hora_str != "DESCANSO" else None

# Función para buscar cajeros disponibles
def buscar_cajeros(cajeros, dia, inhabilitados):
    ubicaciones = []
    for cajero in cajeros:
        if cajero[2] == 'Cajer@':  # Solo considerar cajeros
            horarios = cajero[3:]
            for i in range(0, len(horarios), 2):
                entrada = hora_a_datetime(horarios[i], dia)
                salida = hora_a_datetime(horarios[i + 1], dia)
                if entrada and salida:
                    ubicaciones.append({
                        "apellido": cajero[0],
                        "nombre": cajero[1],
                        "horaEntrada": entrada,
                        "horaSalida": salida,
                        "inhabilitado": cajero[0] in inhabilitados
                    })
    return ubicaciones

# Función para asignar cajeros a las cajas
def asignar_cajeros(ubicaciones):
    cajas = {i: [] for i in range(1, 16)}  # Cajas regulares 1-15
    rapidas = {1: [], 2: []}  # Cajas rápidas 1-2
    cajeros_usados = set()  # Para llevar un registro de los cajeros ya asignados

    # Asignar cajeros a la Caja Regular 1 primero
    for ubicacion in sorted(ubicaciones, key=lambda x: x['horaEntrada']):
        # Asignar a la Caja Regular 1
        if len(cajas[1]) == 0:
            cajas[1].append(ubicacion)
            cajeros_usados.add(f"{ubicacion['apellido']} {ubicacion['nombre']}")
        else:
            ultimo_cajero = cajas[1][-1]
            if ultimo_cajero["horaSalida"] <= ubicacion["horaEntrada"] and f"{ubicacion['apellido']} {ubicacion['nombre']}" not in cajeros_usados:
                cajas[1].append(ubicacion)
                cajeros_usados.add(f"{ubicacion['apellido']} {ubicacion['nombre']}")

    # Verificar el último cajero de la Caja Regular 1
    if cajas[1] and cajas[1][-1]['horaSalida'] < datetime.strptime("22:45", "%H:%M"):
        # Buscar un cajero que salga a las 22:45
        for ubicacion in ubicaciones:
            if ubicacion['horaSalida'] == datetime.strptime("22:45", "%H:%M") and f"{ubicacion['apellido']} {ubicacion['nombre']}" not in cajeros_usados:
                # Cambiar la hora de entrada y salida de este cajero
                nuevo_cajero = ubicacion.copy()
                nuevo_cajero['horaSalida'] = cajas[1][-1]['horaSalida']
                nuevo_cajero['horaEntrada'] = cajas[1][-1]['horaSalida']  # Entrada igual a la salida del último cajero
                nuevo_cajero['nombre'] = "(T) " + nuevo_cajero['nombre']  # Indicar que es el cajero transferido
                cajas[1].append(nuevo_cajero)
                cajeros_usados.add(f"{nuevo_cajero['apellido']} {nuevo_cajero['nombre']}")
                break

    # Asignar cajeros a otras cajas
    for ubicacion in sorted(ubicaciones, key=lambda x: x['horaEntrada']):
        # Revisar otras cajas
        for caja_num in range(2, 16):
            if (len(cajas[caja_num]) == 0 or cajas[caja_num][-1]["horaSalida"] <= ubicacion["horaEntrada"]) and f"{ubicacion['apellido']} {ubicacion['nombre']}" not in cajeros_usados:
                cajas[caja_num].append(ubicacion)
                cajeros_usados.add(f"{ubicacion['apellido']} {ubicacion['nombre']}")
                break

    # Asignar cajeros a cajas rápidas (opcional)
    for caja_num in rapidas.keys():
        if len(rapidas[caja_num]) == 0:
            for ubicacion in ubicaciones:
                if ubicacion["horaEntrada"] >= datetime.strptime("09:00", "%H:%M") and f"{ubicacion['apellido']} {ubicacion['nombre']}" not in cajeros_usados:
                    rapidas[caja_num].append(ubicacion)
                    cajeros_usados.add(f"{ubicacion['apellido']} {ubicacion['nombre']}")
                    break

    return cajas, rapidas

def imprimir_resultados(cajas, rapidas, dia, cajeros_2245):

    for caja_num, cajeros in cajas.items():
        print(f"\nCaja Regular {caja_num}:")
        for i, cajero in enumerate(cajeros):
            # Verificar si es un cajero transferido
            print(f"{cajero['apellido']} {cajero['nombre']} - {cajero['horaEntrada'].strftime('%H:%M')} - {cajero['horaSalida'].strftime('%H:%M')}", end="")
            if i < len(cajeros) - 1:
                siguiente_cajero = cajeros[i + 1]
                sobra = (siguiente_cajero['horaEntrada'] - cajero['horaSalida']).seconds // 60
            else:
                sobra = 0
            print(f" Hueco de {sobra}")
        if caja_num ==1:
                # Imprimir un cajero aleatorio que sale a las 22:45
                ultimoCajeroCaja1 = imprimir_cajero_aleatorio_2245(cajeros_2245)
                print(ultimoCajeroCaja1)

    for caja_num, cajeros in rapidas.items():
        print(f"\nCaja Rápida {caja_num}:")
        for cajero in cajeros:
            print(f"{cajero['apellido']} {cajero['nombre']} - {cajero['horaEntrada'].strftime('%H:%M')} - {cajero['horaSalida'].strftime('%H:%M')}")

# Función para mostrar la lista de cajeros
def mostrar_cajeros(cajeros):
    print("Lista de cajeros:")
    for i, cajero in enumerate(cajeros):
        if cajero[2] == 'Cajer@':
            print(f"{i + 1}. {cajero[0]} {cajero[1]}")

# Función principal
def main():
    cajeros = cargar_horarios("horario.txt")

    # Mostrar lista de cajeros y preguntar por los inhabilitados
    mostrar_cajeros(cajeros)
    inhabilitados_indices = input("Ingrese los números de los cajeros inhabilitados (separados por comas): ")
    inhabilitados_indices = [int(i) - 1 for i in inhabilitados_indices.split(",")]
    inhabilitados = [cajeros[i][0] for i in inhabilitados_indices]

    # Mostrar menú de días
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    print("Seleccione un día:")
    for i, dia in enumerate(dias):
        print(f"{i + 1}. {dia}")

    dia_seleccionado = int(input("Ingrese el número del día: ")) - 1
    dia = f"2024-10-{dia_seleccionado + 1:02d}"  # Ajusta el formato de fecha

    # Buscar cajeros disponibles y asignarles cajas
    ubicaciones = buscar_cajeros(cajeros, dia, inhabilitados)
    cajas, rapidas = asignar_cajeros(ubicaciones)

    # Imprimir los 
    cajeros_2245 = obtener_cajeros_2245(cajeros, dia)
    imprimir_resultados(cajas, rapidas, dia_seleccionado, cajeros_2245)
    
    #Debug

    print(f"\n\n\n========== Imprimir Cajeros 22:45 ==========")
    cajeros_2245 = eliminar_duplicados(cajeros_2245)
    for e in cajeros_2245:
        print(e)


def eliminar_duplicados(lista):
    lista = list({(d['apellido'], d['nombre'], d['horaSalida']): d for d in lista}.values())
    return lista

# Nueva función para obtener cajeros que salen a las 22:45
def obtener_cajeros_2245(cajeros, dia):
    cajeros_2245 = []
    for cajero in cajeros:
        # Verificar que la fila tenga al menos 3 elementos y que contenga 'Cajer@'
        if len(cajero) > 2 and 'Cajer@' in cajero:  # Solo considerar cajeros
            horarios = cajero[3:]
            for i in range(1, len(horarios), 2):  # Solo buscar horas de salida
                salida = hora_a_datetime(horarios[i], dia)
                if salida and salida.strftime("%H:%M") == "22:45":
                    cajeros_2245.append({
                        "apellido": cajero[0],
                        "nombre": cajero[1],
                        "horaSalida": salida
                    })
    return cajeros_2245

def imprimir_cajero_aleatorio_2245(cajeros_2245):
    if cajeros_2245:
        cajero_aleatorio = random.choice(cajeros_2245)
        res = f"(T) {cajero_aleatorio['apellido']} {cajero_aleatorio['nombre']} {cajero_aleatorio['horaSalida'].strftime('%H:%M')}"    
    else:
        print("\nNo hay cajeros que salgan a las 22:45.")
        res = f"Error"
    return res

if __name__ == "__main__":
    cajeros_2245 = ""
    ultimoCajeroCaja1 = ""
    main()
    print(ultimoCajeroCaja1)
    
