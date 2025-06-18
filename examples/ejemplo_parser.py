import sys
import os

# Agregar el directorio src al path de Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.lexer import Lexer
from src.parser import Parser, BinOp, Num, Var, Assign, Print, VarDecl

def mostrar_ast(nodo, nivel=0):
    """Función para mostrar el AST de forma visual."""
    indentacion = "  " * nivel
    
    if isinstance(nodo, list):
        for item in nodo:
            mostrar_ast(item, nivel)
        return
    
    if isinstance(nodo, BinOp):
        print(f"{indentacion}BinOp: {nodo.op.type}")
        print(f"{indentacion}  Izquierda:")
        mostrar_ast(nodo.left, nivel + 2)
        print(f"{indentacion}  Derecha:")
        mostrar_ast(nodo.right, nivel + 2)
    
    elif isinstance(nodo, Num):
        print(f"{indentacion}Num: {nodo.value}")
    
    elif isinstance(nodo, Var):
        print(f"{indentacion}Var: {nodo.value}")
    
    elif isinstance(nodo, Assign):
        print(f"{indentacion}Assign:")
        print(f"{indentacion}  Variable:")
        mostrar_ast(nodo.left, nivel + 2)
        print(f"{indentacion}  Valor:")
        mostrar_ast(nodo.right, nivel + 2)
    
    elif isinstance(nodo, Print):
        print(f"{indentacion}Print:")
        mostrar_ast(nodo.expr, nivel + 2)
    
    elif isinstance(nodo, VarDecl):
        print(f"{indentacion}VarDecl:")
        mostrar_ast(nodo.var_node, nivel + 2)

# Ejemplo 1: Operación aritmética simple
codigo1 = """
var x;
x = 5 + 3 * 2;
"""

# Ejemplo 2: Múltiples operaciones y variables
codigo2 = """
var a;
var b;
a = 10;
b = 5;
print(a + b);
print(a * b);
"""

# Ejemplo 3: Expresiones complejas
codigo3 = """
var resultado;
resultado = (5 + 3) * 2;
print(resultado);
"""

def analizar_codigo(codigo, titulo):
    print(f"\n=== {titulo} ===")
    print("\nCódigo fuente:")
    print("-------------")
    print(codigo)
    
    # Crear el lexer y el parser
    lexer = Lexer(codigo)
    parser = Parser(lexer)
    
    # Obtener el AST
    ast = parser.program()
    
    print("\nÁrbol de Sintaxis Abstracta (AST):")
    print("--------------------------------")
    mostrar_ast(ast)

# Analizar los ejemplos
analizar_codigo(codigo1, "Ejemplo 1: Operación aritmética simple")
analizar_codigo(codigo2, "Ejemplo 2: Múltiples operaciones y variables")
analizar_codigo(codigo3, "Ejemplo 3: Expresiones complejas") 