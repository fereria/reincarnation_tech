---
title: PySideでUSD関係のGUIを作ろう - SceneGraph(1)
---

最近PySideを触っていなくてすっかり頭から抜けてしまったので、リハビリがてらUsd関係の共通GUIを
作っていこうと思います。
まずはUsdのシーングラフをTreeViewで表示するためのModelを作って見ます。

![](https://gyazo.com/9cf9bd866c9735d142353296c2ff941c.png)

完成はこんな感じ。

## 表示するデータ

```
#usda 1.0

def Xform "test"
{
    def "hello"{}
    def "world"{}
    def "hoge"
    {
        def "fuga"{}
    }
}
```
表示するUSDはこんな感じ。
とりあえずはシンプルな状態から。

## ソースコード

長いけど全コード

```python
# -*- coding: utf-8 -*-

import sys
import os.path
from PySide2.QtWidgets import (QApplication, QMainWindow, QTreeView)
from PySide2.QtCore import (QModelIndex, Qt, QAbstractItemModel)
from PySide2.QtUiTools import QUiLoader

from pxr import Usd, Sdf

sample_usd = "D:/work/usd_py36/usd/tree_view_sample.usda"


class UISample(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(600, 400)

        self.view = QTreeView()

        self.ui = QUiLoader().load('D:/work/usd_py36/pysidse/tree_view.ui')
        self.setCentralWidget(self.ui)

        self.model = UsdStageModel(sample_usd)
        self.ui.treeView.setModel(self.model)


class PrimItem(object):

    def __init__(self, prim=None, parentItem=None):
        self._prim = prim
        self._parentItem = parentItem
        self._childItems = []

    def addChild(self, item):
        self._childItems.append(item)

    def getChild(self, row):
        if row <= len(self._childItems):
            return self._childItems[row]
        return None

    def getChildren(self):

        return self._childItems

    def getParentItem(self):
        return self._parentItem

    def getPrim(self):
        return self._prim

    def row(self):
        return self._parentItem.getChildren().index(self)

    def data(self, column):

        if column == 0:
            return self._prim.GetName()
        if column == 1:
            return self._prim.GetTypeName()
        if column == 2:
            return str(self._prim.GetPath())


class UsdStageModel(QAbstractItemModel):
    header = ["PrimName", "Type", "SdfPath"]

    def __init__(self, usdPath: str, parent=None):
        super().__init__(parent)

        # self.setupModelData(data.split('\n'), self.rootItem)
        self.stage = Usd.Stage.Open(usdPath)

        self.createModelTree()

    def createModelTree(self):

        # {SdfPath:Item}
        self.rootItem = PrimItem(self.stage.GetPrimAtPath("/"), None)
        prims = {Sdf.Path("/"): self.rootItem}
        for prim in self.stage.Traverse():
            print(prims)
            parentPath = prim.GetParent().GetPath()
            item = PrimItem(prim, prims[parentPath])
            prims[parentPath].addChild(item)
            prims[prim.GetPath()] = item

    def columnCount(self, parent):
        return 3

    def data(self, index, role):

        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()
        return item.data(index.column())

    def index(self, row, column, parent):

        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.getChild(row)

        if childItem:
            index = self.createIndex(row, column, childItem)
            return index
        else:
            return QModelIndex()

    def parent(self, index):

        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.getParentItem()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):

        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return len(parentItem.getChildren())

    def headerData(self, section, orientation, role):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = UISample()
    a.show()
    sys.exit(app.exec_())
```
以前にも作ったTreeViewの基本構造そのままです。
Modelに渡したUsdFileをTraverseして、Parent/Childの構造をつくります。
ItemにPrimObjectを入れて、そのItemを経由してViewに表示したい文字列を返すようにします。

コレを作る前は、
別にItem作らなくても、CreateIndexでPrimObjectをセットして、
GetParent()/GetChildren()使えばいいんじゃね？
と、試してみたのですが
その場合、internalPointerの部分で問答無用でスクリプトが落ちてしまい動きませんでした。
ポインタでオブジェクト取得してくる当たりが具合が悪いのか....

USDのリポジトリにはusdviewのソースコードも含まれているので
じゃあこちらはどうやってるのかなぁとみてみたら

pxr/usdImaging/lib/usdviewq/primViewItem.py

ここにコードがありました。
usdviewは、TreeWidgetつかってるのかぁとかWidgetItemで実装できるんだ、とか
色々と発見があったのですが
こちらでもItemにPrimObjectを入れて色々やっていたので
私もPrimItemを作る構造にしました。

## 次は

とりあえずこれで基本構造はできたので、今度はこれをGUI上から編集できるように
してみようとおもいます。