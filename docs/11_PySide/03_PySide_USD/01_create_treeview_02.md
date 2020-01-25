---
title: PySideでUSD関係のGUIを作ろう - SceneGraph(2)
---

前回に続いUSD関係のGUIを作っていきます。

前回ベースが出来たので、今回できあがったツリーに対してUSDをDrag&Dropしたら
リファレンスを追加する構造にしてみます。

コードは全部だと長いので、全部は
https://snippets.cacher.io/snippet/b05e2bce8e0398a94682
こちら参照。

## Drag & Dropの構造を作る

まずは、TreeViewに対してDragDropでファイルを追加する仕組みをつくります。

```python
    def dragMoveEvent(self, event):
 
        if event.mimeData().hasUrls():
            # USDファイルか確認
            urls = [x.toLocalFile() for x in event.mimeData().urls()
                    if os.path.splitext(x.toLocalFile())[1] in ['.usda', '.usd', '.usdc']]
            index = self.indexAt(event.pos())
            if index.isValid() and len(urls) > 0:
                QApplication.setActiveWindow(self)
                self.setDropIndicatorShown(True)
                event.accept()
            else:
                event.ignore()
        else:
            super().dragMoveEvent(event)
 
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            index = self.indexAt(event.pos())
            for url in urls:
                file = url.toLocalFile()
                self.model().addUsdReference(file, index)
                self.expandAll()
            event.accept()
        else:
            super().dropEvent(event)
        self.setDropIndicatorShown(False)
```

dragMoveEventとdropEventをオーバーライドして、USDファイルがDragされたときのみ
Dropを許可するようにします。

ホバーしている下のItemは、 indexAt(Position) で Indexを取得して、
取得してから、

```python
    def addUsdReference(self, usdPath, index):
 
        item = index.data(Qt.UserRole)
        prim = item.getPrim()
        path = prim.GetPath()
 
        # DDしたUSDからDefaultPrimを取得
        ref_stage = Usd.Stage.Open(usdPath)
        defPrim = ref_stage.GetDefaultPrim()
        def_prim = self.stage.DefinePrim(path.AppendChild(defPrim.GetName()))
        def_prim.GetReferences().AddReference(usdPath)
 
        self.createModelTree()
```
そのindexを使用してModelに作成した addUsdReference関数から
現在のPrimに対してReferenceを追加するようにします。
今はTreeViewのItemにPrimのオブジェクトを持たせているので、
ItemからDataを取得して、
そのPrimに対してReferenceを追加します。
追加するときには、選択中のPrimにReferenceで読み込むLayerのDefaultPrim名のPrimを
作成して、その作成したPrimに対してReferenceを追加するようにします。

![](https://i.gyazo.com/67e31697c3f49d57d981dcdfc818643d.gif)

DDのたびにTreeViewをアップデーすすることで、
Reference構造もTreeViewに反映させることができます。

## ReferencのItemの色を変更・ReferenceしたUsd取得

このままだと、どこがReferenceだったかわかりにくいので
リファレンスで読み込んだPrimをわかるようにします。

```python
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
 
    def getFontColor(self):
 
        if self._prim.HasAuthoredReferences():
            return QColor(255, 121, 0)
        else:
            return QColor(0, 0, 0)
 
    def row(self):
        if len(self._parentItem.getChildren()) == 0:
            return 0
        return self._parentItem.getChildren().index(self)
 
    def data(self, column):
 
        if column == 0:
            return self._prim.GetName()
        if column == 1:
            return self._prim.GetTypeName()
        if column == 2:
            return str(self._prim.GetPath())
        if column == 3:
            if self._prim.HasAuthoredReferences():
                for f in self._prim.GetPrimStack():
                    ref = f.referenceList.prependedItems
                    if len(ref) != 0:
                        return ref[0].assetPath
                return ""
            else:
                return ""
```
表示する文や色を判定するのはItemクラスで実装します。
まず、Referencにによって作成されたかどうは HasAuthoredReferences で取得できます。
なので、これがTrueだった場合は文字の色を変更するようにします。

もう１つ、そのPrimでReferenceされているレイヤーを取得して、TreeViewで表示したい。
ので、data(column) 下で、判定するのを作りました。

これが地味に苦戦して、APIリファレンスがPythonとC++とではだいぶ変更があって、
関数などがだいぶ違いました。

まず、リファレンスで作成されているPriののPrimStackを取得します。
このPrimStackは、このPrimを定義するのに使用する「主張（Opinion）」を取得することができます。

このPrimStackは、その主張の元になっているレイヤーと、
SdfPathをSdfReferenceオブジェクトで取得することが出来ます。
SdfReferenceまわりはC+のドキュメントとだいぶ違っていて、Pythonの場合は
prependItemsからassetPathで、元Pathを取得できます。
（しかし、取得はできたけど本当にあってるのか・・・これ・・・）

```python
class TableDelegate(QItemDelegate):
 
    def __init__(self, parent=None):
        super().__init__(parent)
 
    def paint(self, painter, option, index):
 
        data = index.data(Qt.UserRole)
 
        bgColor = BACKGROUND_BASE
        if option.state & QStyle.State_Selected:
            bgColor = BACKGROUND_SELECTED
        if option.state & QStyle.State_HasFocus:
            bgColor = BACKGROUND_FOCUS
 
        brush = QBrush(bgColor)
        painter.fillRect(option.rect, brush)
 
        painter.setPen(data.getFontColor())
        painter.drawText(option.rect, Qt.TextWordWrap, data.data(index.column()))
```
Primから必要な情報が取得できるようになったら
あとは各Itemごとの描画をDelegateで作成します。

![](https://gyazo.com/8a1b00b97ff8180713a6a50319190f49.gif)

結果はこんな感じ。
あとは、 self.stage.GetRootLayer().Export(～～～) とかすれば、
追加したリファレンスを保存することができます。

やはりコンポジション込みで中の構造の取得方法とか調べると
沼にはまってなかなか辛いです。
あと、C++ドキュメントとPythonとの差がけっこうあって調べるのが難しいですね。
最終的には、コマンドを実しながら print(dir(ref)) みたいに、関数を取得しつつ..の
繰り返しでなんとかしてましたが、もう少し良い方法はないものか...