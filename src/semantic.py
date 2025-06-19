from .parser import AST, BinOp, Num, Var, Assign, Print, VarDecl

class SemanticError(Exception):
    pass

class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope_level = 0

    def define(self, symbol):
        """Define un nuevo símbolo en la tabla."""
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        """Busca un símbolo por su nombre."""
        return self.symbols.get(name)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_BinOp(self, node):
        """Visita un nodo de operación binaria."""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        # Verifica que ambos operandos sean números
        if not (isinstance(left_type, type) and isinstance(right_type, type)):
            raise SemanticError(f"Operación inválida: {node.op.type} entre {left_type} y {right_type}")
        
        return int  # El resultado de una operación binaria es siempre un número

    def visit_Num(self, node):
        """Visita un nodo de número."""
        return int

    def visit_Var(self, node):
        """Visita un nodo de variable."""
        var_name = node.value
        symbol = self.symbol_table.lookup(var_name)
        
        if symbol is None:
            raise SemanticError(f"Variable no declarada: {var_name}")
        
        return symbol.type

    def visit_Assign(self, node):
        """Visita un nodo de asignación."""
        var_name = node.left.value
        symbol = self.symbol_table.lookup(var_name)
        
        if symbol is None:
            raise SemanticError(f"Variable no declarada: {var_name}")
        
        value_type = self.visit(node.right)
        
        # Verificamos que el tipo del valor sea int
        if value_type != int:
            raise SemanticError(f"No se puede asignar {value_type} a una variable numérica")
        
        return value_type

    def visit_Print(self, node):
        """Visita un nodo de impresión."""
        return self.visit(node.expr)

    def visit_VarDecl(self, node):
        """Visita un nodo de declaración de variable."""
        var_name = node.var_node.value
        
        if self.symbol_table.lookup(var_name) is not None:
            raise SemanticError(f"Variable ya declarada: {var_name}")
        
        self.symbol_table.define(Symbol(var_name, int))
        return None

    def visit(self, node):
        """Método principal para visitar nodos del AST."""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Método genérico para visitar nodos no manejados específicamente."""
        raise SemanticError(f"No hay visitante para {type(node).__name__}")

    def analyze(self, ast):
        """Analiza el AST completo."""
        if isinstance(ast, list):
            for node in ast:
                self.visit(node)
        else:
            self.visit(ast) 