class ErrorSintactico:
    def __init__(self, lexema, tipo, descripcion, fila, columna):
        self.lexema = lexema
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna