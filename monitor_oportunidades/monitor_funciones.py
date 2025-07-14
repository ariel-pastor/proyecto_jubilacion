"""
monitor_funciones.py - Gestor de Cartera de Inversión

Descripción: Este módulo contiene funciones para evaluar oportunidades de compra
basadas en medias móviles y el RSI, y registrar dichas oportunidades en un archivo de log.
"""

import yfinance as yf
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
from datetime import datetime
import pandas as pd
import logging
import os

# Directorio base para guardar el archivo de log dentro de la carpeta monitor_oportunidades
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "oportunidades.log")

# Configuración del archivo de log
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Activos a monitorear con su correspondiente ticker de Yahoo Finance
ACTIVOS = {
    "BTC": "BTC-USD",
    "ORO": "GC=F",
    "SP500": "^GSPC"
}

def registrar_en_log(mensaje):

    """Registra un mensaje en el archivo de log de oportunidades."""

    logging.info(mensaje)

def evaluar_oportunidades():
    
    """
    Evalúa oportunidades de compra para cada activo con base en:
    - Precio actual por debajo de la media móvil de 30 días (SMA30)
    - Precio actual por debajo de la media móvil de 180 días (SMA180)
    - RSI menor a 30 (condición de sobreventa)

    Devuelve una tabla con los resultados por activo.
    """
    tabla = []

    for nombre, simbolo in ACTIVOS.items():
        try:
            data = yf.download(simbolo, period="200d", interval="1d", progress=False, auto_adjust=True)
            if data.empty or "Close" not in data:
                tabla.append([nombre, False, False, False, False])
                continue

            cierre = data["Close"]
            if not isinstance(cierre, pd.Series):
                cierre = cierre.squeeze()

            sma_30 = SMAIndicator(cierre, window=30).sma_indicator().iloc[-1]
            sma_180 = SMAIndicator(cierre, window=180).sma_indicator().iloc[-1]
            rsi = RSIIndicator(cierre, window=14).rsi().iloc[-1]
            precio_actual = cierre.iloc[-1]

            cumple_30 = precio_actual < sma_30
            cumple_180 = precio_actual < sma_180
            cumple_rsi = rsi < 30

            estado = cumple_30 and cumple_180 and cumple_rsi

            if estado:
                registrar_en_log(f"Oportunidad detectada - {nombre} a ${precio_actual:.2f}")

            tabla.append([nombre, cumple_30, cumple_180, cumple_rsi, estado])

        except Exception as e:
            tabla.append([nombre, False, False, False, False])

    return tabla
