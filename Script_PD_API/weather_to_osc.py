import time
import requests
from typing import Optional, Dict, Any
from pythonosc.udp_client import SimpleUDPClient

# ===============================
# Weather → OSC (Open‑Meteo, sin API key)
# ===============================
# Dos modos de ubicación:
# 1) Usar NOMBRE_DE_CIUDAD (usa geocoding de Open‑Meteo)
# 2) Usar LAT y LON directamente
#
# Campos que se envían por OSC (address base /weather):
#  - /weather/temperature_2m       (°C)
#  - /weather/relative_humidity_2m (%)
#  - /weather/wind_speed_10m       (m/s)
#
# Ajustes:
NOMBRE_DE_CIUDAD: Optional[str] = None  # Ej: "Buenos Aires" o None
LAT: Optional[float] = -34.61           # Si NOMBRE_DE_CIUDAD es None, se usan LAT/LON
LON: Optional[float] = -58.38
INTERVAL_SEC: float = 3.0
OSC_TARGET_IP: str = "127.0.0.1"
OSC_PORT: int = 5005
OSC_ADDRESS_BASE: str = "/weather"

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
METEO_URL = "https://api.open-meteo.com/v1/forecast"

def geocode_city(nombre: str) -> Optional[Dict[str, Any]]:
    try:
        r = requests.get(GEO_URL, params={"name": nombre, "count": 1, "language": "es", "format": "json"}, timeout=10)
        r.raise_for_status()
        data = r.json()
        results = data.get("results") or []
        return results[0] if results else None
    except Exception as e:
        print(f"[WARN] Geocoding falló para '{nombre}': {e}")
        return None

def fetch_current_weather(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto",
    }
    try:
        r = requests.get(METEO_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("current")
    except Exception as e:
        print(f"[ERROR] Weather request falló: {e}")
        return None

def main():
    # Resolver ubicación
    lat, lon = LAT, LON
    if NOMBRE_DE_CIUDAD:
        geo = geocode_city(NOMBRE_DE_CIUDAD)
        if geo:
            lat, lon = geo["latitude"], geo["longitude"]
            print(f"[GEO] {NOMBRE_DE_CIUDAD} -> lat={lat}, lon={lon}")
        else:
            print(f"[GEO] No se pudo resolver '{NOMBRE_DE_CIUDAD}', usando LAT/LON provistos.")

    client = SimpleUDPClient(OSC_TARGET_IP, OSC_PORT)
    print(f"[Weather→OSC] Enviando a {OSC_TARGET_IP}:{OSC_PORT} cada {INTERVAL_SEC}s. (lat={lat}, lon={lon})")

    while True:
        current = fetch_current_weather(lat, lon)
        if current:
            # Extraer campos
            temp = current.get("temperature_2m")
            rh = current.get("relative_humidity_2m")
            wind = current.get("wind_speed_10m")

            # Enviar por OSC si existen
            if temp is not None:
                client.send_message(f"{OSC_ADDRESS_BASE}/temperature_2m", float(temp))
                print(f"OSC {OSC_ADDRESS_BASE}/temperature_2m -> {temp}")
            if rh is not None:
                client.send_message(f"{OSC_ADDRESS_BASE}/relative_humidity_2m", float(rh))
                print(f"OSC {OSC_ADDRESS_BASE}/relative_humidity_2m -> {rh}")
            if wind is not None:
                client.send_message(f"{OSC_ADDRESS_BASE}/wind_speed_10m", float(wind))
                print(f"OSC {OSC_ADDRESS_BASE}/wind_speed_10m -> {wind}")
        time.sleep(INTERVAL_SEC)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCerrando...")
