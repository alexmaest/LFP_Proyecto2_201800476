class Token:
    lexema = ""
    type = 0
    row = 0
    column = 0
 
    CLAVES = "CLAVES"
    REGISTROS = "REGISTROS"
    IMPRIMIR = "IMPRIMIR"
    IMPRIMIRLN = "IMPRIMIRLN"
    CONTEO = "CONTEO"
    PROMEDIO = "PROMEDIO"
    CONTARSI = "CONTARSI"
    DATOS = "DATOS"
    SUMAR = "SUMAR"
    MAX = "MAX"
    MIN = "MIN"
    EXPORTARREPORTE = "EXPORTARREPORTE"

    STRING = "CADENA"
    NUMBER = "NUMERO"
    DOUBLE = "DECIMAL"
    IGUAL = "IGUAL"
    LLAVE_ABRE = "LLAVE_ABRE"
    LLAVE_CIERRA = "LLAVE_CIERRA"
    CORCHETE_ABRE = "CORCHETE_ABRE"
    CORCHETE_CIERRA = "CORCHETE_CIERRA"
    COMMA = "COMMA"
    PARENTESIS_ABRE = "PARENTESIS_ABRE"
    PARENTESIS_CIERRA = "PARENTESIS_CIERRA"
    PUNTO_Y_COMA = "PUNTO_Y_COMA"
    UNKNOWN = "DESCONOCIDO"
    COMENTSIMPLE = "COMENTARIO_SIMPLE"
    COMENTMULT = "COMENTARIO_MULTIPLE"
    ULTIMO = "ULTIMO"

    def __init__(self, lexema, type, row, column):
        self.lexema = lexema
        self.type = type
        self.row = row
        self.column = column

    def getLexema(self):
        return self.lexema
    
    def getRow(self):
        return self.row
    
    def getColumns(self):
        return self.column
    
    def getType(self):
        if self.type == self.CLAVES:
            return "CLAVES"
        elif self.type == self.REGISTROS:
            return "REGISTROS"
        elif self.type == self.IMPRIMIR:
            return "IMPRIMIR"
        elif self.type == self.IMPRIMIRLN:
            return "IMPRIMIRLN"
        elif self.type == self.CONTEO:
            return "CONTEO"
        elif self.type == self.PROMEDIO:
            return "PROMEDIO"
        elif self.type == self.CONTARSI:
            return "CONTARSI"
        elif self.type == self.DATOS:
            return "DATOS"
        elif self.type == self.SUMAR:
            return "SUMAR"
        elif self.type == self.MAX:
            return "MAX"
        elif self.type == self.MIN:
            return "MIN"
        elif self.type == self.EXPORTARREPORTE:
            return "EXPORTARREPORTE"
        elif self.type == self.STRING:
            return "CADENA"
        elif self.type == self.NUMBER:
            return "NUMERO"
        elif self.type == self.DOUBLE:
            return "DECIMAL"
        elif self.type == self.IGUAL:
            return "IGUAL"
        elif self.type == self.LLAVE_ABRE:
            return "LLAVE_ABRE"
        elif self.type == self.LLAVE_CIERRA:
            return "LLAVE_CIERRA"
        elif self.type == self.CORCHETE_ABRE:
            return "CORCHETE_ABRE"
        elif self.type == self.CORCHETE_CIERRA:
            return "CORCHETE_CIERRA"
        elif self.type == self.COMMA:
            return "COMMA"
        elif self.type == self.PARENTESIS_ABRE:
            return "PARENTESIS_ABRE"
        elif self.type == self.PARENTESIS_CIERRA:
            return "PARENTESIS_CIERRA"
        elif self.type == self.PUNTO_Y_COMA:
            return "PUNTO_Y_COMA"
        elif self.type == self.UNKNOWN:
            return "DESCONOCIDO"
        elif self.type == self.COMENTSIMPLE:
            return "COMENTARIO_SIMPLE"
        elif self.type == self.COMENTMULT:
            return "COMENTARIO_MULTIPLE"
        elif self.type == self.ULTIMO:
            return "ULTIMO"        