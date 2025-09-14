import sys
import pandas as pd
import time
from pythonosc import osc_message_builder
from pythonosc.udp_client import SimpleUDPClient

def main():
    # Un path a mi archivo csv
    csv_file_path = "./set/TopFive.csv"  # Replace with your file path
    
    # Defino IP y puerto de mi servidor OSC 
    osc_server_ip = "127.0.0.1"  
    osc_server_port = 3000  
    
    # Creo un cliente UDP con mi servidor 
    client = SimpleUDPClient(osc_server_ip, osc_server_port)
    
    # Cargo el "DataFrame" de mi archivo csv 
    df = pd.read_csv(csv_file_path)
    
    #,duracion_recorrido,nombre_estacion_origen,nombre_estacion_destino,MES,DIA
    # Itero sobre las filas del DataFrame
    for index in range(df.shape[0]):
        # Extraigo la informacion que me interesa
        data_to_send = df["duracion_recorrido"][index]
    
        # Crear y enviar un mensaje OSC 
        addr = "/duracion"
        value = float(data_to_send)
        client.send_message(addr, value)
        print("Enviando un mensaje...")
        print(f"OSC {addr} -> {value}")
 

        # Estacion

        data_to_send = df["nombre_estacion_origen"][index] 
        addr = "/origen"
        value = str(data_to_send)
        client.send_message(addr, value)
        print("Enviando otro mensaje...")
        print(f"OSC {addr} -> {value}")
    
        # Introduzco una pausa de 1 segundo entre iteración e iteración 
        time.sleep(1)

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Cerrando mi script..")
        sys.exit()


