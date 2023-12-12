from typing import Optional, Union, Any, List

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt, QObject
from PySide6.QtGui import QAction, QBrush
from PySide6.QtWidgets import QDialog, QStyledItemDelegate, QWidget, QStyleOptionViewItem, QColorDialog

from gameofthegoose.teams import Team
from gui.icondialog import IconDialog
from gui.ui_teamdialog import Ui_TeamDialog


class TeamTableModel(QAbstractTableModel):

    def __init__(self, parent: Optional[QObject] = None):
        QAbstractTableModel.__init__(self, parent)

        self.__headers = ["Name", "Color", "Icon"]
        self.__teams: Optional[List[Team]] = None

    def set_source(self, teams: List[Team]):
        self.__teams = teams

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        ret = 0
        if self.__teams is not None:
            ret = len(self.__teams)
        return ret

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__headers)

    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlag:
        ret = Qt.ItemFlag.ItemIsEnabled
        if index.column() == 0:
            ret |= Qt.ItemFlag.ItemIsEditable
        return ret

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        ret = None
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                ret = self.__headers[section]
            if orientation == Qt.Orientation.Vertical:
                ret = str(section + 1)
        return ret

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        ret = None
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            if col == 0:
                ret = self.__teams[row].name()
        if role == Qt.ItemDataRole.BackgroundRole:
            row = index.row()
            col = index.column()
            if col == 1:
                ret = QBrush(Qt.BrushStyle.SolidPattern)
                ret.setColor(self.__teams[row].color())
        if role == Qt.ItemDataRole.DecorationRole:
            row = index.row()
            col = index.column()
            if col == 2:
                ret = self.__teams[row].pixmap()
        return ret

    def setData(self, index: Union[QModelIndex, QPersistentModelIndex], value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            row = index.row()
            col = index.column()
            if col == 0:
                self.__teams[row].set_name(value)
            if col == 1:
                self.__teams[row].set_color(value)
            if col == 2:
                self.__teams[row].set_pixmap(value)
                print("NEW PIXMAP:", value)
        return True

    def insertRows(self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> bool:
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.__teams.insert(row, Team())
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> bool:
        pass


class TeamDialog(QDialog, Ui_TeamDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.__teams: List[Team] = []
        self.__model = TeamTableModel()
        self.__model.set_source(self.__teams)

        self.__add_team_action = QAction("Add Team")
        self.__remove_team_action = QAction("Remove Team")

        self.tableView.addAction(self.__add_team_action)
        self.tableView.addAction(self.__remove_team_action)
        self.tableView.setModel(self.__model)

        self.__add_team_action.triggered.connect(self.__on_add_team_triggered)
        self.addPushButton.clicked.connect(self.__on_add_team_triggered)
        self.__remove_team_action.triggered.connect(self.__on_remove_team_triggered)
        self.removePushButton.clicked.connect(self.__on_remove_team_triggered)
        self.tableView.doubleClicked.connect(self.__on_table_view_double_clicked)

    def __on_add_team_triggered(self):
        self.__model.insertRow(0)

    def __on_remove_team_triggered(self):
        pass

    def __on_table_view_double_clicked(self):
        index = self.tableView.currentIndex()
        col = index.column()

        if col == 1:
            dialog = QColorDialog()
            dialog.exec_()
            color = dialog.currentColor()
            self.tableView.model().setData(index, color)

        if col == 2:
            dialog = IconDialog()
            dialog.exec_()
            self.tableView.model().setData(index, dialog.current_pixmap())
            self.tableView.resizeRowToContents(index.row())
