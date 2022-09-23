#!python3
# -*- coding: utf-8 -*-

import sys
import os.path
import copy

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
DEFAULT_IMAGE = "D:/sample.png"

# TableViewの1行ごとのItemを管理するクラス


class DataItem(object):

    def __init__(self, name="", description="", img=None):

        self.name = name
        self.description = description
        self.img = img if img else DEFAULT_IMAGE
        self.status = "default"

    def backgroundColor(self):

        return QtGui.QColor(255, 255, 100)

    def data(self, column):

        return self.name

    def setData(self, column, value):

        self.name = value

    @classmethod
    def sizeHint(self):

        return QtCore.QSize(250, 200)


class TableDelegate(QtWidgets.QItemDelegate):

    def __init__(self, parent=None):
        super(TableDelegate, self).__init__(parent)

    def editorEvent(self, event, model, option, index):
        """
        TableのCellに対してなにかしらのイベント（クリックした等）が発生したときに呼ばれる
        """
        return False

    def paint(self, painter, option, index):
        """
        Cellの中の描画を行う
        """

        data = index.data(QtCore.Qt.UserRole)

        if option.state & QtWidgets.QStyle.State_HasFocus:
            painter.setBrush(QtGui.QColor(200, 255, 255))
            painter.drawRect(option.rect)
        elif option.state & QtWidgets.QStyle.State_Selected:
            painter.setBrush(QtGui.QColor(236, 255, 255))
            painter.drawRect(option.rect)
        else:
            painter.setBrush(data.backgroundColor())
            painter.drawRect(option.rect)

        margin = 10
        imgHeight = (option.rect.height() / 2) - margin

        if data.img:
            imgRect = copy.deepcopy(option.rect)
            img = QtGui.QImage(data.img)
            imgWidth = (imgHeight / img.size().height()) * img.size().width()
            imgRect.setWidth(imgWidth)
            imgRect.setHeight(imgHeight)

            pos = option.rect.center()
            imgRect.moveCenter(pos)
            imgRect.translate(0, ((imgHeight / 2) * -1) + margin)
            painter.drawImage(imgRect, img)

        # # タイトル表示
        titleRect = copy.deepcopy(option.rect)

        titleRect.setY(imgRect.bottom() + margin)
        titleRect.setHeight(30)

        font = QtGui.QFont("メイリオ", 11)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(titleRect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop | QtCore.Qt.TextWordWrap, data.name)

        descriptionRect = copy.deepcopy(option.rect)
        descriptionRect.setY(titleRect.bottom() + margin)
        descriptionRect.setX(titleRect.left() + margin)
        descriptionRect.setWidth(descriptionRect.width() - (margin * 2))
        descriptionRect.setHeight(50)

        font = QtGui.QFont("メイリオ", 8)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(descriptionRect, QtCore.Qt.AlignLeft | QtCore.Qt.TextWrapAnywhere,
                         data.description)

    def sizeHint(self, option, index):

        if index.isValid():
            return index.data(QtCore.Qt.UserRole).sizeHint()


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, columnNum=5, parent=None):
        super(TableModel, self).__init__(parent)
        self.items = []
        self.columnNum = columnNum

        self.maxRowCount = 5

    def addMaxRow(self, num=5):

        if (len(self.items) / self.columnNum) > self.maxRowCount:
            self.maxRowCount += num
            self.layoutChanged.emit()

    def changeColumnNum(self, num):

        self.columnNum = num
        self.layoutChanged.emit()

    def headerData(self, col, orientation, role):
        return ""

    def addItem(self, item):
        self.items.append(item)

    def rowCount(self, parent=QtCore.QModelIndex()):
        u"""行数を返す"""
        count = int(len(self.items) / self.columnNum) + 1
        if self.maxRowCount > count:
            return count
        else:
            return self.maxRowCount

    def columnCount(self, parent):
        u"""カラム数を返す"""
        if len(self.items) > self.columnNum:
            return self.columnNum
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            return item.data(index.column())

        if role == QtCore.Qt.UserRole:
            return item

    def index(self, row, column, parent):

        index = (((row) * self.columnNum) + column)
        if index < len(self.items):
            item = self.items[index]
            return self.createIndex(row, column, item)
        return QtCore.QModelIndex()

    def flags(self, index):

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable


class CustomTable(QtWidgets.QTableView):

    columnCountChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.columnCount = 5

        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.verticalScrollBar().valueChanged.connect(self.moveSlider)

    def resizeEvent(self, event):

        count = int(event.size().width() / DataItem.sizeHint().width())
        if self.columnCount != count:
            self.columnCount = count
            self.columnCountChange(count)

    def moveSlider(self, value):
        if value == self.verticalScrollBar().maximum():
            self.model().addMaxRow()

    def columnCountChange(self, num):
        self.model().changeColumnNum(num)


class UISample(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(UISample, self).__init__(parent)

        self.view = CustomTable()
        self.setCentralWidget(self.view)

        self.resize(600, 400)

        self.model = TableModel()

        for i in range(200):
            data = DataItem(str(i).zfill(3), f"これは{str(i).zfill(3)}です。")
            self.model.addItem(data)

        self.view.setModel(self.model)
        self.delegate = TableDelegate()
        self.view.setItemDelegate(self.delegate)
        self.view.clicked.connect(self.clicked)

    def clicked(self, index):

        print(index.data(QtCore.Qt.UserRole))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = UISample()
    a.show()
    sys.exit(app.exec_())
