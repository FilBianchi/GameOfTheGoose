from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsScene

from gameofthegoose import Game, SkipTurnBox, RollTheDiceAgainBox, ChallengeBox, QuizBox
from gameofthegoose.giocodelloca import Quiz, Team

from gui.controllerdialog import ControllerDialog
from gui.teamdialog import TeamDialog
from gui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle(QApplication.instance().applicationName() +
                            " - " +
                            QApplication.instance().applicationVersion())

        self.__game = Game()
        self.__game.load("game.xml")

        team_dialog = TeamDialog()
        team_dialog.exec_()
        teams = team_dialog.get_teams()

        for team in teams:
            self.__game.add_team(team)

        self.__controller_dialog = ControllerDialog()
        self.__controller_dialog.clicked.connect(self.__click)
        self.__controller_dialog.show()

        self.__scene = QGraphicsScene()
        self.graphicsView.setScene(self.__scene)

        self.__game.init_graphics()
        self.__scene.addItem(self.__game)

    def __click(self):
        self.__game.next()
