---
title: 基本Widgetを使ってみる(5): ListWidget TreeWidget
tags:
    - PySide
    - Python
description:
---

PySide には Model を自分で実装して使用する TreeView / ListView がありますが
もう少し手軽にリストを表示したりしたい場合に使用できる「 ListWidget / TreeWidget」が
あります。

今回は、この TreeWidget の基本的な使い方を見ていきたいと思います。

## ListWidget

![](https://gyazo.com/aa5a2615997dbd302666c6eea36153a0.png)

ListWidget は、その名の通り１列のみのシンプルなリストを作成できるウィジェットです。
この基本的なサンプルが以下のコードです。

```python
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
            # 背景色を指定したい場合
            item.setBackground(QBrush(QColor(255, 0, 0)))

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
```

ListWidget に項目を追加する場合は、
List に表示するアイテムは、「ListWidgetItem」というクラスを使用します。

![](https://gyazo.com/c95d8a93d60ada0ca8dbf563357a948e.png)

Item は、List に表示されている項目を管理するためのクラスで、
表示する文字列や Icon、背景色、フォントなど
１項目をどのように表示するかは、この Item 側で指定します。

```python
        for i in ['a', 'b', 'c', 'd', 'e']:
            item = QListWidgetItem(i, listWidget)
            brush = QBrush(QColor(255, 0, 0))
            item.setBackground(brush)
```

例として、背景色を帰る場合。
Item に対して setBackground を指定することで
![](https://gyazo.com/b7aafb9cb7abb275848e43df294b858c.png)
色を指定することができました。

現在選択中の項目を取得したい場合も、 currentItem() で QListWidgetItem を取得できるので
そこから item.text() で、文字列を取得したり、背景色などの値も取得できます。

## TreeWidget

次に TreeWidget。
こちらも ListWidget と同じく QTreeWidgetItem を使用して項目を追加していきます。

```python
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
        # 子供のItemを取得する場合
        if item.childCount() == 0:
            print('子供はいません')
        else:
            for i in range(item.childCount()):
                print(item.child(i).text(0))

        # 親を取得
        if item.parent():
            print(item.parent().text(0))
        else:
            print('RootItemです。')

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = SampleUI()
    ui.show()
    sys.exit(app.exec_())

```

![](https://gyazo.com/f6c8dc196af4add9116f9f594972f5d7.png)

実行結果はこのようになります。
List との違いは、
![](https://gyazo.com/8c1040341960ea477b9054339d4b8c1c.png)
列が複数あるので、 setText でどの列に対して表示するかを指定します。

```python
        rootItem = QTreeWidgetItem()
        rootItem.setText(0, "hoge")
        rootItem.setText(1, "ほげです。")
```

もう一つが、
TreeWidgetItem は、List とは違い addChild をすることで木構造を作成します。

```python
treeWidget.addTopLevelItem(rootItem)
```

TopLebelItem が、TreeWidget の直下に表示される Item です。
それ以下の子 Item は、

```python
        for i in ['A', 'B', 'C']:
            cItem = QTreeWidgetItem()
            cItem.setText(0, i)
            rootItem.addChild(cItem)
```

親 Item の子供として addChild で Item を追加します。

### Item の親・子を取得する場合

```python
    def clicked(self, item):

        print(item.text(0))  # クリックしたItemをプリント
        # 子供のItemを取得する場合
        if item.childCount() == 0:
            print('子供はいません')
        else:
            for i in range(item.childCount()):
                print(item.child(i).text(0))

        # 親を取得
        if item.parent():
            print(item.parent().text(0))
        else:
            print('RootItemです。')
```

選択している Item を取得するのは List と共通ですが、それ以外に
Item の親や子を取得したりすることができます。

## まとめ

以上が ListWidget / TreeWidget の基本的な使い方でした。
重要なポイントは、それぞれ「Item」クラスを使用することでリストに追加できること
各項目の設定もこの Item でできること。
TreeView の場合は、Item を親子化することで、木構造を作れること　です。

TreeView に比べると、細かいカスタマイズはできませんが
多くの場合はこの Widget と Item で対応できるので
List を作成したい場合はおすすめです。
