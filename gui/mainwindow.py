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

        #icon_dialog = TeamDialog()
        #icon_dialog.exec_()

        self.__game = Game()
        self.__game.load("game.xml")
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(QuizBox(Quiz("Anno della prima ascensione dell'Everest?",
        #                          ["1933",
        #                           "1947",
        #                           "1953",
        #                           "1967"],
        #                          [True, False, False, False])))
        # self.__game.add_box(QuizBox(Quiz("Qual'è l'altezza massima del Monte Rosa?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(ChallengeBox())
        # self.__game.add_box(SkipTurnBox())
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["4554m",
        #                           "4615",
        #                           "4637",
        #                           "4701"],
        #                          [True, False, False, False])))
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(ChallengeBox())
        # self.__game.add_box(RollTheDiceAgainBox())
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(ChallengeBox())
        # self.__game.add_box(SkipTurnBox())
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(QuizBox(Quiz("Qual'è la montagna più alta dei pirenei?",
        #                          ["Macizo de la Maladeta",
        #                           "Moncayo",
        #                           "Azkorri",
        #                           "Comabona"],
        #                          [True, False, False, False])))
        # self.__game.add_box(ChallengeBox())
        # self.__game.add_box(RollTheDiceAgainBox())

        team = Team()
        team.set_name("Pippo")
        team.set_pixmap(QPixmap(":/images/teams/picca.png"))
        team.set_color(QColor(255, 0, 0))
        self.__game.add_team(team)

        team = Team()
        team.set_name("Pluto")
        team.set_pixmap(QPixmap(":/images/teams/locker.png"))
        team.set_color(QColor(0, 0, 255))
        self.__game.add_team(team)

        team = Team()
        team.set_name("Paperino")
        team.set_pixmap(QPixmap(":/images/teams/helmet.png"))
        team.set_color(QColor(0, 255, 0))
        self.__game.add_team(team)

        team = Team()
        team.set_name("Minnie")
        team.set_pixmap(QPixmap(":/images/teams/compass.png"))
        team.set_color(QColor(255, 255, 0))
        self.__game.add_team(team)

        team = Team()
        team.set_name("Qui")
        team.set_pixmap(QPixmap(":/images/teams/rope.png"))
        team.set_color(QColor(0, 255, 255))
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
