from Token import Token
from ErrorSintactico import ErrorSintactico

class AnalizadorSintactico:
    tokens = []
    Errores = []
    ErrorBoolean = False
    boolUp = False
    boolLimitator = False
    position = 0
    preanalisis = ""
    types = Token("lexema", 0, 0, 0)
    ultimoCont = 0
    limitators = [types.CORCHETE_CIERRA, types.LLAVE_CIERRA, types.PUNTO_Y_COMA]

    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens.append(Token("$", self.types.ULTIMO, 0, 0))
        self.preanalisis = self.tokens[self.position].getType()
        self.Instrucciones()

    def Match(self, singleToken):
        if self.preanalisis != singleToken:
            self.Errores.append(ErrorSintactico(self.tokens[self.position].getLexema(), "Sintactico", "Se esperaba " + singleToken,
            self.tokens[self.position].getRow(), self.tokens[self.position].getColumns()))
            self.ErrorBoolean = True
            self.boolLimitator = True
            print("Error en el Token " + self.preanalisis + ", se esperaba " + singleToken)
            if self.preanalisis in self.limitators:
                self.boolLimitator = False
                print("---------------------Limitador Detectado---------------------")
            if self.boolUp:
                self.position += 1
                self.preanalisis = self.tokens[self.position].getType()
            else:
                self.preanalisis = self.tokens[self.position].getType()

        elif self.preanalisis != self.types.ULTIMO:
            print("Token correcto: " + str(self.preanalisis))
            if self.boolLimitator == True:
                if self.preanalisis in self.limitators:
                    self.boolLimitator = False
                    print("---------------------Limitador Detectado---------------------")
                    self.Errores.append(ErrorSintactico(self.tokens[self.position].getLexema(), "Sintactico", "Se esperaba " + singleToken,
                    self.tokens[self.position].getRow(), self.tokens[self.position].getColumns()))
                else:
                    print("******Error Agregado = " + self.preanalisis + "******")
                    self.Errores.append(ErrorSintactico(self.tokens[self.position].getLexema(), "Sintactico", "Se esperaba " + singleToken,
                    self.tokens[self.position].getRow(), self.tokens[self.position].getColumns()))
            self.position += 1
            self.preanalisis = self.tokens[self.position].getType()
        else:
            print("\n")
            print("Analisis Sintáctico Finalizado")
            print("\n")

    def Instrucciones(self):
        #-------------------------Arreglos-------------------------
        if self.preanalisis == self.types.CLAVES:
            self.boolUp = True
            self.Match(self.types.CLAVES)
            self.Match(self.types.IGUAL)
            self.Match(self.types.CORCHETE_ABRE)
            self.ListaStrings()
            self.Match(self.types.CORCHETE_CIERRA)
            self.Instrucciones()
        
        elif self.preanalisis == self.types.REGISTROS:
            self.boolUp = True
            self.Match(self.types.REGISTROS)
            self.Match(self.types.IGUAL)
            self.Match(self.types.CORCHETE_ABRE)
            self.ListaRegistros()
            self.Match(self.types.CORCHETE_CIERRA)
            self.Instrucciones()

        #-------------------------Comentarios-------------------------
        elif self.preanalisis == self.types.COMENTMULT:
            self.boolUp = False

            self.Match(self.types.COMENTMULT)
            self.Instrucciones()

        elif self.preanalisis == self.types.COMENTSIMPLE:
            self.boolUp = False

            self.Match(self.types.COMENTSIMPLE)
            self.Instrucciones()

        #-------------------------Funciones-------------------------
        elif self.preanalisis == self.types.IMPRIMIR:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()
        elif self.preanalisis == self.types.IMPRIMIRLN:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()
        elif self.preanalisis == self.types.CONTEO:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()
        elif self.preanalisis == self.types.PROMEDIO:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()
        elif self.preanalisis == self.types.CONTARSI:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()
        elif self.preanalisis == self.types.DATOS:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()
        elif self.preanalisis == self.types.SUMAR:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()
        elif self.preanalisis == self.types.MAX:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()
        elif self.preanalisis == self.types.MIN:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()
        elif self.preanalisis == self.types.EXPORTARREPORTE:
            self.boolUp = False
            self.Funciones()
            self.Instrucciones()

        #-------------------------Ultimo-------------------------
        elif self.preanalisis == self.types.ULTIMO:
                self.Match(self.types.ULTIMO)

        else:
            self.Match(self.types.UNKNOWN)
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
            self.Match(self.types.COMMA)
            self.Match(self.types.NUMBER)
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