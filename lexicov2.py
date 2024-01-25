import tkinter as tk
from tkinter import ttk, messagebox
import ply.lex as lex

# Define tokens
tokens = [
    'Reservadas',
    'ID',
    'NUMBER',
    'LlavesApertura',
    'LlavesCerradura',
    'Asignacion',
    'ParentesisApertura',
    'ParentesisCerradura',
    'Comillas',
    'TipoDato',
    'Coma',
    'Operadores',
]

# Define reserved words
reserved = {
    'int': 'TipoDato',
    'string': 'TipoDato',
    'Fn': 'Reservadas',
    'contenido': 'Reservadas',
    'if': 'Reservadas',
    'else': 'Reservadas',
    'while': 'Reservadas',
    'switch': 'Reservadas',
    'case': 'Reservadas',
    'default': 'Reservadas',
    'break': 'Reservadas',
    'rtn': 'Reservadas',
    'print': 'Reservadas'
}

tokens += list(reserved.values())

# Token patterns
t_ParentesisApertura = r'\('
t_ParentesisCerradura = r'\)'
t_LlavesApertura = r'\{'
t_LlavesCerradura = r'\}'
t_Comillas = r'"'
t_Coma = r','
t_Asignacion = r'=>'
t_Operadores = r'(>=|<=|==|!=|>|<)'

def t_ID(t):
    r'[a-zA-Z_0-9]+'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  
    return t

t_ignore = ' \t\n'

def t_error(t):
    error_table.insert('', 'end', values=(f"Caracter no reconocido: '{t.value[0]}'",))
    t.lexer.skip(1)

lexer = lex.lex()

def check_code():
    # Limpia las tablas de tokens y errores
    token_table.delete(*token_table.get_children())
    error_table.delete(*error_table.get_children())

    # Obtiene el texto del usuario
    code = txt.get("1.0", tk.END).strip()
    if not code:
        messagebox.showinfo("Información", "No hay código para verificar.")
        return

    # Procesa el código con el analizador léxico
    lexer.input(code)
    try:
        for token in lexer:
            token_table.insert('', 'end', values=(token.type, token.value))
        # messagebox.showinfo("Información", "Análisis léxico completado sin errores.")
    except Exception as e:
        print("Error", str(e))
        # messagebox.showerror("Error", str(e))

# Parte de la interfaz gráfica relacionada con el analizador léxico
root = tk.Tk()
root.title("Analizador Lexico")
root.configure(bg='white')

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

codigo = '''numero => int(99)'''
txt = tk.Text(main_frame, width=40, height=20)
txt.grid(row=0, column=0, padx=10, pady=10)
txt.insert(tk.END, codigo)

btn = tk.Button(main_frame, text="Analizar", command=check_code, width=10, height=2)
btn.grid(row=1, column=0, padx=10, pady=10)

token_frame = ttk.LabelFrame(main_frame, text="Tokens", padding=10)
token_frame.grid(row=0, column=1, padx=10, pady=10)

token_table = ttk.Treeview(token_frame, columns=('Type', 'Value'), show='headings')
token_table.heading('Type', text='Token')
token_table.heading('Value', text='Lexema')
token_table.pack()

error_frame = ttk.LabelFrame(main_frame, text="Errores Generales", padding=10)
error_frame.grid(row=1, column=1, padx=10, pady=10)

error_table = ttk.Treeview(error_frame, columns=('Error',), show='headings')
error_table.heading('Error', text='Mensaje de Error')
error_table.column('Error', width=200)
error_table.pack()

result_label = tk.Label(main_frame, text="", fg="red")
result_label.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
