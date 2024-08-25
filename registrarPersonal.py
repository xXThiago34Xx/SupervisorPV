def agregar_empleado():
    cargos = {
        "1": "Cajer@",
        "2": "Asistente de Self Checkout",
        "3": "Representante de Servicio",
        "4": "Ecommerce"
    }
    
    while True:
        # Mostrar las opciones de tipo de personal
        print("Seleccione el tipo de personal que desea ingresar de forma masiva:")
        print("1. Cajer@")
        print("2. Asistente de Self Checkout")
        print("3. Representante de Servicio")
        print("4. Ecommerce")
        print("Escriba 'x' para finalizar el programa.")
        
        # Solicitar el tipo de personal
        tipo_personal = input("Ingrese el número del tipo de personal: ")
        
        if tipo_personal.lower() == 'x':
            print("Finalizando el programa...")
            break
        
        cargo = cargos.get(tipo_personal)
        
        if cargo is None:
            print("Número de tipo de personal inválido. Inténtelo de nuevo.")
            continue
        
        while True:
            # Solicitar los apellidos
            apellidos = input("Ingrese los apellidos (o 'x' para salir): ")
            
            # Verificar si el usuario quiere salir
            if apellidos.lower() == 'x':
                break
            
            # Solicitar los nombres
            nombres = input("Ingrese los nombres: ")
            
            # Convertir apellidos y nombres a mayúsculas
            apellidos = apellidos.upper()
            nombres = nombres.upper()
            
            # Formatear los datos en el formato deseado
            linea = f"{apellidos},{nombres},{cargo}\n"
            
            # Abrir el archivo en modo de agregar y escribir la línea con codificación UTF-8
            with open("personal.txt", "a", encoding="utf-8") as archivo:
                archivo.write(linea)
            
            print("Datos agregados exitosamente.")
    
# Llamar a la función para agregar empleados
agregar_empleado()
