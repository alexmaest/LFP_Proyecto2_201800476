from Token import Token
import re

class AnalizadorLexico:
    lexema = ""
    tokens = []
    state = 1
    row = 0
    column = 0
    types = Token("lexema", 0, 0, 0)
    #aceptedSymbols = ["=","{","}","[","]",",","(",")",";"]

    def __init__(self, text):
        self.state = 1
        self.lexema = ""
        self.tokens = []
        self.row = 1
        self.column = 0
        self.comilla = 1
        text.append("$")
        #print(text)
        current = ""
        textLen = len(text)
        for index in range(textLen):
            #print("tituloDetect: " + str(self.tituloDetect) + ", anchoDetect: " + str(self.anchoDetect) + ", altoDetect: " + str(self.altoDetect) + ", filasDetect: " + str(self.filasDetect) + ", columnasDetect: " + str(self.columnasDetect) + ", celdasDetect: " + str(self.celdasDetect) + ", filtrosDetect: " + str(self.filtrosDetect) + ", singleFiltroDetect: " + str(self.singleFiltroDetect))
            columnLen = len(text[index])
            index2 = 0
            while index2 < columnLen:
                #print("index2: " + str(index2))
                current = text[index][index2]
                index2 += 1
                if self.state == 1:
                    if current.isalpha():
                        #print("Entra -> Current: " + str(current))
                        self.state = 2
                        self.column += 1
                        self.lexema += current
                        continue 
                    elif current.isdigit():
                        #print("Entra -> Current: " + str(current))
                        self.state = 3
                        self.column += 1
                        self.lexema += current
                        continue
                    elif current == "\"":
                        #print("Entra -> Current: " + str(current))
                        self.state = 7
                        self.column += 1
                        self.lexema += current
                        continue
                    elif current == "#":
                        #print("Entra -> Current: " + str(current))
                        self.state = 6
                        self.column += 1
                        self.lexema += current
                        continue
                    elif current == "\'":
                       #print("Entra -> Current: " + str(current))
                       self.state = 8
                       self.column += 1
                       self.lexema += current
                       self.commilla = 1
                       continue
                    elif current == "=":
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.IGUAL)
                        continue
                    elif current == "{":
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.LLAVE_ABRE)
                        continue
                    elif current == "}":
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.LLAVE_CIERRA)
                        continue
                    elif current == "[":
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.CORCHETE_ABRE)
                        continue
                    elif current == "]":
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.CORCHETE_CIERRA)
                        continue
                    elif current == ",":
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.COMMA)
                        continue
                    elif current == "(":
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.PARENTESIS_ABRE)
                        continue
                    elif current == ")":
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.PARENTESIS_CIERRA)
                        continue
                    elif current == ";":
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.PUNTO_Y_COMA)
                        continue
                    elif current == " ":
                        #print("Entra -> Current: " + str(current))
                        self.column += 1
                        self.state = 1
                        continue
                    elif current == "\n":
                        #print("Entra -> Current: " + str(current))
                        self.row += 1
                        self.column = 0
                        self.state = 1
                        continue
                    elif current == "\r":
                        #print("Entra -> Current: " + str(current))
                        self.state = 1
                        continue
                    elif current == "\t":
                        #print("Entra -> Current: " + str(current))
                        self.column += 5
                        self.state = 1
                        continue
                    elif current == "$" and index == textLen - 1:
                        self.printTokens()
                        print("\n")
                        print("Analisis Léxico Finalizado")
                        print("\n")
                        break
                    else:
                        #print("Entra -> Current: " + str(current))
                        self.lexema += current
                        self.column += 1
                        self.generateImage = False
                        self.addToken(self.types.UNKNOWN)
                        continue

                elif self.state == 2:
                    #print("Entra -> Current: " + str(current))
                    if current.isalpha():
                        self.state = 2
                        self.column += 1
                        self.lexema += current
                        continue
                    else:
                        if self.isReservedWord(self.lexema):
                            lexemaLower = self.lexema.lower()
                            if lexemaLower == "claves":
                                self.addToken(self.types.CLAVES)
                            elif lexemaLower == "registros":
                                self.addToken(self.types.REGISTROS)
                            elif lexemaLower == "imprimir":
                                self.addToken(self.types.IMPRIMIR)
                            elif lexemaLower == "imprimirln":
                                self.addToken(self.types.IMPRIMIRLN)
                            elif lexemaLower == "conteo":
                                self.addToken(self.types.CONTEO)
                            elif lexemaLower == "promedio":
                                self.addToken(self.types.PROMEDIO)
                            elif lexemaLower == "contarsi":
                                self.addToken(self.types.CONTARSI)
                            elif lexemaLower == "datos":
                                self.addToken(self.types.DATOS)
                            elif lexemaLower == "sumar":
                                self.addToken(self.types.SUMAR)
                            elif lexemaLower == "max":
                                self.addToken(self.types.MAX)
                            elif lexemaLower == "min":
                                self.addToken(self.types.MIN)
                            elif lexemaLower == "exportarreporte":
                                self.addToken(self.types.EXPORTARREPORTE)
                            index2 -= 1
                            continue
                        else:
                            self.lexema += current
                            self.column += 1
                            self.generateImage = False
                            self.addToken(self.types.UNKNOWN)
                            continue

                elif self.state == 3:
                    if current.isdigit():
                        self.state = 3
                        self.column += 1
                        self.lexema += current
                        continue
                    elif current == ".":
                        self.state = 4
                        self.column += 1
                        self.lexema += current
                        continue
                    else:
                        self.addToken(self.types.NUMBER)
                        index2 = index2 - 1
                        continue

                elif self.state == 4:
                    if current.isdigit():
                        self.state = 4
                        self.column += 1
                        self.lexema += current
                        continue
                    else:
                        self.addToken(self.types.DOUBLE)
                        index2 = index2 - 1
                        continue
                
                elif self.state == 6:
                    if current == "\n":
                        self.column += 1
                        self.addToken(self.types.COMENTSIMPLE)
                        self.column = 1
                        self.row += 1
                        continue
                    else:
                        self.state = 6
                        self.column += 1
                        self.lexema += current
                        continue
                
                elif self.state == 7:
                    if current != "\"":
                        self.state = 7
                        self.column += 1
                        self.lexema += current
                        continue
                    elif current == "\"":
                        self.lexema += current
                        self.column += 1
                        self.addToken(self.types.STRING)
                        continue
                
                elif self.state == 8:
                    if current == "\'":
                        self.comilla += 1

                    if current == "$" and index == textLen - 1:
                        self.addToken(self.types.UNKNOWN)
                        self.printTokens()
                        print("\n")
                        print("Analisis Léxico Finalizado")
                        print("\n")
                        break
                    
                    if self.comilla == 6:
                        self.lexema += current
                        if self.isCommentMult(self.lexema):
                            self.addToken(self.types.COMENTMULT)
                            continue
                        else:
                            self.addToken(self.types.UNKNOWN)
                            continue
                    else:
                        if current == "\n":
                            self.state = 8
                            self.row += 1
                            self.column = 1
                            self.lexema += current
                        elif current == "\r":
                            #print("Entra -> Current: " + str(current))
                            self.lexema += current
                            self.state = 8
                            continue
                        elif current == "\t":
                            #print("Entra -> Current: " + str(current))
                            self.lexema += current
                            self.column += 5
                            self.state = 8
                            continue    
                        else:
                            self.state = 8
                            self.column += 1
                            self.lexema += current
                            continue
        
    def addToken(self, type):
        self.tokens.append(Token(self.lexema, type, self.row, self.column))
        self.lexema = ""
        self.state = 1
    
    def isCommentMult(self, text):
        regex = "([\']{3}[^\'{3}]*[\']{3})"
        if re.search(regex, text):
            return True
        else:
            return False

    def isReservedWord(self, text):
        text2 = text.lower()
        isReserved = False
        reservedWords = ["claves","registros","imprimir","imprimirln","conteo","promedio","contarsi","datos","sumar","max","min","exportarreporte"]

        if text2 in reservedWords:
            isReserved = True
        return isReserved

    def printTokens(self):
        tempRow = 0
        for token in self.tokens:
            if token.row != tempRow:
                print("\n")
                print("Lexema: " + str(token.lexema) + ", tipo: " + str(token.type) + ", fila: " + str(token.row) + ", columna: " + str(token.column))
                tempRow = token.row
            else:
                print("Lexema: " + str(token.lexema) + ", tipo: " + str(token.type) + ", fila: " + str(token.row) + ", columna: " + str(token.column))
    
    def getTokens(self):
        return self.tokens