def limpiar_archivo(archivo):
    # Abrir el archivo en modo escritura para vaciar su contenido
    with open(archivo, "w") as archivo:
        # No escribir nada, lo que vacía el archivo
        pass

def main():
    archivo = "horario.txt"
    limpiar_archivo(archivo)
    print(f"El archivo {archivo} ha sido limpiado.")

if __name__ == "__main__":
    main()
