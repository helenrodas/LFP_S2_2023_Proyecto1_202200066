from CAritmetica import CAritmetica
from CTrigonometricas import CTrigonometrica
from CLexema import CLexema
from abstract import abstract
from COperacion import COperacion
from CError import CError
import json
import os


reversed = {
    'OPERACIONES' : 'operaciones',
    'OPERACION' : 'operacion',
    'Valor1' : 'valor1',
    'Valor2' : 'valor2',
    'SUMA' : 'suma',
    'RESTA': 'resta',
    'MULTIPLICACIÓN' : 'multiplicacion',
    'DIVISIÓN' : 'division',
    'POTENCIA' : 'potencia',
    'RAIZ' : 'raiz',
    'INVERSO' : 'inverso',
    'SENO' : 'seno',
    'COSENO' : 'coseno',
    'TANGENTE' : 'tangente',
    'MOD' : 'mod',
    'CONFIGURACIONES' : 'configuraciones',
    'TEXTO' : 'texto',
    'FONDO' : 'fondo',
    'FUENTE' :'fuente',
    'FORMA' : 'forma',
    'COMA' : ',',
    'PUNTO' : '.',
    'PUNTOS': ':',
    'CORCHETEA' : '[',
    'CORCHETEC' : ']',
    'LLAVEA' : '{',
    'LLAVEC' : '}'
}

lexemas = list(reversed.values())
global linea
global columna
global instruccion
global lista_lexemas
global instruccioness
global lista_lexemas_errores
global textos
global fondo
global fuente
global forma

linea = 1
columna = 1
lista_lexemas = []
instruccion = []
instruccioness = []
lista_lexemas_errores= []


def instruccion(cadena):
    global linea
    global columna
    global lista_lexemas
    global lista_lexemas_errores
    lexema =''
    puntero = 0
    contador = 1
    while cadena:
        caracter = cadena [puntero]
        puntero += 1
        
        if caracter == '\"':
            lexema, cadena = crear_lexema(cadena[puntero:])
            if lexema and cadena:
                columna += 1
                lex = CLexema(lexema,linea,columna)
                lista_lexemas.append(lex)
                columna += len(lexema) + 1
                puntero = 0
        elif caracter.isdigit():
            token,cadena = get_num(cadena)
            if token and cadena:
                columna += 1
                numero = COperacion(token,linea,columna)
                lista_lexemas.append(numero)
                columna += len(str(token))+1
                puntero = 0
        elif caracter == '[' or caracter == ']':
            char = CLexema(caracter,linea,columna)
            lista_lexemas.append(char)
            cadena = cadena[1:]
            puntero = 0
            columna += 1
        elif  caracter == '\t':
            columna += 4
            cadena = cadena[4:]
            puntero = 0
        elif caracter == '\n':
            cadena = cadena[1:]
            puntero = 0
            linea += 1
            columna = 1
        elif caracter == ' ' or caracter == '\r' or caracter == '{' or caracter == '}' or caracter == ',' or caracter == '.' or caracter == ':' :
            cadena = cadena[1:]
            puntero = 0
            columna += 1
        else:
            cadena = cadena[1:]
            puntero = 0
            columna += 1
            lista_lexemas_errores.append(CError(contador,caracter,"Error Lexico",linea,columna))
            contador +=1
    return lista_lexemas


def crear_lexema(cadena):
    global linea
    global columna
    global lista_lexemas
    lexema =''
    puntero = ''
    for caracter in cadena:
        puntero += caracter
        if caracter == '\"':
            return lexema,cadena[len(puntero):]
        else:
            lexema += caracter
    return None,None

def get_num(cadena):
    num = ''
    puntero = ''
    decimal = False
    for caracter in cadena:
        puntero += caracter
        if caracter == '.':
            decimal = True
        if caracter == '"' or caracter == ' ' or caracter == '\n' or caracter == '\t' or caracter == ',':
            if decimal:
                return round(float(num), 3), cadena[len(puntero)-1:]
            else:
                return int(num), cadena[len(puntero)-1:]
        else:
            num += caracter
    return None, None

