from lexer import TokenType, Token

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

# Nodo para representar condiciones
class Condition(AST):
    """Nodo para condiciones en estructuras de control."""
    def __init__(self, left, op, right):
        self.left = left      # Lado izquierdo de la condición
        self.op = op          # Operador de comparación
        self.right = right    # Lado derecho de la condición

# Nodo para operaciones lógicas
class LogicalOp(AST):
    """Nodo para operaciones lógicas (Y, O)."""
    def __init__(self, left, op, right):
        self.left = left      # Lado izquierdo de la operación lógica
        self.op = op          # Operador lógico (Y, O)
        self.right = right    # Lado derecho de la operación lógica

# Nodo para estructuras condicionales
class If(AST):
    """Nodo para estructuras condicionales."""
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition    # Condición del if
        self.then_body = then_body    # Cuerpo del then (lista de nodos)
        self.else_body = else_body    # Cuerpo del else (opcional, lista de nodos)

# Nodo para estructuras de bucle
class While(AST):
    """Nodo para estructuras de bucle while."""
    def __init__(self, condition, body):
        self.condition = condition    # Condición del while
        self.body = body              # Cuerpo del bucle (lista de nodos)

# Nodo para representar cadenas literales
class String(AST):
    """Nodo para cadenas."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

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
        factor : NUMBER | STRING | LPAREN expr RPAREN | IDENTIFIER
        
        Procesa factores en expresiones:
        - Números literales
        - Expresiones entre paréntesis
        - Identificadores (variables)
        """
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Num(token)
        
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token)
        
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

    def concat_expr(self):
        """
        concat_expr : power (CONCATENAR power)*
        Permite concatenar cadenas y expresiones.
        """
        node = self.power()
        while self.current_token.type == TokenType.CONCATENAR:
            token = self.current_token
            self.eat(TokenType.CONCATENAR)
            node = BinOp(left=node, op=token, right=self.power())
        return node

    def expr(self):
        """
        expr : concat_expr ((SUMAR | RESTAR) concat_expr)*
        """
        node = self.concat_expr()
        while self.current_token.type in (TokenType.SUMAR, TokenType.RESTAR):
            token = self.current_token
            if token.type == TokenType.SUMAR:
                self.eat(TokenType.SUMAR)
            elif token.type == TokenType.RESTAR:
                self.eat(TokenType.RESTAR)
            node = BinOp(left=node, op=token, right=self.concat_expr())
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

    def condition(self):
        """
        condition : expr (MAYOR | MENOR | IGUAL | DIFERENTE | MAYOR_IGUAL | MENOR_IGUAL) expr
        
        Procesa condiciones:
        - Expresión Operador Expresión
        """
        left = self.expr()
        
        if self.current_token.type in (TokenType.MAYOR, TokenType.MENOR, TokenType.IGUAL, 
                                     TokenType.DIFERENTE, TokenType.MAYOR_IGUAL, TokenType.MENOR_IGUAL):
            op = self.current_token
            if op.type == TokenType.MAYOR:
                self.eat(TokenType.MAYOR)
            elif op.type == TokenType.MENOR:
                self.eat(TokenType.MENOR)
            elif op.type == TokenType.IGUAL:
                self.eat(TokenType.IGUAL)
            elif op.type == TokenType.DIFERENTE:
                self.eat(TokenType.DIFERENTE)
            elif op.type == TokenType.MAYOR_IGUAL:
                self.eat(TokenType.MAYOR_IGUAL)
            elif op.type == TokenType.MENOR_IGUAL:
                self.eat(TokenType.MENOR_IGUAL)
            
            right = self.expr()
            return Condition(left, op, right)
        
        return left

    def logical_expr(self):
        """
        logical_expr : condition ((Y | O) condition)*
        
        Procesa expresiones lógicas:
        - Condición Y Condición
        - Condición O Condición
        """
        node = self.condition()
        
        while self.current_token.type in (TokenType.Y, TokenType.O):
            op = self.current_token
            if op.type == TokenType.Y:
                self.eat(TokenType.Y)
            elif op.type == TokenType.O:
                self.eat(TokenType.O)
            
            node = LogicalOp(left=node, op=op, right=self.condition())
        
        return node

    def if_statement(self):
        """
        if_statement : SI LPAREN logical_expr RPAREN ENTONCES statement* FIN_SI
        
        Procesa estructuras condicionales:
        - si (condición) entonces sentencias fin_si
        """
        self.eat(TokenType.SI)
        self.eat(TokenType.LPAREN)
        condition = self.logical_expr()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.ENTONCES)
        
        then_body = []
        while (self.current_token.type not in (TokenType.FIN_SI, TokenType.EOF)):
            statement = self.statement()
            then_body.append(statement)
            
            # Solo agregar punto y coma después de sentencias simples dentro del bloque
            if (isinstance(statement, (VarDecl, Assign, Print)) and 
                self.current_token.type == TokenType.SEMICOLON):
                self.eat(TokenType.SEMICOLON)
        
        self.eat(TokenType.FIN_SI)
        return If(condition, then_body)

    def while_statement(self):
        """
        while_statement : MIENTRAS LPAREN logical_expr RPAREN HACER statement* FIN_MIENTRAS
        
        Procesa estructuras de bucle:
        - mientras (condición) hacer sentencias fin_mientras
        """
        self.eat(TokenType.MIENTRAS)
        self.eat(TokenType.LPAREN)
        condition = self.logical_expr()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.HACER)
        
        body = []
        while (self.current_token.type not in (TokenType.FIN_MIENTRAS, TokenType.EOF)):
            statement = self.statement()
            body.append(statement)
            
            # Solo agregar punto y coma después de sentencias simples dentro del bloque
            if (isinstance(statement, (VarDecl, Assign, Print)) and 
                self.current_token.type == TokenType.SEMICOLON):
                self.eat(TokenType.SEMICOLON)
        
        self.eat(TokenType.FIN_MIENTRAS)
        return While(condition, body)

    def statement(self):
        """
        statement : var_declaration | assignment | print_statement | if_statement | while_statement
        
        Procesa sentencias:
        - Declaraciones de variables
        - Asignaciones
        - Instrucciones de impresión
        - Estructuras condicionales
        - Estructuras de bucle
        """
        if self.current_token.type == TokenType.VAR:
            return self.var_declaration()
        elif self.current_token.type == TokenType.PRINT:
            return self.print_statement()
        elif self.current_token.type == TokenType.SI:
            return self.if_statement()
        elif self.current_token.type == TokenType.MIENTRAS:
            return self.while_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.assignment()
        else:
            self.error('Declaración inválida')

    def program(self):
        """
        program : statement*
        
        Procesa un programa completo:
        - Secuencia de sentencias
        - Las sentencias simples terminan con punto y coma
        - Las estructuras de control no terminan con punto y coma
        """
        statements = []
        while self.current_token.type != TokenType.EOF:
            statement = self.statement()
            statements.append(statement)
            
            # Solo agregar punto y coma después de sentencias simples
            if (isinstance(statement, (VarDecl, Assign, Print)) and 
                self.current_token.type == TokenType.SEMICOLON):
                self.eat(TokenType.SEMICOLON)
        
        return statements 