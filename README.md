# Proyecto Jubilación

**Gestor de Cartera + Monitor de Oportunidades**

Este proyecto fue desarrollado como trabajo final de la cursada *ISTEA - INFRAESTRUCTURA - Programación 1*, utilizando Python. Permite registrar y gestionar una cartera de inversiones a largo plazo, visualizar su evolución y monitorear oportunidades de compra usando análisis técnico (medias móviles y RSI).

---

## Estructura del Proyecto

```
Proyecto_jubilacion/
├── gestor_cartera/
│   ├── main.py               # Menú principal del programa
│   ├── modulos_cartera.py    # Funciones del gestor de cartera
│   ├── cartera.json          # Archivo con compras registradas
│   ├── historial.json        # Historial de evolución del valor total
│   └── log_cartera.log       # Log de eventos (registro/modificación/eliminación)
│
├── monitor_oportunidades/
│   ├── monitor.py            # Script de ejecución continua
│   ├── monitor_funciones.py  # Funciones para evaluar oportunidades
│   └── oportunidades.log     # Log con oportunidades detectadas
│
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación del proyecto
```

---

## Librerías utilizadas

### pandas
Se utiliza para manejar los datos históricos de precios descargados desde Yahoo Finance. Específicamente, permite:
- Manipular series temporales (precios de cierre de los activos).
- Calcular indicadores técnicos como SMA y RSI junto a la biblioteca `ta`.
- Asegurar compatibilidad entre los datos y las funciones analíticas del monitor.

### yfinance
Permite obtener datos de cotización diaria de activos como BTC, ORO y SP500 directamente desde Yahoo Finance.

### ta (Technical Analysis)
Proporciona indicadores técnicos como medias móviles (SMA) y RSI, esenciales para evaluar oportunidades de inversión.

### colorama
Permite imprimir colores en consola para diferenciar información relevante (como ganancias o alertas de compra).

### matplotlib
Utilizado para graficar la evolución histórica del valor total de la cartera con fechas y montos.

### json, os, datetime, logging
Módulos estándar de Python para:
- Almacenamiento de datos en archivos.
- Manipulación de fechas y rutas de sistema.
- Registro de eventos y errores mediante logs.

---

## Funcionalidades Principales

### Gestor de Cartera (`gestor_cartera/`)
- Registrar compras por activo (BTC, ORO, SP500).
- Modificar o eliminar compras existentes.
- Ver historial completo de compras realizadas.
- Consultar el estado actual de cada activo (PPC, cotización, ganancia/pérdida).
- Ver la evolución histórica de la cartera en un gráfico.
- Todas las acciones se registran en `log_cartera.log`.

### Monitor de Oportunidades (`monitor_oportunidades/`)
- Evalúa oportunidades de inversión según 3 condiciones:
  - Precio actual < Media Móvil de 30 días (SMA30)
  - Precio actual < Media Móvil de 180 días (SMA180)
  - RSI < 30
- Muestra una tabla por activo con indicadores visuales (colores).
- Guarda oportunidades detectadas en `oportunidades.log`.
- Se ejecuta en modo continuo con actualización automática cada 60 segundos.
- El monitoreo se detiene con `Ctrl + C`.

---

## Instalación y Entorno Virtual

### 1. Clonar o copiar el proyecto
```bash
git clone <repositorio>
cd Proyecto_jubilacion
```

### 2. Crear y activar entorno virtual
```bash
python -m venv .venv
```

#### En Windows:
```bash
.venv\Scripts\activate
```

#### En Linux/macOS:
```bash
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## Ejecución

Desde la raíz del proyecto, ejecutá:

```bash
python gestor_cartera/main.py
```

Desde el menú del gestor se puede acceder directamente al monitor de oportunidades (opción 7).

---

## Requisitos (requirements.txt)

```
yfinance
ta
pandas
matplotlib
colorama
```

---

## Ejemplo de Salida del Monitor

```
========================================
     MONITOR DE OPORTUNIDADES
========================================

ACTIVO    MEDIA30    MEDIA180   RSI        APTO COMPRA
BTC       SI         SI         SI         APTO
ORO       NO         SI         NO         NO APTO
SP500     NO         NO         NO         NO APTO

Actualizando en 60 segundos...
```

---

## Autor y Licencia

Desarrollado por **Ariel Pastor** como parte del Trabajo Final de la cursada *ISTEA - INFRAESTRUCTURA - Programación 1*.

Licencia: MIT
