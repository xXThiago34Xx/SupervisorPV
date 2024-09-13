import os
import win32com.client as win32
from PyPDF2 import PdfMerger

def adjust_page_setup(sheet):
    # Ajustar configuración de página a A4, vertical, centrado
    sheet.PageSetup.PaperSize = 9  # A4
    sheet.PageSetup.Orientation = 1  # Vertical
    sheet.PageSetup.CenterHorizontally = True
    sheet.PageSetup.CenterVertically = True
    sheet.PageSetup.Zoom = False
    sheet.PageSetup.FitToPagesWide = 1
    sheet.PageSetup.FitToPagesTall = 1

def save_sheet_as_pdf(sheet, output_dir, pdf_filename):
    # Definir el área de impresión de la columna A a la Q y de la fila 1 a la 74
    sheet.PageSetup.PrintArea = "A1:Q74"
    
    # Exportar la hoja como PDF
    pdf_path = os.path.join(output_dir, pdf_filename)
    sheet.ExportAsFixedFormat(0, pdf_path)
    return pdf_path

def process_excel_to_pdf(excel_path, output_dir):
    # Inicializar la aplicación de Excel
    excel = win32.Dispatch('Excel.Application')
    workbook = excel.Workbooks.Open(excel_path)
    
    # Crear las carpetas de salida si no existen
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista para almacenar los archivos PDF individuales
    all_pdfs = []
    
    # Recorrer todas las hojas del archivo Excel
    for sheet in workbook.Sheets:
        sheet_name = sheet.Name
        adjust_page_setup(sheet)
        
        # Generar el nombre del archivo PDF basado en el nombre de la hoja
        pdf_filename = f"{sheet_name}.pdf"
        pdf_path = save_sheet_as_pdf(sheet, output_dir, pdf_filename)
        
        # Añadir el archivo PDF a la lista
        all_pdfs.append(pdf_path)
    
    # Crear un PDF combinado que contenga todas las hojas
    final_pdf_path = os.path.join(output_dir, "ES_Semanal.pdf")
    merger = PdfMerger()
    
    for pdf in all_pdfs:
        merger.append(pdf)
    
    # Escribir el PDF combinado
    merger.write(final_pdf_path)
    merger.close()
    
    # Cerrar el libro de Excel y la aplicación
    workbook.Close(False)
    excel.Quit()
    
    print(f"Proceso completado. Todos los archivos PDF se han guardado en {output_dir}")

# Definir la ruta del archivo y el directorio de salida
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_file_path = os.path.join(current_directory, "ES_Semanal.xlsx")
output_directory = os.path.join(current_directory, "ES")
os.makedirs(output_directory, exist_ok=True)

# Ejecutar el proceso
process_excel_to_pdf(excel_file_path, output_directory)
