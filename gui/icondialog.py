from PySide6.QtCore import QDir, Qt, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QPushButton, QSizePolicy

from gui.ui_icondialog import Ui_IconDialog


class IconDialog(QDialog, Ui_IconDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.setWindowTitle("Select icon")

        self.__current_pixmap = QPixmap()

        dir_path = ":images/teams/"
        dir_obj = QDir(dir_path)
        icons_path = dir_obj.entryList()

        r = 0
        c = 0
        for icon_path in icons_path:
            button = QPushButton()
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.pixmap = QPixmap(dir_path + icon_path)
            button.setIcon(button.pixmap)
            button.setIconSize(QSize(50, 50))
            button.clicked.connect(self.__button_clicked)
            self.gridLayout.addWidget(button, r, c)
            c += 1
            if c > 3:
                r += 1
                c = 0

    def __button_clicked(self):
        button: QPushButton = self.sender()
        self.__current_pixmap = button.pixmap

    def current_pixmap(self) -> QPixmap:
        return self.__current_pixmap
