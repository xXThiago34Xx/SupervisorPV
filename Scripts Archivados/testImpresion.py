import os
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def crear_pdf(nombre_archivo, texto):
    # Crear un canvas para el PDF
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    ancho, alto = letter
    
    # Escribir texto en el PDF
    c.drawString(100, alto - 100, texto)
    
    # Finalizar el PDF
    c.save()

def imprimir_pdf(ruta_pdf):
    # Usar el comando print asociado con la aplicación predeterminada en Windows
    try:
        # Ejecuta el comando para imprimir utilizando la aplicación predeterminada del sistema
        subprocess.run(['cmd', '/c', f'start /wait "" "{ruta_pdf}" /p'], check=True)
    except Exception as e:
        print(f"Error al intentar imprimir el PDF: {e}")

if __name__ == "__main__":
    # Crear el PDF con el contenido deseado
    nombre_archivo_pdf = "Exportado2.pdf"
    contenido = "Este es el contenido del PDF que se va a imprimir."
    crear_pdf(nombre_archivo_pdf, contenido)
    
    # Mandar a imprimir el PDF
    imprimir_pdf(nombre_archivo_pdf)
