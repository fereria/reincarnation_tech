---
title: QAbstractItemModelのdataの使い方
---

TreeView を使用するとき、各セルの見た目を細かく調整したい場合は  
デリゲートを作り、paint で細かく自前で書くことで調整ができたりしますが  
正直そこまでするのはめんどくさい...ということもけっこうあります。

そういうときは、Model 内の data の **Role** を使用することで、  
ある程度表示を調整できたりするので  
今回は使えそうなものをいくつかテストしてみました。

![](https://gyazo.com/d300bfc02ecbc24d74860a5ec863ae33.png)

完成図はこちら。

https://snippets.cacher.io/snippet/27cf2d61d60cc5220fce

コードはそこそこ長いので、全コードは ↑ にアップしました。

## QAbstractItemModel から Model クラスを作る

まず Model を作ります。
PySide の ListView は複数カラムを持つことができませんので、上のような  
複数カラムを持つ TreeView を使用します。

この TreeView で使用するための Model は QAbstractItemModel を使用する必要があります。  
このクラスは

- index
- parent
- data
- rowCount
- columnCount

を実装する必要があるのですが、親子化なしの場合はどう作るかがわかりにくいですが

```python
    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, None)

    def parent(self, index):
        """
        引数のIndexの親ModelIndexを返す
        """
        return QModelIndex()
```

特に親子化が不必要な場合は、上のように index と parent を作れば OK です。
（parent が QModelIndex()の場合は、いわゆるルート Item 扱いになるから）

## data・Role について

この Model クラスは、 data 関数を経由して、View で表示するのに  
必要な各種データをやり取りしています。
表示に必要なのは「文字列」とかが考えられますが  
PySide の場合はそれ以外にも「背景色」「文字色」「整列（センタリング）」なども  
この data を経由してやり取りされます。  
では、どのデータがやり取りされているのかというのを判断しているのは  
なにかというと、それが「Role」と呼ばれるもので  
data 関数の 2 つ目の引数としてうけとります。

```python
    def data(self, index, role=Qt.DisplayRole):

        item = self.items[index.row()]

        # 以下色々...

```

data は様々な用途で呼ばれますが、「何に呼ばれたか」を判定するのが role で  
その Role は [こちら](https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html?highlight=pyside2%20qtcore%20qt%20itemdatarole#PySide2.QtCore.PySide2.QtCore.Qt.ItemDataRole)にリストがあります。  
主なものとしては、表示される文字列の DisplayRole、背景色の BackgroundRole などがあります。

つまりは、この data 関数内で role で判定することで、  
セルの見た目をいい感じに変更することができるというわけです。

その中から使えそうなものをテストしてみました。

### DisplayRole

```python
        if role == Qt.DisplayRole:
            return item.data(index.column())
```

おそらく必須なのが DisplayRole
これの return した結果がセルの文字列として表示されます。

列方向は、 index.column() で、何列目を処理しているかを受け取ることができるので

```python
class Item:

    def __init__(self, name="", value="", status=ItemStatus.Waiting):

        self.__data = {
            'name': name,
            'value': value,
            'status': status
        }

    def data(self, column):

        if column == 0:
            if 'name' in self.__data:
                return self.__data['name']
        if column == 1:
            if 'status' in self.__data:
                return self.__data['status'].name
        if column == 2:
            if 'value' in self.__data:
                return self.__data['value']
        return ""
```

このように、表示したいアイテムのクラスを用意して、
取得したい値を返すようにしています。

### BackgroundRole

```python
        # 背景色
        if role == Qt.BackgroundRole:
            return item.getBackgroundColor(index.column())
```

![](https://gyazo.com/b9b196c53c9748a6a5214e43c9b23960.png)

BackgroundRole は、QColor を返すことで、背景色を変更することができます。

```python
    def getBackgroundColor(self, column):

        COLORS = {
            'Waiting': QColor(173, 216, 230),
            'Working': QColor(221, 160, 221),
            'Finish': QColor(153, 255, 153),
            'Error': QColor(255, 51, 102)
        }
        if column == 1:
            return COLORS[self.data(column)]
```

使い方としては、ステータスごとに色を変えたい...みたいなときに  
Item クラス側などに色を取得する関数を入れておくなどができます。

### TextColorRole

```python
        if role == Qt.TextColorRole:
            # 文字の色を変える
            if index.column() == 2:
                return QColor(0, 255, 0)
```

![](https://gyazo.com/5698b72cbe22d1e516913f3b4cf38664.png)

TextColorRole は、表示される文字の色を変更するときに使用します。

### TextAlignmentRole

```python
        if role == Qt.TextAlignmentRole:
            if index.column() == 1:
                return Qt.AlignCenter
```

AlignmentRole は、文字の整列をどうするか（右寄せ・左寄せ・センタリングなど）を
変更することができます。
ステータス表示とかは、センタリングしたほうが見た目が良いので  
そういうときは指定の列のみセンタリングする...みたいな使い方ができます。

### DecorationRole

```python
        if role == Qt.DecorationRole:
            # アイコンを追加
            if index.column() == 0:
                return QPixmap("D:/icons8-folder.svg")
```

DecorationRole は、文字の左側にアイコンを指定することができる Role です。
![](https://gyazo.com/6811ce76f03787ea3c3a042f8279d531.png)
表示したい Icon の QPixmap または QIcon または QColor を指定することができます。

### ToolTipRole

```python
        if role == Qt.ToolTipRole:
            return item.getToolTip()
```

ToolTipRole は、セルにマウスオーバーしたときに表示される ToolTip を
変更することができる Role です。
これを使用すると、各セルごとに Tooltop の文言を
自由に変更することができます。

### SizeHintRole

```python
        if role == Qt.SizeHintRole:
            # セルの大きさを返す
            return QSize(150, 60)
```

SizeHintRole は、各セルごとの大きさを指定することができます。

```python
        self.model = SampleListModel()
        self.view.setModel(self.model)
        self.view.setItemsExpandable(False)
        self.view.setRootIsDecorated(False)
        header = self.view.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
```

この SizeHint でサイズを変えるのは、ResizeToContents を指定したときに  
使用される値になります。

### UserRole

```python
        if role == Qt.UserRole:
            return item
```

最後は UserRole
UserRole は実際にデータを使うときに

```python
    def doubleClicked(self, item):
        # ダブルクリックすると、クリックした行のItemを取得できる
        data = item.data(Qt.UserRole)
        print(data)
```

ModelIndex から値を取得したいときなどに
表示する以外に値を渡せるようにしたい場合等に使用します。
上の例だと、Item オブジェクトを取得できるようになります。

## まとめ

Icon 表示はデリゲートを書かないとできないものだとおもってましたが  
モデルだけでもできるのは初めて知りました。
大体の場合はこの実装でなんとかなりそうです。
