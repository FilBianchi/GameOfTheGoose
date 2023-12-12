from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPixmap, QPen, QBrush, QColor
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, \
    QGraphicsPixmapItem

from giocodelloca.dialogs import QuizDialog, ChallengeDialog

if TYPE_CHECKING:
    from giocodelloca.teams import Team


class Quiz:

    def __init__(self, question: str, answers: List[str], right_answers: List[bool]):
        self.__question = question
        self.__answers = answers
        self.__right_answers = right_answers

    def question(self):
        return self.__question

    def answers(self):
        return self.__answers

    def right_answers(self):
        return self.__right_answers


class Challenge:

    def __init__(self, text: str):
        self.__text = text

    def text(self):
        return self.__text


class Box(QGraphicsItemGroup):

    def __init__(self,
                 pixmap: Optional[QPixmap] = None,
                 parent: Optional[QGraphicsItem] = None):
        QGraphicsItemGroup.__init__(self, parent)

        self.__pixmap = pixmap

        self.__team_pos = {}

        self.__pos = []
        self.__pos.append(QPoint(50, 100))
        self.__pos.append(QPoint(100, 100))
        self.__pos.append(QPoint(100, 50))
        self.__pos.append(QPoint(100, 0))
        self.__pos.append(QPoint(50, 0))
        self.__pos.append(QPoint(0, 0))

        self.idx = None

    def init_graphics(self, size: int):
        self._draw_content(size, self.__pixmap)

    def _draw_content(self, size: int, pixmap: Optional[QPixmap] = None):

        # Rectangle
        pen = QPen()
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(QColor(255, 255, 255))
        rect = QGraphicsRectItem(0, 0, size, size)
        rect.setPen(pen)
        rect.setBrush(brush)
        self.addToGroup(rect)

        # Text
        idx = self.parentItem().boxes().index(self)
        if (idx != 0) and (idx != (len(self.parentItem().boxes()) - 1)):
            text = QGraphicsTextItem(str(idx))
            text.setPos(QPoint(5, 3))
            text.setZValue(4)
            self.addToGroup(text)

        # Pixmap
        if pixmap is not None:
            pixmap_item = QGraphicsPixmapItem(pixmap)
            sx = size / pixmap_item.boundingRect().width()
            sy = size / pixmap_item.boundingRect().height()
            if sx < sy:
                s = sx
            else:
                s = sy
            pixmap_item.setScale(s * 0.8)
            p = (size - (pixmap_item.boundingRect().width() * pixmap_item.scale())) / 2
            pixmap_item.setPos(QPoint(p, p))
            self.addToGroup(pixmap_item)

    def assign_team_pos(self, team: Team) -> QPoint:
        p = self.__pos.pop()
        self.__team_pos[team] = p
        return self.mapToScene(p)

    def release_team_pos(self, team: Team):
        p = self.__team_pos.pop(team)
        self.__pos.append(p)

    def execute(self, team: Team) -> bool:
        return True


class StartBox(Box):

    def __init__(self, parent: Optional[QGraphicsItem] = None):
        Box.__init__(self, QPixmap(":images/boxes/start.png"), parent)


class FinishBox(Box):

    def __init__(self, parent: Optional[QGraphicsItem] = None):
        Box.__init__(self, QPixmap(":images/boxes/finish.jpg"), parent)


class QuizBox(Box):

    def __init__(self, quiz: Quiz, parent: Optional[QGraphicsItem] = None):
        Box.__init__(self, QPixmap(":images/boxes/question_mark.png"), parent)

        self.__quiz = quiz

    def execute(self, team: Team) -> bool:
        dialog = QuizDialog(self.__quiz)
        dialog.exec_()
        return dialog.quiz_result()


class ChallengeBox(Box):

    def __init__(self, challenge: Challenge, parent: Optional[QGraphicsItem] = None):
        Box.__init__(self, QPixmap(":images/boxes/medal.png"), parent)

        self.__challenge = challenge

    def execute(self, team: Team) -> bool:
        dialog = ChallengeDialog(self.__challenge)
        dialog.exec_()
        return dialog.challenge_result()


class SkipTurnBox(Box):

    def __init__(self, parent: Optional[QGraphicsItem] = None):
        Box.__init__(self, QPixmap(":images/boxes/rest.png"), parent)

    def execute(self, team: Team) -> bool:
        team.skip_turn = True
        return True


class RollTheDiceAgainBox(Box):
    def __init__(self, parent: Optional[QGraphicsItem] = None):
        Box.__init__(self, QPixmap(":images/boxes/dice.png"), parent)
