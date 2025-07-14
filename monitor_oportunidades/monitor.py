"""
monitor.py - Gestor de Cartera de Inversión

Este módulo ejecuta un monitor en tiempo real que evalúa activos financieros
(BTC, ORO, SP500) cada 60 segundos para detectar oportunidades de compra.

Una oportunidad se define cuando:
- El precio está por debajo de la media móvil de 30 días.
- El precio está por debajo de la media móvil de 180 días.
- El RSI (Relative Strength Index) es menor a 30.

Si se detecta una oportunidad, se registra automáticamente en el log.
Presionar Ctrl + C para finalizar el monitoreo manualmente.
"""

import time
import os
from colorama import Fore, init
from monitor_funciones import evaluar_oportunidades

init(autoreset=True)

def mostrar_menu():

    """Limpia la pantalla y muestra el encabezado del monitor."""

    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.MAGENTA + "="*40)
    print(Fore.MAGENTA + "     MONITOR DE OPORTUNIDADES")
    print(Fore.MAGENTA + "="*40)
    print(Fore.MAGENTA + "\nPresioná Ctrl + C para detener el monitoreo.\n")

def mostrar_tabla(resultados):

    """
    Muestra en consola una tabla con los resultados de la evaluación.

    Parámetros:
        resultados (list): Lista de listas con los datos por activo.
    """

    print(Fore.CYAN + f"\n{'ACTIVO':<8} {'MEDIA30':<10} {'MEDIA180':<10} {'RSI':<10} {'APTO COMPRA':<15}")
    for fila in resultados:
        activo, cumple_30, cumple_180, cumple_rsi, estado = fila

        m30_col = (Fore.GREEN if cumple_30 else Fore.RED) + f"{'SI' if cumple_30 else 'NO':<10}"
        m180_col = (Fore.GREEN if cumple_180 else Fore.RED) + f"{'SI' if cumple_180 else 'NO':<10}"
        rsi_col = (Fore.GREEN if cumple_rsi else Fore.RED) + f"{'SI' if cumple_rsi else 'NO':<10}"
        estado_col = (Fore.GREEN if estado else Fore.RED) + f"{'APTO' if estado else 'NO APTO':<15}"

        print(f"{activo:<8} {m30_col} {m180_col} {rsi_col} {estado_col}")

def main():

    """
    Bucle principal que actualiza la tabla de oportunidades cada 60 segundos.
    Puede ser detenido manualmente con Ctrl + C.
    """
    
    try:
        while True:
            mostrar_menu()
            resultados = evaluar_oportunidades()
            mostrar_tabla(resultados)
            print(Fore.MAGENTA + "\nActualizando en 60 segundos...")
            time.sleep(60)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\nMonitoreo detenido por el usuario.")

if __name__ == "__main__":
    main()
