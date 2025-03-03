# Diccionario de reemplazo: vocales con tilde -> vocales sin tilde en mayúscula
reemplazos = {
    'á': 'A',
    'é': 'E',
    'í': 'I',
    'ó': 'O',
    'ú': 'U',
    'Á': 'A',
    'É': 'E',
    'Í': 'I',
    'Ó': 'O',
    'Ú': 'U'
}

# Abrir y leer el contenido del archivo
with open('horario.txt', 'r', encoding='utf-8') as archivo:
    contenido = archivo.read()

# Reemplazar las vocales con tilde
for vocal_con_tilde, vocal_sin_tilde_mayus in reemplazos.items():
    contenido = contenido.replace(vocal_con_tilde, vocal_sin_tilde_mayus)

# Guardar el contenido modificado en el mismo archivo
with open('horario.txt', 'w', encoding='utf-8') as archivo:
    archivo.write(contenido)

print("Reemplazo de vocales con tilde completado.")
