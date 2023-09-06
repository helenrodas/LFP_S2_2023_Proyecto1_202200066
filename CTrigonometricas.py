from abstract import abstract
from math import *

class CTrigonometrica(abstract):
    def __init__(self,left,tipo,fila, columna):
        self.left = left
        self.tipo = tipo
        super().__init__(fila, columna)
    
    def operar(self, arbol):
        leftValue = ''
        if self.left != None:
            leftValue = self.left.operar(arbol)
        if self.tipo == 'Seno':
            return sin(leftValue)
        elif self.tipo == 'Coseno':
            return cos(leftValue)
        elif self.tipo == 'Tangente':
            return tan(leftValue)
        else:
            return None