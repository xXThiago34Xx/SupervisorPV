import os
import sys

def clear_screen():
    # Clear the terminal screen
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def menu():
    while True:
        clear_screen()  # Clear the screen before displaying the menu
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
            input("Presiona Enter para continuar...")

def run_script(script_name):
    clear_screen()  # Clear the screen before running the script
    if os.path.exists(script_name):
        print(f"Ejecutando {script_name}...")
        os.system(f'python {script_name}')
    else:
        print(f"El archivo {script_name} no se encuentra.")
    input("Presiona Enter para continuar...")  # Wait for user input before returning to the menu

if __name__ == "__main__":
    menu()
