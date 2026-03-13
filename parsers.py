import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sly import Parser
from lexica import PropLexer
from astree.statement import Operations, PLLiteral, PLBinary


class PropParser(Parser):
    """
    LALR(1) parser for propositional logic.

    Grammar (in BNF form):
        statement : expr

        expr : expr OR expr          (lowest precedence, left-associative)
             | expr AND expr         (higher precedence, left-associative)
             | TRUE
             | FALSE

    Precedence (declared lowest → highest):
        left  OR
        left  AND

    The 'precedence' declaration resolves all shift/reduce conflicts
    introduced by the ambiguous grammar above.  AND binds more tightly
    than OR, matching the problem specification
    ("^ has higher priority than v").

    Outputs (from parse()):
        A PLExpr AST node whose .evaluate() and .prefix() methods
        deliver the two required outputs.
    """

    debugfile = 'parser.out'        # sly writes the LALR tables here
    start     = 'statement'
    tokens    = PropLexer.tokens

    # Precedence: listed from LOWEST to HIGHEST
    precedence = (
        ('left', OR),               # v  — low priority
        ('left', AND),              # ^  — high priority
    )

    # ------------------------------------------------------------------ #
    #  statement rule                                                      #
    # ------------------------------------------------------------------ #

    @_('expr')
    def statement(self, p):
        # Return the root AST node; main.py will call .evaluate() / .prefix()
        return p.expr

    # ------------------------------------------------------------------ #
    #  expr rules                                                          #
    # ------------------------------------------------------------------ #

    @_('expr OR expr')
    def expr(self, p):
        return PLBinary(Operations.OR, p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return PLBinary(Operations.AND, p.expr0, p.expr1)

    @_('TRUE')
    def expr(self, p):
        return PLLiteral(True)

    @_('FALSE')
    def expr(self, p):
        return PLLiteral(False)

    # ------------------------------------------------------------------ #
    #  Error recovery                                                      #
    # ------------------------------------------------------------------ #

    def error(self, p):
        if p:
            print(f"[Parser] Syntax error at token '{p.value}' (line {p.lineno})")
        else:
            print("[Parser] Syntax error: unexpected end of input")


if __name__ == '__main__':
    lexer  = PropLexer()
    parser = PropParser()

    test_cases = [
        ('t',            True,  't'),
        ('f',            False, 'f'),
        ('t ^ f',        False, '^ t f'),
        ('t v f',        True,  'v t f'),
        # Key example from the spec: t v f ^ f  →  t
        # Because ^ binds first:  t v (f ^ f)  =  t v f  =  True
        ('t v f ^ f',    True,  'v t ^ f f'),
        # Parentheses override default precedence
        ('t ^ (f v f)',  False, '^ t v f f'),
        ('(t v f) ^ f',  False, '^ v t f f'),
        # AND chain
        ('t ^ t ^ f',    False, '^ t ^ t f'),
    ]

    print(f"{'Expression':<20} {'Result':<8} {'Prefix'}")
    print('-' * 50)
    for expr_str, expected_val, expected_prefix in test_cases:
        tree = parser.parse(lexer.tokenize(expr_str))
        val    = tree.evaluate()
        prefix = tree.prefix()
        ok = '✓' if (val == expected_val and prefix == expected_prefix) else '✗'
        print(f"{expr_str:<20} {str(val):<8} {prefix}  {ok}")
