import sys
import os

# Agregar el directorio src al path de Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.lexer import Lexer

def mostrar_tokens(codigo_fuente):
    """Función para mostrar los tokens generados por el analizador léxico."""
    print("\nCódigo fuente:")
    print("-------------")
    print(codigo_fuente)
    print("\nTokens generados:")
    print("-----------------")
    
    # Crear el analizador léxico
    lexer = Lexer(codigo_fuente)
    
    # Obtener tokens hasta encontrar EOF
    while True:
        token = lexer.get_next_token()
        print(f"Token: {token}")
        
        # Salir cuando encontremos el token EOF
        if token.type.name == 'EOF':
            break

# Ejemplo 1: Declaración y asignación de variables
codigo1 = """
var x;
var y;
x = 5;
y = 10;
"""

# Ejemplo 2: Operaciones aritméticas
codigo2 = """
var resultado;
resultado = 5 + 3 * 2;
"""

# Ejemplo 3: Impresión de resultados
codigo3 = """
var a;
var b;
a = 10;
b = 5;
print(a + b);
print(a * b);
"""

# Ejecutar los ejemplos
print("\n=== Ejemplo 1: Declaración y asignación de variables ===")
mostrar_tokens(codigo1)

print("\n=== Ejemplo 2: Operaciones aritméticas ===")
mostrar_tokens(codigo2)

print("\n=== Ejemplo 3: Impresión de resultados ===")
mostrar_tokens(codigo3) 