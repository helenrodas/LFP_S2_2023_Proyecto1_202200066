from abstract import abstract

class CError(abstract):
    def __init__(self, contador,lexema_error,tipo_error, fila, columna):
        self.lexema_error= lexema_error
        self.contador = contador
        self.tipo_error  = tipo_error
        super().__init__(fila, columna)
    
    def operar(self, arbol):
        return self.lexema
    
    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()