def operar():
    global lista_lexemas
    global instruccion
    global textos
    global fondo
    global fuente
    global forma
    operacion = ''
    n1 = ''
    n2 = ''
    while lista_lexemas:
        CLexema = lista_lexemas.pop(0)
        if CLexema.operar(None)=='operacion':
            operacion = lista_lexemas.pop(0)
        elif CLexema.operar(None) == 'valor1':
            n1=lista_lexemas.pop(0)
            if n1.operar(None) == '[':
                n1=operar()
        elif CLexema.operar(None) == 'valor2':
            n2=lista_lexemas.pop(0)
            if n2.operar(None) == '[':
                n2=operar()
                
        if CLexema.operar(None) == 'textos':
            textos = lista_lexemas.pop(0)
            
        if CLexema.operar(None) == 'fondo':
            fondo = lista_lexemas.pop(0)
            
        if CLexema.operar(None) == 'fuente':
            fuente = lista_lexemas.pop(0)
            
        if CLexema.operar(None) == 'forma':
            forma  = lista_lexemas.pop(0)

        
        if operacion and n1 and n2:
            return CAritmetica(n1, n2, operacion, f'Inicio:{operacion.getFila()}: {operacion.getColumna()}', f'Fin: {n2.getFila()}:{n2.getColumna()}')
            
        elif operacion and n1 and operacion.operar(None) == ('seno' or 'coseno' or 'tangente'):
            return CTrigonometrica( n1,operacion, f'Inicio:{operacion.getFila()}: {operacion.getColumna()}', f'Fin: {n1.getFila()}:{n1.getColumna()}')
    return None
            

def operar_():
    global instruccioness
    
    while True:
        operacion = operar()
        if operacion:
            instruccioness.append(operacion)
        else:
            break
        
    return instruccioness

def getErrores():
    global lista_lexemas_errores
    return lista_lexemas_errores

def archivo_final():
    global lista_lexemas_errores
    lista_temp = {}
    lista_temp["Errores"] = []
    
    for error in lista_lexemas_errores:
        lista_temp["Errores"].append({
            'No.' : error.contador,
            'descripcion ' :{
                'lexema' : error.lexema_error,
                'tipo' : error.tipo_error,
                'columna' : error.columna,
                'fila' : error.fila
            }
        })
    
    with open('RESULTADOS_202200066.json','w') as file:
        json.dump(lista_temp,file,indent=4)

def clear():
    linea = 1
    columna = 1
    lista_lexemas.clear()
    instruccioness.clear()
    lista_lexemas_errores.clear()

def graficar_operaciones():
        global instruccioness

        texto = """digraph G {
                    label=" """+textos.lexema+""""
                    rankdir="TB"
                    node[style=filled, color=" """+fondo.lexema+"""", fontcolor=" """+fuente.lexema+"""", shape="""+forma.lexema+""", width=1.0, height=1.0]"""

        for i in range(len(instruccioness)):
            texto += nodos_grafica(instruccioness[i], i, 0, '')
            # texto += nodos_grafica(instruccioness[i], i, 0,'')
            

        texto += "\n}"
        f = open('bb.dot', 'w')

        f.write(texto)
        f.close()
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        os.system(f'dot -Tpng bb.dot -o GRAFICA_202200066.png')
    

def nodos_grafica(operacion, numero, llave, barra):
        valor = ""

        if operacion:
            if type(operacion) == COperacion:
                
                valor += f'nodo{numero}{llave}{barra}[label="{operacion.operar(None)}"];\n'


            if type(operacion) == CAritmetica:
                valor += f'nodo{numero}{llave}{barra}[label="{operacion.tipo.lexema}\\n{operacion.operar(None)}"];\n'

                valor += nodos_grafica(operacion.left ,numero, llave+1, barra+"_left")

                valor += f'nodo{numero}{llave}{barra} -> nodo{numero}{llave+1}{barra}_left;\n'

                valor += nodos_grafica(operacion.right,numero, llave+1, barra+"_right")

                valor += f'nodo{numero}{llave}{barra} -> nodo{numero}{llave+1}{barra}_right;\n'
            
            if type(operacion) == CTrigonometrica:
                
                valor += f'nodo{numero}{llave}{barra}[label="{operacion.tipo.lexema}\\n{operacion.operar(None)}"];\n'

                valor += nodos_grafica(operacion.left,numero, llave+1, barra+"_tri")

                valor += f'nodo{numero}{llave}{barra} -> nodo{numero}{llave+1}{barra}_tri;\n'


        return valor
    
