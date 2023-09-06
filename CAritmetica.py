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
        
        if self.tipo == 'Suma':
            return leftValue + rightValue
        elif self.tipo == 'Resta':
            return leftValue - rightValue
        elif self.tipo == 'Multiplicacion':
            return leftValue + rightValue
        elif self.tipo == 'Division':
            return leftValue / rightValue
        elif self.tipo == 'Modulo':
            return leftValue % rightValue
        elif self.tipo == 'Potencia':
            return leftValue ** rightValue
        elif self.tipo == 'Raiz':
            return leftValue ** (1/rightValue)
        elif self.tipo == 'Inverso':
            return 1/leftValue 
        else:
            return None       