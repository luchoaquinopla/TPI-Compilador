#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from lexer import Lexer
from parser import Parser

def debug_parser():
    # Código de prueba simple
    code = """var x;
var y;
x = 5;
y = 3;
si (x mayor y) entonces
    print(x);
fin_si;"""
    
    print("=== DEBUG DEL PARSER ===")
    print("Código fuente:")
    print(code)
    print("\n=== ANÁLISIS LÉXICO ===")
    
    # Análisis léxico
    lexer = Lexer(code)
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        print(f"Token: {token}")
        if token.type.name == 'EOF':
            break
    
    print("\n=== ANÁLISIS SINTÁCTICO ===")
    
    # Análisis sintáctico
    lexer_for_parser = Lexer(code)
    parser = Parser(lexer_for_parser)
    
    try:
        print("Creando parser...")
        print("Generando AST...")
        ast = parser.program()
        print(f"¡Éxito! AST generado con {len(ast)} nodos principales")
        
        # Mostrar estructura básica
        for i, node in enumerate(ast):
            print(f"Nodo {i}: {type(node).__name__}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print("Traceback completo:")
        print(traceback.format_exc())

if __name__ == "__main__":
    debug_parser() 