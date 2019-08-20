# QtCore.QAbstractItemModelを使用したカスタムモデルの作成
<!-- SUMMARY: QtCore.QAbstractItemModelを使用したカスタムモデルの作成-->

今回は、AbstractItemModelを使用してカスタムModelを作成してから  
TreeViewを構成するやり方について。  
  
![](https://gyazo.com/33fdd7b440fb299b98e3ae5a0b76e47c.png)

とりあえず長いですが全コードから。

```python
#!python3
# -*- coding: utf-8 -*-

import sys
import os.path

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader


class TreeItem(object):
    def __init__(self, data=None, parent=None):
        
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 1

    def data(self, column):
        return self.itemData['key']
        

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def clear(self):
        self.childItems = []


class TreeItem(BaseItem):

    def __init__(self, data, parent=None):
        super(TreeItem, self).__init__(data=data, parent=parent)

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, items=[], parent=None):
        super(TreeModel, self).__init__(parent)

        self.__items = items
        self.rootItem = BaseItem(("Title",))
        # 現在のページ
        self.page = 0
        # 1ページに表示するItem数
        self.showItemCount = 20
        self.setItems(items)

    def setItems(self, items):

        self.__items = items
        self.setupModelData()

    def addItem(self, item):

        self.__items.append(item)
        self.setupModelData()

    def columnCount(self, parent):
        
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):

        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent):
        
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        
        if not index.isValid():
            return QtCore.QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):

        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def setupModelData(self):
        """
        表示用のItemを再構築する
        """
        self.rootItem.clear()
        parents = {}
        for item in self.__items:
            if item['parent'] in parents:
                p = parents[item['parent']]
            else:
                p = TreeItem(item, self.rootItem)
                self.rootItem.appendChild(p)
                parents[item['parent']] = p
            treeItem = TreeItem(item, p)
            p.appendChild(treeItem)
        self.layoutChanged.emit()


class UISample(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(UISample, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        # カスタムUIを作成
        self.list = QtWidgets.QTreeView()
        layout.addWidget(self.list)

        # てきとうにListに表示するItemの配列を作る
        data = []
        for i in range(5):
            data.append({'parent': 'hogehoge', 'key': 'homuhomu_' + str(i).zfill(3)})
        for i in range(5):
            data.append({'parent': 'fugafuga', 'key': 'homuhomu_' + str(i).zfill(3)})

        self.model = TreeModel(data)
        self.list.setModel(self.model)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = UISample()
    a.show()
    sys.exit(app.exec_())
```

長いですか、いくつか要点をまとめ。

## データ構造を作る

![](https://gyazo.com/bf70ae4a3631451ab1d10df1253bf060.png)

まず、Modelを作成する場合は、指定の構造になるようにItemのツリーを  
クラスオブジェクトで構成します。  
指定の構造は↑の図の通り。  
  
今回はTreeModelで説明しますが、ListでもModelでも基本は同じです。  
（むしろTreeが一番面倒くさい）  
  
![](https://gyazo.com/b43ef8a27e027aab5d23748db0839d45.png)

TreeViewの場合はこうなります。  
今回のサンプルTreeItemですが、オブジェクトに **childItems** と **parentItem**  
変数を持ちます。  
  
```python
    def setupModelData(self):
        """
        表示用のItemを再構築する
        """
        self.rootItem.clear()
        parents = {}
        for item in self.__items:
            if item['parent'] in parents:
                p = parents[item['parent']]
            else:
                p = TreeItem(item, self.rootItem)
                self.rootItem.appendChild(p)
                parents[item['parent']] = p
            treeItem = TreeItem(item, p)
            p.appendChild(treeItem)
        self.layoutChanged.emit()
```
そのツリー構造を作成しているのが「setupModelData」関数です。  
Itemを作成するときに親ノードにあたるItemを指定し、  
オブジェクトを作成したらappendChildで親ノードの子にObjectをセットします。  
  
トップにはRootItemを作成し、Rootは親が「None」になるようにします。  
構造ができたら、このItemツリーをパースする機能をクラスに実装していきます。

## 関数の実装

### 必須なVirtual関数

QtCore.QAbstractItemModelを使用してModelを作成する場合、最低限実装する必要がある  
関数があります。  
それが、

1. columnCount
2. rowCount
3. parent
4. index

この4つになります。  
  
#### column/rowCountについて

![](https://gyazo.com/a5fa8b50a0596785ff1c7f1a8ee41f3a.png)

まず、Countについて。  
これは名前の通り現在の親Index(引数で受け取る)の子がいくつあるかをreturnするようにします。  
TreeViewの場合は、TreeごとにこのCountが呼ばれ  
そのCount分Itemを表示します。

#### parentについて

```python
    def parent(self, index):
        
        if not index.isValid():
            return QtCore.QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)
```

parent関数は、引数のindexの親にあたるModelIndexをreturnするようにします。  
  
![](https://gyazo.com/58169ce2a6467ef4351a007c9f0ce1e1.png)

ここで重要になるのがModelIndexについて。  
PySideのModelは実体を持たずに、あくまでもIndexで親子関係を持ちます。  
実際に表示するItemは「ModelIndex.internalPointer()」に書いてある通り  
**実体までのポインタ** を、ModelIndexが保持します。  
  
このModelIndexを作成しているのが self.createIndex 関数で  
createIndex(row,column,実体のオブジェクト) を渡すことでModelIndexを生成してくれます。  
  
なので、このparent関数がなにをしているかというと

1. 親を取得したいIndexから、Itemの実体を取得
2. 実体のTreeItemのparentを使用して親の実体を取得
3. 親がない＝Rootの場合は空のIndexを返す
4. 親がある場合はcreateIndexを使用して親のModelIndexを返す

このような挙動をしています。  
  
return QtCore.QModelIndex()  
  
こうしている部分は index.isValud() の判定で無効扱いになります。  
  
#### indexについて

基本はparentと同様ですが、こちらは parent から指定のrow/columnのModelIndexを取得します。  

![](https://gyazo.com/c5cd5041f0a3e63f005c558d852f1941.png)

```python
    def index(self, row, column, parent):
        
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
```
parentItemの実体のTreeItemオブジェクトを取得し、  
childを取得、そしてそのChildの実体とrow,columnから  
createIndexを使用してModelIndexを作成して返します。

### 実際の表示をどうするかを指定する

indexとparentを実装することで、最初に作成したItemのツリーをパースする構造はできました。  
パースはできましたが、じゃあ実際に「なにを表示するのか」は data 関数を実装することで  
指定をします。  
  
```python
    def data(self, index, role):
        
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())
```
dataは、表示する場所のindexとroleとよばれる「ふるまい方」を受け取って処理をします。  
このroleは、Viewに関係するいろいろな情報の受け取り口になっています。  
例えば「背景の色」であったり、「文字の色」であったり  
表示する文字であったり、あるいは自分で指定したり。  
その受け取り口の「今回はなにがほしいのか」が入るのがroleになります。  
  
今回のように文字を取得したい場合は、QtCore.Qt.DisplayRole がroleに入るので  
それ以外はNoneで終了、DisplayRoleの場合はItemのdataで指定した文字列が返ります。  
  
あとは必要に応じてflagsやHeaderを指定したりすればOKです。  
（この２つは見ての通りなので今回は説明スキップ）  
  
重要なのはModelIndexのふるまいと構造について。  
Tree構造をオブジェクトで作成し、internalPointerで実体にアクセスしながら  
親のModelIndex、子のModelIndexを作って  
dataで最終的な出力形式を指定する...  
これを押さえておけば、TreeViewでListViewでも、TableViewでも  
同じ考え方でModelを作成することができます。  
  
  
## 参考

* http://www7a.biglobe.ne.jp/~thor/novel/column/11.html







