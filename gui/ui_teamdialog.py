# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'teamdialog.ui'
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
    QHBoxLayout, QHeaderView, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QVBoxLayout, QWidget)

class Ui_TeamDialog(object):
    def setupUi(self, TeamDialog):
        if not TeamDialog.objectName():
            TeamDialog.setObjectName(u"TeamDialog")
        TeamDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(TeamDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = QTableView(TeamDialog)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addPushButton = QPushButton(TeamDialog)
        self.addPushButton.setObjectName(u"addPushButton")

        self.horizontalLayout.addWidget(self.addPushButton)

        self.removePushButton = QPushButton(TeamDialog)
        self.removePushButton.setObjectName(u"removePushButton")

        self.horizontalLayout.addWidget(self.removePushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(TeamDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TeamDialog)
        self.buttonBox.accepted.connect(TeamDialog.accept)
        self.buttonBox.rejected.connect(TeamDialog.reject)

        QMetaObject.connectSlotsByName(TeamDialog)
    # setupUi

    def retranslateUi(self, TeamDialog):
        TeamDialog.setWindowTitle(QCoreApplication.translate("TeamDialog", u"Dialog", None))
        self.addPushButton.setText(QCoreApplication.translate("TeamDialog", u"Add Team", None))
        self.removePushButton.setText(QCoreApplication.translate("TeamDialog", u"Remove Team", None))
    # retranslateUi

