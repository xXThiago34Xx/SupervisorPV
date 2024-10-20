from openpyxl import load_workbook
from datetime import datetime, timedelta
import locale

# Establecer el locale a español
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')  # Para sistemas basados en Unix
# locale.setlocale(locale.LC_TIME, 'es_ES')  # Para sistemas Windows, si el anterior no funciona

# Función para obtener el lunes anterior, presente o siguiente
def obtener_lunes(tipo):
    hoy = datetime.today()
    if tipo == "anterior":
        return (hoy - timedelta(days=hoy.weekday())) - timedelta(weeks=1)  # Lunes anterior
    elif tipo == "presente":
        return hoy - timedelta(days=hoy.weekday())  # Lunes actual
    elif tipo == "siguiente":
        return (hoy - timedelta(days=hoy.weekday())) + timedelta(weeks=1)  # Lunes siguiente

# Función para formatear la fecha en el formato deseado (DOMINGO 20 DE OCTUBRE 2024)
def formatear_fecha(fecha):
    dias_semana = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO']
    dia_semana = dias_semana[fecha.weekday()]
    # El strftime usa el locale para traducir el nombre del mes a español
    return f"{dia_semana} {fecha.day} DE {fecha.strftime('%B').upper()} {fecha.year}"

# Obtener las fechas de los lunes (anterior, presente y siguiente)
lunes_anterior = obtener_lunes("anterior")
lunes_presente = obtener_lunes("presente")
lunes_siguiente = obtener_lunes("siguiente")

# Mostrar opciones para que el usuario escoja
print(f"1. Lunes anterior: {formatear_fecha(lunes_anterior)}")
print(f"2. Lunes presente: {formatear_fecha(lunes_presente)}")
print(f"3. Lunes siguiente: {formatear_fecha(lunes_siguiente)}")

# Solicitar al usuario que seleccione una opción (1, 2 o 3)
opcion = input("Selecciona el lunes deseado (1, 2 o 3): ")

# Ruta del archivo Excel
ruta_archivo = 'PlantillaSemanal_Exportada.xlsx'

# Cargar el archivo de Excel
wb = load_workbook(ruta_archivo)

# Asignar el lunes seleccionado
if opcion == '1':
    lunes_seleccionado = lunes_anterior
elif opcion == '2':
    lunes_seleccionado = lunes_presente
elif opcion == '3':
    lunes_seleccionado = lunes_siguiente
else:
    raise ValueError("Opción no válida. Debe ser 1, 2 o 3.")

# Iterar por las hojas del archivo Excel y escribir las fechas en cada una
for i, hoja in enumerate(wb.worksheets[:7]):  # Limitar a las primeras 7 hojas
    fecha = lunes_seleccionado + timedelta(days=i)  # Calcular la fecha para esa hoja
    fecha_formateada = formatear_fecha(fecha)
    
    # Escribir la fecha en la celda combinada A2:H2
    hoja["A2"] = fecha_formateada

# Guardar los cambios en el archivo
wb.save(ruta_archivo)

print("Fechas actualizadas en las primeras 7 hojas.")
