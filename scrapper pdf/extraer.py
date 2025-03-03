import PyPDF2
import re


def pdf_to_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            for page in reader.pages:
                text = page.extract_text()
                
                if text:
                    text = text.replace('\n', ' ')  # Elimina los saltos de línea
                    text = add_line_breaks(text)    # Añade saltos de línea antes de los nombres
                    text = remove_dates(text)       # Elimina las fechas y días de la semana
                    text = remove_manual_pattern(text)  # Elimina el patrón manualmente
                    text = add_line_breaks_for_specific_names(text)  # Añade salto de línea antes de ciertos apellidos
                    text = remove_spaces_before_names(text)  # Elimina espacios antes de apellidos
                    text = replace_specific_phrases(text)  # Reemplaza las frases específicas
                    text = remove_comas_before_enter(text)  # Elimina las comas antes de un salto de línea
                    formatted_text = format_text(text)  # Formatea la salida a formato adecuado
                    txt_file.write(formatted_text)


def replace_text_in_file(txt_path, old_text, new_text):
    with open(txt_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = content.replace(old_text, new_text)

    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(content)


def add_line_breaks(text):
    pattern = r'(?<!CFR )(\b[A-ZÁÉÍÓÚÑ]{2,}(?: [A-ZÁÉÍÓÚÑ]{2,})*, [A-ZÁÉÍÓÚÑ]{2,}(?! CFR| DESCANSO))'
    return re.sub(pattern, r'\n\1', text)


def remove_dates(text):
    # Patrón para capturar días de la semana seguidos de fechas en el formato "LUNES 03/02"
    pattern = r'\b(LUNES|MARTES|MIERCOLES|JUEVES|VIERNES|SABADO|DOMINGO) \d{2}/\d{2}'
    text = re.sub(pattern, '', text)
    
    # Eliminar fechas pegadas sin espacio, como "05/02JUEVES"
    pattern_continuo = r'(\d{2}/\d{2})(?=LUNES|MARTES|MIERCOLES|JUEVES|VIERNES|SABADO|DOMINGO)'
    return re.sub(pattern_continuo, r'\1 ', text)


def remove_manual_pattern(text):
    # Elimina patrones como "MIERCOLES  05/02 JUEVES 06/02"
    pattern_manual = r'(MIERCOLES|MARTES|LUNES|JUEVES|VIERNES|SABADO|DOMINGO) *\d{2}/\d{2} *(MIERCOLES|MARTES|LUNES|JUEVES|VIERNES|SABADO|DOMINGO)? *\d{2}/\d{2}'
    return re.sub(pattern_manual, '', text)


def add_line_breaks_for_specific_names(text):
    # Añade salto de línea antes de "GURREONERO" y "CARHUANCHO"
    pattern = r'(GURREONERO|CARHUANCHO|HUANUCO)'
    return re.sub(pattern, r'\n\1', text)


def remove_spaces_before_names(text):
    # Elimina los espacios antes de los apellidos "GURREONERO" y "CARHUANCHO"
    pattern = r' +(\b(GURREONERO|CARHUANCHO)\b)'
    return re.sub(pattern, r'\1', text)


def replace_specific_phrases(text):
    # Reemplaza las frases especificadas
    text = re.sub(r'CFR CAJERO  6X1', ',Cajer@,', text)
    text = re.sub(r'CFR CAJERO  6X1 1ER  TURNO', ',Cajer@,', text)
    text = re.sub(r'CFR CAJERO  6X1 2DO  TURNO', ',Cajer@,', text)
    text = re.sub(r'CFR CAJERO  3X4', ',Cajer@,', text)
    text = re.sub(r'CFR  ASISTENTE DE  SELF CHECK ', ',Self Checkout,', text)
    text = re.sub(r'DIA DE\s*DESCANSO', ',DESCANSO,DESCANSO', text)  # Reemplazo de "DIA DE  DESCANSO" sin importar 
    text = re.sub(',,', ',', text)
    text = re.sub(' ,', ',', text)
    text = re.sub('  ,', ',', text)
    text = re.sub(r'CFR REPRES.  DE SERVICIOS', ',RS,', text)
    text = re.sub(r'CFR  REPRESENTAN TE DE', ',RS,', text)  # Reemplazo corregido
    
    # Elimina "1ER TURNO" y "2DO TURNO" sin importar los espacios entre las palabras
    text = re.sub(r'1ER\s*TURNO', '', text)
    text = re.sub(r'2DO\s*TURNO', '', text)
    text = re.sub('DESCANSO ', 'DESCANSO', text)
    text = re.sub('DESCANSO', 'DESCANSO,', text)
    text = re.sub('DESCANSO,\n', 'DESCANSO\n', text)
    text = re.sub('DESCANSO,,', 'DESCANSO,', text)
    text = re.sub('DESCANSO,,\n', 'DESCANSO\n', text)
    
    text = re.sub(',,', ',', text)
    
    # Modificación añadida: Eliminar espacio o guion entre horas y agregar coma
    text = re.sub(r'(\d{2}:\d{2})\s*[-\s]?\s*(\d{2}:\d{2})', r'\1,\2', text)
    text = re.sub(r'(\d{2}:\d{2})\s*[-\s]?\s*(\d{2}:\d{2})', r'\1,\2', text)

    text = re.sub('  ', ' ', text)
    text = re.sub(', ,', ',', text)
    text = re.sub('DESCANSO', 'DESCANSO,', text)

    text = re.sub('DESCANSO,,', 'DESCANSO,', text)

    text = re.sub(', ', ',', text)

    return text


def remove_comas_before_enter(text):
    # Elimina las comas antes de un salto de línea (enter)
    pattern = r',\s*\n'
    return re.sub(pattern, '\n', text)


def format_text(text):
    # Se asume que el formato de la información es algo como:
    # "Empleado, Cargo, Horario Lunes, Horario Martes, ..., Horario Domingo"
    
    # Separa la información por líneas para procesarla mejor
    lines = text.split('\n')

    formatted_lines = []
    for line in lines:
        # Dividir por comas y agregar formato
        parts = line.split(',')
        if len(parts) >= 2:
            name = parts[0].strip()
            role = parts[1].strip()
            schedule = ",".join(parts[2:]).strip()

            # Crear una línea en el formato solicitado
            formatted_line = f"{name},{role},{schedule}"
            formatted_lines.append(formatted_line)

    # Unir las líneas formateadas
    return '\n'.join(formatted_lines)


# Reemplaza 'archivo.pdf' con el nombre de tu archivo PDF
pdf_to_txt('archivo.pdf', 'salida.txt')

# Ejemplo de uso para reemplazar texto
# replace_text_in_file('salida.txt', 'texto_antiguo', 'texto_nuevo')
