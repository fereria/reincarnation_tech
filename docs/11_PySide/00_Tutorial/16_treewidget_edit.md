---
title: List/Tree Widgetを使おう(2) 編集編
tags:
    - PySide
    - ListView
    - JSON
    - Python
description: TreeWidgetでJsonを編集してみる
---

:fa-external-link: [前回](./15_listwidget.md) ListWidget を表示できるようにしましたが
それだけではなく、List の内容を編集したいということが発生するかと思います。
そういった場合にどうやったらいいのかを解説します。

## 全コード

```python
# -*- coding: utf-8 -*-
import sys
import os.path
import json
import codecs

from PySide2.QtCore import (Qt)
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
```

全コードはこんな感じになります。

![](https://gyazo.com/9a3929a35983c28f44c243d3d9d4e760.gif)

```json
[
	["D", "aaaa"],
	["C", "bbbb"]
]
```

今回の処理はシンプルで、同じフォルダにある指定の構造の json を
TreeView で表示して、リストが変更されたら json も変更します。

変更可能にするにはいくつか重要なポイントがあるので、それぞれを見ていきます。

## setFlags

まず一番大切な個所が、 item に対して指定する Flags です。
変更できるかどうかは、TreeWidget ではなく、各 Item ごとに指定します。
その指定は Flags で指定されます。

```python
        # Listにアイテムを追加する
        for i in data:
            rootItem = QTreeWidgetItem()
            rootItem.setFlags(rootItem.flags() | Qt.ItemIsEditable) # この部分
            rootItem.setText(0, i[0])
            rootItem.setText(1, i[1])
            # 一番上のItemを追加
            self.treeWidget.addTopLevelItem(rootItem)
```

この Flags は、 :fa-external-link: [Qt.ItemFlag](https://doc.qt.io/qtforpython-5/PySide2/QtCore/Qt.html?highlight=itemflags#PySide2.QtCore.PySide2.QtCore.Qt.ItemFlag) にあるフラグで指定します。
編集可能にしたいのならば、 Qt.ItemIsEditable を追加します。

この Flags は、ビットフラグになっているので複数指定したい場合は | を使用します。
なので、現状デフォルトで指定されている Flags に対して（今回なら ItemIsEditable）
を指定したい場合は、 item.flags() | Qt.ItemIsEditable のようにして指定を追加します。

これを入れれば変更は可能になります。

## itemChanged

```python
    def edit(self, item):
        items = []
        for i in range(self.treeWidget.topLevelItemCount()):
            items.append(self.treeWidget.topLevelItem(i))

        with codecs.open(self.jsonPath, 'w', 'utf-8') as f:
            f.write(json.dumps(items, cls=Encode, ensure_ascii=False))
```

編集したら、その編集をトリガーにして何かをしたい場合には この itemChanged で Signal を送ります。
今回の場合、Json がリストになっていて、それが TopLevel 以下に指定されているので
TopLevel の数を数えて、全部の Item を Json に対して Dump するようにしています。

引数は、現在編集している Item のオブジェクトがくるので
編集したらその Item の値に対してなにかをする...みたいなのは
この書き方で作成ができます。

※ 木構造になっていた場合は、トラバースするコードにすればいける ※

## まとめ

今回は TreeWidget でしたが、ListView でも基本は同じです。

1. 編集するかどうかは Item で指定する
2. Widget の itemChanged で編集した Item に対して何かをするのようなものが書ける

この２つを抑えておけば、何かしらのファイルを編集するようなツールが簡単にできます。
