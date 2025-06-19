from parser import AST, BinOp, Num, Var, Assign, Print, VarDecl, Condition, LogicalOp, If, While, String

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
        
        # Concatenación de cadenas
        if node.op.type.name == 'CONCATENAR':
            if left_type == str and right_type == str:
                return str
            else:
                raise SemanticError("La operación 'concatenar' solo es válida entre cadenas")
        # Operaciones numéricas
        if left_type == int and right_type == int:
            return int
        raise SemanticError(f"Operación inválida: {node.op.type} entre {left_type} y {right_type}")

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
        
        # Permitimos asignar int o str
        if value_type not in (int, str):
            raise SemanticError(f"No se puede asignar {value_type} a una variable")
        
        # Actualiza el tipo de la variable en la tabla de símbolos
        symbol.type = value_type
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

    def visit_Condition(self, node):
        """Visita un nodo de condición."""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        # Verifica que ambos operandos sean números
        if left_type != int or right_type != int:
            raise SemanticError(f"Condición inválida: {node.op.type} entre {left_type} y {right_type}")
        
        return bool  # El resultado de una condición es siempre un booleano

    def visit_LogicalOp(self, node):
        """Visita un nodo de operación lógica."""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        # Verifica que ambos operandos sean booleanos
        if left_type != bool or right_type != bool:
            raise SemanticError(f"Operación lógica inválida: {node.op.type} entre {left_type} y {right_type}")
        
        return bool  # El resultado de una operación lógica es siempre un booleano

    def visit_If(self, node):
        """Visita un nodo de estructura condicional."""
        # Verifica que la condición sea booleana
        condition_type = self.visit(node.condition)
        if condition_type != bool:
            raise SemanticError(f"Condición del if debe ser booleana, no {condition_type}")
        
        # Analiza el cuerpo del then
        for statement in node.then_body:
            self.visit(statement)
        
        # Analiza el cuerpo del else si existe
        if node.else_body:
            for statement in node.else_body:
                self.visit(statement)
        
        return None

    def visit_While(self, node):
        """Visita un nodo de estructura de bucle."""
        # Verifica que la condición sea booleana
        condition_type = self.visit(node.condition)
        if condition_type != bool:
            raise SemanticError(f"Condición del while debe ser booleana, no {condition_type}")
        
        # Analiza el cuerpo del bucle
        for statement in node.body:
            self.visit(statement)
        
        return None

    def visit_String(self, node):
        """Visita un nodo de cadena."""
        return str

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