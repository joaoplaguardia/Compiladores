from lexico import Tokens
import json
from enum import Enum, auto

# --------------------------
# Tipos internos (DataTypes)
# --------------------------
class DataTypes(Enum):
    error = -1
    int = 0
    float = 1
    char = 2
    void = 3

# --------------------------
# Estruturas de dados
# --------------------------
class FunctionRegister:
    def __init__(self, name, args):
        self.name = name                      # lexema função chamada
        self.num_args = len(args)
        self.args = args[:]                   # lista de lexemas (strings)

    def to_dict(self):
        return {"name": self.name, "num_args": self.num_args, "args": self.args}

class SymbolEntry:
    def __init__(self, name, datatype=DataTypes.error, is_param=False, pos_param=-1):
        self.name = name
        self.datatype = datatype
        self.is_param = is_param
        self.pos_param = pos_param
        self.call_refs = []

    def to_dict(self):
        return {
            "name": self.name,
            "datatype": self.datatype.name if isinstance(self.datatype, DataTypes) else str(self.datatype),
            "is_param": self.is_param,
            "pos_param": self.pos_param,
            "call_refs": [cr.to_dict() for cr in self.call_refs]
        }

class SymbolTable:
    def __init__(self, function_name):
        self.function_name = function_name
        self.entries = {}
        self.ret_type = DataTypes.void

    def add_entry(self, entry: SymbolEntry):
        self.entries[entry.name] = entry

    def get_or_create_entry(self, name):
        if name not in self.entries:
            self.entries[name] = SymbolEntry(name, datatype=DataTypes.error, is_param=False, pos_param=-1)
        return self.entries[name]

    def to_dict(self):
        return {
            "function_name": self.function_name,
            "ret_type": self.ret_type.name,
            "entries": {k: v.to_dict() for k, v in self.entries.items()}
        }

vetor_tokens = []
token_index = 0

symbol_tables = {}
current_table = None
syntax_errors = []

def check_eof(msg="Unexpected end of input"):
    global token_index, vetor_tokens
    if token_index >= len(vetor_tokens):
        raise SyntaxError(msg)

def match(expected_type):
    global vetor_tokens, token_index
    check_eof()
    if vetor_tokens[token_index].type == expected_type:
        tk = vetor_tokens[token_index]
        token_index += 1
        return tk
    else:
        raise SyntaxError(
            f"Esperado {expected_type}, mas encontrou {vetor_tokens[token_index].type} "
            f"(lexema='{vetor_tokens[token_index].lexema}', linha {vetor_tokens[token_index].line})"
        )

def record_syntax_error(e):
    syntax_errors.append(str(e))

def panic_recovery():

    global token_index, vetor_tokens
    while token_index < len(vetor_tokens):
        if vetor_tokens[token_index].type in (Tokens.SEMICOLON, Tokens.RBRACE):
            token_index += 1
            return True
        token_index += 1
    return False

def Programa():
    global token_index, vetor_tokens

    while token_index < len(vetor_tokens):
        tk = vetor_tokens[token_index]

        if tk.type == Tokens.FUNCTION:
            try:
                Funcao()
            except SyntaxError as e:
                record_syntax_error(e)
                if not panic_recovery():
                    break

        elif tk.type == Tokens.ERROR:
            record_syntax_error(f"Token inválido '{tk.lexema}' na linha {tk.line}")
            token_index += 1
            while token_index < len(vetor_tokens) and vetor_tokens[token_index].type != Tokens.FUNCTION:
                token_index += 1

        else:
            e = SyntaxError(
                f"Esperado 'function' no início de função, mas encontrou {tk.type} "
                f"(lexema='{tk.lexema}', linha {tk.line})"
            )
            record_syntax_error(e)
            if not panic_recovery():
                break


def Funcao():
    global current_table, symbol_tables, token_index
    match(Tokens.FUNCTION)

    func_name = NomeFuncao_get_name()

    if func_name in symbol_tables:
        record_syntax_error(f"Função '{func_name}' já definida (linha {vetor_tokens[token_index-1].line})")
    table = SymbolTable(func_name)
    symbol_tables[func_name] = table
    current_table = table

    match(Tokens.LBRACKET)
    ListaParams()
    match(Tokens.RBRACKET)
    TipoRetornoFuncao()
    Bloco()

    current_table = None

def NomeFuncao_get_name():
    global vetor_tokens, token_index
    check_eof()
    tk = vetor_tokens[token_index].type
    if tk == Tokens.ID:
        token = match(Tokens.ID)
        return token.lexema
    elif tk == Tokens.MAIN:
        token = match(Tokens.MAIN)
        return token.lexema
    else:
        raise SyntaxError("Esperado ID ou MAIN em NomeFuncao")

def NomeFuncao():
    NomeFuncao_get_name()

