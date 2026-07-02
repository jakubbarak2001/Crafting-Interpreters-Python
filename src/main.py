from crafting_intepreters.tokenizer import tokenize

if __name__ == '__main__':
    token = tokenize("< <= > >= = == <== >== ! != ==== ===")
    print(token)
