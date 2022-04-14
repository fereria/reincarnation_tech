# -*- coding: utf-8 -*-
import sys
# from PySide2.QtCore import ()
# from PySide2.QtGui import ()
from PySide2.QtWidgets import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem)


class SampleUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        treeWidget = QTreeWidget()
        treeWidget.setColumnCount(2)
        treeWidget.setHeaderLabels(['名前', "説明"])
        self.setCentralWidget(treeWidget)
        # Listにアイテムを追加する
        rootItem = QTreeWidgetItem()
        rootItem.setText(0, "hoge")
        rootItem.setText(1, "ほげです。")
        # 一番上のItemを追加
        treeWidget.addTopLevelItem(rootItem)
        # その子供にもItemを追加
        for i in ['A', 'B', 'C']:
            cItem = QTreeWidgetItem()
            cItem.setText(0, i)
            rootItem.addChild(cItem)

        treeWidget.itemClicked.connect(self.clicked)

    def clicked(self, item):
        print(item.text(0))  # クリックしたItemをプリント
        print(item.text(1))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = SampleUI()
    ui.show()
    sys.exit(app.exec_())
