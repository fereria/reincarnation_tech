---
title: List/Tree Widgetを使おう(3) Widget配置編
tags:
    - PySide
    - ListView
description: TreeWidgetにWidgetを配置して編集できるようにする方法
---

:fa-external-link: [前回](./16_treewidget_edit.md) TreeWidget を使用して編集 UI を作るのをやりましたが
今回はそれの続きで、セルに対してウィジェットを設定して扱う方法を試してみます。

![](https://gyazo.com/650da6c1705a1a85bdb9e6c7ac209d90.png)

実行するとこのようになります

## 全コード

まずは長いですがコード全体

```python
# -*- coding: utf-8 -*-
import sys
import os.path
import json
import codecs

from PySide2.QtCore import (Qt)
from PySide2.QtWidgets import (QApplication, QMainWindow, QTreeWidget,
                               QTreeWidgetItem, QComboBox, QLabel, QProgressBar, QCheckBox)

CURRENT_DIR = os.path.dirname(sys.argv[0]).replace("\\", "/")


class Encode(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, QTreeWidgetItem):
            return [o.text(0), o.text(1), o.text(2), o.text(3), int(o.text(4))]

        return json.JSONEncoder.default(self, o)


class ComboBoxItem(QComboBox):

    def __init__(self, item, column, parent=None):
        super().__init__(parent)

        self.item = item
        self.column = column
        self.currentTextChanged.connect(self.changed)
        self.setCurrentText(self.item.text(self.column))

    def changed(self, text):
        self.item.setText(self.column, text)


class CheckBoxItem(QCheckBox):

    def __init__(self, item, column, parent=None):
        super().__init__(parent)

        self.item = item
        self.column = column

        self.setChecked(bool(int(self.item.text(self.column))))

        self.clicked.connect(self.changed)

    def changed(self, value):

        self.item.setText(self.column, str(int(value)))


class SampleUI(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.resize(800, 400)

        self.jsonPath = f"{CURRENT_DIR}/sample.json"

        with codecs.open(self.jsonPath, 'r', 'utf-8') as f:
            data = json.load(f)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['名前', 'ComboBox', '説明', 'ProgressBar', 'Bool'])
        self.setCentralWidget(self.treeWidget)

        # Listにアイテムを追加する
        for i in data:

            rootItem = QTreeWidgetItem()
            # 編集可能にする
            rootItem.setFlags(rootItem.flags() | Qt.ItemIsEditable)
            # 表示する行の値をセットする
            for num, j in enumerate(i):
                rootItem.setText(num, str(j))
            # Itemを追加
            self.treeWidget.addTopLevelItem(rootItem)

            # Widgetの指定（1列目は今まで通りダブルクリック編集）
            combo = ComboBoxItem(rootItem, 1)
            combo.addItems(['A', 'B', 'C'])
            combo.setCurrentText(i[1])
            self.treeWidget.setItemWidget(rootItem, 1, combo)
            # 編集不可な列にしたい場合
            self.treeWidget.setItemWidget(rootItem, 2, QLabel())
            # プログレスバー表示
            pbar = QProgressBar()
            pbar.setRange(0, 100)
            pbar.setValue(int(i[3]))
            self.treeWidget.setItemWidget(rootItem, 3, pbar)
            # CheckBox
            check = CheckBoxItem(rootItem, 4)
            self.treeWidget.setItemWidget(rootItem, 4, check)

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
        for i in range(item.columnCount()):
            print(item.text(i))
        print('--')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = SampleUI()
    ui.show()
    sys.exit(app.exec_())
```

基本は前回と同じく JSON を編集する UI ですが、TreeWidget のセルに
PySide のウィジェットを指定しています。
いくつかポイントがあるので、その部分を順番に説明していきます。

## 基本

TreeWidget には、PySide のウィジェットを、セル編集用ウィジェットとして
埋め込むことができます。
やり方は簡単で

```python
            pbar = QProgressBar()
            pbar.setRange(0, 100)
            pbar.setValue(int(i[3]))
            self.treeWidget.setItemWidget(rootItem, 3, pbar)
```

埋め込みたいウィジェットのオブジェクトを、 setItemWidget で
指定のカラム番号に対して指定すれば OK です。
この例だと、プログレスバーを作り、現在のセルの値をバーに割合で表示するようにしています。

## 応用例

ProgressBar のように、現在の値を単純に表示したい場合などは良いですが
それ以外の場合は一工夫が必要です。
以下は工夫している箇所を順番に見ていきます。

### 編集不可なセルをつくる

TreeWidget の編集フラグは、各 Item 単位（行単位）で指定されます。
つまりは、このままだとすべてのセルがダブルクリックで編集できてしまうことになります。
ある指定の列だけ編集不可にしたい、といった場合どうしたらいいのか考えましたが

```python
self.treeWidget.setItemWidget(rootItem, 2, QLabel())
```

setItemWidget で QLabel を指定すると、ダブルクリックをしても編集ができないセルを
作成することができました。

### CheckBox を追加する

次に、編集 GUI にチェックボックスを追加したい場合。
この場合は、配置するだけでは変更などが正しく反映されないので工夫が必要になります。

```python
class CheckBoxItem(QCheckBox):

    def __init__(self, item, column, parent=None):
        super().__init__(parent)

        self.item = item
        self.column = column

        self.setChecked(bool(int(self.item.text(self.column))))

        self.clicked.connect(self.changed)

    def changed(self, value):

        self.item.setText(self.column, str(int(value)))
```

まず、使用したいウィジェットを継承したクラスを作成します。
そしてこのウィジェットに編集対象の Item とカラム数を指定できるようにして、
CheckBox がクリックされたらその Item に対して現在の値をセットするようにします。

!!! info

    サンプルの場合、JSONを 0 or 1 の数字で保存するようにしているので
    bool → int にしている＋ItemのsetTextではstrにしなければいけないので
    int → str を入れています。
    そのうえで、JSONに書き込む場合はEncoderで str → int しています。

このように拡張したクラスを

```python
            check = CheckBoxItem(rootItem, 4)
            self.treeWidget.setItemWidget(rootItem, 4, check)
```

setItemWidget でセットすれば CheckBox を追加することができます。

### ComboBox を追加する

CheckBox と基本は同じやりかたをすれば、ComboBox で選択肢から登録するような
GUI を作成できます。

```python
class ComboBoxItem(QComboBox):

    def __init__(self, item, column, parent=None):
        super().__init__(parent)

        self.item = item
        self.column = column
        self.currentTextChanged.connect(self.changed)
        self.setCurrentText(self.item.text(self.column))

    def changed(self, text):
        self.item.setText(self.column, text)
```

QComboBox を継承したクラスを作成し、currentTextChanged で
カラムが変更されたタイミングで Item に対して setText するようにしておきます。

```python
            combo = ComboBoxItem(rootItem, 1)
            combo.addItems(['A', 'B', 'C'])
            combo.setCurrentText(i[1])
            self.treeWidget.setItemWidget(rootItem, 1, combo)
```

使いかたは ComboBox と同じで、 addItems で選択肢を追加し、
setCurrentText() で、現在の値を選択するようにします。

!!! note

    ComboBoxItemの引数で選択肢を渡すようにして、
    コンストラクタ内で self.setCurrentText(self.item.text(self.column))
    のようにしてもよさそう

拡張したウィジェットで値が変更された場合も、
TreeWidget の itemChanged が実行されるようになるので
これで問題なく JSON が更新できるようになりました。

## まとめ

表示方法、編集方法、その応用　と 3 回に分けて List・TreeWidget の使い方を解説してきました。
多くの場合はこの Widget を利用することで、様々な編集 GUI が作成できそうです。

## 参考

-   https://stackoverflow.com/questions/1667688/qcombobox-inside-qtreewidgetitem
