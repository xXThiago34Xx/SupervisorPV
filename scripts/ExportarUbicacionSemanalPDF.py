import os
import win32com.client as win32
from PyPDF2 import PdfMerger

def process_excel_to_pdf(excel_path, output_dir):
    # Inicializar la aplicación de Excel
    excel = win32.Dispatch('Excel.Application')
    workbook = excel.Workbooks.Open(excel_path)
    
    # Crear las carpetas de salida si no existen
    diario_folder = os.path.join(output_dir, 'diario')
    os.makedirs(diario_folder, exist_ok=True)
    
    # Lista para almacenar los archivos PDF individuales
    all_pdfs = []
    
    # Días de la semana para nombrar los PDFs
    days_of_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    
    # Recorrer todas las hojas del archivo Excel
    for i, sheet in enumerate(workbook.Sheets):
        sheet_name = sheet.Name
        adjust_page_setup(sheet)
        
        # Generar el nombre del archivo PDF basado en el día de la semana
        if i < 7:
            pdf_filename = f"{days_of_week[i]}.pdf"
        else:
            # En caso de que haya más hojas de las necesarias
            pdf_filename = f"extra{i-6}.pdf"
        
        pdf_path = save_sheet_as_pdf(sheet, diario_folder, pdf_filename)
        
        # Añadir el archivo PDF a la lista
        all_pdfs.append(pdf_path)
    
    # Crear un PDF combinado que contenga todas las hojas
    final_pdf_path = os.path.join(output_dir, "consolidado.pdf")
    combine_pdfs(all_pdfs, final_pdf_path)
    
    # Cerrar el libro de Excel y la aplicación
    workbook.Close(False)
    excel.Quit()
    
    print(f"Proceso completado. Todos los archivos PDF se han guardado en {output_dir}")

def adjust_page_setup(sheet):
    # Ajustar la configuración de página: centrado horizontal y vertical
    sheet.PageSetup.Zoom = False  # Desactivar el zoom para usar Ajustar a una página
    sheet.PageSetup.FitToPagesWide = 1
    sheet.PageSetup.FitToPagesTall = False
    sheet.PageSetup.PrintArea = "A1:H55"  # Seleccionar el área de impresión
    sheet.PageSetup.CenterHorizontally = True  # Centrar horizontalmente
    sheet.PageSetup.CenterVertically = True  # Centrar verticalmente

def save_sheet_as_pdf(sheet, output_dir, pdf_filename):
    # Guardar la hoja como PDF
    pdf_path = os.path.join(output_dir, pdf_filename)
    sheet.ExportAsFixedFormat(0, pdf_path)  # 0 para formato PDF
    return pdf_path

def combine_pdfs(pdf_files, output_pdf):
    # Combinar múltiples PDFs en un solo archivo
    merger = PdfMerger()
    
    for pdf in pdf_files:
        merger.append(pdf)
    
    # Escribir el PDF combinado
    with open(output_pdf, 'wb') as f_out:
        merger.write(f_out)

# Ruta del archivo Excel y carpeta de exportación
current_dir = os.path.dirname(os.path.abspath(__file__))  # Carpeta actual donde está el script
excel_file = os.path.join(current_dir, 'PlantillaSemanal_Exportada.xlsx')
output_folder = os.path.join(current_dir, 'Ubicaciones')

# Procesar el archivo Excel y exportar a PDFs
process_excel_to_pdf(excel_file, output_folder)
