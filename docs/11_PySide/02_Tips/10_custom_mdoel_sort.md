---
title: QAbstractItemModelでSort
---

[前回](08_custom_Model.md)　 AbstractItemModel の基本構造を書いたのですが、
この CustomModel を使用したときの TreeView などの Sort を、
やるたびにいつも忘れるので方法をメモしておきます。

## コード

全コードはそこそこ長い+前回とほとんど同じなので
https://snippets.cacher.io/snippet/17e93f71a07ad817b015
こちらを参照。

まず、ソートをしたい場合はデフォルト状態ではなく 2 箇所設定をする必要があるところがあります。

```python
class UISample(QDialog):
    def __init__(self, parent=None):
        super(UISample, self).__init__(parent)

        layout = QVBoxLayout()
        self.view = QTreeView()
        self.view.setSortingEnabled(True)
        layout.addWidget(self.view)
        self.setLayout(layout)
```

まず 1 箇所目は TreeView の setSortingEnabled を True にします。
ここを ON にすることで、TreeView の Header で Sort をできるようになります。

ただし、ここを変更しただけでは実際に Sort は動きません。

AbstractItemModel を使用している場合は、Sort 部分を自前で実装しないと Sort できません。

```python
    def sort(self, column, order):

        rev = False
        if order == Qt.SortOrder.DescendingOrder:
            rev = True

        self.items.sort(key=lambda x: x.data(column), reverse=rev)
        self.layoutChanged.emit()
```

実装方法はかんたんで、AbstractItemModel を継承したクラスに sort 関数を追加します。
このとき、column と order を受け取ります。
column はどのカラムをソートのキーにするか
Order は昇順か降順か
を、TreeView 側から受け取ります。

受けとった情報を元にして、Model 内の構造を Sort します。

上のサンプルの場合、

````python
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

この Item を items を List で持っているので
ソートのキーになるカラムでソートするように sorted 関数の key を指定しています。

python の場合、

```python
a = [1,3,2,5,4]
a.sort()
````

とすると、List の並び順をソートできます。

```python
d = [{'name': 'A', 'value': 10},
        {'name': 'B', 'value': 30},
        {'name': 'C', 'value': 20}]
d.sort(key=lambda x: x['value'])
```

また、上のようなシンプルなリストではなく、Dict のリストやオブジェクトのリスト  
のような List の場合は、こんな感じで key を与えることでそのキーでソートすることができます。

これを利用して、sort 関数が実行されたタイミングで、Model に表示したい Item を
ソートして、表示をアップデートしてあればカスタムモデルでもソートをつけることができます。

![](https://i.gyazo.com/d48613337b2be9dcd559ced84a8fb572.gif)

結果。
