from CAritmetica import CAritmetica
from CTrigonometricas import CTrigonometrica
from CLexema import CLexema
from abstract import abstract
from COperacion import COperacion


reversed = {
    'OPERACIONES' : 'operaciones',
    'SUMA' : 'suma',
    'RESTA': 'resta',
    'MULTIPLICACIÓN' : 'multiplicacion',
    'DIVISIÓN' : 'division',
    'POTENCIA' : 'potencias',
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
global instrucciones
global lista_lexemas

linea = 1
columna = 1
lista_lexemas = []



def instruccion(cadena):
    global linea
    global columna
    global lista_lexemas
    lexema =''
    puntero = 0
    while cadena:
        caracter = cadena [puntero]
        puntero += 1
        
        if caracter == '\"':
            lexema, cadena = crear_lexema(cadena[puntero:])
            if lexema and cadena:
                columna += 1
                #Se arma el lexema como clase
                
                #Se agrega el lexema a la lista de lexemas
                lista_lexemas.append(lexema)
                columna += len(lexema) + 1
                puntero = 0
        elif caracter.isdigit():
            token,cadena = get_num(cadena)
            if token and cadena:
                columna += 1
                lista_lexemas.append(token)
                columna += len(str(token))+1
                puntero = 0
        elif caracter == '[' or caracter == ']':
            lista_lexemas.append(caracter)
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
        else:
            cadena = cadena[1:]
            puntero = 0
            columna += 1
    print("--------------------")
    for lexema in lista_lexemas:  #En caso de necesitar un reporte de lexemas
        print(lexema)
    print("--------------------")


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
                return float(num), cadena[len(puntero)-1:]
            else:
                return int(num), cadena[len(puntero)-1:]
        else:
            num += caracter
    return None, None


entrada = '''{
    "operaciones": [
        {
            "operacion": "restas",
            "valor1": 4.5,
            "valor2": 5.32
        },
        {
            "operacion": "resta",
            "valor1": 4.5,
            "valor2": [
                {
                    "operaciones": "potencias",
                    "valor1": 10,
                    "valor2": 3
                }
            ]
        },
        {
            "operacion": "suma",
            "valor1": [
                {
                    "operacion": "seno",
                    "valor1": 90
                }
            ],
            "valor2": 5.32
        },
        {
            "operaciones": "multiplicacion",
            "valor1": 7,
            "valor2": 3
        },
        {
            "operaciones": "division",
            "valor1": 15,
            "valor2": 3
        }
    ],
    "configuraciones": [
        {
            "textos": "Opercaiones",
            "fondo": "azul",
            "fuente": "blanco",
            "forma": "circulo"
        }
    ]
}'''

instruccion(entrada)
