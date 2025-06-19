import sys
from .lexer import Lexer
from .parser import Parser
from .semantic import SemanticAnalyzer
from .tools import DevelopmentTools

def compile_file(file_path, debug=False, visualize=False):
    """Compila un archivo VLS."""
    try:
        # Inicializar herramientas de desarrollo
        tools = DevelopmentTools()
        if debug:
            tools.start_debug()
        
        # Leer el archivo fuente
        with open(file_path, 'r') as file:
            source = file.read()
        
        # Análisis léxico
        lexer = Lexer(source)
        
        # Análisis sintáctico
        parser = Parser(lexer)
        ast = parser.program()
        
        # Visualizar AST si se solicita
        if visualize:
            tools.visualize_ast(ast)
        
        # Análisis semántico
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)
        
        # Si estamos en modo debug, exportar el gráfico de ejecución
        if debug:
            tools.export_execution_graph()
            tools.stop_debug()
        
        print("Compilación exitosa!")
        return True
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {file_path}")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def generate_example(concept):
    """Genera un ejemplo de código para un concepto específico."""
    tools = DevelopmentTools()
    example = tools.generate_example(concept)
    print(f"\nEjemplo de {concept}:")
    print(example)
    return example

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.vls> [--debug] [--visualize]")
        print("     python main.py --example <concepto>")
        sys.exit(1)
    
    if sys.argv[1] == '--example':
        if len(sys.argv) != 3:
            print("Uso: python main.py --example <concepto>")
            print("Conceptos disponibles: variables, operations, precedence")
            sys.exit(1)
        generate_example(sys.argv[2])
        sys.exit(0)
    
    file_path = sys.argv[1]
    if not file_path.endswith('.vls'):
        print("Error: El archivo debe tener extensión .vls")
        sys.exit(1)
    
    # Procesar opciones
    debug = '--debug' in sys.argv
    visualize = '--visualize' in sys.argv
    
    success = compile_file(file_path, debug, visualize)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 