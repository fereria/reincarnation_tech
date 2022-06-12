---
title: GraphicsViewでQColorをアニメーションさせる
tags:
    - GraphicsView
    - PySide
    - Python
---

# GraphicsView で QColor をアニメーションさせる

タイトルの通り。  
GraphicsView のアイテムの色などをアニメーションさせるやり方を  
調べてみました。

## コード

```python
#!python3
# -*- coding: utf-8 -*-

import sys
from PySide2 import QtCore, QtWidgets, QtGui


class testWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(testWindow, self).__init__(parent)

        self.scene = Scene(QtCore.QRect(0, 0, 640, 480))
        self.scene.addRect(0, 0, 640, 480, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.white))
        self.view  = QtWidgets.QGraphicsView(self.scene)
        self.view.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))

        # itemを配置
        self.item = TestItem(QtCore.QRect(270, 190, 100, 100))
        self.scene.addItem(self.item)

        self.setCentralWidget(self.view)
        self.setGeometry(100, 100, 700, 500)


class Scene(QtWidgets.QGraphicsScene):

    mouse_pos = None
    sel_item  = None

    def __init__(self, *args, **kwargs):

        super(Scene, self).__init__(*args, **kwargs)


class TestItem(QtWidgets.QGraphicsObject):

    rect = None

    def __init__(self, rect, parent=None):
        super(TestItem, self).__init__(parent)
        self.__rect = rect

        self.setProperty('color', QtGui.QColor('red'))

        self.animStopped = False

        self.ani = QtCore.QPropertyAnimation(self, b'color')
        self.ani.setDuration(1000)
        self.ani.setStartValue(QtGui.QColor('white'))
        self.ani.setEndValue(QtGui.QColor('blue'))
        # ずっとループする
        self.ani.finished.connect(self.animLoop)
        # 点滅タイプを変更
        self.ani.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        # アニメーションを永遠にループするようにする
        # それだと止められないからBoolのフラグで制御
        self.ani.valueChanged.connect(lambda: self.update(self.boundingRect()))
        self.ani.start()

        self.setAcceptHoverEvents(True)

    def animStop(self):

        if self.animStopped:
            self.animStopped = False
            self.ani.start()
        else:
            self.animStopped = True
            self.ani.stop()

    def animLoop(self):

        if self.animStopped is False:
            self.ani.start()

    def boundingRect(self):

        return self.__rect

    def paint(self, painter, option, widget):

        painter.setBrush(self.property('color'))
        painter.drawRoundedRect(self.__rect, 5, 5)

    def mouseDoubleClickEvent(self, event):
        self.animStop()
        return super().mouseDoubleClickEvent(event)

    def changeRect(self, rect):

        self.__rect = rect
        self.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = testWindow()
    a.show()

    sys.exit(app.exec_())
```

![](https://gyazo.com/c8bb0a55b87ccdea7a22a10c2056f48b.gif)

実行すると、こんな感じで白 → 青にアニメーションするようになります。

## いくつかはまりポイント

一応できたのですが、いくつかはまりポイントがあったので軽く解説。

### Property を作る

アニメーションを使用するには、「プロパティ」を作成する必要があります。  
ネットで調べた限りだと、出てくるプロパティは「Property 関数」を使用して  
作っている例しかありませんでした。  
が、PySide の場合なのかはわかりませんが

```python
self.setProperty('color', QtGui.QColor('red'))
```

こんな感じで setProperty(プロパティ名、初期値)  
のように指定する必要がありました。

そしてこのプロパティを使用する場合は

```python
self.property(プロパティ名)
```

のようにする必要があります。

### PropertyAnimation の引数

アニメーションを行う　 PropertyAnimation 　ですが、  
引数は　プロパティのあるオブジェクト、プロパティ名　のように指定します。  
が、

```python
self.ani = QtCore.QPropertyAnimation(self, 'color')
```

![](https://gyazo.com/644bde1386e5bafe9051158f400f13b6.png)
これだとエラーになってしまいます。

対応方法は、エラーの Supported signatures を見て分かるとおり  
第二引数は「ByteArray」である必要があるので

```python
self.ani = QtCore.QPropertyAnimation(self, b'color')
```

こうすれば OK です。

### GraphicsObject を使う

プロパティを使用するためには、QObject を継承している必要があります。  
が、QGraphicsItem のほうは QObject を継承していません。  
なので、QGraphicsItem ではなく  
QObject を継承している「 **QGraphicsObject** 」を使用する必要があります。

### ずっとループする

PropertyAnimation には「何回ループするか」の設定はあるのですが  
ずっとループしてほしいという設定はありません。  
ので、ずっとループしたい場合は

```python
self.ani.finished.connect(self.ani.start)
```

このようにすればとりあえずできます。

が、これだと絶対に終了しなくなるので  
今回は Bool でフラグを作って、ダブルクリックで停止と再開をできるようにしています。

### アニメーションカーブの指定

アニメーションカーブは

```python
self.ani.setEasingCurve(QtCore.QEasingCurve.OutCubic)
```

これで指定できます。

今回は

![](https://gyazo.com/e7cade6c28d215792ea8b5d16fdec7d5.png)

こんなカーブになりました。

他にも種類は色々あるので、詳しくは [こちら](http://pyside.github.io/docs/pyside/PySide/QtCore/QEasingCurve.html?highlight=qeasingcurve) を参照してください。

色々と罠はありましたが、分かってしまえば簡単なので  
色々幅が広がりそう。

## 参考

-   https://dftalk.jp/?p=19675
-   https://stackoverflow.com/questions/8191255/how-do-i-create-and-animate-a-custom-widget-property-in-pyqt4
-   https://github.com/janbodnar/pyqt-qpropertyanimation/blob/master/color_anim.py
