from openpyxl import load_workbook
from datetime import datetime, timedelta
import locale

# Establecer el locale a español
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')  # Para sistemas basados en Unix
# locale.setlocale(locale.LC_TIME, 'es_ES')  # Para sistemas Windows, si el anterior no funciona

# Función para obtener el lunes anterior o el lunes actual si hoy es lunes
def obtener_lunes_actual():
    hoy = datetime.today()
    if hoy.weekday() == 0:  # Si hoy es lunes
        return hoy
    else:
        return hoy - timedelta(days=hoy.weekday())  # Lunes anterior

# Función para formatear la fecha en el formato deseado (DOMINGO 20 DE OCTUBRE 2024)
def formatear_fecha(fecha):
    dias_semana = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO']
    dia_semana = dias_semana[fecha.weekday()]
    # El strftime usa el locale para traducir el nombre del mes a español
    return f"{dia_semana} {fecha.day} DE {fecha.strftime('%B').upper()} {fecha.year}"

# Ruta del archivo Excel
ruta_archivo = 'PlantillaSemanal_Exportada.xlsx'

# Cargar el archivo de Excel
wb = load_workbook(ruta_archivo)

# Obtener la fecha del lunes de la semana en curso
lunes_actual = obtener_lunes_actual()

# Iterar por las hojas del archivo Excel y escribir las fechas en cada una
for i, hoja in enumerate(wb.worksheets[:7]):  # Limitar a las primeras 7 hojas
    fecha = lunes_actual + timedelta(days=i)  # Calcular la fecha para esa hoja
    fecha_formateada = formatear_fecha(fecha)
    
    # Escribir la fecha en la celda combinada A2:H2
    hoja["A2"] = fecha_formateada

# Guardar los cambios en el archivo
wb.save(ruta_archivo)

print("Fechas actualizadas en las primeras 7 hojas.")
