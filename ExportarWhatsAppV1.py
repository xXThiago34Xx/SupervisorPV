import csv
import pyperclip
import time
import keyboard
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

def generar_mensaje(horarios_dia):
    mensaje = ""
    if not horarios_dia:
        mensaje = "No se encontraron Registros"
    else:
        mensaje += "Entradas y Salidas:\n"
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
            mensaje += f"\n{hora}\n"
            if hora in horarios_entradas:
                mensaje += "Entradas:\n"
                for apellidos, nombres, entrada, salida in sorted(horarios_entradas[hora], key=lambda x: x[1]):
                    mensaje += f"{apellidos} {nombres} - {entrada} - {salida}\n"
            if hora in horarios_salidas:
                mensaje += "Salidas:\n"
                for apellidos, nombres, entrada, salida in sorted(horarios_salidas[hora], key=lambda x: x[1]):
                    mensaje += f"{apellidos} {nombres} - {entrada} - {salida}\n"
        if 'DESCANSO' in horarios_dia:
            mensaje += "\nDescansos:\n"
            for apellidos, nombres in horarios_dia['DESCANSO']:
                mensaje += f"{apellidos} {nombres} - DESCANSO\n"
    return mensaje

def procesar_opcion(opcion, horarios):
    dia_mapping = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    tipos_personal = ["Asistente de Self Checkout", "Representante de Servicio", "Cajer@", "Ecommerce", "Supervisor(@)"]
    
    if opcion == 6:
        print("\nSeleccionar Día:")
        for i, dia in enumerate(dia_mapping, 1):
            print(f"{i}. {dia.capitalize()}")
        dia_opcion = int(input("Ingrese el número de opción: ")) - 1
        dia = dia_mapping[dia_opcion]
        
        for tipo_personal in tipos_personal:
            print(f"\nEsperando 10 segundos para {tipo_personal} - {dia.capitalize()}...")
            time.sleep(10)
            encabezado = f"--- {tipo_personal} --- {dia.capitalize()} ---\n"
            print(encabezado)
            horarios_dia = obtener_horarios_por_dia(horarios, dia, tipo_personal)
            mensaje = generar_mensaje(horarios_dia)
            mensaje_completo = encabezado + mensaje
            pyperclip.copy(mensaje_completo)
            time.sleep(3)  # Espera antes de pegar
            keyboard.press_and_release('ctrl+v')  # Pega el mensaje
            time.sleep(3)  # Espera antes de enviar
            keyboard.press_and_release('enter')  # Envía el mensaje
    
    else:
        tipo_personal = tipos_personal[opcion - 1]
        dia_mapping = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        
        for dia in dia_mapping:
            print(f"\nEsperando 10 segundos para {tipo_personal} - {dia.capitalize()}...")
            time.sleep(10)
            encabezado = f"--- {tipo_personal} --- {dia.capitalize()} ---\n"
            print(encabezado)
            horarios_dia = obtener_horarios_por_dia(horarios, dia, tipo_personal)
            mensaje = generar_mensaje(horarios_dia)
            mensaje_completo = encabezado + mensaje
            pyperclip.copy(mensaje_completo)
            time.sleep(3)  # Espera antes de pegar
            keyboard.press_and_release('ctrl+v')  # Pega el mensaje
            time.sleep(3)  # Espera antes de enviar
            keyboard.press_and_release('enter')  # Envía el mensaje
    
    input("\nPresiona Enter para volver al menú inicial...")

def main():
    archivo_horarios = "horario.txt"
    horarios = cargar_horarios(archivo_horarios)
    
    while True:
        print("\nExportar a WhatsApp De:")
        print("1. Asistente de Self Checkout")
        print("2. Representante de Servicio")
        print("3. Cajer@")
        print("4. Ecommerce")
        print("5. Supervisor(@)")
        print("6. Exportar por Día")
        print("0. Salir")
        opcion = int(input("Ingrese el número de opción: "))
        
        if opcion == 0:
            break
        
        if opcion in [1, 2, 3, 4, 5, 6]:
            procesar_opcion(opcion, horarios)
        else:
            print("Opción inválida. Intente nuevamente.")
        
        continuar = int(input("\n¿Desea volver al menú inicial? (1 para sí, 0 para no): ").strip())
        if continuar != 1:
            break

if __name__ == "__main__":
    main()
