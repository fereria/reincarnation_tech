# -*- coding: utf-8 -*-
import sys
# from PySide2.QtCore import ()
# from PySide2.QtGui import ()
from PySide2.QtWidgets import (QApplication, QMainWindow, QDialog, QListWidget, QListWidgetItem)


class SampleUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        listWidget = QListWidget()
        self.setCentralWidget(listWidget)
        # Listにアイテムを追加する
        for i in ['a', 'b', 'c', 'd', 'e']:
            QListWidgetItem(i, listWidget)

        listWidget.itemClicked.connect(self.clicked)

    def clicked(self, item):
        print(item.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = SampleUI()
    ui.show()
    sys.exit(app.exec_())
