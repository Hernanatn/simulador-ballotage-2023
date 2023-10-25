from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from enum import Enum, _simple_enum
from os.path import isdir, isfile
from solteron import Singleton
from typing import Any
from mimetypes import guess_type
from json import loads
from urllib.parse import unquote

class Computador():

    def __init__(self, valores : dict) -> None:
        self.votosValidos   : int = int(valores['votosValidos'])
        self.votantesNuevos : int = int(valores['votantesNuevos'])

        self.massaSTM       : int = int(valores['massaSTM'])
        self.mileiSTM : int = int(valores['mileiSTM'])
        self.bullrichSTM   : int = int(valores['bullrichSTM'])
        self.schiarettiSTM   : int = int(valores['schiarettiSTM'])
        self.bregmanSTM : int = int(valores['bregmanSTM'])
        self.nuevosSTM : int = int(valores['nuevosSTM'])

        self.massaJM       : int = int(valores['massaJM'])
        self.mileiJM : int = int(valores['mileiJM'])
        self.bullrichJM   : int = int(valores['bullrichJM'])
        self.schiarettiJM   : int = int(valores['schiarettiJM'])
        self.bregmanJM : int = int(valores['bregmanJM'])
        self.nuevosJM : int = int(valores['nuevosJM'])
        
        for k,v in valores.items():
            print(k,v)


    @property
    def Afirmativos(self) -> int:
        return self.votosSTM + self.votosJM
    @property
    def votosSTM(self) -> int:
        return sum([self.massaSTM,self.mileiSTM,self.bullrichSTM,self.schiarettiSTM,self.bregmanSTM,self.nuevosSTM])

    @property
    def votosJM(self) -> int:
        return sum([self.massaJM,self.mileiJM,self.bullrichJM,self.schiarettiJM,self.bregmanJM,self.nuevosJM])

    @property
    def mitadMasUno(self) -> int:
        return round(self.Afirmativos/2)+1

    def generarHTML(self) -> str:
        base : str
        with open("./html/resultado.html","r",encoding="utf-8") as plantilla:
            base = plantilla.read()
        
        ganador = "Sergio Tomás Massa" if self.votosSTM > self.votosJM else "Javier Gerardo Milei"
        rutaImagen = "./recursos/imagenes/stm-ganador.jpg" if self.votosSTM > self.votosJM else "../recursos/imagenes/jgm-ganador.jpg"
        cantidadVotos = max(self.votosSTM,self.votosJM)

        resultado = base\
                    .replace("[VOTOS-TOTALES]",f"{self.Afirmativos:,}")\
                    .replace("[VOTOS-AFIRMATIVOS]",f"{self.Afirmativos}")\
                    .replace("[MITAD-MAS-UNO]",f"{self.mitadMasUno:,}")\
                    .replace("[IMAGEN-GANADOR]",rutaImagen)\
                    .replace("[VOTOS-STM]",f"{self.votosSTM}")\
                    .replace("[VOTOS-JM]",f"{self.votosJM}")\

        return resultado

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
        self.refrescarIndice()
        super().__init__(request, client_address, server)

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


    def leerArchivo(self,ruta):
        ARCHIVO : bytes
        with open(ruta,"rb") as archivo:
            ARCHIVO = archivo.read()    
        return ARCHIVO

    def refrescarIndice(self):
        INDICE : bytes
        with open("simulador.html","rb") as simulador:
            INDICE = simulador.read()    
        self.indice = INDICE

    def do_GET(self) -> None:
        URI_SOLICITUD : str = self.path
        if URI_SOLICITUD == "/" or URI_SOLICITUD == "":
            self.refrescarIndice()
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(self.indice)
        elif isfile(f"./{URI_SOLICITUD}"):
            tipo = guess_type(URI_SOLICITUD)[0]
            self.send_response(200)
            self.send_header("Content-type",tipo)
            self.end_headers()
            archivo = open(f"./{URI_SOLICITUD}","rb")
            data = archivo.read()
            archivo.close()
            self.wfile.write(data)
        
        elif isfile(f"./html/{URI_SOLICITUD}"):
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            html = self.leerArchivo(f"./html/{URI_SOLICITUD}")
            self.wfile.write(html)

        else:
            self.send_error(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(b"404 no encotrada")            
        self.wfile.flush()
        
    def do_POST(self):
        if self.path == "/botonPrueba":
            print("boton apretado")
            print(f"{self.requestline}")
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(bytes(b"<div>boton apretado!</div>"))
            self.wfile.write(bytes(b'<button hx-post="/botonPrueba" hx-swap="outerHTML"> otro boton de prueba </button>'))
            self.wfile.write(bytes(b'<button hx-post="/botonERROR" hx-swap="outerHTML"> esteBotonLanzaUnError </button>'))

        elif self.path == "/computar":
            largo = int(self.headers.get('content-length'))
            data = loads(unquote(self.rfile.read(largo).decode("utf-8")).replace("valores=",""))
            computador = Computador(data)
            resultado = computador.generarHTML()
            
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()

            self.wfile.write(bytes(resultado,"utf-8"))

        self.wfile.flush

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
        except:
            self.cerrar()
        finally:
            self.abrir()
            
if __name__ == '__main__': pass