def ListaParams():
    global token_index, current_table
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.ID:
        pos = 0
        while token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.ID:
            id_token = match(Tokens.ID)
            match(Tokens.COLON)
            dtype = Type_get_datatype()
            if current_table is not None:
                entry = SymbolEntry(id_token.lexema, datatype=dtype, is_param=True, pos_param=pos)
                current_table.add_entry(entry)
            pos += 1
            if token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.COMMA:
                match(Tokens.COMMA)
            else:
                break

def ListaParams2():
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.COMMA:
        match(Tokens.COMMA)
        match(Tokens.ID)
        match(Tokens.COLON)
        Type()
        ListaParams2()

def TipoRetornoFuncao():
    global current_table
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.ARROW:
        match(Tokens.ARROW)
        dtype = Type_get_datatype()
        if current_table is not None:
            current_table.ret_type = dtype

def Bloco():
    match(Tokens.LBRACE)
    Sequencia()
    match(Tokens.RBRACE)

def Sequencia():
    global vetor_tokens, token_index
    while token_index < len(vetor_tokens):
        tk = vetor_tokens[token_index].type
        if tk == Tokens.RBRACE:
            break
        if tk == Tokens.LET:
            Declaracao()
        elif tk in (Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.PRINTLN, Tokens.RETURN, Tokens.LBRACE):
            Comando()
        else:
            break

def Declaracao():
    match(Tokens.LET)
    ids = VarList_get_ids()
    match(Tokens.COLON)
    dtype = Type_get_datatype()
    if current_table is not None:
        for lex in ids:
            entry = SymbolEntry(lex, datatype=dtype, is_param=False, pos_param=-1)
            current_table.add_entry(entry)
    match(Tokens.SEMICOLON)

def VarList_get_ids():
    ids = []
    id_token = match(Tokens.ID)
    ids.append(id_token.lexema)
    while token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.COMMA:
        match(Tokens.COMMA)
        id_token = match(Tokens.ID)
        ids.append(id_token.lexema)
    return ids

def VarList():
    VarList_get_ids()

def Type_get_datatype():
    check_eof()
    tk = vetor_tokens[token_index].type
    if tk == Tokens.INT:
        match(Tokens.INT)
        return DataTypes.int
    elif tk == Tokens.FLOAT:
        match(Tokens.FLOAT)
        return DataTypes.float
    elif tk == Tokens.CHAR:
        match(Tokens.CHAR)
        return DataTypes.char
    else:
        raise SyntaxError("Esperado tipo int, float ou char")

def Type():
    Type_get_datatype()

def Comando():
    global token_index, current_table
    check_eof()
    tk = vetor_tokens[token_index].type

    if tk == Tokens.ID:
        id_token = match(Tokens.ID)
        AtribuicaoOuChamada(id_token.lexema)

    elif tk == Tokens.LBRACE or tk == Tokens.IF:
        ComandoSe()

    elif tk == Tokens.WHILE:
        match(Tokens.WHILE)
        Expr()
        Bloco()

    elif tk == Tokens.PRINTLN:
        match(Tokens.PRINTLN)
        match(Tokens.LBRACKET)
        match(Tokens.FMT_STRING)
        match(Tokens.COMMA)
        ListaArgs()
        match(Tokens.RBRACKET)
        match(Tokens.SEMICOLON)

    elif tk == Tokens.RETURN:
        match(Tokens.RETURN)
        Expr()
        match(Tokens.SEMICOLON)

    else:
        raise SyntaxError(f"Comando inesperado: {vetor_tokens[token_index]}")

def AtribuicaoOuChamada(prev_id_lexema):
    global token_index, current_table
    check_eof()
    tk = vetor_tokens[token_index].type

    if tk == Tokens.ASSIGN:
        match(Tokens.ASSIGN)
        Expr()
        match(Tokens.SEMICOLON)

    elif tk == Tokens.LBRACKET:
        match(Tokens.LBRACKET)
        args = ListaArgs_get_list()
        match(Tokens.RBRACKET)
        match(Tokens.SEMICOLON)

        fr = FunctionRegister(prev_id_lexema, args)
        if current_table is not None:
            entry = current_table.get_or_create_entry(prev_id_lexema)
            entry.call_refs.append(fr)
    else:
        raise SyntaxError("Esperado '=' ou '(' após ID")

def ComandoSe():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.LBRACE:
        Bloco()
    elif tk == Tokens.IF:
        match(Tokens.IF)
        Expr()
        Bloco()
        ComandoSenao()
    else:
        raise SyntaxError("Esperado bloco ou comando IF")

def ComandoSenao():
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.ELSE:
        match(Tokens.ELSE)
        ComandoSe()

def Expr():
    Rel()
    ExprOpc()

def ExprOpc():
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type in (Tokens.EQ, Tokens.NE):
        OpIgual()
        Rel()
        ExprOpc()

def OpIgual():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.EQ:
        match(Tokens.EQ)
    elif tk == Tokens.NE:
        match(Tokens.NE)
    else:
        raise SyntaxError("Esperado operador == ou !=")

def Rel():
    Adicao()
    RelOpc()

def RelOpc():
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type in (Tokens.LT, Tokens.LE, Tokens.GT, Tokens.GE):
        OpRel()
        Adicao()
        RelOpc()

