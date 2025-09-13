from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

IP = "127.0.0.1"
PORT = 5005

def print_handler(address, *args):
    print(f"RX {address} :: {', '.join(str(a) for a in args)}")

if __name__ == "__main__":
    disp = Dispatcher()
    disp.set_default_handler(print_handler)
    server = BlockingOSCUDPServer((IP, PORT), disp)
    print(f"[OSC Listener] Escuchando en {IP}:{PORT} (Ctrl+C para salir)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando...")
