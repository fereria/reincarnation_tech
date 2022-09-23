# -*- coding: utf-8 -*-
import sys
# from PySide2.QtCore import ()
# from PySide2.QtGui import ()
from PySide2.QtWidgets import (QApplication, QMainWindow, QDialog, QTreeView, QDirModel)


class SampleUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        listView = QTreeView()
        self.setCentralWidget(listView)

        model = QDirModel()
        listView.setModel(model)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = SampleUI()
    ui.show()
    sys.exit(app.exec_())
