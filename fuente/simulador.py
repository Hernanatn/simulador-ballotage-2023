import webbrowser
from threading import Thread
from py.servidor import ConfigServidor, Servidor, ManejadorSolicitudes

DEBUG = True

CONFIG : ConfigServidor = ConfigServidor()
HOST, PUERTO = CONFIG.direccion

def iniciarServidor(host :str = HOST, puerto :int = PUERTO):
    servidor = Servidor((host,puerto),ManejadorSolicitudes)
    print(f"Servidor iniciado: http://{servidor.server_address[0]}:{servidor.server_address[1]}")
    try:
        servidor.abrir()
    except Exception as e:
        pass


def cerrarSimulador(hiloServidor,ventana):
    hiloServidor.join()
    ventana.destroy()


def abrirSimulador(hilo, cerrar, host :str = HOST, puerto :int = PUERTO):
    if DEBUG: webbrowser.open(f"http://{host}:{puerto}/")
    else:
        import webview
        ventana = webview.create_window("Simulador 2023",f"http://{host}:{puerto}/",width=800,height=1000,min_size=(450,1000))
        webview.start(cerrar,(hilo,ventana))


def main():
    hiloServidor : Thread = Thread(target=iniciarServidor)
    hiloServidor.start()
    abrirSimulador(hiloServidor,cerrarSimulador)
    
    


if __name__ == '__main__':
    main()