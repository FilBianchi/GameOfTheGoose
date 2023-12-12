# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'icondialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QSizePolicy, QVBoxLayout, QWidget)

class Ui_IconDialog(object):
    def setupUi(self, IconDialog):
        if not IconDialog.objectName():
            IconDialog.setObjectName(u"IconDialog")
        IconDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(IconDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(IconDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(IconDialog)
        self.buttonBox.accepted.connect(IconDialog.accept)
        self.buttonBox.rejected.connect(IconDialog.reject)

        QMetaObject.connectSlotsByName(IconDialog)
    # setupUi

    def retranslateUi(self, IconDialog):
        IconDialog.setWindowTitle(QCoreApplication.translate("IconDialog", u"Dialog", None))
    # retranslateUi

