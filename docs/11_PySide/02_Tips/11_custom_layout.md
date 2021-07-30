---
title: CustomLayoutを作ろう
tags:
    - PySide
    - Python
description: QLayoutを使用してFlowLayoutをつくる
---


最近あまりPySideを触っていなかったせいで、だいぶ忘れかけてしまったので  
勉強を兼ねて C++のサンプルを参考にPySideのカスタムレイアウトを作ってみます。
https://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html
参考にしたサンプルはこちら。

## PySideのレイアウト

まず、PySideにはデフォルトで 

![](https://gyazo.com/95c18dd4ce451f22e871e8b3a74cc37f.png)

* Vertical Layout（縦に並べる）
* Horizontal Layout（横に並べる）
* Grid Layout（格子状に並べる）
* Form Layout（Formみたいに並べる）

の４つが用意されています。  
大体のことはこの４つでできますが、それ以外に幅によって改行するようなレイアウトを作りたい場合  
などは、自分で作らないといけません。

![](https://gyazo.com/d3f4ec642c83ceb8a6a2b1bf52269668.gif)

https://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html

このようなレイアウトを、「Flow Layout」呼ぶようで  
公式に、C++のコードサンプルが用意されています。

ので、今回はこのサンプルをベースに、PySide2でかきなおしつつ  
細かい実装方法をみていこうとおもいます。

## QLayout / QLayoutItem

まず、PySideのレイアウトは、QLayoutを継承して作成します。

![](layout.drawio#0)

クラスの継承はこのようになっています。

まず、QLayoutItemが、QLayoutが操作する抽象的なアイテムを提供します。
QLayoutを継承して作るカスタムレイアウトは、このQLayoutItemで指定された関数を  
再実装することで、作ることができます。

```python
class SampleGridLayout(QLayout):
    def __init__(self, margin: int, hSpacing: int, vSpacing: int, parent=None):
        super().__init__(parent=parent)
        self.setContentsMargins(margin, margin, margin, margin)

        self.itemList = []
        self.hSpacing = hSpacing
        self.vSpacing = vSpacing
```

まずは基本構造。

カスタムレイアウトを作る場合は、QLayoutを継承したクラスを作成します。  
まず、レイアウトは、Widgetに対して配置します。  
そしてそのWidgetとLayoutのスペース（緑の部分）が contentsMargins という形で指定されます。  
それとは別に、FlowLayoutでは  
WidgetとWidgetとの間のスペースを調整できるようにしたいので、そのパラメーターを
hSpacing vSpacing という形で指定できるようにします。

今回作りたいFlowLayoutはどういう挙動かというと、  
基本は横方向にWidgetを配置し、配置するWidgetがウィンドウの範囲を超えた場合
越えたところでWidgetを改行させます。
なので、まず必要なのはレイアウトの範囲の取得と、ウィジェットの大きさの取得
そしてそれをどこのタイミングでアップデートするのか？
というのが今回の実装のポイントになります。

### 必要な関数の実装

まず、配置部分の前に、最低限必要な関数の解説から。
QLayoutでレイアウトを実装する場合  
かならず定義がひつようとなる関数があります。
それが

* addItem
* sizeHint
* setGeometry
* itemAt
* takeAt
* hasHeightForWidth
* heightForWidth
* count

です。

#### レイアウトの追加/取得

```python
    def addItem(self, item: QLayoutItem):

        self.itemList.append(item)

    def count(self):

        return len(self.itemList)

    def itemAt(self, index: int):

        if self.count() > 0 and index < self.count():
            return self.itemList[index - 1]
        return None

    def takeAt(self, index):

        if index >= 0 and index < self.count():
            return self.itemList.pop(index - 1)
        return None

```

#### Widgetの追加・取得関係

addItemは、QLayoutで addWidget したときに呼ばれる関数で  
その名の通りレイアウトに配置するアイテムを変数に入れる部分です。  
今回のレイアウトは二次元配列ではなく、レイアウトの幅に応じて改行するので
単純なリストであればOKです。

このときに受け取るのは、Widgetではなく QLayoutItemになります。

countはその名の通りレイアウトに配置しているWidget数を返します。  

itemAtは、指定のIndexのアイテムを返し  
takeAtは、指定のIndexのアイテムを取り出して返します。

```python
    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width: int):
        height = self.doLayout(QRect(0, 0, width, 0))
        return height
```

次にhasHeightForWidth と heightForWidth。
これは、レイアウトのサイズが横サイズに応じて縦のサイズが決定する場合  
hasHeightForWidth をTrueにします。
今回の場合は動的に決めたいのでTrueをかえしていますが  
そうではない場合、hasHeightForWidth で判定を入れることで heightForWidthが呼ばれないので  
その分処理を軽くすることができます。

heightForWidthの処理は doLayout のときに詳しく書きます。

#### sizeHint

```python

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):

        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
```

次にレイアウトサイズ関連。
今回の場合の最小サイズは、レイアウトに配置しているWidgetの中で最も大きな値＋マージンを指定するようにします。

#### doLayout

```python
    def setGeomertry(self, rect):
        # 配置されるWidgetのジオメトリを計算するときに呼び出される
        super().setGeometry(rect)
        self.doLayout(rect)

    def doLayout(self, rect):

        # rect は、現在のLayoutの矩形
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            # 次のWidgetの配置場所
            nextX = x + item.sizeHint().width() + self.hSpacing
            if nextX - self.hSpacing > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + self.vSpacing
                nextX = x + item.sizeHint().width() + self.hSpacing
                lineHeight = 0

            item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()
```

そしてこれが今回のメインになるレイアウト部分です。

まず、レイアウトの再配置の計算が必要になるタイミングがなにかというと

* setGeometry で、レイアウトの大きさをコマンドで変更した場合
* ウィンドウサイズを変更した場合

の2パターンになります。
このうち、setGeometry を使った場合は、指定のQRect（矩形）を受け取ったときに
そのサイズにレイアウトサイズを変更後、その枠内に収まるように再配置をします。

ウィンドウサイズを変更した場合が heightForWidth で、  
ウィンドウを変更したときにこの関数が呼ばれ、その中の処理が実行されるようになります。

```python
height = self.doLayout(QRect(0, 0, width, 0))
```

そのときに呼ぶのがこの再配置のメイン処理を行う doLayout。  
このときは横のサイズは決定しているので横サイズ以外は0にしたQRectを  
引数として渡します。

### レイアウトのメイン処理

![](layout.drawio#2)

まず、レイアウトの中を書き表すとこのようになります。
配置したWidgetとWidgetの間のスペースは hSpacing vSpacing として指定されています。
レイアウトの位置は、

レイアウトの矩形（黄色部分）は、Geometryという名前で表されていて、
setGeometry getometry 関数でそれぞれ指定や取得をすることができます。
取得できるのは [QRect](https://doc.qt.io/qtforpython-5/PySide2/QtCore/QRect.html?highlight=qrect#PySide2.QtCore.PySide2.QtCore.QRect)です。
このQRectはレイアウト・Widgetそれぞれの現在の位置(x,y)と大きさ(width,height)を取得・設定することができます。

![](layout.drawio#3)

まず、引数で指定したRectから、開始位置の座標を決めます。

![](layout.drawio#4)

そして、配置しているWidget分繰り返します。
widgetのサイズは、 item.sizeHint().width() で取得することができるので、  
配置位置は 前回の配置位置 + Widgetサイズ（sizeHint().width()) + 最初にしていたスペースです。
そして、その位置がレイアウトの大きさ（geometry()）よりも大きい場合は  
次の行に改行したいので、

```python
            if nextX - self.hSpacing > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + self.vSpacing
                nextX = x + item.sizeHint().width() + self.hSpacing
```

xは初期位置（引数で指定された左側）に戻し、  
配置しているアイテムの height() つまり右下の位置にスペース分の値を追加した値を  
セットします。

そうして計算した位置に、item自体のサイズ(item.sizeHint()) の QRectを作り  
itemに対して setGeometryを使用して移動します。

最後は、最終的な高さを返します。
この値が、heightForWidth （指定した widthのときに自動てきにきまる高さ）  
となります。

https://snippets.cacher.io/snippet/1a7849e8231b23939f03
https://snippets.cacher.io/snippet/5c7938abe6b116fbb156 (テスト用UI)
全コードはこちら。

![](https://gyazo.com/d1154ad622b3a6e77dcf2d3289d80dff.png)

FlowLayoutを利用して、ScrollAreaに対して100個のボタンを配置しましました。  
よくある使い方として、タグクラウド的なUIを作りたい場合  
このFlowLayoutは重宝します。

## まとめ

最初はどうやって作るのかわかりにくかったですが、
heightForWidthとgometryを理解できれば、全体像がわかりやすくなります。

VBoxやHBoxなどでは微妙にやりにくいものなどは
カスタムを作ると色々便利になりそうです。

## 参考

* https://stackoverflow.com/questions/55820951/qt-flowlayout-example-how-to-get-sizehint-to-be-called-when-layout-changes
* https://code.qt.io/cgit/qt/qtbase.git/tree/examples/widgets/layouts/flowlayout/flowlayout.cpp?h=5.15
