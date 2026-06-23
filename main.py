def scan_operators(self):
    tokenizer = []

    for d in incoming_data:
        match d:
            case "+":
                tokenizer.append("OP (+)")
            case "-":
                tokenizer.append("OP (-)")
            case "*":
                tokenizer.append("OP (*)")
            case "/":
                tokenizer.append("OP (/)")
            case _:
                print(f"input '{d}' not supported")

    return tokenizer

incoming_data = ["+", "-", "*", "/"]
print(scan_operators(incoming_data))