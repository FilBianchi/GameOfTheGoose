from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog
from gui.ui_controllerdialog import Ui_ControllerDialog


class ControllerDialog(QDialog, Ui_ControllerDialog):
    clicked = Signal()
    dice_value = Signal(int)

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)

        self.setWindowTitle("Controller")

        self.nextPushButton.clicked.connect(self.clicked)


