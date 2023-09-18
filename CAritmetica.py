from abstract import abstract

class CAritmetica(abstract):
    
    def __init__(self,left,right,tipo,fila, columna):
        self.left = left
        self.right = right
        self.tipo = tipo
        super().__init__(fila, columna)
    
    def operar(self,arbol):
        leftValue = ''
        rightValue = ''
        if self.left != None:
            leftValue = self.left.operar(arbol)
        if self.right != None:
            rightValue = self.right.operar(arbol)
        
        if self.tipo.operar(arbol).lower() == 'suma':
            return round(leftValue + rightValue, 3)
        elif self.tipo.operar(arbol).lower()  == 'resta':
            return round(leftValue - rightValue, 3)
        elif self.tipo.operar(arbol).lower() == 'multiplicacion':
            return round(leftValue * rightValue, 3)
        elif self.tipo.operar(arbol).lower() == 'division':
            return round(leftValue / rightValue, 3)
        elif self.tipo.operar(arbol).lower() == 'modulo':
            return round(leftValue % rightValue, 3)
        elif self.tipo.operar(arbol).lower() == 'potencia':
            return round(leftValue ** rightValue, 3)
        elif self.tipo.operar(arbol).lower() == 'raiz':
            return round(leftValue ** (1/rightValue), 3)
        
        else:
            return 0      
    
    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()