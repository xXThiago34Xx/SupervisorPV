import win32com.client as win32
import os
from PyPDF2 import PdfMerger

def adjust_column_width(sheet):
    sheet.Columns(1).AutoFit()  # Ajusta el ancho de la primera columna

def select_range(sheet):
    last_column = sheet.Cells(1, sheet.Columns.Count).End(win32.constants.xlToLeft).Column
    last_row = 74  # Se seleccionan las primeras 74 filas
    sheet.Range(sheet.Cells(1, 1), sheet.Cells(last_row, last_column)).Select()

def set_page_orientation(sheet, sheet_name):
    if "Cajer@" in sheet_name:
        sheet.PageSetup.Orientation = win32.constants.xlLandscape  # Horizontal
    else:
        sheet.PageSetup.Orientation = win32.constants.xlPortrait  # Vertical

def save_sheet_as_pdf(sheet, output_dir, pdf_filename):
    sheet.PageSetup.PaperSize = win32.constants.xlPaperA4  # Tamaño A4
    sheet.PageSetup.Zoom = False  # Desactiva el ajuste por zoom
    sheet.PageSetup.FitToPagesWide = 1  # Ajusta a una página de ancho
    sheet.PageSetup.FitToPagesTall = False  # No ajustar a altura de página

    pdf_path = os.path.join(output_dir, pdf_filename)
    sheet.ExportAsFixedFormat(0, pdf_path)
    return pdf_path

def process_excel_to_pdf(excel_path, output_dir):
    excel = win32.Dispatch('Excel.Application')
    workbook = excel.Workbooks.Open(excel_path)
    
    all_pdfs = []
    
    for sheet in workbook.Sheets:
        if sheet.UsedRange.Count > 1:  # Omitir hojas sin contenido
            sheet_name = sheet.Name
            adjust_column_width(sheet)  # Ajusta el ancho de la primera columna
            select_range(sheet)  # Selecciona el rango
            set_page_orientation(sheet, sheet_name)  # Establece la orientación de la página
            
            pdf_filename = f"{sheet_name}.pdf"
            pdf_path = save_sheet_as_pdf(sheet, output_dir, pdf_filename)
            all_pdfs.append(pdf_path)

    # Combinar todos los PDFs en uno solo
    final_pdf_path = os.path.join(output_dir, "combined_output.pdf")
    merger = PdfMerger()
    
    for pdf in all_pdfs:
        merger.append(pdf)
    
    merger.write(final_pdf_path)
    merger.close()
    
    workbook.Close(False)
    excel.Quit()
    
    print(f"Proceso completado. Todos los archivos PDF se han guardado en {output_dir}")

# Definir la ruta del archivo y directorio de salida
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_file_path = os.path.join(current_directory, "Horario_Semana_Completo.xlsx")
output_directory = os.path.join(current_directory, "output_pdfs")
os.makedirs(output_directory, exist_ok=True)

# Ejecutar el proceso
process_excel_to_pdf(excel_file_path, output_directory)
