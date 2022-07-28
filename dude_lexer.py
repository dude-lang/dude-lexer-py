import re


class InvalidSymbolError(BaseException):
    def __init__(self, line: int, col: int, pos: int, sym: str, hint: str = ''):
        hint = '' if not hint else '\n\n  {}\n  {}^\n'.format(hint, ' ' * (col - 1))
        super().__init__(f'Invalid Symbol in Line {line} Column {col} Position {pos}: \'{sym}\' {hint}')


def tokenize(program: str) -> [str]:
    ids = [NEWLINE, SPACE,
           CT_COL, CT_PAR_OP, CT_PAR_CL, CT_BRA_OP, CT_BRA_CL,
           OP_EQ, OP_PLUS, OP_MINUS, OP_MUL, OP_DIV, OP_LT, OP_GT, OP_AND, OP_OR, OP_XOR, OP_COMP, OP_NOT] = range(19)

    syms = ['\n', ' ',
            ',', '(', ')', '[', ']',
            '=', '+', '-', '*', '/', '<', '>', '&', '|', '^', '~', '!']

    lookup = dict(zip(ids, syms))
    lookup_str = ''.join(syms)
    lines = program.split('\n')
    re_alpha = re.compile("[a-zA-Z_0-9'.]")

    tokens = []
    try:
        line, col, tok = 0, 0, ''
        line_comment = False

        for pos, c in enumerate(program):
            col += 1

            # Find any non-alphanumeric tokens that separate alphanumeric ones
            match = lookup_str.find(c)
            if match > -1:
                if tok:
                    tokens.append(tok)
                tok = ''

                if match == NEWLINE:
                    line += 1
                    col = 0
                    line_comment = False
                    continue

                elif match > SPACE:
                    if match == OP_DIV and tokens[-1] == lookup[OP_DIV]:
                        tokens.pop()
                        line_comment = True

                    if line_comment:
                        continue

                    tokens.append(c)

            # Concat alphanumeric symbols to the current token
            elif re.search(re_alpha, c):
                if line_comment:
                    continue

                tok += c

            # Invalid token
            else:
                raise InvalidSymbolError(line, col, pos, c, lines[line])

    except BaseException as e:
        print(e)

    return tokens
