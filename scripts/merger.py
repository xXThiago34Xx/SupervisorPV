import os
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs_intercalated(pdf1_path, pdf2_path, a, b, output_path):
    # Cargar los PDFs
    pdf1 = PdfReader(pdf1_path)
    pdf2 = PdfReader(pdf2_path)

    # Obtener el número de páginas de cada PDF
    num_pages_pdf1 = len(pdf1.pages)
    num_pages_pdf2 = len(pdf2.pages)

    # Crear el escritor de PDF para el archivo final
    pdf_writer = PdfWriter()

    # Contadores de páginas
    pdf1_index = 0
    pdf2_index = 0
    total_pages_written = 0

    # Mezclar las páginas intercalando
    while pdf1_index < num_pages_pdf1:
        # Insertar 'a' páginas del primer PDF
        for _ in range(a):
            if pdf1_index < num_pages_pdf1:
                pdf_writer.add_page(pdf1.pages[pdf1_index])
                pdf1_index += 1
                total_pages_written += 1

        # Insertar 'b' páginas del segundo PDF
        for _ in range(b):
            if pdf2_index < num_pages_pdf2:
                # Insertamos página del segundo PDF después de cada bloque de 'a' páginas
                pdf_writer.add_page(pdf2.pages[pdf2_index])
                pdf2_index += 1
                total_pages_written += 1

    # En caso de que queden páginas del segundo PDF que no se hayan agregado
    while pdf2_index < num_pages_pdf2:
        pdf_writer.add_page(pdf2.pages[pdf2_index])
        pdf2_index += 1

    # Escribir el archivo resultante
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"Archivo combinado creado en {output_path}")

if __name__ == "__main__":
    # Solicitar al usuario las rutas de los archivos y los valores de 'a' y 'b'
    pdf1_path = input("Ingrese la ruta del primer archivo PDF: ")
    pdf2_path = input("Ingrese la ruta del segundo archivo PDF: ")
    a = int(input("Ingrese el valor de 'a' (cada cuántas páginas del primer archivo insertar): "))
    b = int(input("Ingrese el valor de 'b' (cuántas páginas del segundo archivo insertar): "))
    output_path = input("Ingrese la ruta para guardar el archivo resultante: ")

    # Verificar que los archivos existan
    if not os.path.exists(pdf1_path):
        print(f"El archivo {pdf1_path} no existe.")
    elif not os.path.exists(pdf2_path):
        print(f"El archivo {pdf2_path} no existe.")
    else:
        # Llamar a la función para combinar los PDFs
        merge_pdfs_intercalated(pdf1_path, pdf2_path, a, b, output_path)
