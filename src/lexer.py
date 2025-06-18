from enum import Enum, auto

class TokenType(Enum):
    # Palabras reservadas
    VAR = auto()
    PRINT = auto()
    
    # Operadores
    PLUS = auto()      # +
    MINUS = auto()     # -
    MULTIPLY = auto()  # *
    DIVIDE = auto()    # /
    POWER = auto()     # ^
    ASSIGN = auto()    # =
    
    # Identificadores y literales
    IDENTIFIER = auto()
    NUMBER = auto()
    
    # Delimitadores
    SEMICOLON = auto() # ;
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    
    # Fin de archivo
    EOF = auto()

class Token:
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None
        
        # Diccionario de palabras reservadas
        self.keywords = {
            'var': TokenType.VAR,
            'print': TokenType.PRINT
        }
    
    def advance(self):
        """Avanza al siguiente carácter en el código fuente."""
        self.position += 1
        self.column += 1
        
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
            
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
    
    def skip_whitespace(self):
        """Omite espacios en blanco y saltos de línea."""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def number(self):
        """Procesa números."""
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, result, self.line, self.column - len(result))
    
    def identifier(self):
        """Procesa identificadores y palabras reservadas."""
        result = ''
        start_column = self.column
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        token_type = self.keywords.get(result.lower(), TokenType.IDENTIFIER)
        return Token(token_type, result, self.line, start_column)
    
    def get_next_token(self):
        """Obtiene el siguiente token del código fuente."""
        while self.current_char:
            # Omite espacios en blanco
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Números
            if self.current_char.isdigit():
                return self.number()
            
            # Identificadores y palabras reservadas
            if self.current_char.isalpha():
                return self.identifier()
            
            # Operadores y delimitadores
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.line, self.column - 1)
            
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.line, self.column - 1)
            
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*', self.line, self.column - 1)
            
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/', self.line, self.column - 1)
            
            if self.current_char == '^':
                self.advance()
                return Token(TokenType.POWER, '^', self.line, self.column - 1)
            
            if self.current_char == '=':
                self.advance()
                return Token(TokenType.ASSIGN, '=', self.line, self.column - 1)
            
            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';', self.line, self.column - 1)
            
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line, self.column - 1)
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line, self.column - 1)
            
            raise Exception(f"Carácter inválido: {self.current_char} en línea {self.line}, columna {self.column}")
        
        return Token(TokenType.EOF, '', self.line, self.column) 