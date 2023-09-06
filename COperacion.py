from abstract import abstract

class COperacion(abstract):
    
    def __init__(self, valor,tipo,fila, columna):
        self.valor = valor
        self.tipo = tipo
        super().__init__(fila, columna)
    
    def operar(self,arbol):
        return self.valor