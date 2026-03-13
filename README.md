# Propositional Logic Evaluator

An evaluator for a propositional logic that tells us two things: whether it evaluates to true or false, and what it looks like written in prefix notation.

Built with Python, [sly](https://github.com/dabeaz/sly) for lexing/parsing, and PySide6 for the GUI.

---

## What it does

Type an expression using `t` (true), `f` (false), `^` (AND), and `v` (OR), then hit **Evaluate**.

```
Input:   t v f ^ f
Result:  t
Prefix:  v t ^ f f
```

`^` has higher precedence than `v`, so `t v f ^ f` is read as `t v (f ^ f)`, not `(t v f) ^ f`.

---

## Installation

You need Python 3.10+ and two packages:

```bash
pip install sly PySide6
```

Then run from anywhere:

```bash
python path/to/prop_logic/main.py
```

---

## Syntax

| Symbol | Meaning | Precedence |
|--------|---------|------------|
| `t` | true | — |
| `f` | false | — |
| `^` | AND | higher |
| `v` | OR | lower |

Both operators are left-associative. `t ^ f ^ t` parses as `(t ^ f) ^ t`.

You can type expressions directly into the input field or use the buttons. The **C** button clears everything.

---

## Examples

| Expression | Result | Prefix |
|------------|--------|--------|
| `t` | t | `t` |
| `t ^ f` | f | `^ t f` |
| `t v f` | t | `v t f` |
| `t v f ^ f` | t | `v t ^ f f` |
| `f v t ^ f` | f | `v f ^ t f` |
| `t ^ f v t` | t | `v ^ t f t` |

---

## Project structure

```
prop_logic/
├── main.py          # application entry point, PySide6 MainWindow
├── ui.py            # widget layout (mirrors the Ui_MainWindow pattern)
├── lexica.py        # tokeniser — turns the input string into a token stream
├── parsers.py       # LALR(1) parser — builds the AST from tokens
└── ast/
    └── statement.py # AST node classes: PLLiteral, PLBinary
```

The flow when you press Evaluate:

```
input string  →  PropLexer  →  token stream  →  PropParser  →  AST  →  .evaluate() / .prefix()
```

The parser never computes anything directly — it just builds a tree. `evaluate()` and `prefix()` are methods on the tree nodes, so adding a new kind of output (a truth table, CNF form, etc.) only requires adding a new method, not touching the parser.

---

## How the parser works

The grammar is intentionally ambiguous:

```
expr  ::=  expr 'v' expr
        |  expr '^' expr
        |  't'
        |  'f'
```

Ambiguity is resolved by a precedence declaration in `parsers.py` — `^` is declared higher than `v`, and both are left-associative. sly uses this to build an LALR(1) parse table that handles operator priority without requiring a more complex unambiguous grammar.

---

## Dependencies

- [sly](https://github.com/dabeaz/sly) — lexer and LALR(1) parser generator
- [PySide6](https://doc.qt.io/qtforpython/) — Qt bindings for the GUI
