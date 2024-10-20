def agregar_empleado():
    cargos = {
        "1": "Cajer@",
        "2": "Self Checkout",
        "3": "RS",
        "4": "Ecommerce",
        "5": "Supervisor(@)"  # Nueva opción añadida
    }
    
    while True:
        # Mostrar las opciones de tipo de personal
        print("Seleccione el tipo de personal que desea ingresar de forma masiva:")
        print("1. Cajer@")
        print("2. Self Checkout")
        print("3. RS")
        print("4. Ecommerce")
        print("5. Supervisor(@)")  # Nueva opción añadida
        print("Escriba '0' para finalizar el programa.")
        
        # Solicitar el tipo de personal
        tipo_personal = input("Ingrese el número del tipo de personal: ")
        
        if tipo_personal == '0':
            print("Finalizando el programa...")
            break
        
        cargo = cargos.get(tipo_personal)
        
        if cargo is None:
            print("Número de tipo de personal inválido. Inténtelo de nuevo.")
            continue
        
        while True:
            # Solicitar los apellidos
            apellidos = input("Ingrese los apellidos (o '0' para salir): ")
            
            # Verificar si el usuario quiere salir
            if apellidos == '0':
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
