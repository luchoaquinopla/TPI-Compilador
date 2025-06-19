from enum import Enum, auto

class TokenType(Enum):
    # Palabras clave
    VAR = auto()
    PRINT = auto()
    
    # Operadores como palabras
    SUMAR = auto()      # en lugar de PLUS
    RESTAR = auto()     # en lugar de MINUS
    MULTIPLICAR = auto() # en lugar de MULTIPLY
    DIVIDIR = auto()    # en lugar de DIVIDE
    POTENCIA = auto()   # en lugar de POWER
    
    # Otros tokens
    NUMBER = auto()
    IDENTIFIER = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

    def error(self):
        raise Exception('Carácter inválido')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.number())

            if self.current_char.isalpha():
                identifier = self.identifier()
                
                # Palabras clave
                if identifier == 'var':
                    return Token(TokenType.VAR, identifier)
                elif identifier == 'print':
                    return Token(TokenType.PRINT, identifier)
                # Operadores como palabras
                elif identifier == 'sumar':
                    return Token(TokenType.SUMAR, identifier)
                elif identifier == 'restar':
                    return Token(TokenType.RESTAR, identifier)
                elif identifier == 'multiplicar':
                    return Token(TokenType.MULTIPLICAR, identifier)
                elif identifier == 'dividir':
                    return Token(TokenType.DIVIDIR, identifier)
                elif identifier == 'potencia':
                    return Token(TokenType.POTENCIA, identifier)
                else:
                    return Token(TokenType.IDENTIFIER, identifier)

            if self.current_char == '=':
                self.advance()
                return Token(TokenType.ASSIGN, '=')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';')

            self.error()

        return Token(TokenType.EOF, None) 