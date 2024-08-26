import os
import win32com.client as win32
import pandas as pd

def configurar_hoja_para_pdf(sheet, orientacion='Vertical'):
    # Configurar márgenes y ajustar todo a una página
    sheet.PageSetup.Zoom = False
    sheet.PageSetup.FitToPagesWide = 1
    sheet.PageSetup.FitToPagesTall = 1
    
    # Configurar orientación de la página
    if orientacion.lower() == 'horizontal':
        sheet.PageSetup.Orientation = 2  # xlLandscape
    else:
        sheet.PageSetup.Orientation = 1  # xlPortrait
    
    # Configurar centrado
    sheet.PageSetup.CenterHorizontally = True
    sheet.PageSetup.CenterVertically = True
    
    # Configurar todos los bordes en la selección
    sheet.UsedRange.Borders.Weight = 2  # xlThin
    
    # Configurar área de impresión para incluir la selección actual
    sheet.PageSetup.PrintArea = sheet.UsedRange.Address

def exportar_hoja_como_pdf(excel, sheet, output_dir, filename, orientacion='Vertical'):
    configurar_hoja_para_pdf(sheet, orientacion)
    pdf_path = os.path.join(output_dir, filename)
    sheet.ExportAsFixedFormat(0, pdf_path)  # xlTypePDF = 0

def procesar_excel_y_exportar_pdf(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    excel = win32.Dispatch('Excel.Application')
    excel.Visible = False
    workbook = excel.Workbooks.Open(input_file)

    for sheet in workbook.Sheets:
        nombre_hoja = sheet.Name.lower()
        orientacion = 'Horizontal' if 'cajer@' in nombre_hoja else 'Vertical'
        pdf_filename = f"{sheet.Name}.pdf"
        exportar_hoja_como_pdf(excel, sheet, output_dir, pdf_filename, orientacion)
    
    workbook.Close(SaveChanges=False)
    excel.Quit()

def unir_pdfs(pdf_files, output_pdf):
    from PyPDF2 import PdfMerger
    
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    
    with open(output_pdf, 'wb') as output_file:
        merger.write(output_file)

def main():
    input_file = input("Ingrese la ruta del archivo Excel generado por newGrafic.py: ").strip()
    output_dir = "pdf_exportados"
    
    procesar_excel_y_exportar_pdf(input_file, output_dir)
    
    # Unir todos los PDFs generados
    pdf_files = [os.path.join(output_dir, pdf) for pdf in os.listdir(output_dir) if pdf.endswith('.pdf')]
    output_pdf = os.path.join(output_dir, "documento_final.pdf")
    unir_pdfs(pdf_files, output_pdf)
    
    print(f"Todos los PDFs han sido exportados y unidos en: {output_pdf}")

if __name__ == "__main__":
    main()
