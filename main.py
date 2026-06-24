def scan_operators(data):
    tokens = []

    for d in data:
        match d.strip():
            case "+":
                tokens.append("OP (+)")
            case "-":
                tokens.append("OP (-)")
            case "*":
                tokens.append("OP (*)")
            case "/":
                tokens.append("OP (/)")
            case _:
                print(f"input '{d}' not supported")

    return tokens