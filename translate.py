from tokenize import tokenize, Separator, emit_code, Unknown

def remove_class(tokens):
    if starts_with(tokens, 'class Program {') and tokens[-1] == Separator('}'):
        return tokens[3:-1]
    else:
        print tokens

def rewrite_callouts(tokens):
    emmited = set()
    tokens = rewrite_callouts_int(tokens, emmited)
    new_tokens = [token for func in emmited for token in tokenize('callout %s;' % func)]
    tokens = new_tokens + tokens
    return tokens


def rewrite_callouts_int(tokens, emmited_callouts):
    if not tokens:
        return []
    else:
        if tokens[0].s == 'callout':
            (callout, lparen, func_name) = tokens[0:3]
            func_name = Unknown(func_name.s.strip("'"))
            emmited_callouts.add(func_name.s)
            return [func_name, lparen] + rewrite_callouts_int(tokens[4:], emmited_callouts)
        else:
            return [tokens[0]] + rewrite_callouts_int(tokens[1:], emmited_callouts)


def starts_with(tokens, code):
    matches = tokenize(code)
    return all([l == r for (l, r) in zip(tokens, matches)])


def translate(code):
    tokens = tokenize(code)
    tokens = remove_class(tokens)
    tokens = rewrite_callouts(tokens)
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



#translate_file('test.dcf')
translate_file('callouts.dcf')
