# -*- coding: utf-8 -*-
import sys
import os.path
import json
import codecs

from PySide2.QtCore import (Qt)
# from PySide2.QtGui import ()
from PySide2.QtWidgets import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem)

CURRENT_DIR = os.path.dirname(sys.argv[0]).replace("\\", "/")


class Encode(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, QTreeWidgetItem):
            return [o.text(0), o.text(1)]

        return json.JSONEncoder.default(self, o)


class SampleUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(600, 400)

        self.jsonPath = f"{CURRENT_DIR}/sample.json"

        with codecs.open(self.jsonPath, 'r', 'utf-8') as f:
            data = json.load(f)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['名前', "説明"])
        self.setCentralWidget(self.treeWidget)

        # Listにアイテムを追加する
        for i in data:
            rootItem = QTreeWidgetItem()
            rootItem.setFlags(rootItem.flags() | Qt.ItemIsEditable)
            rootItem.setText(0, i[0])
            rootItem.setText(1, i[1])
            # 一番上のItemを追加
            self.treeWidget.addTopLevelItem(rootItem)

        self.treeWidget.itemClicked.connect(self.clicked)
        self.treeWidget.itemChanged.connect(self.edit)

    def edit(self, item):
        items = []
        for i in range(self.treeWidget.topLevelItemCount()):
            items.append(self.treeWidget.topLevelItem(i))

        with codecs.open(self.jsonPath, 'w', 'utf-8') as f:
            f.write(json.dumps(items, cls=Encode, ensure_ascii=False))

    def clicked(self, item):
        # クリックしたItemをプリント
        print(item.text(0))
        print(item.text(1))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = SampleUI()
    ui.show()
    sys.exit(app.exec_())
