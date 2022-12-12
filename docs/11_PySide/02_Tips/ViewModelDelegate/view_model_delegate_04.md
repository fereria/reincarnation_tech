---
title: PySideのTableViewでDelegateを使う(3) もっとpaintする
---

今回は、 [paint する](view_model_delegate_02.md) に続いて、
PySide の TableView で、Delegate 内の paint を駆使していい感じの GUI を作っていきます。

## 完成図

![](https://gyazo.com/0508950bbbcbce51b92ee726e1927a6c.png)

実行すると、こんな感じで表示されます。

![](https://gyazo.com/c6f154dbc0dabe6822f07ad61a95d5bb.gif)

表示の工夫としては、ウィンドウの大きさを変更すると、TableView のセルの数を変更して
サイズに収まる量だけ表示するようにします。
もう１つは、開いたタイミングだとすべてのセルを表示せず、スクロールバーが一番下に来た時に  
指定の行数以上のデータがある場合は追加でロードするようにします。

セルの中身は、デリゲートの paint で書きます。

{{markdown_link('pyside_Delegate')}}
全コードはこちら。

## Item/Model/View を作る

まずは Model 部分とセルに表示するデータの構造を作ります。

今回の TableView は横の数が可変なので、Item は List 型で持つようにします。
1 セルごとにデータは管理したいので、この部分は

```python
class DataItem(object):

    def __init__(self, name="", description="", img=None):

        self.name = name
        self.description = description
        self.img = img if img else DEFAULT_IMAGE
        self.status = "default"

    def backgroundColor(self):
        return QtGui.QColor(255, 255, 100)

    def data(self, column):
        return self.name

    def setData(self, column, value):
        self.name = value

    @classmethod
    def sizeHint(self):
        return QtCore.QSize(250, 200)
```

Item クラスを作成し、セル内に表示したい情報はこのクラスで管理するようにします。
今回はセルの大きさは共通なので、sizeHint は固定の値を返しますが
場合によってはここを変更する...といったこともできるようにしておきます。

### Model

次に Model 部分。
TableView ですが、データは List なので
これを適切な Row/Column でアクセスできるように index を実装します。

```python
    def index(self, row, column, parent):

        index = ((row * self.columnNum) + column)
        if index < len(self.items):
            item = self.items[index]
            return self.createIndex(row, column, item)
        return QtCore.QModelIndex()
```

(row \* columnCount) + column が Index になるのですが、TableView の場合
何もないセルであっても index は実行されるので 範囲が井の場合は 空の ModelIndex を返します。

```python
    def data(self, index, role=QtCore.Qt.DisplayRole):

        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.UserRole:
            return item
```

data は、DisplayRole は使用せず、UserRole で item を取得できるようにだけします。
（表示は全部 Delegate のため）

```python
    def rowCount(self, parent=QtCore.QModelIndex()):
        u"""行数を返す"""
        count = int(len(self.items) / self.columnNum) + 1
        if self.maxRowCount > count:
            return count
        else:
            return self.maxRowCount

    def addMaxRow(self, num=5):

        if (len(self.items) / self.columnNum) > self.maxRowCount:
            self.maxRowCount += num
            self.layoutChanged.emit()

    def changeColumnNum(self, num):

        self.columnNum = num
        self.layoutChanged.emit()
```

最後に、スクロールが一番したに来たら追加する仕組みをつくります。
構造はシンプルで、 rowCount で返す値に最大値を指定します。
そして、self.addMaxRow が呼ばれたときに追加分の Row をセットすると
上限が解放されるようになります。

あとは、横のサイズも変更できるように関数を追加します。

どちらの関数も layoutChanged.emit() すれば、表示を更新することができます。

### View

最後にビュー部分。

```python
    def __init__(self,parent):
        # (略)
        self.verticalScrollBar().valueChanged.connect(self.moveSlider)

    def resizeEvent(self, event):

        count = int(event.size().width() / DataItem.sizeHint().width())
        if self.columnCount != count:
            self.columnCount = count
            self.columnCountChange(count)

    def moveSlider(self, value):
        if value == self.verticalScrollBar().maximum():
            self.model().addMaxRow()

    def columnCountChange(self, num):
        self.model().changeColumnNum(num)
```

まず、ビューサイズが変更された場合は、 resizeEvent で取得できます。
変更前が oldSize() 変更後が size() で取得できるので、横サイズで割って
配置できる数を取得します。

毎回 Emit すると遅くなりそうなので、値が変更したときのみ changeColumnNum を実行します。

スライドバーは、valueChanged で変更を取得できます。
この valueChanged で取得される最大値は、Model の RowCount です。
途中で rowCount が変わった場合は、value はそのままで max が変化します。

## paint する

これで準備ができたので Delegate の paint でセル内を書いていきます。

```python
    def paint(self, painter, option, index):
        """
        Cellの中の描画を行う
        """
        data = index.data(QtCore.Qt.UserRole)

```

Delegate では、index のセルを描画を実装します。
データでそのセルの DataItem を取得して、以降は QPainter でひたすら書いていきます。

### セルの範囲

![](delegate.drawio#0)

描画するセルの範囲は、option.rect で取得します。
図にすると、上のような QRect で取得できるので、以降はこの矩形をベースにして
描画したい画像や文字を配置します。

```python
        margin = 10
        imgHeight = (option.rect.height() / 2) - margin

        if data.img:
            imgRect = copy.deepcopy(option.rect)
            img = QtGui.QImage(data.img)
            imgWidth = (imgHeight / img.size().height()) * img.size().width()
            imgRect.setWidth(imgWidth)
            imgRect.setHeight(imgHeight)

            pos = option.rect.center()
            imgRect.moveCenter(pos)
            imgRect.translate(0, ((imgHeight / 2) * -1) + margin)
            painter.drawImage(imgRect, img)
```

まず、セルの矩形を複製します。
（複製しないと元の option.rect が書き換わるため）

![](delegate.drawio#1)

画像はセルの縦幅の半分からマージンを引いた数を上限として、
縦横比がいい感じになるように調整。
そして、中央になるように移動します。

```python
        # # タイトル表示
        titleRect = copy.deepcopy(option.rect)

        titleRect.setY(imgRect.bottom() + margin)
        titleRect.setHeight(30)

        font = QtGui.QFont("メイリオ", 11)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(titleRect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop | QtCore.Qt.TextWordWrap, data.name)

        descriptionRect = copy.deepcopy(option.rect)
        descriptionRect.setY(titleRect.bottom() + margin)
        descriptionRect.setX(titleRect.left() + margin)
        descriptionRect.setWidth(descriptionRect.width() - (margin * 2))
        descriptionRect.setHeight(50)

        font = QtGui.QFont("メイリオ", 8)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(descriptionRect, QtCore.Qt.AlignLeft | QtCore.Qt.TextWrapAnywhere,
                         data.description)
```

次に文字の配置。
基本は同じようにベースとなる矩形を複製し、文字エリアの矩形の縦幅を setHeight で変更。
drawText で、中央揃え＋行が溢れたら改行できるようにしておきます。

あとは必用に応じて paint 内に記述を追加すれば OK です。

## まとめ

とりあえずこれでカスタムモデル・ビュー・デリゲートを使用した TableView ができました。
あとは DataItem に必用な情報を足して、paint 部分を拡張したりすれば
いろいろ作れそうです。
