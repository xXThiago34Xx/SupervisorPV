def generar_nicknames():
    try:
        # Leer el archivo personal.txt
        with open("personal.txt", "r", encoding="utf-8") as archivo_personal:
            personal_data = archivo_personal.readlines()

        # Leer el archivo nicks.txt si ya existe, para evitar duplicados
        try:
            with open("nicks.txt", "r", encoding="utf-8") as archivo_nicks:
                nicks_data = archivo_nicks.readlines()
        except FileNotFoundError:
            nicks_data = []

        # Crear un conjunto de nombres completos ya registrados en nicks.txt
        nombres_completos_registrados = set()
        for linea in nicks_data:
            nombre_completo = linea.split(",")[0]  # Primera columna es el nombre completo
            nombres_completos_registrados.add(nombre_completo)

        # Abrir nicks.txt en modo de agregar
        with open("nicks.txt", "a", encoding="utf-8") as archivo_nicks:
            for linea in personal_data:
                # Separar la línea en columnas (apellido, nombre, tipo de personal)
                apellidos, nombres, tipo_personal = linea.strip().split(",")

                # Procesar el primer apellido (todos menos el último elemento)
                apellidos_separados = apellidos.split()
                primer_apellido = " ".join(apellidos_separados[:-1])

                # Crear el nombre completo
                nombre_completo = f"{nombres} {apellidos}"

                # Verificar si la persona ya está registrada
                if nombre_completo in nombres_completos_registrados:
                    print(f"{nombre_completo} ya está registrado. Saltando...")
                    continue  # Si está registrado, pasamos a la siguiente persona

                # Dividir nombres por espacios para permitir la elección
                nombres_separados = nombres.split()
                
                # Mostrar opciones al usuario para elegir el nombre
                print(f"Apellidos: {apellidos}")
                print(f"Nombres disponibles: {nombres_separados}")
                print("Escriba el número del nombre que desea usar o escriba un nombre personalizado.")
                
                # Mostrar opciones numeradas para los nombres
                for i, nombre in enumerate(nombres_separados, start=1):
                    print(f"{i}. {nombre}")
                
                seleccion = input("Seleccione un nombre (número o personalizado): ")
                
                # Verificar si el usuario ingresó un número válido
                if seleccion.isdigit() and 1 <= int(seleccion) <= len(nombres_separados):
                    nombre_seleccionado = nombres_separados[int(seleccion) - 1]
                else:
                    # Usar el nombre personalizado si no seleccionó un número válido
                    nombre_seleccionado = seleccion.strip()
                
                # Guardar la información en nicks.txt
                archivo_nicks.write(f"{nombre_completo},{tipo_personal},{primer_apellido},{nombre_seleccionado}\n")
                print(f"Nickname generado: {nombre_completo},{tipo_personal},{primer_apellido},{nombre_seleccionado}")
    
    except FileNotFoundError:
        print("Error: El archivo 'personal.txt' no fue encontrado.")

# Llamar a la función para generar los nicknames
generar_nicknames()
