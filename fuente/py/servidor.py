from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from enum import Enum, _simple_enum
from os.path import isdir, isfile
from solteron import Singleton
from typing import Any
from mimetypes import guess_type
from json import loads
from urllib.parse import unquote
from threading import Thread
def rutaRecurso(rutaRelativa):
    import sys
    import os
    try:
        rutaBase = sys._MEIPASS
    except Exception:
        rutaBase = os.path.abspath(".")

    return os.path.join(rutaBase, rutaRelativa)

class ServidorMuerto(Exception): ...

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

    def resultadosHTML(self) -> str:
        base : str
        with open(rutaRecurso("./html/resultado.html"),"r",encoding="utf-8") as plantilla:
            base = plantilla.read()
        
        ganador = "Sergio Tomás Massa" if self.votosSTM > self.votosJM else "Javier Gerardo Milei"
        rutaImagen = "./recursos/imagenes/stm-ganador.jpg" if self.votosSTM > self.votosJM else "./recursos/imagenes/jgm-ganador.jpg"
        cantidadVotos = max(self.votosSTM,self.votosJM)

        resultado = base\
                    .replace("[VOTOS-TOTALES]",f"{self.Afirmativos:,}")\
                    .replace("[VOTOS-AFIRMATIVOS]",f"{self.Afirmativos}")\
                    .replace("[MITAD-MAS-UNO]",f"{self.mitadMasUno:,}")\
                    .replace("[IMAGEN-GANADOR]",rutaImagen)\
                    .replace("[VOTOS-STM]",f"{self.votosSTM}")\
                    .replace("[VOTOS-JM]",f"{self.votosJM}")\

        return resultado

    @staticmethod
    def dadosHTML() -> str:
        
        base : str
        with open(rutaRecurso("./html/dados.html"),"r",encoding="utf-8") as plantilla:
            base = plantilla.read()
        
        # [HACER]: Dados, variables aleatorias.

        votosValidos = 0
        votantesNuevos = 0
        massaSTM = 0
        mileiSTM = 0
        bullrichSTM = 0
        schiarettiSTM = 0
        bregmanSTM = 0
        nuevosSTM = 0
        massaJM = 0
        mileiJM  = 0
        bullrichJM = 0
        schiarettiJM = 0
        bregmanJM = 0
        nuevosJM = 0

        dados = base\
                    .replace("[VOTOS-TOTALES]",f"{self.Afirmativos:,}")\

        return dados
        

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
        with open(rutaRecurso("indice.html"),"rb") as simulador:
            INDICE = simulador.read()    
        self.indice = INDICE

    def refrescarSimulador(self):
        SIMULADOR : bytes
        with open(rutaRecurso("simulador.html"),"rb") as simulador:
            SIMULADOR = simulador.read()    
        self.simulador = SIMULADOR

    def do_GET(self) -> None:
        URI_SOLICITUD : str = self.path
        if URI_SOLICITUD == "/" or URI_SOLICITUD == "":
            self.refrescarIndice()
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(self.indice)

        elif URI_SOLICITUD == "/simulador":
            self.refrescarSimulador()
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(self.simulador)

        elif isfile(rutaRecurso(f"./{URI_SOLICITUD}")):
            tipo = guess_type(URI_SOLICITUD)[0]
            self.send_response(200)
            self.send_header("Content-type",tipo)
            self.end_headers()
            archivo = open(rutaRecurso(f"./{URI_SOLICITUD}"),"rb")
            data = archivo.read()
            archivo.close()
            self.wfile.write(data)
        
        elif isfile(rutaRecurso(f"./html/{URI_SOLICITUD}")):
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            html = self.leerArchivo(rutaRecurso(f"./html/{URI_SOLICITUD}"))
            self.wfile.write(html)

        else:
            self.send_error(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(b"404 no encotrada")            
        self.wfile.flush()
        
    def do_POST(self):
        if self.path == "/cerrar":
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(bytes(b'<div id="principal"><h1>Gracias por usar el Simulador.</h1></div>'))

            self.wfile.flush()
            self.server.server_close()
            

        elif self.path == "/computar":
            largo = int(self.headers.get('content-length'))
            data = loads(unquote(self.rfile.read(largo).decode("utf-8")).replace("valores=",""))
            computador = Computador(data)
            resultado = computador.resultadosHTML()
            
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()

            self.wfile.write(bytes(resultado,"utf-8"))

        elif self.path == "/dados":
            dados = Computador.dadosHTML()
            
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()

            self.wfile.write(bytes(dados,"utf-8"))
        else:
            self.send_error(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(b"404 no encotrada")            
        self.wfile.flush()
        

        self.wfile.flush

class Servidor(HTTPServer):
    
    def __init__(self, config : tuple, manejador : type):
        super().__init__(config,manejador)

    def cerrar(self):
        print("Servidor cerrado")
        self.server_close()
        return self


    def morir(self):
        print("Servidor muerto")
        raise ServidorMuerto()

    def abrir(self):
        try:
            self.serve_forever()
        except ServidorMuerto as e:
            raise(e)
        except:
            self.morir()
            return
            
if __name__ == '__main__': pass