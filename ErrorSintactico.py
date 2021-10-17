class ErrorSintactico:
    def __init__(self, token, lexema, tipo, fila, columna):
        self.token = token
        self.lexema = lexema
        self.tipo = tipo
        self.fila = fila
        self.columna = columna