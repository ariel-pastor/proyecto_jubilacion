"""
modulos_cartera.py - Gestor de Cartera de Inversión

Descripción: Este módulo permite gestionar una cartera de inversiones, registrando compras,
consultando el estado actual, modificando/eliminando registros, y visualizando la evolución histórica.
"""

import json
import os
from datetime import datetime
import logging
from colorama import init, Fore
import yfinance as yf
import matplotlib.pyplot as plt

init(autoreset=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CAR = os.path.join(BASE_DIR, "cartera.json")
ARCHIVO_LOG = os.path.join(BASE_DIR, "log_cartera.log")
HISTORIAL_JSON = os.path.join(BASE_DIR, "historial.json")

ACTIVOS_VALIDOS = {
    "BTC": "BTC-USD",
    "ORO": "GC=F",
    "SP500": "^GSPC"
}

logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def cargar_cartera():
    """Carga el archivo cartera.json y devuelve una lista con las compras registradas."""
    if not os.path.exists(ARCHIVO_CAR):
        return []
    try:
        with open(ARCHIVO_CAR, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error al leer cartera: {e}")
        return []

def guardar_cartera(cartera):
    """Guarda la cartera actual en el archivo cartera.json."""
    try:
        with open(ARCHIVO_CAR, "w", encoding="utf-8") as f:
            json.dump(cartera, f, indent=4)
    except Exception as e:
        logging.error(f"Error al guardar cartera: {e}")

def registrar_compra(cartera, activo, cantidad, monto):
    """Registra una nueva compra en la cartera."""
    if activo.upper() not in ACTIVOS_VALIDOS:
        print(Fore.RED + f"✖ Activo inválido. Solo se permiten: {', '.join(ACTIVOS_VALIDOS.keys())}")
        return

    compra = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "activo": activo.upper(),
        "cantidad": cantidad,
        "monto": monto
    }
    cartera.append(compra)
    guardar_cartera(cartera)
    logging.info(f"Compra registrada: {compra}")
    print(Fore.GREEN + "✔ Compra registrada con éxito.")

def modificar_compra(cartera, indice, nueva_cantidad, nuevo_monto):
    """Modifica una compra existente en la cartera."""
    try:
        cartera[indice]["cantidad"] = nueva_cantidad
        cartera[indice]["monto"] = nuevo_monto
        guardar_cartera(cartera)
        logging.info(f"Compra modificada: {cartera[indice]}")
        print(Fore.GREEN + "✔ Compra modificada con éxito.")
    except IndexError:
        print(Fore.RED + "✖ El índice ingresado no existe.")
    except Exception as e:
        print(Fore.RED + f"✖ Error al modificar la compra: {e}")

def eliminar_compra(cartera, indice):
    """Elimina una compra de la cartera según su índice."""
    try:
        compra_eliminada = cartera.pop(indice)
        guardar_cartera(cartera)
        logging.info(f"Compra eliminada: {compra_eliminada}")
        print(Fore.GREEN + f"✔ Compra eliminada correctamente: {compra_eliminada['activo']} del {compra_eliminada['fecha']}")
    except IndexError:
        print(Fore.RED + "✖ El número ingresado no corresponde a una compra existente.")
    except Exception as e:
        print(Fore.RED + f"✖ Error al eliminar la compra: {e}")

def mostrar_compras(cartera):
    """Muestra por pantalla todas las compras registradas en la cartera."""
    if not cartera:
        print(Fore.YELLOW + "No hay compras registradas.")
        return

    print(Fore.BLUE + "\n=== COMPRAS REGISTRADAS ===\n")
    for idx, compra in enumerate(cartera):
        print(f"[{idx}] {compra['fecha']} | {compra['activo']} | {compra['cantidad']} unidades | ${compra['monto']:.2f}")

def try_cotizacion(simbolo_yf):
    """Intenta obtener la cotización actual del activo desde Yahoo Finance."""
    try:
        ticker = yf.Ticker(simbolo_yf)
        data = ticker.history(period="1d")
        if data.empty:
            data = ticker.history(period="3d")
        if not data.empty:
            return data["Close"].dropna().iloc[-1]
    except:
        pass
    return 0

def guardar_en_historial(fecha, valor):
    """Agrega el valor total de la cartera al historial para seguimiento temporal."""
    historial = []
    if os.path.exists(HISTORIAL_JSON):
        try:
            with open(HISTORIAL_JSON, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except:
            pass

    historial.append({"fecha": fecha, "valor": valor})

    with open(HISTORIAL_JSON, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4)

def mostrar_grafico_historial():
    """Muestra una gráfica de evolución del valor de la cartera a lo largo del tiempo."""
    if not os.path.exists(HISTORIAL_JSON):
        print(Fore.YELLOW + "No hay datos históricos disponibles.")
        return

    with open(HISTORIAL_JSON, "r", encoding="utf-8") as f:
        historial = json.load(f)

    if not historial:
        print(Fore.YELLOW + "No hay datos históricos disponibles.")
        return

    fechas = [dato["fecha"] for dato in historial]
    valores = [dato["valor"] for dato in historial]

    plt.figure(num="Evolución histórica de la cartera", figsize=(7, 3))
    plt.plot(fechas, valores, marker="o", color="blue")
    plt.title("Evolución histórica del valor de la cartera")
    plt.xlabel("Fecha")
    plt.ylabel("Valor en USD")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def mostrar_estado_actual(cartera):
    """Muestra el estado actual de la inversión por cada activo de la cartera."""
    if not cartera:
        print(Fore.YELLOW + "No hay compras registradas.")
        return

    print(Fore.BLUE + "\n=== ESTADO ACTUAL DE LA INVERSIÓN POR ACTIVO ===\n")
    for activo in ACTIVOS_VALIDOS:
        compras_activas = [c for c in cartera if c["activo"] == activo]
        if not compras_activas:
            continue

        total_cantidad = sum(c["cantidad"] for c in compras_activas)
        total_monto = sum(c["monto"] for c in compras_activas)
        ppc = total_monto / total_cantidad if total_cantidad else 0
        cotizacion = try_cotizacion(ACTIVOS_VALIDOS[activo])
        valor_actual = total_cantidad * cotizacion
        ganancia = valor_actual - total_monto
        ganancia_pct = (ganancia / total_monto * 100) if total_monto else 0

        color = Fore.GREEN if ganancia > 0 else Fore.RED if ganancia < 0 else Fore.YELLOW

        print(f"{Fore.CYAN}Activo: {activo}")
        print(f"  Cantidad total: {total_cantidad:.6f}")
        print(f"  Total invertido: ${total_monto:.2f}")
        print(f"  Precio Promedio de Compra (PPC): ${ppc:.2f}")
        print(f"  Precio actual: ${cotizacion:.2f}")
        print(f"  Valor actual: ${valor_actual:.2f}")
        print(color + f"  Ganancia/Pérdida: ${ganancia:.2f} ({ganancia_pct:.2f}%)\n")

def mostrar_resumen_general(cartera):
    """Muestra un resumen general de la cartera, incluyendo inversión total, valor actual y ganancia/pérdida."""
    resumen = {}
    for compra in cartera:
        activo = compra["activo"]
        cantidad = compra["cantidad"]
        monto = compra["monto"]

        if activo not in resumen:
            resumen[activo] = {"cantidad_total": 0, "monto_total": 0}
        resumen[activo]["cantidad_total"] += cantidad
        resumen[activo]["monto_total"] += monto

    total_invertido = sum(datos["monto_total"] for datos in resumen.values())
    total_valor_actual = sum(
        resumen[activo]["cantidad_total"] * try_cotizacion(ACTIVOS_VALIDOS.get(activo, activo))
        for activo in resumen
    )
    ganancia_total = total_valor_actual - total_invertido
    ganancia_pct_total = (ganancia_total / total_invertido * 100) if total_invertido else 0

    if ganancia_total > 0:
        color_total = Fore.GREEN
    elif ganancia_total < 0:
        color_total = Fore.RED
    else:
        color_total = Fore.YELLOW

    print(Fore.BLUE + "\n=== RESUMEN GENERAL DE LA CARTERA ===\n")
    print(f"Total invertido: ${total_invertido:.2f}")
    print(f"Valor actual: ${total_valor_actual:.2f}")
    print(color_total + f"Ganancia/Pérdida total: ${ganancia_total:.2f} ({ganancia_pct_total:.2f}%)\n")