def OpRel():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.LT:
        match(Tokens.LT)
    elif tk == Tokens.LE:
        match(Tokens.LE)
    elif tk == Tokens.GT:
        match(Tokens.GT)
    elif tk == Tokens.GE:
        match(Tokens.GE)
    else:
        raise SyntaxError("Esperado operador relacional (<, <=, >, >=)")

def Adicao():
    Termo()
    AdicaoOpc()

def AdicaoOpc():
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type in (Tokens.PLUS, Tokens.MINUS):
        OpAdicao()
        Termo()
        AdicaoOpc()

def OpAdicao():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.PLUS:
        match(Tokens.PLUS)
    elif tk == Tokens.MINUS:
        match(Tokens.MINUS)
    else:
        raise SyntaxError("Esperado + ou -")

def Termo():
    Fator()
    TermoOpc()

def TermoOpc():
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type in (Tokens.MULT, Tokens.DIV):
        OpMult()
        Fator()
        TermoOpc()

def OpMult():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.MULT:
        match(Tokens.MULT)
    elif tk == Tokens.DIV:
        match(Tokens.DIV)
    else:
        raise SyntaxError("Esperado * ou /")

def Fator():
    global token_index, current_table
    check_eof()
    tk = vetor_tokens[token_index].type
    if tk == Tokens.ID:
        id_token = match(Tokens.ID)
        ChamadaFuncao_optional(id_token.lexema)
    elif tk == Tokens.INT_CONST:
        match(Tokens.INT_CONST)
    elif tk == Tokens.FLOAT_CONST:
        match(Tokens.FLOAT_CONST)
    elif tk == Tokens.CHAR_LITERAL:
        match(Tokens.CHAR_LITERAL)
    elif tk == Tokens.LBRACKET:
        match(Tokens.LBRACKET)
        Expr()
        match(Tokens.RBRACKET)
    else:
        raise SyntaxError("Fator inválido")

def ChamadaFuncao_optional(caller_name):
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.LBRACKET:
        match(Tokens.LBRACKET)
        args = ListaArgs_get_list()
        match(Tokens.RBRACKET)
        fr = FunctionRegister(caller_name, args)
        if current_table is not None:
            entry = current_table.get_or_create_entry(caller_name)
            entry.call_refs.append(fr)

def ListaArgs_get_list():
    args = []
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type in (Tokens.ID, Tokens.INT_CONST, Tokens.FLOAT_CONST, Tokens.CHAR_LITERAL):
        tok = token_snapshot_and_consume()
        args.append(tok.lexema)
        while token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.COMMA:
            match(Tokens.COMMA)
            tok = token_snapshot_and_consume()
            args.append(tok.lexema)
    return args

def ListaArgs():
    ListaArgs_get_list()

def ListaArgs2():
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.COMMA:
        match(Tokens.COMMA)
        Arg()
        ListaArgs2()

def Arg():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.ID:
        id_token = match(Tokens.ID)
        ChamadaFuncao_optional(id_token.lexema)
    elif tk in (Tokens.INT_CONST, Tokens.FLOAT_CONST, Tokens.CHAR_LITERAL):
        match(tk)
    else:
        raise SyntaxError("Argumento inválido")

def token_snapshot_and_consume():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.ID:
        return match(Tokens.ID)
    elif tk == Tokens.INT_CONST:
        return match(Tokens.INT_CONST)
    elif tk == Tokens.FLOAT_CONST:
        return match(Tokens.FLOAT_CONST)
    elif tk == Tokens.CHAR_LITERAL:
        return match(Tokens.CHAR_LITERAL)
    else:
        raise SyntaxError(f"Argumento inválido (esperado ID/INT/FLOAT/CHAR), mas encontrou {vetor_tokens[token_index].type} (lexema='{vetor_tokens[token_index].lexema}', linha {vetor_tokens[token_index].line})")

def sintatico(Lista_de_tokens, output_symbols_filename="symbol_tables.json", output_errors_filename="syntax_errors.txt"):
    global vetor_tokens, token_index, symbol_tables, current_table, syntax_errors
    vetor_tokens = Lista_de_tokens
    token_index = 0
    symbol_tables = {}
    current_table = None
    syntax_errors = []

    try:
        Programa()
    except SyntaxError as e:
        record_syntax_error(e)
        panic_recovery()

    with open(output_errors_filename, "w", encoding="utf-8") as f:
        if syntax_errors:
            for err in syntax_errors:
                f.write(str(err) + "\n")
        else:
            f.write("Nenhum erro sintático encontrado.\n")

    out = {}
    for fname, table in symbol_tables.items():
        out[fname] = table.to_dict()

    with open(output_symbols_filename, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    if syntax_errors:
        print(f"Análise concluída com {len(syntax_errors)} erro(s) sintático(s). Ver {output_errors_filename}.")
    else:
        print("Análise sintática concluída com sucesso. Nenhum erro sintático encontrado.")
    print(f"Tabelas de símbolos escritas em: {output_symbols_filename}")
