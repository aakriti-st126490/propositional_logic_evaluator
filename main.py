import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QKeySequence, QShortcut, QColor
from PySide6.QtCore import Qt

from ui      import Ui_MainWindow
from lexica  import PropLexer
from parsers import PropParser


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._lexer  = PropLexer()
        self._parser = PropParser()

        self.ui.button_t.clicked.connect(lambda: self._insert("t"))
        self.ui.button_f.clicked.connect(lambda: self._insert("f"))
        self.ui.button_and.clicked.connect(lambda: self._insert(" ^ "))
        self.ui.button_or.clicked.connect(lambda: self._insert(" v "))
        self.ui.button_evaluate.clicked.connect(self._evaluate)
        self.ui.button_clear.clicked.connect(self._clear)

        for key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            sc = QShortcut(QKeySequence(key), self)
            sc.activated.connect(self._evaluate)

    def _set_truth_color(self, hex_color: str) -> None:
        """Set truth_value_label text color via QPalette (always visible)."""
        pal = self.ui.truth_value_label.palette()
        pal.setColor(pal.ColorRole.WindowText, QColor(hex_color))
        self.ui.truth_value_label.setPalette(pal)

    def _insert(self, text: str) -> None:
        self.ui.input_text.setText(self.ui.input_text.text() + text)
        self.ui.input_text.setFocus()
        self.ui.status_label.setText("")

    def _clear(self) -> None:
        self.ui.input_text.clear()
        self.ui.truth_value_label.setText("—")
        self._set_truth_color("#555555")
        self.ui.prefix_output.clear()
        self.ui.status_label.setText("")
        self.ui.input_text.setFocus()

    def _evaluate(self) -> None:
        expression = self.ui.input_text.text().strip()
        if not expression:
            self._show_error("Please enter an expression first.")
            return

        try:
            tree = self._parser.parse(self._lexer.tokenize(expression))
        except Exception as exc:
            self._show_error(f"Parse error: {exc}")
            return

        if tree is None:
            self._show_error("Invalid expression — check your syntax.")
            return

        truth_val = tree.evaluate()
        prefix    = tree.prefix()

        self.ui.truth_value_label.setText("t" if truth_val else "f")
        self._set_truth_color("#1a8a45" if truth_val else "#b05f00")
        self.ui.prefix_output.setText(prefix)
        self.ui.status_label.setText("")

    def _show_error(self, message: str) -> None:
        self.ui.status_label.setText(message)
        self.ui.truth_value_label.setText("—")
        self._set_truth_color("#555555")
        self.ui.prefix_output.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
