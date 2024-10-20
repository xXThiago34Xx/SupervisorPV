import re
import sys
import os

class CalculadoraRollo:
    def __init__(self):
        self.cuentas = []
        self.cuenta_actual = None
        self.iniciar()

    def limpiar_pantalla(self):
        # Limpia la pantalla según el sistema operativo
        os.system('cls' if os.name == 'nt' else 'clear')

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
        self.operar_en_cuenta()  # Comienza a operar en la nueva cuenta

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
                self.operar_en_cuenta()  # Comienza a operar en la cuenta seleccionada
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
            print("Volviendo al menú principal.")
        else:
            print("Opción no válida. Volviendo al menú principal.")

    def evaluar_operacion(self, entrada):
        entrada = entrada.replace(" ", "")
        if re.match(r'^[+-]?\d+(\.\d+)?$', entrada):
            valor = float(entrada)
            if valor >= 0:
                operacion = f"+{valor:.1f}"
            else:
                operacion = f"{valor:.1f}"
            self.cuenta_actual["total"] += valor
            self.cuenta_actual["operaciones"].append(operacion)
            self.limpiar_pantalla()
            self.mostrar_operaciones()
        else:
            try:
                resultado = eval(entrada)
                if resultado >= 0:
                    operacion = f"+{resultado:.1f}"
                else:
                    operacion = f"{resultado:.1f}"
                self.cuenta_actual["total"] += resultado
                self.cuenta_actual["operaciones"].append(f"{entrada} = {operacion}")
                self.limpiar_pantalla()
                self.mostrar_operaciones()
            except Exception as e:
                print(f"Error en la operación: {e}")

        self.mostrar_total_actual()  # Mostrar el total acumulado después de cada operación

    def mostrar_operaciones(self):
        print(f"Operando en cuenta '{self.cuenta_actual['nombre']}' > {self.cuenta_actual['operaciones'][-1]}")
        for operacion in self.cuenta_actual["operaciones"]:
            print(f"  {operacion}")

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
            if nuevo_resultado >= 0:
                operacion = f"+{nuevo_resultado:.1f}"
            else:
                operacion = f"{nuevo_resultado:.1f}"
            self.cuenta_actual["total"] += nuevo_resultado
            self.cuenta_actual["operaciones"].append(f"{nueva_operacion} = {operacion}")
            print(f"{nueva_operacion} = {operacion}")
        except Exception as e:
            print(f"Error en la corrección: {e}")

        self.limpiar_pantalla()
        self.mostrar_total_actual()

    def mostrar_total_actual(self):
        total = self.cuenta_actual["total"]
        if total >= 0:
            total_str = f"+{total:.1f}"
        else:
            total_str = f"{total:.1f}"
        print(f"Total actual de '{self.cuenta_actual['nombre']}': {total_str}\n")

    def mostrar_totales_finales(self):
        if not self.cuentas:
            print("No hay cuentas disponibles para mostrar.\n")
            return

        print("\nTotales finales de todas las cuentas:")
        for cuenta in self.cuentas:
            nombre = cuenta["nombre"]
            total = cuenta["total"]
            if total >= 0:
                total_str = f"+{total:.1f}"
            else:
                total_str = f"{total:.1f}"
            print(f"Cuenta: {nombre} (Total: {total_str})")
            for operacion in cuenta["operaciones"]:
                print(f"  {operacion}")

    def reiniciar_o_continuar(self):
        decision = input("\n¿Deseas reiniciar el programa (1: Sí, 0: No)? ").strip()
        if decision == "1":
            self.__init__()  # Reinicia la instancia de la clase
        elif decision == "0":
            print("Volviendo al menú principal.")
        else:
            print("Opción no válida. Volviendo al menú principal.")

    def operar_en_cuenta(self):
        if not self.cuenta_actual:
            print("No hay ninguna cuenta activa para operar.\n")
            return

        while True:
            entrada = input(f"Operando en cuenta '{self.cuenta_actual['nombre']}' (escribe '.....' para salir): ").strip()
            self.procesar_entrada(entrada)

    def iniciar(self):
        while True:
            entrada = input("Comando: ").strip()
            self.procesar_entrada(entrada)

    def cerrar_programa(self):
        print("Cerrando programa.")
        sys.exit()

if __name__ == "__main__":
    CalculadoraRollo()
