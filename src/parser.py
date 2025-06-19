from .lexer import TokenType, Token

# Clase base para todos los nodos del Árbol de Sintaxis Abstracta (AST)
class AST:
    """Clase base para todos los nodos del AST."""
    pass

# Nodo para operaciones binarias (suma, resta, multiplicación, división, potencia)
class BinOp(AST):
    """Nodo para operaciones binarias."""
    def __init__(self, left, op, right):
        self.left = left      # Nodo izquierdo de la operación
        self.token = self.op = op  # Token del operador (+, -, *, /, ^)
        self.right = right    # Nodo derecho de la operación

# Nodo para representar números literales
class Num(AST):
    """Nodo para números."""
    def __init__(self, token):
        self.token = token    # Token que contiene el número
        self.value = int(token.value)  # Valor numérico convertido a entero

# Nodo para representar variables
class Var(AST):
    """Nodo para variables."""
    def __init__(self, token):
        self.token = token    # Token que contiene el nombre de la variable
        self.value = token.value  # Nombre de la variable

# Nodo para representar asignaciones de variables
class Assign(AST):
    """Nodo para asignaciones."""
    def __init__(self, left, op, right):
        self.left = left      # Nodo de la variable a asignar
        self.token = self.op = op  # Token del operador de asignación (=)
        self.right = right    # Nodo de la expresión a asignar

# Nodo para representar instrucciones de impresión
class Print(AST):
    """Nodo para instrucciones de impresión."""
    def __init__(self, expr):
        self.expr = expr      # Nodo de la expresión a imprimir

# Nodo para representar declaraciones de variables
class VarDecl(AST):
    """Nodo para declaraciones de variables."""
    def __init__(self, var_node):
        self.var_node = var_node  # Nodo de la variable declarada

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer    # Instancia del analizador léxico
        self.current_token = self.lexer.get_next_token()  # Obtener el primer token

    def error(self, message):
        """Lanza una excepción con un mensaje de error de sintaxis."""
        raise Exception(f'Error de sintaxis: {message}')

    def eat(self, token_type):
        """
        Consume el token actual si coincide con el tipo esperado.
        Si no coincide, lanza un error de sintaxis.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Token inesperado: {self.current_token.type}')

    def factor(self):
        """
        factor : NUMBER | LPAREN expr RPAREN | IDENTIFIER
        
        Procesa factores en expresiones:
        - Números literales
        - Expresiones entre paréntesis
        - Identificadores (variables)
        """
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Num(token)
        
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Var(token)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        
        self.error('Factor inválido')

    def term(self):
        """
        term : factor ((MULTIPLICAR | DIVIDIR) factor)*
        
        Procesa términos en expresiones:
        - Multiplicaciones
        - Divisiones
        """
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLICAR, TokenType.DIVIDIR):
            token = self.current_token
            if token.type == TokenType.MULTIPLICAR:
                self.eat(TokenType.MULTIPLICAR)
            elif token.type == TokenType.DIVIDIR:
                self.eat(TokenType.DIVIDIR)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def power(self):
        """
        power : term (POTENCIA term)*
        
        Procesa potencias en expresiones:
        - Términos elevados a una potencia
        """
        node = self.term()

        while self.current_token.type == TokenType.POTENCIA:
            token = self.current_token
            self.eat(TokenType.POTENCIA)
            node = BinOp(left=node, op=token, right=self.term())

        return node

    def expr(self):
        """
        expr : power ((SUMAR | RESTAR) power)*
        
        Procesa expresiones:
        - Sumas
        - Restas
        """
        node = self.power()

        while self.current_token.type in (TokenType.SUMAR, TokenType.RESTAR):
            token = self.current_token
            if token.type == TokenType.SUMAR:
                self.eat(TokenType.SUMAR)
            elif token.type == TokenType.RESTAR:
                self.eat(TokenType.RESTAR)

            node = BinOp(left=node, op=token, right=self.power())

        return node

    def assignment(self):
        """
        assignment : IDENTIFIER ASSIGN expr
        
        Procesa asignaciones de variables:
        - Variable = Expresión
        """
        left = Var(self.current_token)
        self.eat(TokenType.IDENTIFIER)
        
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        
        right = self.expr()
        return Assign(left, token, right)

    def print_statement(self):
        """
        print_statement : PRINT LPAREN expr RPAREN
        
        Procesa instrucciones de impresión:
        - print(Expresión)
        """
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        expr = self.expr()
        self.eat(TokenType.RPAREN)
        return Print(expr)

    def var_declaration(self):
        """
        var_declaration : VAR IDENTIFIER
        
        Procesa declaraciones de variables:
        - var Variable
        """
        self.eat(TokenType.VAR)
        var_node = Var(self.current_token)
        self.eat(TokenType.IDENTIFIER)
        return VarDecl(var_node)

    def statement(self):
        """
        statement : var_declaration | assignment | print_statement
        
        Procesa sentencias:
        - Declaraciones de variables
        - Asignaciones
        - Instrucciones de impresión
        """
        if self.current_token.type == TokenType.VAR:
            return self.var_declaration()
        elif self.current_token.type == TokenType.PRINT:
            return self.print_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.assignment()
        else:
            self.error('Declaración inválida')

    def program(self):
        """
        program : statement*
        
        Procesa un programa completo:
        - Secuencia de sentencias separadas por punto y coma
        """
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
            self.eat(TokenType.SEMICOLON)
        return statements 