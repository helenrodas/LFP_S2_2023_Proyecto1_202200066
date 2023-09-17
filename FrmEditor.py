import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from analizador_lexico import instruccion, operar_,archivo_final,clear,graficar_operaciones
# from analizador_lexico import analizador_lexico

class TextEditorApp:
    global content
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


    def save_file(self):
        global content
        file_path = self.file_path
        if file_path:
            content = self.text_widget.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
    
    def save_as_file(self):
        global content
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos", "*.json")])
        if file_path:
            content = self.text_widget.get(1.0, tk.END)
            with open(file_path, 'w+') as file:
                file.write(content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")

    def update_line_numbers(self, event=None):
        line_count = self.text_widget.get('1.0', tk.END).count('\n')
        if line_count != self.current_line:
            self.line_number_bar.config(state=tk.NORMAL)
            self.line_number_bar.delete(1.0, tk.END)
            for line in range(1, line_count + 1):
                self.line_number_bar.insert(tk.END, f"{line}\n")
            self.line_number_bar.config(state=tk.DISABLED)
            self.current_line = line_count
    
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
                    resultados_as_string += str(f"Operacion: {operacion}: {resultado.tipo.operar(None)} = {resultado.operar(None)}") + "\n"
                    operacion += 1
                # print(resultado.operar(None))
            messagebox.showinfo("Resultados",resultados_as_string)
        except:
            messagebox.showinfo("Error", "No se encontro archivo para analizar")
    
    def errores(self):
        try:
            archivo_final()
            messagebox.showinfo("Archivo salida", "Se genero archivo de errores")
        except:
            messagebox.showinfo("Error", "No se pudo crear archivo de errores")
    
    def reporte_grafica(self):
        try:
            graficar_operaciones()
            messagebox.showinfo("Grafica", "Grafica creada exitosamente")
        except:
            messagebox.showinfo("Error", "No se pudo crear grafica")
            
            


if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()