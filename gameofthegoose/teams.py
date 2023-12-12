from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize
from PySide6.QtGui import QBrush, QPixmap, QColor
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItemGroup, QGraphicsPixmapItem

if TYPE_CHECKING:
    from gameofthegoose.boxes import Box


class Team(QGraphicsItemGroup):

    def __init__(self):
        QGraphicsItemGroup.__init__(self)

        self.skip_turn = False

        self.__box = None

        self.__name = "New team"
        self.__pixmap = QPixmap()
        self.__color = QColor(255, 255, 255)

    def set_name(self, name: str):
        self.__name = name

    def name(self):
        return self.__name

    def set_pixmap(self, pixmap: QPixmap):
        self.__pixmap = pixmap

    def pixmap(self) -> QPixmap:
        return self.__pixmap

    def set_color(self, color: QColor):
        self.__color = color

    def color(self) -> QColor:
        return self.__color

    def init_graphics(self, size):
        if (self.__pixmap is not None) and (self.__pixmap.size() != QSize(0, 0)):
            pixmap_item = QGraphicsPixmapItem(self.__pixmap)
            sx = size / pixmap_item.boundingRect().width()
            sy = size / pixmap_item.boundingRect().height()
            if sx < sy:
                s = sx
            else:
                s = sy
            pixmap_item.setScale(s)
            pixmap_item.setZValue(3)
            self.addToGroup(pixmap_item)
        if self.__color is not None:
            color_item = QGraphicsEllipseItem(0, 0, size, size)
            brush = QBrush(self.__color)
            color_item.setBrush(brush)
            color_item.setZValue(2)
            self.addToGroup(color_item)

    def set_box(self, box: Box):
        if self.__box is not None:
            self.__box.release_team_pos(self)
        self.__box = box
        if self.__box is not None:
            self.setPos(self.__box.assign_team_pos(self))

    def box(self) -> Box:
        return self.__box