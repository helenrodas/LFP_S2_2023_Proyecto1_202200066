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
        if self.tipo.operar(arbol).lower() == 'seno':
            return round(sin(radians(leftValue)), 3)
        elif self.tipo.operar(arbol).lower() == 'coseno':
            return round(cos(radians(leftValue)), 3)
        elif self.tipo.operar(arbol).lower() == 'tangente':
            return round(tan(radians(leftValue)), 3)
        
        elif self.tipo.operar(arbol) == 'inverso':
            return  round(1/leftValue, 3)
        else:
            return 0
    
    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()