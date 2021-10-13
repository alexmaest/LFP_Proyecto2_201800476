from tkinter.constants import S
from Token import Token
from ErrorSintactico import ErrorSintactico
from reporteRegistros import reporteRegistros

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
    #Funciones
    functionError = False
    Claves = []
    clavesCont = 0
    singleClaves = []
    singleRegistros = []
    Registros = []
    registrosCont = 0
    reportError = False
    consoleText = ""

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
            #print("Error en el Token " + self.preanalisis + ", se esperaba " + singleToken)
            self.functionError = True
            if self.preanalisis in self.limitators:
                self.boolLimitator = False
                #print("---------------------Limitador Detectado---------------------")
            if self.boolUp:
                self.position += 1
                self.preanalisis = self.tokens[self.position].getType()
            else:
                self.preanalisis = self.tokens[self.position].getType()

        elif self.preanalisis != self.types.ULTIMO:
            #print("Token correcto: " + str(self.preanalisis))
            if self.boolLimitator == True:
                if self.preanalisis in self.limitators:
                    self.boolLimitator = False
                    #print("---------------------Limitador Detectado---------------------")
                    self.Errores.append(ErrorSintactico(self.tokens[self.position].getLexema(), "Sintactico", "Se esperaba " + singleToken,
                    self.tokens[self.position].getRow(), self.tokens[self.position].getColumns()))
                else:
                    #print("******Error Agregado = " + self.preanalisis + "******")
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
            self.Claves = []
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
            self.Registros = []
            self.registrosCont = 0
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
        singleString = self.tokens[self.position].getLexema()
        self.Match(self.types.STRING)
        if self.functionError == False:
            clean = singleString.replace("\"", "")
            self.Claves.append(clean)
            self.clavesCont += 1
        else:
            self.reportError == True
        self.functionError = False
        if self.preanalisis == self.types.COMMA:
            self.Match(self.types.COMMA)
            self.ListaStrings()
    
    def ListaRegistros(self):
        self.Match(self.types.LLAVE_ABRE)
        self.ListaValores()
        if self.functionError == False:
            self.Registros.append(self.singleRegistros)
            self.registrosCont += 1
        else:
            self.reportError == True
        self.singleRegistros = []
        self.functionError = False
        self.Match(self.types.LLAVE_CIERRA)
        if self.preanalisis == self.types.LLAVE_ABRE:
            self.ListaRegistros()
    
    def ListaValores(self):
        tempLexema = self.tokens[self.position].getLexema()
        if self.preanalisis == self.types.NUMBER:
            if self.functionError == False:
                self.singleRegistros.append(tempLexema)
            else:
                self.reportError == True
            self.Match(self.types.NUMBER)
            if self.preanalisis == self.types.COMMA:
                self.Match(self.types.COMMA)
                self.ListaValores()
        elif self.preanalisis == self.types.STRING:
            if self.functionError == False:
                self.singleRegistros.append(tempLexema)
            else:
                self.reportError == True
            self.Match(self.types.STRING)
            if self.preanalisis == self.types.COMMA:
                self.Match(self.types.COMMA)
                self.ListaValores()
        elif self.preanalisis == self.types.DOUBLE:
            if self.functionError == False:
                self.singleRegistros.append(tempLexema)
            else:
                self.reportError == True
            self.Match(self.types.DOUBLE)
            if self.preanalisis == self.types.COMMA:
                self.Match(self.types.COMMA)
                self.ListaValores()
    
    def Funciones(self):
        if self.preanalisis == self.types.IMPRIMIR:
            self.boolUp = True
            self.Match(self.types.IMPRIMIR)
            self.Match(self.types.PARENTESIS_ABRE)
            letras = self.tokens[self.position].getLexema()
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            if self.functionError == False:
                lPrint = letras.replace("\"", "")
                self.consoleText += lPrint
                print(lPrint, end = '')
            self.functionError = False

        elif self.preanalisis == self.types.IMPRIMIRLN:
            self.boolUp = True
            self.Match(self.types.IMPRIMIRLN)
            self.Match(self.types.PARENTESIS_ABRE)
            letras2 = self.tokens[self.position].getLexema()
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            if self.functionError == False:
                lPrint2 = letras2.replace("\"", "")
                self.consoleText += lPrint2 + "\n"
                print(lPrint2)
            self.functionError = False

        elif self.preanalisis == self.types.CONTEO:
            self.boolUp = True
            self.Match(self.types.CONTEO)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            if self.functionError == False:
                print(str(self.registrosCont))
                self.consoleText += str(self.registrosCont) + "\n"
            self.functionError = False

        elif self.preanalisis == self.types.PROMEDIO:
            self.boolUp = True
            self.Match(self.types.PROMEDIO)
            self.Match(self.types.PARENTESIS_ABRE)
            arg1 = self.tokens[self.position].getLexema()
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            promCont = 0
            plus = 0
            prom = 0
            found = False
            if self.functionError == False:
                arg = arg1.replace("\"", "")
                for clave in self.Claves:
                    if clave == arg:
                        for registro in self.Registros:
                            plus += float(registro[promCont])
                        prom = round(plus / self.registrosCont, 2)
                        print(str(prom))
                        self.consoleText += str(prom) + "\n"
                        found = True
                        break
                    else:
                        promCont += 1
                if found == False:
                    text = "Argumento de la función promedio() no encontrado"
                    self.consoleText += text + "\n"
            promCont = 0
            self.functionError = False

        elif self.preanalisis == self.types.CONTARSI:
            self.boolUp = True
            self.Match(self.types.CONTARSI)
            self.Match(self.types.PARENTESIS_ABRE)
            arg1 = self.tokens[self.position].getLexema()
            self.Match(self.types.STRING)
            self.Match(self.types.COMMA)
            arg2 = self.tokens[self.position].getLexema()
            self.ListaValores()
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            found = False
            contarCont = 0
            foundCont = 0
            if self.functionError == False:
                arg = arg1.replace("\"", "")
                for clave in self.Claves:
                    if clave == arg:
                        for registro in self.Registros:
                            value = registro[contarCont]
                            if value == arg2:
                                foundCont += 1
                        print(str(foundCont))
                        self.consoleText += str(foundCont) + "\n"
                        found = True
                        break
                    else:
                        contarCont += 1
                if found == False:
                    text = "Argumento de la función contarsi() no encontrado"
                    self.consoleText += text + "\n"
            contarCont = 0
            self.functionError = False

        elif self.preanalisis == self.types.DATOS:
            self.boolUp = True
            self.Match(self.types.DATOS)
            self.Match(self.types.PARENTESIS_ABRE)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            if self.functionError == False:
                for data in self.Claves:
                    print(data + "       ", end = '')
                    self.consoleText += str(data) + "   "
                print("\n")
                self.consoleText += "\n"
                for registro in self.Registros:
                    for single in registro:
                        print(single + "       ", end = '')
                        self.consoleText += str(single) + "   "
                    print("\n")
                    self.consoleText += "\n"
            self.functionError = False

        elif self.preanalisis == self.types.SUMAR:
            self.boolUp = True
            self.Match(self.types.SUMAR)
            self.Match(self.types.PARENTESIS_ABRE)
            arg1 = self.tokens[self.position].getLexema()
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            found = False
            plus = 0
            sumarCont = 0
            if self.functionError == False:
                arg = arg1.replace("\"", "")
                for clave in self.Claves:
                    if clave == arg:
                        for registro in self.Registros:
                            plus += float(registro[sumarCont])
                        print(str(plus))
                        self.consoleText += str(plus) + "\n"
                        found = True
                        break
                    else:
                        sumarCont += 1
                if found == False:
                    text = "Argumento de la función sumar() no encontrado"
                    self.consoleText += text + "\n"
            self.functionError = False

        elif self.preanalisis == self.types.MAX:
            self.boolUp = True
            self.Match(self.types.MAX)
            self.Match(self.types.PARENTESIS_ABRE)
            arg1 = self.tokens[self.position].getLexema()
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            found = False
            value = 0
            maxCont = 0
            maxValue = 0
            if self.functionError == False:
                arg = arg1.replace("\"", "")
                for clave in self.Claves:
                    if clave == arg:
                        for registro in self.Registros:
                            value = float(registro[maxCont])
                            if value > maxValue:
                                maxValue = value
                        print(str(maxValue))
                        self.consoleText += str(maxValue) + "\n"
                        found = True
                        break
                    else:
                        maxCont += 1
                if found == False:
                    text = "Argumento de la función max() no encontrado"
                    self.consoleText += text + "\n"
            self.functionError = False

        elif self.preanalisis == self.types.MIN:
            self.boolUp = True
            self.Match(self.types.MIN)
            self.Match(self.types.PARENTESIS_ABRE)
            arg1 = self.tokens[self.position].getLexema()
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)
            found = False
            value = 0
            minCont = 0
            minValue = 0
            if self.functionError == False:
                arg = arg1.replace("\"", "")
                for clave in self.Claves:
                    if clave == arg:
                        for registro in self.Registros:
                            minValue = float(registro[minCont])
                            break
                        found = True
                        break
                    else:
                        minCont += 1
                        
                for registro in self.Registros:
                    value = float(registro[minCont])
                    if value < minValue:
                        minValue = value
                print(str(minValue))
                self.consoleText += str(minValue) + "\n"

                if found == False:
                    text = "Argumento de la función min() no encontrado"
                    self.consoleText += text + "\n"
            self.functionError = False
            
        elif self.preanalisis == self.types.EXPORTARREPORTE:
            self.boolUp = True
            self.Match(self.types.EXPORTARREPORTE)
            self.Match(self.types.PARENTESIS_ABRE)
            arg1 = self.tokens[self.position].getLexema()
            self.Match(self.types.STRING)
            self.Match(self.types.PARENTESIS_CIERRA)
            self.Match(self.types.PUNTO_Y_COMA)     
            if self.functionError == False:
                if self.reportError == False:
                    argClean = arg1.replace("\"", "")
                    reporteRegistros(argClean, self.Claves, self.Registros)
            self.functionError = False
        
    #Getters
    def getClaves(self):
        return self.Claves

    def getRegistros(self):
        return self.Registros
    
    def getConsoleText(self):
        return self.consoleText