# Python → OSC Starter (Windows-friendly)

Este starter incluye dos scripts para enviar datos por OSC cada N segundos:
- `api_to_osc.py`: consulta una API HTTP y envía uno o varios valores por OSC.
- `csv_to_osc.py`: lee filas de un CSV y envía columnas por OSC.
- `osc_listener.py`: receptor OSC simple para probar localmente.
- `sample_data.csv`: dataset de ejemplo.

## 1) Instalación (opción recomendada: Miniconda)
```powershell
# Instalar Miniconda (descargar .exe desde la web oficial)
# Luego, en "Anaconda Prompt" o PowerShell:
conda create -n osc_env python=3.11 -y
conda activate osc_env
pip install -r requirements.txt
```

## 2) Instalación (opción simple: Python + pip)
- Descargá e instalá Python desde https://www.python.org/
- Marcá la opción "Add python.exe to PATH" durante la instalación.
```powershell
pip install -r requirements.txt
```

## 3) Probar un receptor OSC local
En una terminal:
```powershell
python osc_listener.py
```
Deberías ver en consola cualquier mensaje que llegue al `127.0.0.1:5005`.

## 4) Enviar desde una API → OSC
En otra terminal:
```powershell
python api_to_osc.py
```
- Configurá en el archivo (variables arriba) `API_URL`, `JSON_PATHS`, `OSC_ADDRESS_BASE`, `OSC_PORT`, `INTERVAL_SEC`.
- `JSON_PATHS` es una lista de rutas a claves dentro del JSON para extraer valores.
  Ejemplo: `["bpi.USD.rate_float", "bpi.EUR.rate_float"]`

## 5) Enviar desde un CSV → OSC
En otra terminal:
```powershell
python csv_to_osc.py
```
- Configurá `CSV_PATH`, `COLUMNS_TO_SEND`, `OSC_ADDRESS_BASE`, `OSC_PORT`, `INTERVAL_SEC`.
- Recorre el CSV fila por fila y envía las columnas seleccionadas como mensajes OSC.

## 6) Formato OSC sugerido
- Ruta (address): `/data/<nombre_columna>` o `/data/<alias>`
- Payload: valor numérico o string.
- Frecuencia: `INTERVAL_SEC = 3` (modificable).

## 7) Tips para clase
- Si una API falla, el script registra el error y reintenta.
- Para debug, corré el `osc_listener.py` y verificá la salida.
- Si usás TouchDesigner/Unity/etc., configurá el puerto para recibir `5005` o ajustá el script.

## 8) Licencia
Uso educativo. Ajustá libremente para tus clases.


---
## 4 bis) Enviar clima (Open‑Meteo) → OSC (sin API key)
```powershell
python weather_to_osc.py
```
- Opcional: definí `NOMBRE_DE_CIUDAD = "Buenos Aires"` en el script para resolver lat/lon automáticamente.
- O dejá `NOMBRE_DE_CIUDAD = None` y usá `LAT`/`LON` manualmente.
- Envía por OSC: `/weather/temperature_2m`, `/weather/relative_humidity_2m`, `/weather/wind_speed_10m`.
