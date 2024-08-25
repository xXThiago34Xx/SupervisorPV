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
        clear_screen()
        print("Selecciona una opción:")
        print("1. Registrar Personal")
        print("2. Limpiar Horario")
        print("3. Registrar Horario")
        print("4. Entradas y Salidas")
        print("5. Exportar WhatsApp")
        print("6. Exportar Gráfico")
        print("11. Tools")
        print("0. Salir")
        
        choice = input("Ingresa el número de tu elección: ")
        
        if choice == '1':
            run_script('registrarPersonal.py')
        elif choice == '2':
            run_script('limpiarHorario.py')
        elif choice == '3':
            run_script('registrarHorarioV2.py')
        elif choice == '4':
            run_script('EntradasSalidasV2.py')
        elif choice == '5':
            run_script('ExportarWhatsapp.py')
        elif choice == '6':
            run_script('newGraficV2.py')
        elif choice == '11':
            run_script('Tools.py')
        elif choice == '0':
            print("Saliendo...")
            sys.exit()
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            input("Presiona Enter para continuar...")

def run_script(script_name):
    if os.path.exists(script_name):
        print(f"Ejecutando {script_name}...")
        os.system(f'python {script_name}')
    else:
        print(f"El archivo {script_name} no se encuentra.")
        input("Presiona Enter para continuar...")

if __name__ == "__main__":
    menu()
