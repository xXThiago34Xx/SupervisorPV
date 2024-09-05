import win32com.client as win32
import os
from PyPDF2 import PdfMerger

def adjust_column_width(sheet):
    sheet.Columns(1).AutoFit()  # Ajusta el ancho de la primera columna

def set_page_orientation(sheet, sheet_name):
    if "Cajer@" in sheet_name:
        sheet.PageSetup.Orientation = 2  # Horizontal
    else:
        sheet.PageSetup.Orientation = 1  # Vertical

def save_sheet_as_pdf(sheet, output_dir, pdf_filename):
    # Ajustar el tamaño de la página a A4 y el rango de impresión
    sheet.PageSetup.PaperSize = 9  # Tamaño A4
    sheet.PageSetup.Zoom = False  # Desactiva el ajuste por zoom
    sheet.PageSetup.FitToPagesWide = 1  # Ajusta a una página de ancho
    sheet.PageSetup.FitToPagesTall = 1  # Ajustar a altura de página

    # Ajustar el rango de impresión
    last_column = sheet.Cells(1, sheet.Columns.Count).End(-4159).Column  # -4159 es el valor de xlToLeft
    last_row = min(sheet.Cells(sheet.Rows.Count, 1).End(-4162).Row, 74)  # -4162 es el valor de xlUp
    sheet.PageSetup.PrintArea = sheet.Range(sheet.Cells(1, 1), sheet.Cells(last_row, last_column)).Address

    pdf_path = os.path.join(output_dir, pdf_filename)
    sheet.ExportAsFixedFormat(0, pdf_path)
    return pdf_path

def process_excel_to_pdf(excel_path, output_dir):
    excel = win32.Dispatch('Excel.Application')
    workbook = excel.Workbooks.Open(excel_path)
    
    all_pdfs = []
    day_pdfs = {}
    
    # Crear carpetas para los PDFs
    individual_folder = os.path.join(output_dir, "Individuales")
    days_folder = os.path.join(output_dir, "Dias")
    combined_folder = os.path.join(output_dir, "Combinado")
    
    os.makedirs(individual_folder, exist_ok=True)
    os.makedirs(days_folder, exist_ok=True)
    os.makedirs(combined_folder, exist_ok=True)
    
    for sheet in workbook.Sheets:
        if sheet.UsedRange.Count > 1:  # Omitir hojas sin contenido
            sheet_name = sheet.Name
            adjust_column_width(sheet)  # Ajusta el ancho de la primera columna
            set_page_orientation(sheet, sheet_name)  # Establece la orientación de la página
            
            # Guardar el PDF individual
            pdf_filename = f"{sheet_name}.pdf"
            pdf_path = save_sheet_as_pdf(sheet, individual_folder, pdf_filename)
            all_pdfs.append(pdf_path)
            
            # Organizar los PDFs por día
            day_name = sheet_name.split()[0]  # Suponiendo que el nombre del día es la primera parte del nombre de la hoja
            if day_name not in day_pdfs:
                day_pdfs[day_name] = []
            day_pdfs[day_name].append(pdf_path)
    
    # Crear PDFs por día (5 hojas por PDF)
    for day_name, pdfs in day_pdfs.items():
        day_pdf_path = os.path.join(days_folder, f"{day_name}.pdf")
        merger = PdfMerger()
        
        for pdf in pdfs:
            merger.append(pdf)
        
        merger.write(day_pdf_path)
        merger.close()
    
    # Combinar todos los PDFs en uno solo
    final_pdf_path = os.path.join(combined_folder, "combined_output.pdf")
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
output_directory = os.path.join(current_directory, "Exportados")
os.makedirs(output_directory, exist_ok=True)

# Ejecutar el proceso
process_excel_to_pdf(excel_file_path, output_directory)
