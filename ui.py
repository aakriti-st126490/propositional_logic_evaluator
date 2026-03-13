# -*- coding: utf-8 -*-
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QStatusBar, QWidget, QFrame
)


class Ui_MainWindow(object):

    WIN_W, WIN_H = 460, 380
    BTN_W, BTN_H = 64, 36
    GAP          = 12
    LEFT         = 20

    def setupUi(self, MainWindow: QMainWindow) -> None:
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(self.WIN_W, self.WIN_H)
        MainWindow.setWindowTitle("Propositional Logic Evaluator")

        cw = QWidget(MainWindow)
        cw.setObjectName("centralwidget")
        MainWindow.setCentralWidget(cw)

        title_font = QFont("Arial", 13, QFont.Weight.Bold)
        label_font = QFont("Arial", 10)
        btn_font   = QFont("Courier New", 12, QFont.Weight.Bold)
        input_font = QFont("Courier New", 12)

        y = 16

        # ── Title ──────────────────────────────────────────────────── #
        self.title_label = QLabel("Propositional Logic Evaluator", cw)
        self.title_label.setObjectName("title_label")
        self.title_label.setGeometry(QRect(self.LEFT, y, 420, 28))
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        y += 38

        sep1 = QFrame(cw)
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setGeometry(QRect(self.LEFT, y, self.WIN_W - 2 * self.LEFT, 2))
        y += 14

        # ── Expression row ─────────────────────────────────────────── #
        expr_lbl = QLabel("Expression:", cw)
        expr_lbl.setFont(label_font)
        expr_lbl.setGeometry(QRect(self.LEFT, y + 4, 90, 22))

        self.input_text = QLineEdit(cw)
        self.input_text.setObjectName("input_text")
        self.input_text.setFont(input_font)
        self.input_text.setGeometry(QRect(114, y, 256, 30))
        self.input_text.setPlaceholderText("e.g.  t v f ^ f")

        self.button_clear = QPushButton("C", cw)
        self.button_clear.setObjectName("button_clear")
        self.button_clear.setFont(btn_font)
        self.button_clear.setGeometry(QRect(378, y, 50, 30))
        y += 46

        # ── Button row 1: t  f  ^  v ───────────────────────────────── #
        bx = self.LEFT
        for attr, label, tip in [
            ("button_t",   "t", "Insert true"),
            ("button_f",   "f", "Insert false"),
            ("button_and", "^", "Insert AND (higher precedence)"),
            ("button_or",  "v", "Insert OR (lower precedence)"),
        ]:
            btn = QPushButton(label, cw)
            btn.setObjectName(attr)
            btn.setFont(btn_font)
            btn.setGeometry(QRect(bx, y, self.BTN_W, self.BTN_H))
            btn.setToolTip(tip)
            setattr(self, attr, btn)
            bx += self.BTN_W + self.GAP
        y += self.BTN_H + self.GAP

        # ── Evaluate button ─────────────────────────────────────────── #
        self.button_evaluate = QPushButton("Evaluate", cw)
        self.button_evaluate.setObjectName("button_evaluate")
        self.button_evaluate.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.button_evaluate.setGeometry(QRect(self.LEFT + 2*(self.BTN_W + self.GAP), y, 200, self.BTN_H))
        y += self.BTN_H + 18

        sep2 = QFrame(cw)
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setGeometry(QRect(self.LEFT, y, self.WIN_W - 2 * self.LEFT, 2))
        y += 14

        # ── Truth value row ────────────────────────────────────────── #
        tv_lbl = QLabel("Truth value:", cw)
        tv_lbl.setFont(label_font)
        tv_lbl.setGeometry(QRect(self.LEFT, y + 2, 100, 24))

        self.truth_value_label = QLabel("—", cw)
        self.truth_value_label.setObjectName("truth_value_label")
        self.truth_value_label.setFont(QFont("Courier New", 22, QFont.Weight.Bold))
        self.truth_value_label.setGeometry(QRect(124, y - 4, 120, 36))
        self.truth_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # Use QPalette to set color — this is immune to stylesheet inheritance issues
        pal = self.truth_value_label.palette()
        pal.setColor(pal.ColorRole.WindowText, QColor("#555555"))
        self.truth_value_label.setPalette(pal)
        y += 42

        # ── Prefix form row ────────────────────────────────────────── #
        pf_lbl = QLabel("Prefix form:", cw)
        pf_lbl.setFont(label_font)
        pf_lbl.setGeometry(QRect(self.LEFT, y + 4, 100, 22))

        self.prefix_output = QLineEdit(cw)
        self.prefix_output.setObjectName("prefix_output")
        self.prefix_output.setFont(input_font)
        self.prefix_output.setReadOnly(True)
        self.prefix_output.setGeometry(QRect(124, y, 310, 30))
        self.prefix_output.setPlaceholderText("prefix notation appears here")
        # Force text/background via QPalette — bypasses all stylesheet color inheritance
        pf_pal = self.prefix_output.palette()
        pf_pal.setColor(pf_pal.ColorRole.Text, QColor("#1a1a2e"))
        pf_pal.setColor(pf_pal.ColorRole.Base, QColor("#edecea"))
        pf_pal.setColor(pf_pal.ColorRole.Window, QColor("#edecea"))
        self.prefix_output.setPalette(pf_pal)
        y += 46

        # ── Status / error label ───────────────────────────────────── #
        self.status_label = QLabel("", cw)
        self.status_label.setObjectName("status_label")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setGeometry(QRect(self.LEFT, y, 420, 20))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        MainWindow.setMenuBar(QMenuBar(MainWindow))
        MainWindow.setStatusBar(QStatusBar(MainWindow))

        MainWindow.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f5f5f0;
            }
            QLabel#title_label {
                color: #1a1a2e;
            }
            QLabel {
                color: #1a1a2e;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1.5px solid #c0bdb5;
                border-radius: 5px;
                padding: 2px 6px;
                color: #1a1a2e;
            }
            QLineEdit:focus {
                border-color: #4a6fa5;
            }
            QPushButton {
                background-color: #dddbd3;
                border: 1.5px solid #b0ada5;
                border-radius: 5px;
                color: #1a1a2e;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #c8c5bc;
                border-color: #8a8880;
            }
            QPushButton:pressed {
                background-color: #b0ada5;
            }
            QPushButton#button_evaluate {
                background-color: #4a6fa5;
                border-color: #3a5f95;
                color: #ffffff;
            }
            QPushButton#button_evaluate:hover {
                background-color: #3a5f95;
            }
            QPushButton#button_evaluate:pressed {
                background-color: #2a4f85;
            }
            QPushButton#button_clear {
                background-color: #c0392b;
                border-color: #a93226;
                color: #ffffff;
            }
            QPushButton#button_clear:hover {
                background-color: #a93226;
            }
            QLabel#status_label {
                color: #c0392b;
            }
        """)
