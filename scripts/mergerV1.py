import os
from PyPDF2 import PdfReader, PdfWriter

# Días de la semana para la búsqueda de archivos
dias_de_la_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def merge_pdfs_from_folders(folder1, folder2, output_file):
    pdf_writer = PdfWriter()

    # Recorrer los días de la semana
    for dia in dias_de_la_semana:
        # Encontrar el archivo del día en la primera carpeta
        pdf1_path = find_pdf_with_day(folder1, dia)
        if pdf1_path:
            # Leer el PDF de la primera carpeta
            pdf1 = PdfReader(pdf1_path)
            # Agregar las páginas al archivo de salida
            for page in pdf1.pages:
                pdf_writer.add_page(page)

        # Encontrar el archivo del día en la segunda carpeta
        pdf2_path = find_pdf_with_day(folder2, dia)
        if pdf2_path:
            # Leer el PDF de la segunda carpeta
            pdf2 = PdfReader(pdf2_path)
            # Agregar las páginas al archivo de salida
            for page in pdf2.pages:
                pdf_writer.add_page(page)

    # Escribir el archivo combinado
    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"PDF combinado guardado como {output_file}")

def find_pdf_with_day(folder, day):
    # Buscar un archivo PDF que contenga el nombre del día
    for filename in os.listdir(folder):
        if day.lower() in filename.lower() and filename.endswith(".pdf"):
            return os.path.join(folder, filename)
    return None

if __name__ == "__main__":
    folder1 = "./ES"
    folder2 = "./Exportados/Dias"
    output_file = "./Exportado.pdf"

    merge_pdfs_from_folders(folder1, folder2, output_file)
