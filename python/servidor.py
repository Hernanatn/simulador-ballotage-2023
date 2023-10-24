from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from enum import Enum, _simple_enum
from os.path import isdir
from sobrecargar import overload
from solteron import Singleton
from typing import Any


class ConfigServidor(metaclass=Singleton):

    HOST : str = "localhost"
    PUERTO: int = 420

    @property
    def direccion(self) -> tuple[str,int]:
        return(self.HOST,self.PUERTO)

    def __setattr__(self, nombre : str, dato : Any):
        raise AttributeError(f"No se puede reasignar el atributo {nombre}")


class ManejadorSolicitudes(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server): 
        super().__init__(self, request, client_address, server)

    def enviar_VISTA(self, ruta : str) -> None:
        MAX_BYTES_LECTURA : int = 2048 

        self.send_header("Content-type","text/html")
        self.end_headers()

        with open(f".{ruta}", mode="rb") as vista:
            data : bytes
            while True:
                data = vista.read(MAX_BYTES_LECTURA) 
                if data is None or len(data) == 0: break
                self.wfile.write(data)

    @overload
    def enviar_INTERCAMBIO(self, ruta : str):
        ...

    @overload
    def enviar_INTERCAMBIO(self, etiqueta : EtiquetaHTML):
        ...

    def do_GET(self) -> None:
        URI_SOLICITUD : str = self.path
        if URI_SOLICITUD in self.vistas: 
            ... #[HACER]
        
        elif URI_SOLICITUD in self.plantillas:
            ... #[HACER]
        
        else:
            self.send_error(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(b"404 no encotrada")
            return

        self.wfile.flush()
        
    def do_POST(self):
        print(self.path)
        if self.path == "/botonPrueba":
            print("boton apretado")
            print(f"{self.requestline}")
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(bytes(b"<div>boton apretado!</div>"))
            self.wfile.write(bytes(b'<button hx-post="/botonPrueba" hx-swap="outerHTML"> otro boton de prueba </button>'))
            self.wfile.write(bytes(b'<button hx-post="/botonERROR" hx-swap="outerHTML"> esteBotonLanzaUnError </button>'))

        elif self.path == "/botonERROR":
            print("boton apretado")
            print(f"{self.requestline}")
            self.send_response(218)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(bytes(b"<div>UPS! Se genero un error!!!!!!</div>"))
            self.wfile.flush()
            raise RuntimeError("ERROR GENERADO POR EL BOTON!!")

class Servidor(HTTPServer):
    
    def __init__(self, config : tuple, manejador : type):
        super().__init__(config,manejador)

    def cerrar(self):
        print("Servidor cerrado")
        self.server_close()
        return self

    def abrir(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.cerrar()

def main() :
    from sys import argv, stdin
    servidor = Servidor((argv[1],int(argv[2])),ManejadorSolicitudes)
    print(f"Servidor iniciado: http://{servidor.server_address[0]}:{servidor.server_address[1]}")

    servidor.abrir()




if __name__ == '__main__':
    main()