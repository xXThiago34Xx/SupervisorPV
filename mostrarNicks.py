# Función que obtiene el nickname del archivo nicks.txt
def getNick(nombre_completo):
    primer_nombre = lambda nombre_completo: nombre_completo.split()[0] if nombre_completo.split() else None
    try:
        with open("nicks.txt", "r", encoding="utf-8") as archivo_nicks:
            for linea in archivo_nicks:
                # Dividir la línea del archivo en columnas
                nombre_archivo, tipo_personal, apellido_registrado, nickname = linea.strip().split(",")

                # Verificar si el nombre completo coincide con el nombre en el archivo
                if nombre_completo == nombre_archivo:
                    return nickname

        return primer_nombre(nombre_completo)

    except FileNotFoundError:
        return "Error: El archivo 'nicks.txt' no fue encontrado."

# Función para leer el archivo personal.txt y mostrar los nicks de cada persona
def mostrar_nicks():
    try:
        # Abrir el archivo personal.txt
        with open("personal.txt", "r", encoding="utf-8") as archivo_personal:
            for linea in archivo_personal:
                # Dividir la línea en columnas (asumiendo formato: apellido, nombre, cargo)
                apellidos, nombres, cargo = linea.strip().split(",")
                
                # Formar el nombre completo
                nombre_completo = f"{nombres} {apellidos}"
                
                # Obtener el nickname correspondiente desde el archivo nicks.txt
                nick = getNick(nombre_completo)
                
                # Mostrar el nombre completo junto con su nickname
                print(f"{nombre_completo}: {nick}")

    except FileNotFoundError:
        print("Error: El archivo 'personal.txt' no fue encontrado.")

def getApNick(nombre_completo):
    try:
        with open("nicks.txt", "r", encoding="utf-8") as archivo_nicks:
            for linea in archivo_nicks:
                # Dividir la línea del archivo en columnas
                nombre_archivo, tipo_personal, apellido_registrado, nickname = linea.strip().split(",")

                # Verificar si el nombre completo coincide con el nombre en el archivo
                if nombre_completo == nombre_archivo:
                    return apellido_registrado

        return f"ERROR NR"

    except FileNotFoundError:
        return "Error: El archivo 'nicks.txt' no fue encontrado."
    
def mostrar_APS():
    try:
        # Abrir el archivo personal.txt
        with open("personal.txt", "r", encoding="utf-8") as archivo_personal:
            for linea in archivo_personal:
                # Dividir la línea en columnas (asumiendo formato: apellido, nombre, cargo)
                apellidos, nombres, cargo = linea.strip().split(",")
                
                # Formar el nombre completo
                nombre_completo = f"{nombres} {apellidos}"
                
                # Obtener el nickname correspondiente desde el archivo nicks.txt
                ap = getApNick(nombre_completo)
                
                # Mostrar el nombre completo junto con su nickname
                print(f"{nombre_completo}: {ap}")
    except FileNotFoundError:
        return "Error: El archivo 'nicks.txt' no fue encontrado."
# Llamar a la función para mostrar los nicks
if __name__ == "__main__":
    mostrar_nicks()
    mostrar_APS()