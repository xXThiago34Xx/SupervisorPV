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
        print("1. Registrar Personal")
        print("12. Registrar NICKNAMES de Personal")
        print("2. Limpiar Horario")
        print("3. Registrar Horario")
        print("4. Entradas y Salidas")
        print("41. // EN DESARROLLO // Personal Presente A Cierta Hora")
        print("5. Exportar WhatsApp")
        print("6. Exportar Excel de Mapa de Horario ESPECIFICO")
        print("7. Exportar Excel de Mapa de Horario SEMANAL")
        print("8. Exportar Excel de Mapa de Horario SEMANAL a PDF")
        print("9. Exportar Excel de Mapa de Personal del Area DIA ESPECIFICO")
        print("10. // EN DESARROLLO // Exportar Excel de Mapa de Personal del Area SEMANAL")
        print("11. // EN DESARROLLO // Exportar Excel de Mapa de Personal del Area SEMANAL a PDF")
        print("13. // EN DESARROLLO // Generar Ubicacion de Cajer@s DIA ESPECIFICO")
        print("14. // EN DESARROLLO // Generar Ubicacion de Cajer@s SEMANAL")
        print("15. // EN DESARROLLO // Generar Ubicacion de Cajer@s SEMANAL a PDF")
        print("19. Generar PDF SEMANAL (Juntar todos los documentos Semanales en un PDF) (Ejecutar 7, 8, 11 y 15)")
        print("20. Tools")
        print("0. Salir")
        
        choice = input("Ingresa el número de tu elección: ")
        
        if choice == '1':
            run_script('registrarPersonalV1.py')
        elif choice == '12':
            run_script('nick.py')
        elif choice == '2':
            run_script('limpiarHorario.py')
        elif choice == '3':
            run_script('registrarHorarioV6.py')
        elif choice == '4':
            run_script('EntradasSalidasV5.py')
        elif choice == '5':
            run_script('ExportarWhatsappV1.py')
        elif choice == '6':
            run_script('newGraficV8.py')
        elif choice == '7':
            run_script('GenerarHojasSemanaV5.py')
        elif choice == '8':
            run_script('ExportarImprimibleV6.py')
        elif choice == '9':
            run_script('ESV2.py')
        elif choice == '19':
            run_script('GenerarHojasSemanaV5.py')
            run_script('ExportarImprimibleV6.py')
        elif choice == '20':
            run_script('Tools.py')
        elif choice == '0':
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
    clear_screen()  # Clear the screen before displaying the menu again

if __name__ == "__main__":
    menu()
