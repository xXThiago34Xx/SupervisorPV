import os
import sys

def menu():
    while True:
        print("Selecciona una opción:")
        print("1. Cuentas")
        print("2. EAN13")
        print("3. Salir")
        
        choice = input("Ingresa el número de tu elección: ")
        
        if choice == '1':
            run_script('cuentas.py')
        elif choice == '2':
            run_script('EAN.py')
        elif choice == '3':
            print("Saliendo...")
            sys.exit()
        else:
            print("Opción no válida. Inténtalo de nuevo.")

def run_script(script_name):
    if os.path.exists(script_name):
        print(f"Ejecutando {script_name}...")
        os.system(f'python {script_name}')
    else:
        print(f"El archivo {script_name} no se encuentra.")

if __name__ == "__main__":
    menu()
