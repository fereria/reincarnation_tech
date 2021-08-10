# -*- coding: utf-8 -*-
# 参考C++コード
# https://stackoverflow.com/questions/55820951/qt-flowlayout-example-how-to-get-sizehint-to-be-called-when-layout-changes
# https://code.qt.io/cgit/qt/qtbase.git/tree/examples/widgets/layouts/flowlayout/flowlayout.cpp?h=5.15

# HEADER:START
title = "tagClowd実装サンプル"
tags = ['PySide']
# HEADER:END


import sys
import os.path
import os

from PySide2.QtWidgets import (QApplication,
                               QDialog,
                               QLayout,
                               QPushButton,
                               QLayoutItem,
                               QLineEdit,
                               QLabel,
                               QVBoxLayout,
                               QHBoxLayout,
                               QWidget,
                               QFrame)
from PySide2.QtCore import (QSize, QRect, Qt, QPoint, Signal)
from PySide2.QtGui import QColor, QIcon, QPixmap, QCursor
from PySide2.QtUiTools import QUiLoader

CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))


class FlowLayout(QLayout):
    def __init__(self, margin: int, hSpacing: int, vSpacing: int, parent=None):
        super().__init__(parent)

        self.setContentsMargins(margin, margin, margin, margin)

        self.itemList = []
        self.hSpacing = hSpacing
        self.vSpacing = vSpacing

    def clear(self):

        self.itemList = []
        self.doLayout()

    def addItem(self, item: QLayoutItem):

        self.itemList.append(item)

    def count(self):

        return len(self.itemList)

    def itemAt(self, index: int):

        if self.count() > 0 and index < self.count():
            return self.itemList[index - 1]
        return None

    def takeAt(self, index):

        if index >= 0 and index < self.count():
            return self.itemList.pop(index - 1)
        return None

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width: int):
        height = self.doLayout(QRect(0, 0, width, 0))
        return height

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):

        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())

        return size

    def setGeomertry(self, rect):
        # 配置されるWidgetのジオメトリを計算するときに呼び出される
        super().setGeometry(rect)
        self.doLayout(rect)

    def doLayout(self, rect=QRect(0, 0, 0, 0)):

        # rect は、現在のLayoutの矩形
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            # 次のWidgetの配置場所
            nextX = x + item.sizeHint().width() + self.hSpacing
            if nextX - self.hSpacing > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + self.vSpacing
                nextX = x + item.sizeHint().width() + self.hSpacing
                lineHeight = 0

            item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


class Tag(QFrame):

    deleteTag = Signal(object)

    def __init__(self, name="", color: QColor = QColor(200, 200, 200), deletable=True, parent=None):
        super().__init__(parent)

        css = f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});border-radius: 5px;"
        self.setStyleSheet(css)
        self.label = QLabel(name)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(10, 5, 10, 5)

        if deletable:
            self.button = QPushButton()
            icon = QIcon()
            icon.addPixmap(QPixmap("D:/work/py37/PySide/icons/batu.png"), QIcon.Normal, QIcon.On)
            self.button.setIcon(icon)
            self.button.setFlat(True)
            layout.addWidget(self.button)
            self.button.clicked.connect(self.delete)

    @property
    def name(self):
        return self.label.text()

    def delete(self):

        self.deleteTag.emit(self)


class PopupEdit(QDialog):

    send = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)

        self.edit = QLineEdit(self)
        layout.addWidget(self.edit)
        self.setLayout(layout)
        # 現在のマウス位置にGUIを出す
        size_x = 200
        size_y = 50
        pos = QCursor().pos()
        self.setGeometry(pos.x() - size_x,
                         pos.y() - size_y,
                         size_x,
                         size_y)

        self.edit.returnPressed.connect(self.Submit)
        self.edit.setFocus()

    def Submit(self):
        # Enterしたら文字をEmitして閉じる
        self.send.emit(self.edit.text())
        self.close()


class TagCrowd(QWidget):

    def __init__(self, addNewTag=True, deletetable=True, parent=None):
        super().__init__(parent)

        self.layout = FlowLayout(3, 5, 5)
        self.setLayout(self.layout)

        self.addNewTag = addNewTag
        self.deletable = deletetable

        if addNewTag:
            self.button = QPushButton(self)
            self.button.clicked.connect(self.showAddEdit)
            icon = QIcon()
            icon.addPixmap(QPixmap("D:/work/py37/PySide/icons/plus.png"), QIcon.Normal, QIcon.On)
            self.button.setIcon(icon)
            self.button.setFlat(True)

        self.tags = []

    def getTagNames(self):

        return [x.name for x in self.tags]

    def showAddEdit(self):

        editor = PopupEdit(self)
        editor.send.connect(self.addTag)
        editor.show()

    def deleteTag(self, widget):

        self.tags = [x for x in self.tags if x.name != widget.name]
        widget.deleteLater()

    def addTag(self, name):

        self.layout.clear()
        currentTags = [x.name for x in self.tags]

        if name not in currentTags:
            tag = Tag(name, deletable=self.deletable)
            tag.deleteTag.connect(self.deleteTag)
            self.tags.append(tag)

        for i in self.tags:
            self.layout.addWidget(i)

        if self.addNewTag:
            self.layout.addWidget(self.button)


class SampleUI(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = QUiLoader().load(f"{CURRENT_PATH}/scroll.ui")

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.ui)

        self.crowd = TagCrowd()
        self.ui.scrollArea.setWidget(self.crowd)

        self.crowd.addTag('aaa')
        self.crowd.addTag('bbb')
        self.crowd.addTag('ccc')

        self.ui.pushButton.clicked.connect(self.showTags)

    def showTags(self):
        print(self.crowd.getTagNames())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setFallbackSessionManagementEnabled(True)
    a = SampleUI()
    a.show()
    sys.exit(app.exec_())
