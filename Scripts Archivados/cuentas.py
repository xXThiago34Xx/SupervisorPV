import re
import sys

class CalculadoraRollo:
    def __init__(self):
        self.cuentas = []
        self.cuenta_actual = None
        self.iniciar()

    def nueva_cuenta(self):
        while True:
            nombre = input("Ingresa el nombre de la cuenta (1: Depósitos Soles, 2: Depósitos Dólares, 3: Préstamos, 4: Fondos, 5: Bóveda, otro: nombre personalizado): ").strip()
            nombre_map = {
                "1": "Depósitos Soles",
                "2": "Depósitos Dólares",
                "3": "Préstamos",
                "4": "Fondos",
                "5": "Bóveda"
            }
            
            if nombre == "5":
                self.eliminar_cuenta()
                return
            elif nombre in nombre_map:
                nombre = nombre_map[nombre]
                break
            else:
                if not any(cuenta["nombre"] == nombre for cuenta in self.cuentas):
                    break
                print("Ya existe una cuenta con ese nombre. Intenta con otro nombre.")

        cuenta = {"nombre": nombre, "operaciones": [], "total": 0}
        self.cuentas.append(cuenta)
        self.cuenta_actual = cuenta
        print(f"Cuenta '{nombre}' creada y seleccionada.")

    def eliminar_cuenta(self):
        if not self.cuentas:
            print("No hay cuentas disponibles para eliminar.\n")
            return

        print("\nSelecciona la cuenta que deseas eliminar:")
        for i, cuenta in enumerate(self.cuentas):
            nombre = cuenta["nombre"]
            total = cuenta["total"]
            print(f"{i + 1}: {nombre} (Total: {total})")

        seleccion = input("Ingresa el número de la cuenta a eliminar (o '0' para cancelar): ").strip()
        try:
            index = int(seleccion) - 1
            if index == -1:
                print("Selección cancelada.\n")
                return
            if 0 <= index < len(self.cuentas):
                cuenta_eliminar = self.cuentas.pop(index)
                if self.cuenta_actual == cuenta_eliminar:
                    self.cuenta_actual = None
                print(f"Cuenta '{cuenta_eliminar['nombre']}' eliminada.\n")
            else:
                print("Número de cuenta no válido.\n")
        except ValueError:
            print("Selección no válida. Debe ingresar un número.\n")

    def procesar_entrada(self, entrada):
        entrada = entrada.strip()
        if entrada == ".....":
            self.cerrar_programa()
        elif entrada == "..":
            self.nueva_cuenta()
        elif entrada == "...":
            self.mostrar_totales_finales()
            self.reiniciar_o_continuar()
        elif entrada == "*****":
            self.mostrar_detalle_operaciones()
        elif entrada == ".":
            self.editar_ultima_operacion()
        elif entrada == "***":
            self.seleccionar_cuenta()
        elif entrada == "**":
            self.eliminar_cuenta_y_reiniciar()
        else:
            self.evaluar_operacion(entrada)

    def mostrar_detalle_operaciones(self):
        if not self.cuentas:
            print("No hay cuentas disponibles.\n")
            return

        print("\nDetalle de operaciones de todas las cuentas:")
        for cuenta in self.cuentas:
            nombre = cuenta["nombre"]
            total = cuenta["total"]
            print(f"\nCuenta: {nombre} (Total: {total})")
            for operacion in cuenta["operaciones"]:
                print(f"  {operacion}")

    def seleccionar_cuenta(self):
        if not self.cuentas:
            print("No hay cuentas disponibles para seleccionar.\n")
            return

        print("\nSelecciona la cuenta a la que deseas continuar operando:")
        for i, cuenta in enumerate(self.cuentas):
            nombre = cuenta["nombre"]
            total = cuenta["total"]
            print(f"{i + 1}: {nombre} (Total: {total})")

        seleccion = input("Ingresa el número de la cuenta (o '0' para cancelar): ").strip()
        try:
            index = int(seleccion) - 1
            if index == -1:
                print("Selección cancelada.\n")
                return
            if 0 <= index < len(self.cuentas):
                self.cuenta_actual = self.cuentas[index]
                print(f"Ahora estás operando en la cuenta '{self.cuenta_actual['nombre']}'.\n")
            else:
                print("Número de cuenta no válido.\n")
        except ValueError:
            print("Selección no válida. Debe ingresar un número.\n")

    def eliminar_cuenta_y_reiniciar(self):
        if not self.cuentas:
            print("No hay cuentas disponibles para eliminar.\n")
            return

        print("\nSelecciona la cuenta que deseas eliminar:")
        for i, cuenta in enumerate(self.cuentas):
            nombre = cuenta["nombre"]
            total = cuenta["total"]
            print(f"{i + 1}: {nombre} (Total: {total})")

        seleccion = input("Ingresa el número de la cuenta a eliminar (o '0' para cancelar): ").strip()
        try:
            index = int(seleccion) - 1
            if index == -1:
                print("Selección cancelada.\n")
                return
            if 0 <= index < len(self.cuentas):
                cuenta_eliminar = self.cuentas.pop(index)
                if self.cuenta_actual == cuenta_eliminar:
                    self.cuenta_actual = None
                print(f"Cuenta '{cuenta_eliminar['nombre']}' eliminada.\n")
            else:
                print("Número de cuenta no válido.\n")
        except ValueError:
            print("Selección no válida. Debe ingresar un número.\n")

        decision = input("\n¿Deseas crear una nueva cuenta (1: Sí, 0: No)? ").strip()
        if decision == "1":
            self.nueva_cuenta()
        elif decision == "0":
            self.seleccionar_cuenta()
        else:
            print("Opción no válida. Continuando con la cuenta actual.")

    def evaluar_operacion(self, entrada):
        entrada = entrada.replace(" ", "")
        if re.match(r'^[+-]?\d+(\.\d+)?$', entrada):
            valor = float(entrada)
            self.cuenta_actual["total"] += valor
            self.cuenta_actual["operaciones"].append(f"{entrada} = {valor}")
            print(f"{entrada} = {valor}")
        else:
            try:
                resultado = eval(entrada)
                self.cuenta_actual["total"] += resultado
                self.cuenta_actual["operaciones"].append(f"{entrada} = {resultado}")
                print(f"{entrada} = {resultado}")
            except Exception as e:
                print(f"Error en la operación: {e}")

        self.mostrar_total_actual()  # Mostrar el total acumulado después de cada operación

    def editar_ultima_operacion(self):
        if not self.cuenta_actual["operaciones"]:
            print("No hay operaciones para editar.\n")
            return

        ultima_operacion = self.cuenta_actual["operaciones"].pop()
        operacion, resultado_str = ultima_operacion.split(" = ")
        resultado_anterior = float(resultado_str)
        self.cuenta_actual["total"] -= resultado_anterior  # Revertir la última operación

        print(f"Editando la última operación: {operacion}")
        nueva_operacion = input("Ingresa la corrección: ")

        try:
            nuevo_resultado = eval(nueva_operacion)
            self.cuenta_actual["total"] += nuevo_resultado
            self.cuenta_actual["operaciones"].append(f"{nueva_operacion} = {nuevo_resultado}")
            print(f"{nueva_operacion} = {nuevo_resultado}")
        except Exception as e:
            print(f"Error en la corrección: {e}")

        self.mostrar_total_actual()

    def mostrar_total_actual(self):
        total = self.cuenta_actual["total"]
        nombre = self.cuenta_actual["nombre"]
        print(f"Total actual de '{nombre}': {total}\n")

    def mostrar_totales_finales(self):
        print("\nResumen de todas las cuentas:")
        for cuenta in self.cuentas:
            nombre = cuenta["nombre"]
            total = cuenta["total"]
            print(f"{nombre}: {total}")

    def reiniciar_o_continuar(self):
        decision = input("\n¿Deseas borrar todas las cuentas y empezar de nuevo (1: Sí, 0: No)? ").strip()
        if decision == "1":
            self.cuentas = []
            self.cuenta_actual = None
        elif decision != "0":
            print("Opción no válida. Manteniendo las cuentas actuales.")
        self.nueva_cuenta()

    def cerrar_programa(self):
        print("Cerrando el programa...")
        sys.exit()

    def iniciar(self):
        print("Calculadora con Rollo de Impresión. Inserta operaciones línea por línea.")
        print("Usa '.' para editar la última operación.")
        print("Usa '..' para cerrar la cuenta actual y empezar una nueva.")
        print("Usa '...' para mostrar el total de todas las cuentas y decidir si deseas continuar o reiniciar.")
        print("Usa '***' para seleccionar y continuar operando en una cuenta existente.")
        print("Usa '*****' para mostrar el detalle de todas las operaciones de todas las cuentas.")
        print("Usa '**' para eliminar una cuenta existente y decidir si crear una nueva o continuar con otra cuenta.")
        print("Usa '.....' para cerrar el programa.")
        
        self.nueva_cuenta()
        
        while True:
            entrada = input("\nIngresa una operación o comando: ")
            self.procesar_entrada(entrada)

if __name__ == "__main__":
    CalculadoraRollo()
