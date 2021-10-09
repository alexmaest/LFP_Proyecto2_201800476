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
                self.position += 1
                try:
                    self.preanalisis = self.tokens[self.position].getType()
                except:
                    self.position -= 2
                    self.preanalisis = self.tokens[self.position].getType()
            else:
                if self.ultimoCont == 0:
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
                        self.ultimoCont += 1
                    else:
                        pass


        elif self.preanalisis != self.types.ULTIMO:
            print("Token correcto: " + str(self.preanalisis))
            self.position += 1
            self.preanalisis = self.tokens[self.position].getType()
        else:
            print("\n")
            print("Analisis Sintáctico Finalizado")
            print("\n")

    def Instrucciones(self):

        #-------------------------Arreglos-------------------------
        if self.preanalisis == self.types.CLAVES:
            self.Match(self.types.CLAVES)
            self.Match(self.types.IGUAL)
            self.Match(self.types.CORCHETE_ABRE)
            self.ListaStrings()
            self.Match(self.types.CORCHETE_CIERRA)
        
        elif self.preanalisis == self.types.REGISTROS:
            self.Match(self.types.REGISTROS)
            self.Match(self.types.IGUAL)
            self.Match(self.types.CORCHETE_ABRE)
            self.ListaRegistros()
            self.Match(self.types.CORCHETE_CIERRA)

        #-------------------------Comentarios-------------------------
        elif self.preanalisis == self.types.COMENTMULT:
            self.Match(self.types.COMENTMULT)

        elif self.preanalisis == self.types.COMENTSIMPLE:
            self.Match(self.types.COMENTSIMPLE)

        #-------------------------Funciones-------------------------
        elif self.preanalisis == self.types.IMPRIMIR:
            self.Funciones()
        elif self.preanalisis == self.types.IMPRIMIRLN:
            self.Funciones()
        elif self.preanalisis == self.types.CONTEO:
            self.Funciones()
        elif self.preanalisis == self.types.PROMEDIO:
            self.Funciones()
        elif self.preanalisis == self.types.CONTARSI:
            self.Funciones()
        elif self.preanalisis == self.types.DATOS:
            self.Funciones()
        elif self.preanalisis == self.types.SUMAR:
            self.Funciones()
        elif self.preanalisis == self.types.MAX:
            self.Funciones()
        elif self.preanalisis == self.types.MIN:
            self.Funciones()
        elif self.preanalisis == self.types.EXPORTARREPORTE:
            self.Funciones()

        #-------------------------Ultimo-------------------------
        if self.preanalisis == self.types.ULTIMO:
            self.Match(self.types.ULTIMO)

        #--------------------Más instrucciones--------------------
        elif self.preanalisis != None:
            self.Instrucciones()

    def ListaStrings(self):
        self.Match(self.types.STRING)
        if self.preanalisis == self.types.COMMA:
            self.Match(self.types.COMMA)
            self.ListaStrings()
    
    def ListaRegistros(self):
        self.Match(self.types.LLAVE_ABRE)
        self.ListaValores()
        self.Match(self.types.LLAVE_CIERRA)
        if self.preanalisis == self.types.LLAVE_ABRE:
            self.ListaRegistros()
    
    def ListaValores(self):
        if self.preanalisis == self.types.NUMBER:
            self.Match(self.types.NUMBER)
            if self.preanalisis == self.types.COMMA:
                self.Match(self.types.COMMA)
                self.ListaValores()
        elif self.preanalisis == self.types.STRING:
            self.Match(self.types.STRING)
            if self.preanalisis == self.types.COMMA:
                self.Match(self.types.COMMA)
                self.ListaValores()
        elif self.preanalisis == self.types.DOUBLE:
            self.Match(self.types.DOUBLE)
            if self.preanalisis == self.types.COMMA:
                self.Match(self.types.COMMA)
                self.ListaValores()
    
    def Funciones(self):
        if self.preanalisis == self.types.IMPRIMIR:
            self.Match(self.types.IMPRIMIR)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)

        elif self.preanalisis == self.types.IMPRIMIRLN:
            self.Match(self.types.IMPRIMIRLN)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)

        elif self.preanalisis == self.types.CONTEO:
            self.Match(self.types.CONTEO)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)

        elif self.preanalisis == self.types.PROMEDIO:
            self.Match(self.types.PROMEDIO)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)

        elif self.preanalisis == self.types.CONTARSI:
            self.Match(self.types.CONTARSI)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.STRING)
            if self.preanalisis == self.types.COMMA:
                self.Match(self.types.COMMA)
                self.ListaValores()
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)

        elif self.preanalisis == self.types.DATOS:
            self.Match(self.types.DATOS)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)

        elif self.preanalisis == self.types.SUMAR:
            self.Match(self.types.SUMAR)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)

        elif self.preanalisis == self.types.MAX:
            self.Match(self.types.MAX)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)

        elif self.preanalisis == self.types.MIN:
            self.Match(self.types.MIN)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            
        elif self.preanalisis == self.types.EXPORTARREPORTE:
            self.Match(self.types.EXPORTARREPORTE)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
        