import collections
import re
ReservedWord = collections.namedtuple('ReservedWord', 's')
Identifier = collections.namedtuple('Identifier', 's')
Separator = collections.namedtuple('Separator', 's')
# No reason to handle ints, etc.
Unknown = collections.namedtuple('Unknown', 's')

reserved_words = ['boolean', 'break', 'callout', 'class', 'continue', 'else', 'false', 'for', 'if', 'int', 'return',
'true', 'void']

# Newline is missing so that we preserve newlines
white_space = [' ', '\n', '\t', """\\"""]
separators = ['(', ')', '{', '}', '==', '!=', '>=', '!=', ',', ';']

def tokenize_raw(code, buff):
    if not code:
        return [buff]
    elif code[0] in white_space:
        return [buff] + tokenize_raw(code[1:], '')
    elif code[0] in separators:
        return [buff] + [code[0]]+ tokenize_raw(code[1:], '')
    else:
        return tokenize_raw(code[1:], buff + code[0])

def process(buff):
    '''
    Turn a string into a syntax object
    >>> process('abc')
    Identifier(s='abc')

    >>> process('ab_123cde')
    Identifier(s='ab_123cde')

    >>> process('{')
    Separator(s='{')

    '''
    if buff in reserved_words:
        return ReservedWord(buff)
    elif re.match('[a-zA-Z_][a-zA-Z0-9_]*', buff):
        return Identifier(buff)
    elif re.match('\(|\)|{|}', buff):
        return Separator(buff)
    else:
        return Unknown(buff)

def filter_whitespace(c):
    return c != ''

def tokenize(code):
    ''' 
    Tokenize a string of Decaf code
    >>> tokenize('a   b \t  boolean c \t   d')
    [Identifier(s='a'), Identifier(s='b'), ReservedWord(s='boolean'), Identifier(s='c'), Identifier(s='d')]

    >>> tokenize('class Program{ab }')
    [ReservedWord(s='class'), Identifier(s='Program'), Separator(s='{'), Identifier(s='ab'), Separator(s='}')]
    
    '''
    filtered = filter(filter_whitespace, tokenize_raw(code, ''))
    return map(process, filtered)


def get_indent(indent):
    return 2 * ' ' * indent

def emit_code(tokens, indent, indent_required, disregard_newline):
    # If the head token ends the line
    if not tokens:
        return ''
    else:
        head = tokens[0].s

    if head == 'for':
        disregard_newline = True

    indent_str = get_indent(indent) if indent_required else ' '

    if head == ',':
      indent_str = ''

    if head == ';':
        new_line = '' if disregard_newline else '\n'
        return ';' + new_line + emit_code(tokens[1:], indent, not disregard_newline, disregard_newline)
    elif head == '{':
        return indent_str + '{\n' + emit_code(tokens[1:], indent + 1, True, False)
    elif head == '}':
        return get_indent(indent -1) + '}\n' + emit_code(tokens[1:], indent -1, True, False)
    else:
        return indent_str + head + emit_code(tokens[1:], indent, False, disregard_newline)
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()

