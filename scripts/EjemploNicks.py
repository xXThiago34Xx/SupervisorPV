# Función que obtiene el nickname del archivo nicks.txt
def getNick(nombre_completo):
    try:
        with open("nicks.txt", "r", encoding="utf-8") as archivo_nicks:
            for linea in archivo_nicks:
                # Dividir la línea del archivo en columnas
                nombre_archivo, tipo_personal, apellido_registrado, nickname = linea.strip().split(",")

                # Verificar si el nombre completo coincide con el nombre en el archivo
                if nombre_completo == nombre_archivo:
                    return nickname

        return f"Nickname no encontrado para {nombre_completo}"

    except FileNotFoundError:
        return "Error: El archivo 'nicks.txt' no fue encontrado."

# Función que obtiene el apellido registrado en la penúltima columna de nicks.txt
def getApNick(nombre_completo):
    try:
        with open("nicks.txt", "r", encoding="utf-8") as archivo_nicks:
            for linea in archivo_nicks:
                # Dividir la línea del archivo en columnas
                nombre_archivo, tipo_personal, apellido_registrado, nickname = linea.strip().split(",")

                # Verificar si el nombre completo coincide con el nombre en el archivo
                if nombre_completo == nombre_archivo:
                    return apellido_registrado

        return f"Apellido registrado no encontrado para {nombre_completo}"

    except FileNotFoundError:
        return "Error: El archivo 'nicks.txt' no fue encontrado."


# Nombre completo tal como aparece en el archivo nicks.txt
nombres = "GUSTAVO"
apellidos = "TORRES"

# Juntar los nombres y apellidos en una sola cadena
nombre_completo = f"{nombres} {apellidos}"

# Llamar a las funciones
print(getNick(nombre_completo) + " " + getApNick(nombre_completo))

