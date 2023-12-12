from __future__ import annotations

from typing import List, Optional

from PySide6.QtCore import QObject, Signal, Qt, QPoint, QLine, QFile, QIODevice
from PySide6.QtGui import QPen, QColor, QBrush, QPixmap, QRadialGradient, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsLineItem, QGraphicsItem, QGraphicsItemGroup, QGraphicsRectItem, \
    QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsEllipseItem, QGraphicsWidget, QGraphicsProxyWidget, QRadioButton
from PySide6.QtXml import QDomDocument, QDomElement

from giocodelloca.boxes import Box, StartBox, FinishBox, Quiz, QuizBox, Challenge, ChallengeBox, SkipTurnBox, \
    RollTheDiceAgainBox
from giocodelloca.dialogs import RollTheDiceDialog, QuizDialog, SkipTheTurnDialog, YesDialog, NoDialog
from giocodelloca.teams import Team


class Game(QGraphicsItemGroup):

    def __init__(self):
        QGraphicsItemGroup.__init__(self)
        self.setHandlesChildEvents(False)

        self.__box_size = 120

        self.__boxes: List[Box] = []
        self.__teams: List[Team] = []

        self.__team_idx = 0

    def load(self, filename: str) -> bool:
        ret = False
        doc = QDomDocument()
        file = QFile(filename)
        if file.open(QIODevice.OpenModeFlag.ReadOnly):
            if doc.setContent(file):
                self.__load(doc)
                ret = True
            file.close()
        return ret

    def __load(self, doc: QDomDocument):
        root = doc.documentElement()
        node = root.firstChild()
        while not node.isNull():
            el = node.toElement()
            if not el.isNull():
                name = el.tagName()
                if name == "start":
                    box = StartBox()
                    self.add_box(box)
                if name == "quiz":
                    self.__load_quiz(el)
                if name == "challenge":
                    self.__load_challenge(el)
                if name == "rollthediceagain":
                    box = RollTheDiceAgainBox()
                    self.add_box(box)
                if name == "skiptheturn":
                    box = SkipTurnBox()
                    self.add_box(box)
                if name == "finish":
                    box = FinishBox()
                    self.add_box(box)
            node = node.nextSibling()

    def __load_quiz(self, el: QDomElement):
        question = el.attribute("question", "")
        answers = []
        right_answers = []
        answer_node = el.firstChild()
        while not answer_node.isNull():
            answer_el = answer_node.toElement()
            if not answer_el.isNull():
                if answer_el.tagName() == "answer":
                    answer = answer_el.attribute("text", "")
                    if answer.endswith("*"):
                        right_answers.append(True)
                        answer = answer[:-2]
                    else:
                        right_answers.append(False)
                    answers.append(answer)
            answer_node = answer_node.nextSibling()
        quiz = Quiz(question, answers, right_answers)
        quiz_box = QuizBox(quiz)
        self.add_box(quiz_box)

    def __load_challenge(self, el: QDomElement):
        text = el.attribute("text", "")
        challenge = Challenge(text)
        challenge_box = ChallengeBox(challenge)
        self.add_box(challenge_box)

    def add_box(self, box: Box):
        box.setParentItem(self)
        self.__boxes.insert(len(self.__boxes), box)

    def add_team(self, team: Team):
        self.__teams.insert(len(self.__teams) - 1, team)

    def boxes(self) -> List[Box]:
        return self.__boxes

    def init_graphics(self):
        item = QGraphicsPixmapItem(QPixmap(":/images/game_background.jpg"))
        item.setScale(1.5)
        item.setZValue(-2)
        self.addToGroup(item)

        i = 0
        box_size = 120
        x_interbox = 70
        y_interbox = 25

        p = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0],
             [7, 1], [7, 2], [7, 3], [7, 4],
             [6, 4], [5, 4], [4, 4], [3, 4], [2, 4], [1, 4], [0, 4],
             [0, 3], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2]]

        p_old = None
        for box in self.__boxes:
            pp = QPoint(25 + p[i][0] * (box_size + x_interbox), 25 + p[i][1] * (box_size + y_interbox))
            box.init_graphics(self.__box_size)
            box.idx = i
            box.setPos(pp)
            self.addToGroup(box)
            if p_old is not None:
                pen = QPen()
                pen.setWidth(20)
                pen.setColor(QColor(0, 0, 255))
                item = QGraphicsLineItem(QLine(p_old.x() + (box_size / 2),
                                               p_old.y() + (box_size / 2),
                                               pp.x() + (box_size / 2),
                                               pp.y() + (box_size / 2)))
                item.setPen(pen)
                item.setZValue(-1)
                self.addToGroup(item)
            p_old = pp
            i += 1

        for team in self.__teams:
            team.init_graphics(50)
            team.set_box(self.__boxes[0])
            self.addToGroup(team)

    def next(self):
        team = self.__teams[self.__team_idx]
        if not team.skip_turn:
            old_idx = team.box().idx
            dialog = RollTheDiceDialog(team)
            dialog.exec_()
            val = dialog.dice_value()
            self.__move_team(team, val)
            box = team.box()

            if type(box) == RollTheDiceAgainBox:
                dialog = RollTheDiceDialog(team)
                dialog.exec_()
                val = dialog.dice_value()
                self.__move_team(team, val)
                box = team.box()

            result = box.execute(team)
            if not result:
                dialog = NoDialog()
                dialog.exec_()
                team.set_box(self.__boxes[old_idx])
            else:
                dialog = YesDialog()
                dialog.exec_()
        else:
            dialog = SkipTheTurnDialog(team)
            dialog.exec_()
            team.skip_turn = False

        self.__next_team()

    def finish(self):
        pass

    def set_box_result(self, result: bool):
        pass

    def __move_team(self, team: Team, val: int):
        box = team.box()
        idx = box.idx + val
        team.set_box(self.__boxes[idx])

    def __next_team(self):
        self.__team_idx += 1
        if self.__team_idx >= len(self.__teams):
            self.__team_idx = 0
