import webbrowser
from threading import Thread

from python.servidor import ConfigServidor
#webbrowser.open("http://localhost:420")



CONFIG : ConfigServidor = ConfigServidor()
HOST, PUERTO = CONFIG.direccion

def iniciarServidor(): ...

def abrirSimulador(host :str = HOST, puerto :int = PUERTO):
    webbrowser.open(f"http://{host}:{puerto}",new=1,autoraise=True)

def main():
    hiloServidor : Thread = Thread(target=iniciarServidor)
    hiloCliente : Thread = Thread(target=abrirSimulador)

    hiloServidor.start()
    hiloCliente.start()

    hiloCliente.join()
    hiloServidor.join()
    


if __name__ == '__main__':
    main()