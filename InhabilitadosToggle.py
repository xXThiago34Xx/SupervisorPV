'''
- Enumerar desde el 1 los cajeros
- Mostrar un indicador de que son inhabilitados
- El usuario escribe el número o números
- El usuario puede salir con un 0
'''

from ubicacionv3 import cargar_horarios, get_cajeros
import os

def get_inhabilitados_indices(cajeros, inhabilitados_path):
    inhabilitados = load_inhabilitados(inhabilitados_path)
    indices_inhabilitados = []
    for cajero in cajeros:
        full_name = f"{cajero['apellido']}, {cajero['nombre']}"
        if full_name in inhabilitados:
            indices_inhabilitados.append(cajero["index"])
    return indices_inhabilitados

def load_inhabilitados(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass  # Create the file if it doesn't exist
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def save_inhabilitados(file_path, inhabilitados):
    with open(file_path, 'w') as f:
        for cajero in inhabilitados:
            f.write(f"{cajero}\n")

def toggle_inhabilitado(cajeros, inhabilitados, file_path):
    while True:
        print("\nLista de Cajeros:")
        for i, cajero in enumerate(cajeros):
            full_name = f"{cajero['apellido']}, {cajero['nombre']}"  # Format: <apellido>, nombre
            estado = "❌" if full_name in inhabilitados else "✅"
            print(f"{i+1}. {full_name} - {estado}")

        print("\nIngrese el número del cajero para cambiar su estado, o 0 para salir.")
        try:
            seleccion = int(input("Seleccionar cajero: "))
            if seleccion == 0:
                break
            if 1 <= seleccion <= len(cajeros):
                cajero = cajeros[seleccion - 1]
                full_name = f"{cajero['apellido']}, {cajero['nombre']}"
                if full_name in inhabilitados:
                    inhabilitados.remove(full_name)
                    print(f"{full_name} ha sido habilitado.")
                else:
                    inhabilitados.append(full_name)
                    print(f"{full_name} ha sido inhabilitado.")
                
                # Save changes after every toggle
                save_inhabilitados(file_path, inhabilitados)
            else:
                print("Número de cajero no válido.")
        except ValueError:
            print("Entrada no válida. Intente nuevamente.")
    
    return inhabilitados

if __name__ == '__main__':
    inhabilitados_path = "inhabilitados.txt"
    
    horarios = cargar_horarios("horario.txt")
    cajeros = get_cajeros(horarios)
    
    inhabilitados = load_inhabilitados(inhabilitados_path)
    
    inhabilitados = toggle_inhabilitado(cajeros, inhabilitados, inhabilitados_path)
    
    # Get indices of inhabilitados
    indices_inhabilitados = get_inhabilitados_indices(cajeros, inhabilitados_path)
    print(f"Indices de cajeros inhabilitados: {indices_inhabilitados}")