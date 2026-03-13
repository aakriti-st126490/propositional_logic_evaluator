from enum import Enum
from abc import ABC, abstractmethod


class Operations(Enum):
    AND = 'AND'
    OR  = 'OR'


class PLExpr(ABC):
    """Abstract base for every node in the propositional-logic AST."""

    @abstractmethod
    def evaluate(self) -> bool:
        """Return the truth value of this sub-expression."""

    @abstractmethod
    def prefix(self) -> str:
        """Return a prefix-notation (Polish notation) string."""


class PLLiteral(PLExpr):
    """A leaf node: one of the truth values t (True) or f (False)."""

    def __init__(self, value: bool) -> None:
        self._value = value

    def evaluate(self) -> bool:
        return self._value

    def prefix(self) -> str:
        return 't' if self._value else 'f'

    def __repr__(self) -> str:
        return f"PLLiteral({'t' if self._value else 'f'})"


class PLBinary(PLExpr):
    """An interior node: operator applied to two sub-expressions."""

    def __init__(self, op: Operations, left: PLExpr, right: PLExpr) -> None:
        assert op in Operations, f"Unknown operator: {op}"
        self.op    = op
        self.left  = left
        self.right = right

    def evaluate(self) -> bool:
        lv = self.left.evaluate()
        rv = self.right.evaluate()
        if self.op == Operations.AND:
            return lv and rv
        else:                            # OR
            return lv or rv

    def prefix(self) -> str:
        op_symbol = '^' if self.op == Operations.AND else 'v'
        return f"{op_symbol} {self.left.prefix()} {self.right.prefix()}"

    def __repr__(self) -> str:
        return f"PLBinary({self.op.value}, {self.left!r}, {self.right!r})"


if __name__ == '__main__':
    # Manual test: build the tree for  (t ^ f) v f
    tree = PLBinary(
        Operations.OR,
        PLBinary(Operations.AND, PLLiteral(True), PLLiteral(False)),
        PLLiteral(False)
    )
    print("Tree     :", tree)
    print("Evaluate :", tree.evaluate())   # False
    print("Prefix   :", tree.prefix())     # v ^ t f f
