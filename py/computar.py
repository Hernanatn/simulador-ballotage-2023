

class Computador():

    def __init__(self, valores : dict) -> None:
        self.votosValidos   : int = int(valores['votosValidos'])
        self.votantesNuevos : int = int(valores['votantesNuevos'])

        self.massaSTM       : int = int(valores['massaSTM'])
        self.mileiSTM : int = int(valores['mileiSTM'])
        self.schiarettiSTM   : int = int(valores['schiarettiSTM'])
        self.bregmanSTM : int = int(valores['bregmanSTM'])
        self.nuevosSTM : int = int(valores['nuevosSTM'])

        self.massaJM       : int = int(valores['massaJM'])
        self.mileiJM : int = int(valores['mileiJM'])
        self.schiarettiJM   : int = int(valores['schiarettiJM'])
        self.bregmanJM : int = int(valores['bregmanJM'])
        self.nuevosJM : int = int(valores['nuevosJM'])

    @property
    def NoAfirmativos(self) -> int:
        return self.validos - devolverAfirmativos()

    @property
    def Afirmativos(self) -> int:
        return (sum([self.massaSTM,self.mileiSTM,self.schiarettiSTM,self.bregmanSTM,self.nuevosSTM]) + sum([self.massaJM,self.mileiJM,self.schiarettiJM,self.bregmanJM,self.nuevosJM]))

    @property
    def votosSTM(self) -> int:
        return sum([self.massaSTM,self.mileiSTM,self.schiarettiSTM,self.bregmanSTM,self.nuevosSTM])

    @property
    def votosJM(self) -> int:
        return sum([self.massaJM,self.mileiJM,self.schiarettiJM,self.bregmanJM,self.nuevosJM])

    @property
    def mitadMasUno(self) -> int:
        return round(self.Afirmativos/2)+1

    def generarHTML(self) -> str:
        base : str
        with open("../html/resultado.html","r",encoding="utf-8") as plantilla:
            base = plantilla.read()
        
        ganador = "Sergio Tomás Massa" if votosSTM > votosJM else "Javier Gerardo Milei"
        rutaImagen = "../recursos/imagenes/stm-ganador.png" if votosSTM > votosJM else "../recursos/imagenes/jgm-ganador.png"
        cantidadVotos = max(votosSTM,votosJM)

        resultado = base\
                    .replace("[VOTOS-TOTALES]",self.Afirmativos)\
                    .replace("[MITAD-MAS-UNO]",self.mitadMasUno)\
                    .replace("[GANADOR]",ganador)\
                    .replace("[IMAGEN-GANADOR]",rutaImagen)\
                    .replace("[CANTIDAD-VOTOS]",cantidadVotos)\
                    .replace("[PORCENTAJE]",round(cantidadVotos/self.Afirmativos,2))\

        return resultado