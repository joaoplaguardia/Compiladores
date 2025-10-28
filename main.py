from lexico import lexico
from sintatico import sintatico

if __name__ == "__main__":
    with open("teste.txt", "r") as f:
        code = f.read()

    tokens = lexico(code)
    sintatico(tokens)

