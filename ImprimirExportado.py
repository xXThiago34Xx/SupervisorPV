import os
import time
import pyautogui

def abrir_pdf(ruta_pdf):
    # Abre el archivo PDF usando la aplicación predeterminada del sistema
    try:
        os.startfile(ruta_pdf)
        print(f"Archivo {ruta_pdf} abierto.")
    except Exception as e:
        print(f"Error al abrir el PDF: {e}")

def imprimir_pdf():
    # Esperar unos segundos para que el PDF se abra
    time.sleep(5)
    
    # Enviar la combinación de teclas Ctrl + P para abrir el diálogo de impresión
    pyautogui.hotkey('ctrl', 'p')
    print("Diálogo de impresión abierto.")
    
    # Esperar 2 segundos para que se cargue el diálogo de impresión
    time.sleep(2)
    
    # Presionar ENTER para imprimir
    pyautogui.press('enter')
    print("Imprimiendo...")

if __name__ == "__main__":
    nombre_archivo_pdf = "Exportado.pdf"
    
    # Abrir el archivo PDF
    abrir_pdf(nombre_archivo_pdf)
    
    # Enviar comandos para imprimir el PDF
    imprimir_pdf()
