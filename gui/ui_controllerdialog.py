# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'controllerdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_ControllerDialog(object):
    def setupUi(self, ControllerDialog):
        if not ControllerDialog.objectName():
            ControllerDialog.setObjectName(u"ControllerDialog")
        ControllerDialog.resize(207, 75)
        self.verticalLayout = QVBoxLayout(ControllerDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nextPushButton = QPushButton(ControllerDialog)
        self.nextPushButton.setObjectName(u"nextPushButton")

        self.verticalLayout.addWidget(self.nextPushButton)


        self.retranslateUi(ControllerDialog)

        QMetaObject.connectSlotsByName(ControllerDialog)
    # setupUi

    def retranslateUi(self, ControllerDialog):
        ControllerDialog.setWindowTitle(QCoreApplication.translate("ControllerDialog", u"Dialog", None))
        self.nextPushButton.setText(QCoreApplication.translate("ControllerDialog", u"Next", None))
    # retranslateUi

