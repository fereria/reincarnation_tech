---
title: ColumnViewを使おう
---

![](https://gyazo.com/5fe4c4834598f70bbef4327ee157332e.gif)

ColumnView は、上のような複数の ListView を並べて
クリックすることで次の ListView に選択肢を表示していくようなことができる View です。

あるのは知っていたものの使ったこともなければ資料もなかったので
使い方を調べてみました。

## 基本構造

基本的な Model の構造は TreeView と同じです。

```python
        self.view = QColumnView()
        self.model = ColumnModel(data)
        self.view.setModel(self.model)
        layout.addWidget(self.view)
```

こんな感じで ColumnView を作り、Model をセットすれば OK です。

TreeView の場合は Model で作られている木構造をすべて TreeView として表示しますが
ColumnView は木構造の親階層から選択していくことで子階層を表示するような挙動になります。

サンプルコードは長いので
https://snippets.cacher.io/snippet/22c5ee4b0ab81ecae002
Cacher にアップしましたが、ほぼ TreeView の Model と同じ構造で動きました。

## Model を作る

動いたのですが、どうやって設定するようにするか考えた結果

```python
        data = ["a/b/c",
                "a/b/d",
                "a/e/f",
                "b/d/c",
                "てすと/はろー/ワールド"]
```

こんな感じで、 / で各カラムの構造を指定するようにしてみました。

```python
    def setupModelData(self):
        """
        表示用のItemを再構築する
        """
        self.rootItem.clear()
        parents = {}
        self.beginResetModel()
        for item in self.__items:
            buff = item.split("/")
            for num, i in  enumerate(buff):
                key = "/".join(buff[:num])
                if key in parents:
                    parent = parents[key]
                else:
                    parent = self.rootItem
                if not parent.dataExists(i):
                    p = BaseItem(i, parent)
                    parent.appendChild(p)
                    parents["/".join(buff[:num + 1])] = p
```

TreeView と同じ用に parent と addChild を使用して
Item オブジェクトで木構造を作ります。

## 選択している項目を取得する

ColumnView で選択した項目を、全て結合したテキストを取得したいとします。
ただ

```python
    def showSelection(self):
        a = self.view.selectedIndexes()
        if len(a) > 0:
            data = a[0].data(Qt.UserRole)
            print(data.getFullPath())
```

view.selectedIndexes() を実行した場合は
最後のカラムの選択 Index が取得されるだけでした。

なので、Item に対してパスを取得する関数を追加で作成します。

selectedIndexes から data を使用して Item を取得します。

```python
    def getFullPath(self):

        current = self
        retVal = []
        while current.data(0) != "":
            retVal.insert(0,current.data(0))
            current = current.parent()
        return "/".join(retVal)
```

Item は ColumnView に表示されている木構造が作られているので
自分自身を起点にして親を検索することで
選択状態を取得できます。

![](https://gyazo.com/371b13620a8678cb47c7f9a05407173e.png)

結果、こんな感じで最後に選択しているカラムの List から
全カラムの選択情報を結合したものを取得できるようになりました。

また試してないですが、かくカラムの View を拡張したりもできるみたいなので
使い方次第では色々使えそうです。
