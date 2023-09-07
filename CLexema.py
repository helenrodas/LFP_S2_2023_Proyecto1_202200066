from abstract import abstract

class CLexema(abstract):
    def __init__(self, lexema, fila, columna):
        self.lexema= lexema
        super().__init__(fila, columna)
    
    def operar(self, arbol):
        return self.lexema
    
    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()
