from Token import Token
import graphviz

class treeReport:
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
    stringCont = 0
    registCont = 0
    nameCont = 0
    valueCont = 0
    ComentCont = 0 
    Functions = 0

    g = graphviz.Graph('G', filename='reportes/derivationTree.gv')
    init = "Inicio"
    g.node(init, init)


    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens.append(Token("$", self.types.ULTIMO, 0, 0))
        self.preanalisis = self.tokens[self.position].getType()
        self.Instrucciones()

    def Match(self, singleToken):
        if self.preanalisis != singleToken:
            self.ErrorBoolean = True
            self.boolLimitator = True
            self.functionError = True
            if self.preanalisis in self.limitators:
                self.boolLimitator = False
            if self.boolUp:
                self.position += 1
                self.preanalisis = self.tokens[self.position].getType()
            else:
                self.preanalisis = self.tokens[self.position].getType()

        elif self.preanalisis != self.types.ULTIMO:
            if self.boolLimitator == True:
                if self.preanalisis in self.limitators:
                    self.boolLimitator = False
            self.position += 1
            self.preanalisis = self.tokens[self.position].getType()
        else:
            print("\n")
            print("Reporte Graphviz generado")
            print("\n")
            self.g.view()

    def Instrucciones(self):
        self.boolUp = False
        #-------------------------Arreglos-------------------------
        if self.preanalisis == self.types.CLAVES:
            self.Claves = []
            self.boolUp = True

            one = self.tokens[self.position].getLexema()
            self.g.node("theone", one)
            self.g.edge(self.init, "theone")
            self.Match(self.types.CLAVES)

            two = self.tokens[self.position].getLexema()
            self.g.node("thetwo", two)
            self.g.edge("theone", "thetwo")
            self.Match(self.types.IGUAL)

            three = self.tokens[self.position].getLexema()
            self.g.node("thethree", three)
            self.g.edge("theone", "thethree")
            self.Match(self.types.CORCHETE_ABRE)

            strings = "ListaStrings"
            self.g.node("theoneLS", strings)
            self.g.edge("theone", "theoneLS")
            self.ListaStrings()

            four = self.tokens[self.position].getLexema()
            self.g.node("thefour", four)
            self.g.edge("theone", "thefour")
            self.Match(self.types.CORCHETE_CIERRA)
            self.Instrucciones()
        
        elif self.preanalisis == self.types.REGISTROS:
            self.boolUp = True

            regist = self.tokens[self.position].getLexema()
            self.g.node("theregist", regist)
            self.g.edge(self.init, "theregist")
            self.Match(self.types.REGISTROS)

            equal1 = self.tokens[self.position].getLexema()
            self.g.node("theequal1", equal1)
            self.g.edge("theregist", "theequal1")
            self.Match(self.types.IGUAL)

            cor1 = self.tokens[self.position].getLexema()
            self.g.node("thecor1", cor1)
            self.g.edge("theregist", "thecor1")
            self.Match(self.types.CORCHETE_ABRE)

            self.Registros = []
            self.registrosCont = 0
            regist = "ListaRegistros"
            self.registCont += 1
            self.g.node("theLR"+ str(self.registCont), regist)
            self.g.edge("theregist", "theLR"+ str(self.registCont))
            self.ListaRegistros()

            corC1 = self.tokens[self.position].getLexema()
            self.g.node("thecorC1", corC1)
            self.g.edge("theregist", "thecorC1")
            self.Match(self.types.CORCHETE_CIERRA)
            self.Instrucciones()

        #-------------------------Comentarios-------------------------
        elif self.preanalisis == self.types.COMENTMULT:
            if self.ComentCont == 0:
                self.boolUp = False
                AllComent = "Cometarios"
                self.g.node(AllComent, AllComent)
                self.g.edge(self.init, AllComent)
                comment = self.tokens[self.position].getLexema()
                self.g.node("theCM" + str(self.ComentCont), comment)
                self.g.edge(AllComent, "theCM" + str(self.ComentCont))
                self.Match(self.types.COMENTMULT)
                self.ComentCont += 1 
                self.Instrucciones()
            else:
                self.boolUp = False
                AllComent = "Cometarios"
                comment = self.tokens[self.position].getLexema()
                self.g.node("theCM" + str(self.ComentCont), comment)
                self.g.edge(AllComent, "theCM" + str(self.ComentCont))
                self.Match(self.types.COMENTMULT)
                self.ComentCont += 1 
                self.Instrucciones()

        elif self.preanalisis == self.types.COMENTSIMPLE:
            if self.ComentCont == 0:
                self.boolUp = False
                AllComent = "Cometarios"
                self.g.node(AllComent, AllComent)
                self.g.edge(self.init, AllComent)
                comment = self.tokens[self.position].getLexema()
                self.g.node("theCS" + str(self.ComentCont), comment)
                self.g.edge(AllComent, "theCS" + str(self.ComentCont))
                self.Match(self.types.COMENTSIMPLE)
                self.ComentCont += 1 
                self.Instrucciones()
            else:
                self.boolUp = False
                AllComent = "Cometarios"
                comment = self.tokens[self.position].getLexema()
                self.g.node("theCS" + str(self.ComentCont), comment)
                self.g.edge(AllComent, "theCS" + str(self.ComentCont))
                self.Match(self.types.COMENTSIMPLE)
                self.ComentCont += 1 
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
            self.boolUp = True
            self.Instrucciones()

    def ListaStrings(self):
        singleString = self.tokens[self.position].getLexema()
        self.stringCont += 1
        self.g.node("theone" + str(self.stringCont), singleString)
        self.g.edge("theoneLS", "theone" + str(self.stringCont))
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
        self.nameCont += 1
        LlaA = self.tokens[self.position].getLexema()
        self.g.node("theLA" + str(self.nameCont), LlaA)
        self.g.edge("theLR"+ str(self.registCont), "theLA" + str(self.nameCont))
        self.Match(self.types.LLAVE_ABRE)
        valores = "ListaValores"
        self.g.node("theLV" + str(self.nameCont), valores)
        self.g.edge("theLR"+ str(self.registCont), "theLV" + str(self.nameCont))
        self.ListaValores()
        if self.functionError == False:
            self.Registros.append(self.singleRegistros)
            self.registrosCont += 1
        else:
            self.reportError == True
        self.singleRegistros = []
        self.functionError = False
        LlaC = self.tokens[self.position].getLexema()
        self.g.node("theLlaC"+ str(self.nameCont), LlaC)
        self.g.edge("theLR"+ str(self.registCont), "theLlaC"+ str(self.nameCont))
        self.Match(self.types.LLAVE_CIERRA)
        if self.preanalisis == self.types.LLAVE_ABRE:
            self.ListaRegistros()
    
    def ListaValores(self):
        self.valueCont += 1
        value = self.tokens[self.position].getLexema()
        tempLexema = self.tokens[self.position].getLexema()
        if self.preanalisis == self.types.NUMBER:
            if self.functionError == False:
                self.g.node("number" + str(self.valueCont), value)
                self.g.edge("theLV"+ str(self.nameCont), "number" + str(self.valueCont))
                self.singleRegistros.append(tempLexema)
            else:
                self.reportError == True
            self.Match(self.types.NUMBER)
            if self.preanalisis == self.types.COMMA:
                value1 = self.tokens[self.position].getLexema()
                self.Match(self.types.COMMA)
                self.g.node("comma1" + str(self.valueCont), value1)
                self.g.edge("theLV"+ str(self.nameCont), "comma1" + str(self.valueCont))
                self.ListaValores()

        elif self.preanalisis == self.types.STRING:
            if self.functionError == False:
                self.g.node("string" + str(self.valueCont), value)
                self.g.edge("theLV"+ str(self.nameCont), "string" + str(self.valueCont))
                self.singleRegistros.append(tempLexema)
            else:
                self.reportError == True
            self.Match(self.types.STRING)
            if self.preanalisis == self.types.COMMA:
                value2 = self.tokens[self.position].getLexema()
                self.Match(self.types.COMMA)
                self.g.node("comma2" + str(self.valueCont), value2)
                self.g.edge("theLV"+ str(self.nameCont), "comma2" + str(self.valueCont))
                self.ListaValores()

        elif self.preanalisis == self.types.DOUBLE:
            if self.functionError == False:
                self.g.node("double" + str(self.valueCont), value)
                self.g.edge("theLV"+ str(self.nameCont), "double" + str(self.valueCont))
                self.singleRegistros.append(tempLexema)
            else:
                self.reportError == True
            self.Match(self.types.DOUBLE)
            if self.preanalisis == self.types.COMMA:
                value3 = self.tokens[self.position].getLexema()
                self.Match(self.types.COMMA)
                self.g.node("comma3" + str(self.valueCont), value3)
                self.g.edge("theLV"+ str(self.nameCont), "comma3" + str(self.valueCont))
                self.ListaValores()

        else:
            self.Match(self.types.UNKNOWN)
            self.boolUp = True
            self.reportError == True


    def Funciones(self):
        AllFunctions = "Funciones"
        if self.Functions == 0:
            self.g.node(AllFunctions, AllFunctions)
            self.g.edge(self.init, AllFunctions)
            self.Functions += 1

        self.Functions += 1
        if self.preanalisis == self.types.IMPRIMIR:
            imprimir = "imprimir"
            self.g.node(imprimir + str(self.Functions), imprimir)
            self.g.edge(AllFunctions, imprimir + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(imprimir + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.IMPRIMIR)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(imprimir + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            try:
                letras = self.tokens[self.position].getLexema()
            except:
                letras = ""
                self.functionError == True
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(imprimir + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.STRING)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(imprimir + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(imprimir + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PUNTO_Y_COMA)
            if self.functionError == False:
                lPrint = letras.replace("\"", "")
                self.consoleText += lPrint
                #print(l#Print, end = '')
            self.functionError = False

        elif self.preanalisis == self.types.IMPRIMIRLN:
            imprimirln = "imprimirln"
            self.g.node(imprimirln + str(self.Functions), imprimirln)
            self.g.edge(AllFunctions, imprimirln + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(imprimirln + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.IMPRIMIRLN)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(imprimirln + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            try:
                letras2 = self.tokens[self.position].getLexema()
            except:
                letras2 = ""
                self.functionError == True
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(imprimirln + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.STRING)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(imprimirln + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(imprimirln + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PUNTO_Y_COMA)
            if self.functionError == False:
                lPrint2 = letras2.replace("\"", "")
                self.consoleText += lPrint2 + "\n"
                #print(l#Print2)
            self.functionError = False

        elif self.preanalisis == self.types.CONTEO:
            conteo = "conteo"
            self.g.node(conteo + str(self.Functions), conteo)
            self.g.edge(AllFunctions, conteo + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(conteo + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.CONTEO)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(conteo + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(conteo + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(conteo + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PUNTO_Y_COMA)
            if self.functionError == False:
                #print(str(self.registrosCont))
                self.consoleText += str(self.registrosCont) + "\n"
            self.functionError = False

        elif self.preanalisis == self.types.PROMEDIO:
            promedio = "promedio"
            self.g.node(promedio + str(self.Functions), promedio)
            self.g.edge(AllFunctions, promedio + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(promedio + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.PROMEDIO)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(promedio + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            try:
                arg1 = self.tokens[self.position].getLexema()
            except:
                arg1 = ""
                self.functionError == True
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(promedio + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.STRING)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(promedio + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(promedio + str(self.Functions), function + str(self.Functions))
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
                        #print(str(prom))
                        self.consoleText += str(prom) + "\n"
                        found = True
                        break
                    else:
                        promCont += 1
                if found == False:
                    text = "Argumento de la función promedio() no encontrado"
                    self.consoleText += text + "\n"
            self.functionError = False

        elif self.preanalisis == self.types.CONTARSI:
            contarsi = "contarsi"
            self.g.node(contarsi + str(self.Functions), contarsi)
            self.g.edge(AllFunctions, contarsi + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(contarsi + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.CONTARSI)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(contarsi + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            try:
                arg1 = self.tokens[self.position].getLexema()
            except:
                arg1 = ""
                self.functionError == True
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(contarsi + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.STRING)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(contarsi + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.COMMA)
            try:
                arg2 = self.tokens[self.position].getLexema()
            except:
                arg2 = ""
                self.functionError == True
            self.ListaValores()
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(contarsi + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(contarsi + str(self.Functions), function + str(self.Functions))
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
                        #print(str(foundCont))
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
            datos = "datos"
            self.g.node(datos + str(self.Functions), datos)
            self.g.edge(AllFunctions, datos + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(datos + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.DATOS)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(datos + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(datos + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(datos + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PUNTO_Y_COMA)
            if self.functionError == False:
                for data in self.Claves:
                    #print(data + "       ", end = '')
                    self.consoleText += str(data) + "   "
                #print("\n")
                self.consoleText += "\n"
                for registro in self.Registros:
                    for single in registro:
                        #print(single + "       ", end = '')
                        self.consoleText += str(single) + "   "
                    #print("\n")
                    self.consoleText += "\n"
            self.functionError = False

        elif self.preanalisis == self.types.SUMAR:
            sumar = "sumar"
            self.g.node(sumar + str(self.Functions), sumar)
            self.g.edge(AllFunctions, sumar + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(sumar + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.SUMAR)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(sumar + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            try:
                arg1 = self.tokens[self.position].getLexema()
            except:
                arg1 = ""
                self.functionError == True
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(sumar + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.STRING)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(sumar + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(sumar + str(self.Functions), function + str(self.Functions))
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
                        #print(str(plus))
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
            maxN = "max"
            self.g.node(maxN + str(self.Functions), maxN)
            self.g.edge(AllFunctions, maxN + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(maxN + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.MAX)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(maxN + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            try:
                arg1 = self.tokens[self.position].getLexema()
            except:
                arg1 = ""
                self.functionError == True
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(maxN + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.STRING)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(maxN + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(maxN + str(self.Functions), function + str(self.Functions))
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
                        #print(str(maxValue))
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
            minN = "min"
            self.g.node(minN + str(self.Functions), minN)
            self.g.edge(AllFunctions, minN + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(minN + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.MIN)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(minN + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            try:
                arg1 = self.tokens[self.position].getLexema()
            except:
                arg1 = ""
                self.functionError == True
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(minN + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.STRING)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(minN + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(minN + str(self.Functions), function + str(self.Functions))
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
                #print(str(minValue))
                self.consoleText += str(minValue) + "\n"

                if found == False:
                    text = "Argumento de la función min() no encontrado"
                    self.consoleText += text + "\n"
            self.functionError = False
            
        elif self.preanalisis == self.types.EXPORTARREPORTE:
            exr = "exportarReporte"
            self.g.node(exr + str(self.Functions), exr)
            self.g.edge(AllFunctions, exr + str(self.Functions))
            self.boolUp = False
            function = self.tokens[self.position].getLexema()
            self.g.node(function + "fun" + str(self.Functions), function)
            self.g.edge(exr + str(self.Functions), function + "fun" + str(self.Functions))
            self.Match(self.types.EXPORTARREPORTE)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(exr + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_ABRE)
            try:
                arg1 = self.tokens[self.position].getLexema()
            except:
                arg1 = ""
                self.functionError == True
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(exr + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.STRING)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(exr + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PARENTESIS_CIERRA)
            function = self.tokens[self.position].getLexema()
            self.g.node(function + str(self.Functions), function)
            self.g.edge(exr + str(self.Functions), function + str(self.Functions))
            self.Match(self.types.PUNTO_Y_COMA)     
            if self.functionError == False:
                if self.reportError == False:
                    argClean = arg1.replace("\"", "")
            self.functionError = False