from PySide6.QtWidgets import QDialog

from gui.ui_rollthedicedialog import Ui_RollTheDiceDialog


class ControllerDialog(QDialog, Ui_RollTheDiceDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)

