from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsProxyWidget, QRadioButton, QGraphicsItemGroup, \
    QGraphicsPixmapItem, QGraphicsItem, QButtonGroup, QVBoxLayout, QGroupBox, QFrame, QPushButton, QDialog, QLabel, \
    QSpinBox, QDialogButtonBox, QMessageBox, QHBoxLayout

if TYPE_CHECKING:
    from gameofthegoose.boxes import Quiz, Challenge
    from gameofthegoose.giocodelloca import Team


class Dialog(QDialog):

    def __init__(self, parent: Optional[QGraphicsItem] = None):
        QDialog.__init__(self, parent)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        self._background = QLabel()
        pixmap = QPixmap(":/images/message_background.png")
        self._background.setPixmap(pixmap.scaled(600, 700, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(self._background)


class RollTheDiceDialog(Dialog):

    def __init__(self, team: Team, parent: Optional[QGraphicsItem] = None):
        Dialog.__init__(self, parent)

        s = "Team {}! \n ROLL THE DICE!".format(team.name())

        font = QFont("Times", 20)

        layout = QVBoxLayout(self._background)
        layout.setContentsMargins(100, 100, 100, 100)

        question_text = QLabel()
        question_text.setWordWrap(True)
        question_text.setFont(font)
        question_text.setText(s)
        layout.addWidget(question_text)

        self.__spin_box = QSpinBox()
        self.__spin_box.setMinimum(1)
        self.__spin_box.setMaximum(6)
        layout.addWidget(self.__spin_box)

        button_box = QDialogButtonBox()
        button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        button_box.setCenterButtons(True)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)

    def dice_value(self):
        return self.__spin_box.value()


class SkipTheTurnDialog(Dialog):

    def __init__(self, team: Team, parent: Optional[QGraphicsItem] = None):
        Dialog.__init__(self, parent)

        s = "Team {}! \n SKIP THE TURN!".format(team.name())

        font = QFont("Times", 20)

        layout = QVBoxLayout(self._background)
        layout.setContentsMargins(100, 100, 100, 100)

        question_text = QLabel()
        question_text.setWordWrap(True)
        question_text.setFont(font)
        question_text.setText(s)
        layout.addWidget(question_text)

        button_box = QDialogButtonBox()
        button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        button_box.setCenterButtons(True)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)


class QuizDialog(Dialog):

    def __init__(self, quiz: Quiz, parent: Optional[QGraphicsItem] = None):
        Dialog.__init__(self, parent)

        self.__quiz = quiz

        font = QFont("Times", 20)

        layout = QVBoxLayout(self._background)
        layout.setContentsMargins(100, 100, 100, 100)
        question_text = QLabel()
        question_text.setWordWrap(True)
        question_text.setFont(font)
        question_text.setText(quiz.question())
        layout.addWidget(question_text)

        font = QFont("Times", 14)
        self.__radio_buttons: List[QRadioButton] = []
        for answer in quiz.answers():
            h_layout = QHBoxLayout()
            radio_button = QRadioButton()
            radio_button.setFont(font)
            radio_button.setText(answer)
            h_layout.addWidget(radio_button)
            self.__radio_buttons.append(radio_button)
            layout.addLayout(h_layout)

        button_box = QDialogButtonBox()
        button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)

    def quiz_result(self) -> bool:
        result = True
        for i in range(0, len(self.__radio_buttons)):
            if self.__quiz.right_answers()[i] != self.__radio_buttons[i].isChecked():
                result = False
        return result


class ChallengeDialog(Dialog):

    def __init__(self, challenge: Challenge, parent: Optional[QGraphicsItem] = None):
        Dialog.__init__(self, parent)

        self.__challenge = challenge

        font = QFont("Times", 20)

        layout = QVBoxLayout(self._background)
        button_box = QDialogButtonBox()
        button_box.setStandardButtons(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)
        layout.setContentsMargins(100, 100, 100, 100)
        challenge_text = QLabel()
        challenge_text.setWordWrap(True)
        challenge_text.setFont(font)
        challenge_text.setText(challenge.text())
        layout.addWidget(challenge_text)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def challenge_result(self) -> bool:
        result = False
        if self.result() == 1:
            result = True
        return result


class YesDialog(QDialog):

    def __init__(self, parent: Optional[QGraphicsItem] = None):
        QDialog.__init__(self, parent)

        layout = QVBoxLayout(self)
        self._background = QLabel()
        pixmap = QPixmap(":/images/yes.gif")
        self._background.setPixmap(pixmap)
        layout.addWidget(self._background)


class NoDialog(QDialog):

    def __init__(self, parent: Optional[QGraphicsItem] = None):
        QDialog.__init__(self, parent)

        layout = QVBoxLayout(self)
        self._background = QLabel()
        pixmap = QPixmap(":/images/no.jpg")
        self._background.setPixmap(pixmap)
        layout.addWidget(self._background)


class WinnerDialog(QDialog):

    def __init__(self, team: Team, parent: Optional[QGraphicsItem] = None):
        QDialog.__init__(self, parent)

        layout = QVBoxLayout(self)
        self._background = QLabel()
        pixmap = QPixmap(":/images/winner.png")
        self._background.setPixmap(pixmap)
        layout.addWidget(self._background)

        s = "The winner is {}!".format(team.name())

        font = QFont("Times", 20)

        layout = QVBoxLayout(self._background)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        text = QLabel()
        text.setWordWrap(True)
        text.setFont(font)
        text.setText(s)
        layout.addWidget(text)
