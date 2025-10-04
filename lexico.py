from enum import Enum, auto
from dataclasses import dataclass

class Tokens(Enum):
    FUNCTION = auto()
    MAIN = auto()
    LET = auto()
    INT = auto()
    FLOAT = auto()
    CHAR = auto()
    IF = auto()
    ELSE = auto() 
    WHILE = auto() 
    PRINTLN = auto()
    RETURN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    ARROW = auto()
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    ASSIGN = auto()
    EQ = auto()
    NE = auto()
    GT = auto()
    GE = auto()
    LT = auto()
    LE = auto()
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    ID = auto()
    INT_CONST = auto()
    FLOAT_CONST = auto()
    CHAR_LITERAL = auto()
    FMT_STRING = auto()

RESERVED = {
    "fn": Tokens.FUNCTION,
    "main": Tokens.MAIN,
    "let": Tokens.LET,
    "int": Tokens.INT,
    "float": Tokens.FLOAT,
    "char": Tokens.CHAR,
    "if": Tokens.IF,
    "else": Tokens.ELSE,
    "while": Tokens.WHILE,
    "println": Tokens.PRINTLN,
    "return": Tokens.RETURN

}

@dataclass
class Token:
    type: Tokens
    lexema: str
    line: int


def criar_token(lista_tokens: list, type: Tokens, lexeame: str, line: int) -> Token:
    t = Token(type, lexeame, line)
    lista_tokens.append(t)

def main():

    with open("teste.txt", "r") as f:
        arquivo = f.read()


    lista_tokens = []
    estado = 0
    num_linha = 1
    USOU_ULTIMO = True
    i = 0
    lexema_temp =  ""
    tamanho_do_arquivo = len(arquivo)

    while i < tamanho_do_arquivo:
        USOU_ULTIMO = True
        c = arquivo[i]

        match estado:
            case 0:
                if c == '(':
                    criar_token(lista_tokens, Tokens.LBRACKET, c, num_linha)
                    estado = 0
                elif c == ')':
                    criar_token(lista_tokens, Tokens.RBRACKET, c, num_linha)
                    estado = 0
                elif c == '{':
                    criar_token(lista_tokens, Tokens.LBRACE, c, num_linha)
                    estado = 0
                elif c == '}':  
                    criar_token(lista_tokens, Tokens.RBRACE, c, num_linha)
                    estado = 0
                elif c == ':':
                    criar_token(lista_tokens, Tokens.COLON, c, num_linha)
                    estado = 0
                elif c == ';':
                    criar_token(lista_tokens, Tokens.SEMICOLON, c, num_linha)
                    estado = 0
                elif c == ',':
                    criar_token(lista_tokens, Tokens.COMMA, c, num_linha)
                    estado = 0
                elif c == '+':
                    criar_token(lista_tokens, Tokens.PLUS, c, num_linha)
                    estado = 0
                elif c == '*':
                    criar_token(lista_tokens, Tokens.MULT, c, num_linha)
                    estado = 0
                elif c == '/':
                    criar_token(lista_tokens, Tokens.DIV, c, num_linha)
                    estado = 0
                elif c == '\n':
                    num_linha += 1
                elif c == '-':
                    lexema_temp += c
                    estado = 1
                elif c == '!':
                    lexema_temp += c
                    estado = 2
                elif c.isalpha():
                    lexema_temp += c
                    estado = 6
                
            
            case 1:
                if c == '>':
                    lexema_temp += c
                    criar_token(lista_tokens, Tokens.ARROW, lexema_temp, num_linha)
                    lexema_temp = ""
                    estado = 0
                else:
                    criar_token(lista_tokens, Tokens.MINUS, lexema_temp, num_linha)
                    lexema_temp = ""
                    estado = 0
                    USOU_ULTIMO = False

            case 2:
                if c == '=':
                    lexema_temp += c
                    criar_token(lista_tokens, Tokens.NE, lexema_temp, num_linha)
                    lexema_temp = ""
                    estado = 0
                else:
                    # Tratar erro léxico
                    lexema_temp = ""
                    estado = 0
                    USOU_ULTIMO = False
                
            case 6:
                if c.isalnum() or c == '_':
                    lexema_temp += c
                    estado = 6
                else:
                    if lexema_temp in RESERVED:
                        criar_token(lista_tokens, RESERVED[lexema_temp], lexema_temp, num_linha)
                    else:
                        criar_token(lista_tokens, Tokens.ID, lexema_temp, num_linha)
                    lexema_temp = ""
                    estado = 0
                    USOU_ULTIMO = False

        if USOU_ULTIMO:
            i += 1
