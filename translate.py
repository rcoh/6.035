from tokenize import tokenize, Separator, emit_code

def remove_class(tokens):
    if starts_with(tokens, 'class Program {') and tokens[-1] == Separator('}'):
        return tokens[3:-1]
    else:
        print tokens


def starts_with(tokens, code):
    matches = tokenize(code)
    return all([l == r for (l, r) in zip(tokens, matches)])


def translate(code):
    tokens = tokenize(code)
    tokens = remove_class(tokens)
    return emit_code(tokens, 0, True, False)

def translate_file(name):
    with open(name) as f:
        new_code = translate(f.read())
        with file('trans'+name, 'w') as n:
            n.write(new_code)

def identity(name):
    with open(name) as f:
        new_code = (f.read())
        with file('trans'+name, 'w') as n:
            n.write(new_code)



translate_file('test.dcf')
