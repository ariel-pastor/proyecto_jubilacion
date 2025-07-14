"""
main.py - Gestor de Cartera de Inversión

Este módulo ejecuta la interfaz principal del programa de gestión de inversiones. Permite registrar,
modificar, eliminar compras, consultar estado actual de activos, ver evolución histórica de la cartera
y ejecutar el monitor de oportunidades.
"""

from modulos_cartera import (
    cargar_cartera,
    registrar_compra,
    mostrar_estado_actual,
    mostrar_compras,
    eliminar_compra,
    modificar_compra,
    mostrar_resumen_general,
    mostrar_grafico_historial
)
import os
from colorama import Fore
import subprocess

def menu():

    """Menú principal que gestiona las opciones del usuario y llama a las funciones correspondientes."""

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        cartera = cargar_cartera()

        print(Fore.MAGENTA + "="*40)
        print(Fore.MAGENTA + "   GESTOR DE CARTERA DE INVERSIÓN")
        print(Fore.MAGENTA + "="*40)

        print(Fore.MAGENTA + "\n=== GESTIÓN DE CARTERA ===\n")
        print("1. Registrar nueva compra")
        print("2. Modificar una compra")
        print("3. Eliminar una compra")
        print("4. Historial de compras")
        print("5. Estado actual de la inversión")
        print("6. Evolución histórica de la cartera")
        print("7. Monitor oportunidades")
        print("8. Salir")

        opcion = input("Seleccioná una opción: ")

        if opcion == "1":
            print(Fore.MAGENTA + "\n=== REGISTRAR NUEVA COMPRA ===\n")
            activo = input("Activo (BTC, ORO, SP500): ").upper()
            if activo not in ["BTC", "ORO", "SP500"]:
                print(Fore.RED + "✖ Activo inválido.")
                input("Presioná Enter para continuar...")
                continue

            try:
                cantidad = float(input("Cantidad comprada: "))
                monto = float(input("Monto invertido en USD: "))
                registrar_compra(cartera, activo, cantidad, monto)
            except ValueError:
                print(Fore.RED + "✖ Ingreso inválido.")
            input("Presioná Enter para continuar...")

        elif opcion == "2":
            print(Fore.MAGENTA + "\n=== MODIFICAR UNA COMPRA ===\n")
            mostrar_compras(cartera)
            try:
                indice_input = input("Número de compra a modificar: ")
                if not indice_input.isdigit():
                    raise ValueError
                indice = int(indice_input)
                if indice < 0 or indice >= len(cartera):
                    raise IndexError
                nueva_cantidad = float(input("Nueva cantidad: "))
                nuevo_monto = float(input("Nuevo monto en USD: "))
                modificar_compra(cartera, indice, nueva_cantidad, nuevo_monto)
            except ValueError:
                print(Fore.RED + "✖ Ingreso inválido.")
            except IndexError:
                print(Fore.RED + "✖ El índice ingresado no existe.")
            input("Presioná Enter para continuar...")

        elif opcion == "3":
            print(Fore.MAGENTA + "\n=== ELIMINAR UNA COMPRA ===\n")
            mostrar_compras(cartera)
            try:
                indice_input = input("Número de compra a eliminar: ")
                if not indice_input.isdigit():
                    raise ValueError
                indice = int(indice_input)
                if indice < 0 or indice >= len(cartera):
                    raise IndexError
                eliminar_compra(cartera, indice)
            except ValueError:
                print(Fore.RED + "✖ Ingreso inválido.")
            except IndexError:
                print(Fore.RED + "✖ El índice ingresado no existe.")
            input("Presioná Enter para continuar...")

        elif opcion == "4":
            print(Fore.MAGENTA + "\n=== HISTORIAL DE COMPRAS ===\n")
            mostrar_compras(cartera)
            input("Presioná Enter para volver al menú...")

        elif opcion == "5":
            print(Fore.MAGENTA + "\n=== ESTADO ACTUAL DE LA INVERSIÓN ===\n")
            mostrar_estado_actual(cartera)
            input("Presioná Enter para volver al menú...")

        elif opcion == "6":
            print(Fore.MAGENTA + "\n=== EVOLUCIÓN HISTÓRICA DE LA CARTERA ===\n")
            mostrar_resumen_general(cartera)
            mostrar_grafico_historial()
            input("Presioná Enter para volver al menú...")

        elif opcion == "7":
            print(Fore.MAGENTA + "\n=== MONITOR DE OPORTUNIDADES ===\n")
            try:
                subprocess.run(["python", "monitor_oportunidades/monitor.py"])
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n\nMonitoreo detenido. Volviendo al menú...")
            except Exception as e:
                print(Fore.RED + f"✖ Error al ejecutar el monitor: {e}")

        elif opcion == "8":
            print("¡Hasta luego!")
            break

        else:
            print(Fore.RED + "✖ Opción inválida.")
            input("Presioná Enter para volver al menú...")

if __name__ == "__main__":
    menu()
