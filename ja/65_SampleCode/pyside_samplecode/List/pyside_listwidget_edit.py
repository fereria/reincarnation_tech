# -*- coding: utf-8 -*-
import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QListWidget, QListWidgetItem)
from PySide2.QtGui import (QBrush, QColor)
from PySide2.QtCore import Qt


class SampleUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.listWidget = QListWidget()
        self.setCentralWidget(self.listWidget)
        # Listにアイテムを追加する
        for i in ['a', 'b', 'c', 'd', 'e']:
            item = QListWidgetItem(i, self.listWidget)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

        self.listWidget.itemClicked.connect(self.clicked)

    def clicked(self, item):
        # Signalで受け取る場合
        print(item.text())
        # listWidgetから選択されている値を取得したい場合
        print(self.listWidget.currentItem().text())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = SampleUI()
    ui.show()
    sys.exit(app.exec_())
