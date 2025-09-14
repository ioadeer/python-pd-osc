import time
import requests
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio


NOMBRE_DE_CIUDAD = "Buenos Aires"  # Ej: "Buenos Aires" o None
LAT = -34.61           # Si NOMBRE_DE_CIUDAD es None, se usan LAT/LON
LON = -58.38
INTERVAL_SEC= 3.0
OSC_TARGET_IP = "127.0.0.1"
OSC_PORT_SEND = 5005
OSC_ADDRESS_BASE = "/weather"

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
METEO_URL = "https://api.open-meteo.com/v1/forecast"

def geocode_city(nombre):
    try:
        r = requests.get(GEO_URL, params={"name": nombre, "count": 1, "language": "es", "format": "json"}, timeout=10)
        r.raise_for_status()
        data = r.json()
        results = data.get("results") or []
        return results[0] if results else None
    except Exception as e:
        print(f"[WARN] Geocoding falló para '{nombre}': {e}")
        return None

def fetch_current_weather(lat, lon):
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

city_name = ""

def filter_handler(address, *args):
    print(f"{address}: {args}")
    return " ".join(args)
    


dispatcher = Dispatcher()
dispatcher.map("/ciudad", filter_handler)

ip = "127.0.0.1"
# para esuchar
port = 5006


async def loop():
    """Example main loop that only runs for 10 iterations before finishing"""
     # Resolver ubicación
    lat, lon = LAT, LON
    current = None

  
    client = SimpleUDPClient(OSC_TARGET_IP, OSC_PORT_SEND)
    print(f"[Weather→OSC] Enviando a {OSC_TARGET_IP}:{OSC_PORT_SEND} cada {INTERVAL_SEC}s. (lat={lat}, lon={lon})")

    while True:
        if NOMBRE_DE_CIUDAD:
            geo = geocode_city(NOMBRE_DE_CIUDAD)
            if geo:
                lat, lon = geo["latitude"], geo["longitude"]
                print(f"[GEO] {NOMBRE_DE_CIUDAD} -> lat={lat}, lon={lon}")
            else:
                print(f"[GEO] No se pudo resolver '{NOMBRE_DE_CIUDAD}', usando LAT/LON provistos.")
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
        #time.sleep(INTERVAL_SEC)
        await asyncio.sleep(INTERVAL_SEC)

        


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())





