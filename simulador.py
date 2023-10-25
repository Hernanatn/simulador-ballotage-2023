import webbrowser
from threading import Thread
from py.servidor import ConfigServidor, Servidor, ManejadorSolicitudes
#webbrowser.open("http://localhost:420")

CONFIG : ConfigServidor = ConfigServidor()
HOST, PUERTO = CONFIG.direccion

def iniciarServidor(host :str = HOST, puerto :int = PUERTO):
    servidor = Servidor((host,puerto),ManejadorSolicitudes)
    print(f"Servidor iniciado: http://{servidor.server_address[0]}:{servidor.server_address[1]}")

    servidor.abrir()

def abrirSimulador(host :str = HOST, puerto :int = PUERTO):
    webbrowser.open(f"http://{host}:{puerto}/",new=1,autoraise=True)

def main():
    hiloServidor : Thread = Thread(target=iniciarServidor)
    hiloCliente : Thread = Thread(target=abrirSimulador)

    hiloServidor.start()
    hiloCliente.start()

    hiloCliente.join()
    hiloServidor.join()
    
    


if __name__ == '__main__':
    main()