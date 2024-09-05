import openpyxl
from openpyxl.utils.exceptions import InvalidFileException

def reparar_excel(archivo_entrada, archivo_salida):
    try:
        # Intenta abrir el archivo Excel de entrada
        wb = openpyxl.load_workbook(archivo_entrada)
        
        # Guarda el contenido en un nuevo archivo
        wb.save(archivo_salida)
        
        print(f"Archivo reparado exitosamente y guardado como {archivo_salida}.")
    
    except InvalidFileException:
        print("Error: El archivo de entrada no es un archivo Excel válido.")
    
    except Exception as e:
        print(f"Se produjo un error al intentar reparar el archivo: {e}")

if __name__ == "__main__":
    archivo_entrada = "Horario_Semana_Completo.xlsx"  # Nombre del archivo Excel corrupto
    archivo_salida = "Horario_Semana_Completo_Reparado.xlsx"   # Nombre del archivo reparado
    reparar_excel(archivo_entrada, archivo_salida)
