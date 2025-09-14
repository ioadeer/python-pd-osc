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
(osc_env) python bicing_osc_script.py
```

Abrir el patch bicing_osc.pd en Pure data.

## 2) Enviar desde una API → OSC → PD
Desde la terminal de Anaconda Prompt, con mi  entorno activado y desde el directorio donde se encuentra el script ejecutar:
```powershell
(osc_env) python weather_to_osc.py
```

Abrir el patch weather_osc.pd en Pure data.
