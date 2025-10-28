from lexico import Tokens

vetor_tokens = []
token_index = 0


def match(expected_type):
    global vetor_tokens, token_index
    if vetor_tokens[token_index].type == expected_type:
        token_index += 1
    else:
        raise SyntaxError(
            f"Esperado {expected_type}, mas encontrou {vetor_tokens[token_index].type} "
            f"(lexema='{vetor_tokens[token_index].lexema}', linha {vetor_tokens[token_index].line})"
        )


def Programa():
    Funcao()
    FuncaoSeq()


def FuncaoSeq():
    global vetor_tokens, token_index
    if token_index < len(vetor_tokens) and vetor_tokens[token_index].type == Tokens.FUNCTION:
        Funcao()
        FuncaoSeq()
    # ε


def Funcao():
    match(Tokens.FUNCTION)
    NomeFuncao()
    match(Tokens.LBRACKET)  # (
    ListaParams()
    match(Tokens.RBRACKET)  # )
    TipoRetornoFuncao()
    Bloco()


def NomeFuncao():
    global vetor_tokens, token_index
    tk = vetor_tokens[token_index].type
    if tk == Tokens.ID:
        match(Tokens.ID)
    elif tk == Tokens.MAIN:
        match(Tokens.MAIN)
    else:
        raise SyntaxError("Esperado ID ou MAIN em NomeFuncao")


def ListaParams():
    global vetor_tokens, token_index
    if vetor_tokens[token_index].type == Tokens.ID:
        match(Tokens.ID)
        match(Tokens.COLON)
        Type()
        ListaParams2()
    # ε


def ListaParams2():
    if vetor_tokens[token_index].type == Tokens.COMMA:
        match(Tokens.COMMA)
        match(Tokens.ID)
        match(Tokens.COLON)
        Type()
        ListaParams2()
    # ε


def TipoRetornoFuncao():
    if vetor_tokens[token_index].type == Tokens.ARROW:
        match(Tokens.ARROW)
        Type()
    # ε


def Bloco():
    match(Tokens.LBRACE)  # {
    Sequencia()
    match(Tokens.RBRACE)  # }


def Sequencia():
    global vetor_tokens, token_index
    tk = vetor_tokens[token_index].type

    if tk == Tokens.LET:
        Declaracao()
        Sequencia()
    elif tk in (Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.PRINTLN, Tokens.RETURN, Tokens.LBRACE):
        Comando()
        Sequencia()
    # ε


def Declaracao():
    match(Tokens.LET)
    VarList()
    match(Tokens.COLON)
    Type()
    match(Tokens.SEMICOLON)


def VarList():
    match(Tokens.ID)
    VarList2()


def VarList2():
    if vetor_tokens[token_index].type == Tokens.COMMA:
        match(Tokens.COMMA)
        match(Tokens.ID)
        VarList2()
    # ε


def Type():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.INT:
        match(Tokens.INT)
    elif tk == Tokens.FLOAT:
        match(Tokens.FLOAT)
    elif tk == Tokens.CHAR:
        match(Tokens.CHAR)
    else:
        raise SyntaxError("Esperado tipo int, float ou char")


def Comando():
    tk = vetor_tokens[token_index].type

    if tk == Tokens.ID:
        match(Tokens.ID)
        AtribuicaoOuChamada()

    elif tk in (Tokens.IF, Tokens.LBRACE):
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


def AtribuicaoOuChamada():
    tk = vetor_tokens[token_index].type

    if tk == Tokens.ASSIGN:
        match(Tokens.ASSIGN)
        Expr()
        match(Tokens.SEMICOLON)

    elif tk == Tokens.LBRACKET:
        match(Tokens.LBRACKET)
        ListaArgs()
        match(Tokens.RBRACKET)
        match(Tokens.SEMICOLON)

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
    if vetor_tokens[token_index].type == Tokens.ELSE:
        match(Tokens.ELSE)
        ComandoSe()
    # ε


def Expr():
    Rel()
    ExprOpc()


def ExprOpc():
    if vetor_tokens[token_index].type in (Tokens.EQ, Tokens.NE):
        OpIgual()
        Rel()
        ExprOpc()
    # ε


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
    if vetor_tokens[token_index].type in (Tokens.LT, Tokens.LE, Tokens.GT, Tokens.GE):
        OpRel()
        Adicao()
        RelOpc()
    # ε


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
    if vetor_tokens[token_index].type in (Tokens.PLUS, Tokens.MINUS):
        OpAdicao()
        Termo()
        AdicaoOpc()
    # ε


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
    if vetor_tokens[token_index].type in (Tokens.MULT, Tokens.DIV):
        OpMult()
        Fator()
        TermoOpc()
    # ε


def OpMult():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.MULT:
        match(Tokens.MULT)
    elif tk == Tokens.DIV:
        match(Tokens.DIV)
    else:
        raise SyntaxError("Esperado * ou /")


def Fator():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.ID:
        match(Tokens.ID)
        ChamadaFuncao()
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


def ChamadaFuncao():
    if vetor_tokens[token_index].type == Tokens.LBRACKET:
        match(Tokens.LBRACKET)
        ListaArgs()
        match(Tokens.RBRACKET)
    # ε


def ListaArgs():
    if vetor_tokens[token_index].type in (Tokens.ID, Tokens.INT_CONST, Tokens.FLOAT_CONST, Tokens.CHAR_LITERAL):
        Arg()
        ListaArgs2()
    # ε


def ListaArgs2():
    if vetor_tokens[token_index].type == Tokens.COMMA:
        match(Tokens.COMMA)
        Arg()
        ListaArgs2()
    # ε


def Arg():
    tk = vetor_tokens[token_index].type
    if tk == Tokens.ID:
        match(Tokens.ID)
        ChamadaFuncao()
    elif tk in (Tokens.INT_CONST, Tokens.FLOAT_CONST, Tokens.CHAR_LITERAL):
        match(tk)
    else:
        raise SyntaxError("Argumento inválido")


def sintatico(Lista_de_tokens):
    global vetor_tokens, token_index
    vetor_tokens = Lista_de_tokens
    token_index = 0
    Programa()
    print("Análise sintática concluída com sucesso.")
