---
title: AbstractItemModelでItemを追加・削除
---

[以前](custom_model.md)AbstractItemModel を作ったときは Item の追加や削除したときの
挙動を正しく理解できていなかったのですが、
最近正しい作法？を理解したのでメモをば。

https://snippets.cacher.io/snippet/631af0caf686255ebd58
全コードはこちら。

## Model と View について

PySide で TreeView や ListView、TableView を作る際には
表示に関わる部分を View、中のデータ部分を Model として実装します。

View はいわゆるフロントエンドで、ユーザーが触りその変更などを Model に通知します。
Model 側は、View 側からの変更を受け取り
実データを変更する部分を行います。

なので、View は Model に対して変更を通知し
Model はその変更を View 側に通知する必要があります。

## 今までのやり方

今までどうやってたかというと、

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

self.layoutChanged.emit()

を利用して、Model の構造が変わったから View を更新するように
通知していました。
あるいは
self.dataChanged.emit(top,bottom)
を使用して、指定の ModelIndex を使用して指定の Item をアップデートするようにしていました。

が、この場合いくつか問題があって
ProxyModel で正規表現を使用した絞り込みをしたときに妙な挙動になったり
特にデータが削除した場合 internalPointer が Null を指してしまい
Python が異常終了したりしてしまい
非常に不安定になってしまいました。

このあたりどうやるのが正解なんだ？
と、かなり悩んでいたのですがようやくまともな方法がみつかりました。

## Model のアップデート方法

モデルの更新をする場合は layoutChanged.emit() でシグナルを Emit するのではなく
https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractItemModel.html#PySide2.QtCore.PySide2.QtCore.QAbstractItemModel.beginInsertColumns
begin###～～から始まる関数群を使用することです。

```python
    def setupModelData(self):
        """
        表示用のItemを再構築する
        """
        self.rootItem.clear()
        parents = {}
        self.beginResetModel()
        for item in self.__items:
            if item['parent'] in parents:
                p = parents[item['parent']]
            else:
                p = TreeItem(item, self.rootItem)
                self.rootItem.appendChild(p)
                parents[item['parent']] = p
            treeItem = TreeItem(item, p)
            p.appendChild(treeItem)
        self.endResetModel()
```

まずはリセットから。
すべての Tree 構造をアップデートする場合は beginResetModel ～ endResetModel
これを、Model のデータ構造を操作する間を囲います。

### 追加する

```python
    def addItem(self, parent, text):

        item = parent.internalPointer()
        self.beginInsertRows(parent, item.childCount(), item.childCount())
        i = TreeItem(data={"key": text}, parent=item)
        item.appendChild(i)
        self.endInsertRows()
```

次が追加。
追加する場合は beginInsertRows() を使用します。
この場合は、追加する Item の親と、追加先の Index を指定します。

![](https://gyazo.com/913e903652f1708215b820baa7b6896e.png)

PySide の Model は ModelIndex の Index で管理されていて、
その実体 internalPointer() を使用して実体の Item を取得できます。

Model の構造を作るときは Item の木構造の作成と
その木構造の Index の更新をする必要があります。
木構造側は appendChild と parent 指定で作っていますが
それが ModelIndex のうちどれが更新されているのか？というのを beginInsertRows で
指定してアップデートします。

なので、追加する場合は
まず ModelIndex から Item オブジェクトを取得して、
その Item オブジェクトに TreeItem を追加し、
どの Index が追加されるかを beginInsertRows で指定しています。

こうすると、内部で columnsAboutToBeInserted()シグナルが Emit されて
指定部分だけが更新されます。

### 削除する

```python
    def removeItem(self, item):

        parent = self.parent(item)
        if parent.isValid():
            pItem = parent.internalPointer()
            self.beginRemoveRows(parent, item.row(), item.row())
            pItem.removeChild(item.row())
            self.endRemoveRows()
```

削除側も理屈は同じで、変更する ModelIndex の指定と
Item 側の木構造から削除したい Item を削除するのを書きます。

Item 側は配列から Item を削除すれば良いので

```python
    def removeChild(self, row):
        self.childItems.pop(row)
```

Child から指定の番号を pop しています。

![](https://i.gyazo.com/3ff82459ca7bd512b2df740348d82f78.gif)

結果。
begin ～ end で囲った中で、Itemの木構造を更新し
begin に変更するItemのparentとIndexを指定することでデータ更新...
これで、指定部分だけのアップデートができるようになります。

layoutChanged を使うのとは違って、指定のIndexのみをアップデートすると
高速なのとTreeViewの場合はTabが開いたまま追加・削除できるメリットがあるので
やりたい操作に応じて begin - end の関数を使い分けるのが良さそうです。