# Python → OSC Starter (Windows-friendly)

Este starter incluye dos scripts para enviar datos por OSC cada N segundos:
- `Script_PD_API/weather_to_osc.py`: consulta una API HTTP y envía uno o varios valores por OSC.
- `Script_PD_API/weather_osc.pd`: recibe datos desde weather_to_osc.py via OSC.
- `Script_PD_Dataset/osc_script.py` : lee filas de un CSV y envía columnas por OSC.
- `Script_PD_Dataset/bicing_osc.pd`: recibe datos desde weather_to_osc.py via OSC.

## 1) Instalación (opción recomendada: Miniconda)
```powershell
# Instalar Miniconda (descargar .exe desde la web oficial)
# Luego, en "Anaconda Prompt" o PowerShell:
conda create -n osc_env python=3.11 -y
conda activate osc_env
pip install -r requirements.txt
```

para ver entornos
```
conda env list
```

## 2) Enviar desde un CSV → OSC → PD
Desde la terminal de Anaconda Prompt, con mi  entorno activado:
```powershell
(osc_env) python csv_to_osc.py
```

Abrir el patch weather_osc.pd en Pure data.

## 2) Enviar desde una API → OSC → PD
Desde la terminal de Anaconda Prompt, con mi  entorno activado:
```powershell
(osc_env) python weather_to_osc.py
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
