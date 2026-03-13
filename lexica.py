from sly import Lexer


class PropLexer(Lexer):
    """
    Lexer for propositional logic expressions.

    Tokens recognised:
      TRUE   -> 't'
      FALSE  -> 'f'
      AND    -> '^'  (higher precedence)
      OR     -> 'v'  (lower precedence)

    Grammar the lexer feeds:
      expr -> TRUE | FALSE | expr AND expr | expr OR expr
    """

    tokens = {TRUE, FALSE, AND, OR}

    # Whitespace is silently skipped
    ignore = ' \t'

    # Literal truth values – must be matched BEFORE the general NAME rule
    # so 't' and 'f' are not accidentally swallowed as identifiers.
    TRUE   = r't'
    FALSE  = r'f'

    # Logical operators
    AND    = r'\^'
    OR     = r'v'


    # Track line numbers so error messages are useful
    @_(r'\n+')
    def ignore_newline(self, token):
        self.lineno += token.value.count('\n')

    def error(self, token):
        print(f"[Lexer] Illegal character '{token.value[0]}' at line {self.lineno}")
        self.index += 1


if __name__ == '__main__':
    lex = PropLexer()
    for expr in ['t', 'f', 't ^ f', 't v f', 't ^ f v f', 't v f ^ f']:
        print(f"\nInput: {expr!r}")
        for tok in lex.tokenize(expr):
            print(' ', tok)
