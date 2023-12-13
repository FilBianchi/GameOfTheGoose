from __future__ import annotations

from typing import List
from logging import getLogger

from PySide6.QtCore import QPoint, QLine, QFile, QIODevice
from PySide6.QtGui import QPen, QColor, QPixmap
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsItemGroup, QGraphicsPixmapItem
from PySide6.QtXml import QDomDocument, QDomElement

from gameofthegoose.boxes import Box, StartBox, FinishBox, Quiz, QuizBox, Challenge, ChallengeBox, SkipTurnBox, \
    RollTheDiceAgainBox
from gameofthegoose.dialogs import RollTheDiceDialog, WinnerDialog
from gameofthegoose.teams import Team

logging = getLogger(__name__)


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

        team = self.current_team()
        box = team.box()
        old_idx = box.idx

        run = True
        while run:
            ret = box.pre_execute(self)
            if ret:
                box = team.box()
                result = box.post_execute(self)
                if result == Box.Result.FINISH_THE_TURN:
                    run = False
                elif result == Box.Result.CAME_BACK:
                    team.set_box(self.__boxes[old_idx])
                    run = False
                elif result == Box.Result.GO_ON:
                    run = True
            else:
                run = False

        self.__next_team()

    def finish(self):
        pass

    def current_team(self):
        return self.__teams[self.__team_idx]

    def move_team(self, team: Team, val: int):
        box = team.box()
        idx = box.idx + val
        if idx < (len(self.__boxes) - 1):
            team.set_box(self.__boxes[idx])
        else:
            team.set_box(self.__boxes[(len(self.__boxes) - 1)])
            team = self.current_team()
            dialog = WinnerDialog(team)
            dialog.exec_()

    def roll_the_dice(self):
        team = self.current_team()
        box = team.box()
        start_idx = box.idx
        if start_idx < (len(self.__boxes) - 1):
            dialog = RollTheDiceDialog(team)
            dialog.exec_()
            val = dialog.dice_value()
            self.move_team(team, val)

    def __next_team(self):
        self.__team_idx += 1
        if self.__team_idx >= len(self.__teams):
            self.__team_idx = 0
