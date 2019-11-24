---
title: PySide の GraphicsView で Item を親子化したときの問題
---
# PySide の GraphicsView で Item を親子化したときの問題


## 問題

PySide の GraphicsView の Item を setParentItem で親子化した場合

![](https://gyazo.com/842e92c71e5192118cc673404cca06ec.gif)

子オブジェクトの上をホバーすると、子オブジェクトだけではなく親オブジェクトも「ホバーした」扱いになり  
色が変わってしまう。

これは、Item を親子化した場合  
イベント処理が親側から発生するためであり、親 → 子の処理のいずれかで「ホバーした！」という Event が検知されると  
すべての親子に対して Event が適応されてしまうからの模様。

```python
    def hoverEnterEvent(self, e):

        self.color = QtGui.QColor('yellow')
        self.update()
```

PySide では、このように各イベントに対しての動作をオーバーライドして作成する分けですが  
この中でなにもしていない場合は  
ホバーするたびに、この hoverEnterEvent が呼ばれるため  
意図しないタイミングでイベントが発生してしまう。

## 対策

なので、なんとかするためにこのホバーしたタイミングで呼ばれるイベント関数内に  
実行するかどうかの判定を追加する。  
以下テストコード

```python
#!python2
# -*- coding: utf-8 -*-

import sys
from PySide import QtCore, QtGui

class testWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):

        super(testWindow, self).__init__(parent)

        self.scene = Scene(QtCore.QRect(0, 0, 640, 480))
        self.scene.addRect(0, 0, 640, 480, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.white))
        self.view  = QtGui.QGraphicsView(self.scene)
        self.view.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))

        # itemを配置
        item = TestItem(QtCore.QRect(0, 0, 100, 100))
        self.scene.addItem(item)
        child = TestItem(QtCore.QRect(150, 0, 100, 100))
        self.scene.addItem(child)
        child.setParentItem(item)

        self.setCentralWidget(self.view)
        self.setGeometry(100, 100, 700, 500)


class Scene(QtGui.QGraphicsScene):

    mouse_pos = None
    sel_item  = None

    def __init__(self, *args, **kwargs):

        super(Scene, self).__init__(*args, **kwargs)


class TestItem(QtGui.QGraphicsItem):

    rect = None
    color = QtGui.QColor('pink')

    def __init__(self, rect, parent=None):
        super(TestItem, self).__init__(parent)

        self.__rect = rect
        self.setAcceptHoverEvents(True)

    def boundingRect(self):

        return self.__rect

    def paint(self, painter, option, widget):

        painter.setBrush(self.color)
        painter.drawRoundedRect(self.__rect, 5, 5)

    def hoverMoveEvent(self, e):
        # hoverEnterEventからhoverMoveEventに修正。
        if self.isUnderMouse():
            self.color = QtGui.QColor('yellow')
        else:
            self.color = QtGui.QColor('pink')

        self.update()

    def hoverLeaveEvent(self, e):

        self.color = QtGui.QColor('pink')
        self.update()

    def changeRect(self, rect):

        self.__rect = rect
        self.update()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    a = testWindow()
    a.show()
    sys.exit(app.exec_())
```

テストコードでは、とりあえず（移動出来ない）GraphicsItem をシーンに配置して  
setParentItem で親子化。  
この状態でマウスのホバーのところに「カーソルがオブジェクトの上に乗っているか」を判定する  
if 文を追加。

![](https://gyazo.com/a6a890480ed4ccfa42252af5b73ce33d.gif)

結果。

Item クラスには isUnderMouse 関数という、Item 範囲内にマウスがある場合 True を返す  
関数があるので、これを使用している。

これ以外にも、Shape オブジェクトには「contains」という関数があり  
引数に Point を渡すことで Shape 内かどうかを判定して True/False を返す機能もあるので  
Painter で図形を描画したときに、マウスが上に載っているかを判定して  
何かしらの処理をするとかもできるはず。(たぶん)

## 追記 (2019/2/3)

自分が当初テストしていた時は、inUnderMouse で判定をしていたのは  
「hoverEnterEvent」だったのだけれども  
Enter で判定を行うと判定が外れてしまうことがあるという指摘がありました。  
ので、

```python
    def hoverMoveEvent(self, e):

        if self.isUnderMouse():
            self.color = QtGui.QColor('yellow')
        else:
            self.color = QtGui.QColor('pink')

        self.update()
```

マウス移動時に呼ばれる hoverMoveEvent 内でマウス移動時毎度評価するようにした方が  
良いとのこと。  
hoverMoveEvent にしたら、反応しなくなるなどの謎挙動はなくなりました。

## まとめ

Event 系の関数をオーバーライドする場合は  
関数ないで細かい条件を判定して処理をしてあげる。

## 参考

- https://translate.google.com/translate?depth=1&hl=ja&rurl=translate.google.co.jp&sl=en&sp=nmt4&tl=ja&u=https://stackoverflow.com/questions/44757789/hover-on-a-child-qgraphicsitem-makes-parent-item-hovered-as-well&xid=17259,15700002,15700023,15700186,15700190,15700248
