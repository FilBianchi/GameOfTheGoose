import logging
import sys

from PySide6.QtWidgets import QApplication

import gui.rc_resources
from gui import MainWindow

'''Application entry point'''
if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(threadName)s %(module)s: %(message)s', level=logging.DEBUG)

    app = QApplication(sys.argv)
    app.setOrganizationName("La MULA")
    app.setApplicationName("Gioco dell'oca")
    app.setApplicationVersion("0.0.1")
    main_window = MainWindow()

    main_window.showMaximized()

    app.exec()
