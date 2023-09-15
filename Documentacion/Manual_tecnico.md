# Manual Tecnico

## Helen Rodas - 202200066

### El proyecto de analizador lexico consta de 8 archivos de python, el primero es la interfaz grafica, el  siguiente es el analizador_lexico el cual contiene la mayor parte de la logica asi como el archivo abstract. Los demas archivos son clases para ver que tipo de operacion es, ya sea aritmetica o trigonometrica, o tambien para guardar errores de tipo lexicos o los lexemas en general.

## FrmEditor
En este archivo se maneja la interfaz grafica y las opciones del menu

- El constructor de la clase donde se inicializa la primera pantalla del menu
```python
    def __init__(self, root):
        self.root = root
        self.root.title("Menu")
        self.file_path = None
        

        self.line_number_bar = tk.Text(root, width=4, padx=4, takefocus=0, border=0, background='lightblue', state='disabled')
        self.line_number_bar.pack(side=tk.LEFT, fill=tk.Y)

    

        self.text_widget = ScrolledText(self.root, wrap=tk.WORD)
        self.text_widget=ScrolledText(root,width=150,height=50)
        self.text_widget.pack(expand=True, fill='both')
        # self.text_widget.pack(side=tk.TOP, fill=tk.Y)

        self.text_widget.bind('<Key>', self.update_line_numbers)
        self.text_widget.bind('<MouseWheel>', self.update_line_numbers)

        self.current_line = 1

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Abrir", command=self.open_file)
        self.file_menu.add_command(label="Guardar", command=self.save_file)
        self.file_menu.add_command(label="Guardar Como", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.root.quit)
        
        self.menu_bar.add_cascade(label="Analizar", command=self.analizar)
        self.menu_bar.add_cascade(label="Errores", command=self.errores)
        self.menu_bar.add_cascade(label="Reporte", command=self.reporte_grafica)
```
- Opcion openfile(): funciona para que pueda abrir el archivo tipo json desde los archivos de la computadora
```python
def open_file(self):
        clear()
        global content
        file_path = filedialog.askopenfilename(filetypes=[("Archivos json", "*.json")])
        self.file_path = file_path 
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)
            self.update_line_numbers()
```
- Opcion savefile(): guarda el archivo ya existente pero modificado de tipo json
```python
def save_file(self):
        global content
        file_path = self.file_path
        if file_path:
            content = self.text_widget.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
```
- Opcion save_as_file(): guarda un archivo nuevo de tipo json
```python
def save_as_file(self):
        global content
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos", "*.json")])
        if file_path:
            content = self.text_widget.get(1.0, tk.END)
            with open(file_path, 'w+') as file:
                file.write(content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
```
- Opcion analizar(): esta opcion llamara a la funcion para leer, analizar y leer las operaciones del archivo json
```python
def analizar(self):
        try:
            clear()
            global content
            instruccion(content)
            resultados = operar_()
            resultados_as_string = ""
            operacion = 1
            for resultado in resultados:
                if isinstance(resultado.operar(None), int) or isinstance(resultado.operar(None),float) == True:
                    resultados_as_string += str(f"Operacion: {operacion} --> {resultado.tipo.operar(None)} = {resultado.operar(None)}") + "\n"
                    operacion += 1
                # print(resultado.operar(None))
            messagebox.showinfo("Resultados",resultados_as_string)
        except:
            messagebox.showinfo("Error", "No se encontro archivo para analizar")
```
- Opcion errores(): esta opcion va a identificar los errores que trae el json para luego presentarlos al usuario.
```python
def errores(self):
        try:
            archivo_final()
            messagebox.showinfo("Archivo salida", "Se genero archivo de errores")
        except:
            messagebox.showinfo("Error", "No se pudo crear archivo de errores")
```
- En esta funcion se van incrementado los numeros laterales de la vista cada vez que se escribe en una nueva linea.
```python
def update_line_numbers(self, event=None):
        line_count = self.text_widget.get('1.0', tk.END).count('\n')
        if line_count != self.current_line:
            self.line_number_bar.config(state=tk.NORMAL)
            self.line_number_bar.delete(1.0, tk.END)
            for line in range(1, line_count + 1):
                self.line_number_bar.insert(tk.END, f"{line}\n")
            self.line_number_bar.config(state=tk.DISABLED)
            self.current_line = line_count
```
- Esta funcion inicializa el programa
```python
if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()
```
## abstract
Esta clase sirve para que funcione como herencia para obtener el tipo de operacion que se va a realizar, obtener fila y la columna.
```python
def __init__(self,fila,columna):
        self.fila = fila
        self.columna = columna
    
    @abstractmethod
    def operar(self,arbol):
        pass
    
    @abstractmethod
    def getFila(self):
        return self.fila
    
    @abstractmethod
    def getColumna(self):
        return self.columna
```
## analizador_lexico
En esta clase se maneja la mayoria de la logica del programa ya que analiza los lexemas, operaciones y los errores.

- primero se inicializan las listas y algunas variables como globales pues mas adelante se van a utilizar.
```python
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
```
- En el metodo instruccion() se va a leer el archivo y se va crear la lista_lexemas donde se guardaran los caracteres que son permitidos asi como su fila y columna. Tambien se crea la lista_errores donde guarda los caracteres que no estan permitidos en el archivo.
```python
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
```
- en crear_lexema() se forma los lexemas que estan permitidos
```python
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
```
- get_num() regresa el valor numerico para que se pueda operar, ya sea decimal o entero.
```python
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
```
- operar() va a tomar los valores numericos y el tipo de operacion que tiene que realizar con cada uno.
```python
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
```