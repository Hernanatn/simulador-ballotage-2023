import webbrowser
from threading import Thread
from py.servidor import ConfigServidor, Servidor, ManejadorSolicitudes
#webbrowser.open("http://localhost:420")

CONFIG : ConfigServidor = ConfigServidor()
HOST, PUERTO = CONFIG.direccion

def iniciarServidor(host :str = HOST, puerto :int = PUERTO):
    servidor = Servidor((host,puerto),ManejadorSolicitudes)
    print(f"Servidor iniciado: http://{servidor.server_address[0]}:{servidor.server_address[1]}")
    try:
        servidor.abrir()
    except Exception as e:
        print(f"{e}")
        return

def abrirSimulador(host :str = HOST, puerto :int = PUERTO):
    import webview
    webview.create_window("Simulador 2023",f"http://{host}:{puerto}/",width=800,height=1000,min_size=(450,1000))
    webview.start()

def main():
    hiloServidor : Thread = Thread(target=iniciarServidor)
    hiloServidor.start()
    abrirSimulador()
    hiloServidor.join()
    
    


if __name__ == '__main__':
    main()