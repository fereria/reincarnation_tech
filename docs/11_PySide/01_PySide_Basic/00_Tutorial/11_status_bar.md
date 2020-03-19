---
title: QMainwindowのStatusBarを使う
---

今回は基本Widget「StatusBarのの使い方について。

![](https://gyazo.com/637b2a04a8fd2b4b74f4836cb47737f0.png)

StatusBarとはQMainwindowに追加することができる（QDialogではない）Widgetで
Windowの下のほうにメッセージやWidgetを追加することが出来るWidgetです。
（WidgetというよりLayoutに近い）

## 使い方

まず全体サンプル。

```python
# -*- coding: utf-8 -*-

import sys

from PySide2.QtWidgets import (QApplication,
                               QMainWindow,
                               QStatusBar,
                               QProgressBar,
                               QSizePolicy,
                               QPushButton)
from PySide2.QtCore import (Qt)


class UISample(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.status = QStatusBar()
        self.setStatusBar(self.status)        
        
        self.progress = QProgressBar()
        # 幅を固定する
        self.progress.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.progress.setMinimumWidth(200)

        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(50)
        self.status.addPermanentWidget(self.progress)
        
        self.resize(600, 400)

        # self.button = QPushButton("PUSH")
        # self.status.addWidget(self.button)

        self.showMessage("Hogehoge Fugafuga")

    def showMessage(self, message):
        self.status.showMessage(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setFallbackSessionManagementEnabled(True)
    a = UISample()
    a.show()
    sys.exit(app.exec_())
```

## WindowにStatusBarを追加する

```python
        self.status = QStatusBar()
        self.setStatusBar(self.status)        
```
まず、追加するにはこの２行で完了です。
StatusBarは他のWidgetとは違いQMainwindowのsetStatusBarで追加します。

あとは、 self.status.showMessage("表示したいメッセージ") で、
StatusBarにメッセージを表示することができます。

## ProgressBarを追加する

![](https://gyazo.com/927d3c4a089cf7340e889dfcf5077460.png)

StatusBarには、任意のWidgetを追加することが出来ます。
これを利用して、StatusBarを表示させたり出来ます。

```python
        self.progress = QProgressBar()
        # 幅を固定する
        self.progress.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.progress.setMinimumWidth(200)

        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(50)
        self.status.addPermanentWidget(self.progress)
```

追加方法は、まずWidgetを追加して addPermanentWidget で追加します。
この方法で追加すると、右寄せでWidgetが追加されます。
幅調整や、ProgressBaの設定は
通常のProgressBarと同じく使えばOKです。
~~addPermanentWidgetの存在を調べるのにかなりはまった~~

![](https://gyazo.com/8a3f7add58279eb20b2445a974654298.png)

このように、他のWidgetでもOKです。

```python
self.status.addWidget(self.button)
```
addPermanentWidget ではなく addWidgetもありますが、この場合は左寄せになり
StatusBarのMessageに覆い被さるようにWidgetが追加されます。
なので、Messageではなく、QLabelをaddWidgetで追加して
メッセージ表示をカスタマイズさせることなども可能です。

