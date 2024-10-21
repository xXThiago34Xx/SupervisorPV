# Definir el rango de horas
start_hour = 6
end_hour = 24

# Inicializar el contador
counter = 1

# Iterar sobre el rango de horas
for hour in range(start_hour, end_hour + 1):
    for minute in [0, 15, 30, 45]:
        # Formatear la hora y los minutos
        formatted_time = f"{hour:02d}:{minute:02d}"
        # Imprimir el número y la hora
        print(f"{counter} - {formatted_time}")
        # Incrementar el contador
        counter += 1
# Esperar que el usuario presione Enter para finalizar
input("Presione Enter para continuar...")