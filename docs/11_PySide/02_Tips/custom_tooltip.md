# PySideのTooltipを自作する

<!-- SUMMARY:PySideのTooltipを自作する -->

いわゆるオブジェクトにカーソルがあたるとHelpが表示される「Tooltip」ですが  
PySideデフォルトのTooltipは非常に使いにくいので、自前で作ってみます。  
  
![](https://gyazo.com/2760c9373c3a9b76b9e665bb62aa35f9.png)

実行結果はこんな感じになります。  
やりたい事は、

1. 指定のItem範囲にマウスカーソルが入ったら
2. painterで作った描画のTooltipを表示して
3. 範囲外にでたら消す

ようにします。  
大分コードが長いですが、せっかくなので全部貼り。  
  
とりあえず全コード貼ると長いので全部は  
https://snippets.cacher.io/snippet/c58f263509ee12c0155f  
ここにUPしました。  
  
今回は主にカスタムTooltip部分と、Item部分をまとめ。

## Tooltip用UIを作る

上のコードのうち、ポイントになるのが表示されるTooltip部分。
```python
class MyPopup(QtWidgets.QDialog):
    def __init__(self, text="", width=200, height=100, positionOffset=10, parent=None):
        super(MyPopup, self).__init__(parent)
 
        self._text = text
 
        self.color = [0, 0, 255]
        self.tooltipWidth = width
        self.tooltipHeight = height
        self.positionOffset = positionOffset
        # 枠を消して、透明にする
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
 
        self.positionUpdate()
 
    def setText(self, text):
        self._text = text
        self.update()
 
    def getText(self):
        return self._text
 
    def positionUpdate(self):
        pos = QtGui.QCursor().pos()
        self.setGeometry(pos.x() + self.positionOffset,
                         pos.y() + self.positionOffset,
                         self.tooltipWidth,
                         self.tooltipHeight)
 
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
 
        pen = QtGui.QPen(QtGui.QColor(*self.color), 8)
        bg_color = QtGui.QColor(*self.color)
        painter.setPen(pen)
        painter.setBrush(bg_color)
        rect = QtCore.QRect(0, 0, self.geometry().width(), self.geometry().height())
        painter.drawRoundedRect(rect, 20, 20)
        # 文字を描画
        painter.setFont(QtGui.QFont(u'メイリオ', 20, QtGui.QFont.Bold, False))
        painter.setPen(QtCore.Qt.white)
        painter.drawText(QtCore.QPoint(10, 30), self.getText())
```
このポイントは setWindowFlagsで設定している **QtCore.Qt.FramelessWindowHint** と、  
ウィンドウを透明にする **QtCore.Qt.WA_TranslucentBackground** の2つです。  
  
試しにこの2つをOFFにすると

![](https://gyazo.com/a27f187b3bf538311e01f806ffa2eaca.png)

こんな感じになってしまい、非常に残念な感じになってしまいます。  
  
もう1つのポイントはウィンドウを表示する位置について。  
ウィンドウ位置は setGeometry() で指定できるのですが、これをマウスカーソル位置とイコールにすると  
作成したUI側にフォーカスが移ってしまうらしく、色々と挙動がおかしくなります。  
ので、ある程度マウスから外した所にだしたほうが安全です。  
  
## Itemを作る

次に GraphicsItemを継承したカスタムのItemを作ります。

```python
class BaseNodeItem(QtWidgets.QGraphicsItem):
 
    def __init__(self, parent=None):
 
        super(BaseNodeItem, self).__init__(parent)
 
        self._width = 200
        self._height = 100
 
        self.color = [255, 0, 0]
        self.tooltip = None
        self.tooltipText = "hogehoge"
 
        self.setAcceptHoverEvents(True)
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
 
    def boundingRect(self):
 
        return QtCore.QRectF(0.0, 0.0, self._width, self._height)
 
    def paint(self, painter, option, widget):
 
        margin = 20
        rect = self.boundingRect()
        dis_rect = QtCore.QRectF(rect.left() - (margin / 2),
                                 rect.top() - (margin / 2),
                                 rect.width() + margin,
                                 rect.height() + margin)
 
        pen = QtGui.QPen(QtGui.QColor(*self.color), 8)
        bg_color = QtGui.QColor(*self.color)
        painter.setPen(pen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(dis_rect, 5, 5)
 
    def hoverEnterEvent(self, e):
 
        self.tooltip = MyPopup("hogehogefugafuga", parent=self.window())
        self.tooltip.show()
 
    def hoverMoveEvent(self, e):
 
        if self.tooltip is not None:
            self.tooltip.positionUpdate()
 
    def hoverLeaveEvent(self, e):
 
        self.tooltip.close()
        self.tooltip = None
```

こちらのポイントは hover###Event になっている3つ。  
その名の通り、マウスがItemの上に入った時・入ってる間・出たときに呼ばれる関数です。  
ので、  

1. 入った時にPopup用Windowを作り
2. 入ってる間Positionを更新し
3. 出たら閉じる

ようにします。  
ですが、これだけだとHoverイベントが発生してくれないので
```python
self.setAcceptHoverEvents(True)
```
HoverEventをOnにしてあげます。  
  
今回はテスト用なのでものすごいアレなPopupですが、  
paintEvent内でちゃんと描画さえ書いてあげれば表示までのラグなどもなく  
好きな感じでToolTipを出せるようになります。  
  
ついでに、枠消してカスタム描画なUIも同じような方法で作れるので  
いわゆる普通のWindowsのUIからも卒業できそう。  
  
## 参考

* https://kiwamiden.com/how-to-draw-text-with-qpainter
* https://kiwamiden.com/use-setwindowflags
* https://codeday.me/jp/qa/20190304/361492.html