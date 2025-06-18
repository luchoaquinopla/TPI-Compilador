import sys
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer

def compile_file(file_path):
    """Compila un archivo VLS."""
    try:
        # Leer el archivo fuente
        with open(file_path, 'r') as file:
            source = file.read()
        
        # Análisis léxico
        lexer = Lexer(source)
        
        # Análisis sintáctico
        parser = Parser(lexer)
        ast = parser.program()
        
        # Análisis semántico
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)
        
        print("Compilación exitosa!")
        return True
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {file_path}")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.vls>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not file_path.endswith('.vls'):
        print("Error: El archivo debe tener extensión .vls")
        sys.exit(1)
    
    success = compile_file(file_path)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 