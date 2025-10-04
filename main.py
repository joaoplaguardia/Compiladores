from lexico import lexico

if __name__ == "__main__":
    with open("teste.txt", "r") as f:
        code = f.read()

    tokens = lexico(code)

    for token in tokens:
        print(token)
