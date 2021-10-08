from Token import Token
from ErrorSintactico import ErrorSintactico

class AnalizadorSintactico:
    tokens = []
    Errores = []
    ErrorBoolean = False
    position = 0
    preanalisis = ""
    types = Token("lexema", 0, 0, 0)
    ultimoCont = 0

    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens.append(Token("$", self.types.ULTIMO, 0, 0))
        self.preanalisis = self.tokens[self.position].getType()
        self.Instrucciones()

    def Match(self, singleToken):
        if self.preanalisis != singleToken:
            if self.preanalisis != self.types.ULTIMO:
                self.Errores.append(ErrorSintactico(self.tokens[self.position].getLexema(), "Sintactico", "Se esperaba " + singleToken,
                self.tokens[self.position].getRow(), self.tokens[self.position].getColumns()))
                self.ErrorBoolean = True
                print("Error en el Token " + self.preanalisis + ", se esperaba " + singleToken)
                self.position += 2
                try:
                    self.preanalisis = self.tokens[self.position].getType()
                except:
                    self.position -= 2
                    self.preanalisis = self.tokens[self.position].getType()
            else:
                if self.ultimoCont == 0:
                    self.Errores.append(ErrorSintactico(self.tokens[self.position].getLexema(), "Sintactico", "Se esperaba " + singleToken,
                    self.tokens[self.position].getRow(), self.tokens[self.position].getColumns()))
                    self.ErrorBoolean = True
                    print("Error en el Token " + self.preanalisis + ", se esperaba " + singleToken)
                    self.position += 2
                    try:
                        self.preanalisis = self.tokens[self.position].getType()
                    except:
                        self.position -= 2
                        self.preanalisis = self.tokens[self.position].getType()
                    self.ultimoCont += 1


        elif self.preanalisis != self.types.ULTIMO:
            print("Token correcto: " + str(self.preanalisis))
            self.position += 1
            self.preanalisis = self.tokens[self.position].getType()
        else:
            print("\n")
            print("Analisis Sintáctico Finalizado")
            print("\n")

    def Instrucciones(self):

        if self.preanalisis == self.types.CLAVES:
            self.Match(self.types.CLAVES)
            self.Match(self.types.IGUAL)
            self.Match(self.types.CORCHETE_ABRE)
            self.ListaStrings()
            self.Match(self.types.CORCHETE_CIERRA)
        
        elif self.preanalisis == self.types.REGISTROS:
            pass

        elif self.preanalisis == self.types.COMENTMULT:
            pass

        elif self.preanalisis == self.types.COMENTSIMPLE:
            pass
        
        if self.preanalisis == self.types.ULTIMO:
            self.Match(self.types.ULTIMO)

        elif self.preanalisis != None:
            self.Instrucciones()

    def ListaStrings(self):
        self.Match(self.types.STRING)
        if self.preanalisis == self.types.COMMA:
            self.Match(self.types.COMMA)
            self.ListaStrings()
        else:
            pass