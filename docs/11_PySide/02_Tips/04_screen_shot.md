---
title: PySideで範囲スクリーンショットを作る
---

以前Blogで書いていた記事が色々古かったのでPySide2で書き直してみました。
とりあえず全コード。

```python
# -*- coding: utf-8 -*-
"""
範囲指定でScreenShotを撮影するスクリプト
"""
import sys
from PySide2.QtWidgets import (QWidget, QApplication)
from PySide2.QtGui import (QPixmap, QPainter, QPainterPath, QColor, QBrush)
from PySide2.QtCore import (Qt, QRect)


class ScreenShot(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        # 現在の画面をキャプチャー
        screen = QApplication.primaryScreen()
        self.originalPixmap = screen.grabWindow(QApplication.desktop().winId())

        self.endpos = None
        self.stpos = None

    def paintEvent(self, event):

        p = QPainter()
        p.begin(self)
        p.setPen(Qt.NoPen)

        rectSize = QApplication.desktop().screenGeometry()
        p.drawPixmap(rectSize, self.originalPixmap)

        if self.endpos and self.stpos:

            pp = QPainterPath()
            pp.addRect(rectSize)
            pp.addRoundRect(QRect(self.stpos, self.endpos), 0, 0)
            p.setBrush(QBrush(QColor(0, 0, 100, 100)))
            p.drawPath(pp)

        p.end()

    def mouseMoveEvent(self, event):

        self.endpos = event.pos()
        # マウスが動いたときに、再度描画処理を実行する
        self.repaint()

    def mousePressEvent(self, event):

        self.stpos = event.pos()

    def mouseReleaseEvent(self, event):

        self.endpos = event.pos()
        self.screenShot()

    def screenShot(self):

        # 切り取り処理をして保存後、ツールを終了する
        pmap = self.originalPixmap.copy(QRect(self.stpos, self.endpos))
        pmap.save("E:/test.jpg")
        self.close()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    wid = ScreenShot()
    wid.showFullScreen()
    sys.exit(app.exec_())
```

まず、スクリーンキャプチャを作るためには QWidgetsまたはQMainWindowを使用します。
PySideの各種イベントはGUIの上でないと発生しないというトラップがあるので
表示を  show()ではなく showFullScreen() にすることで全画面にします。

それだとただの全画面GUIになってしまうので
現在のWindowのスクリーンの画像を取得して、それをpaintEvent内で画面全体に対して描画します。

```python
        # 現在の画面をキャプチャー
        screen = QApplication.primaryScreen()
        self.originalPixmap = screen.grabWindow(QApplication.desktop().winId())
```

現在の画面をキャプチャし、QPixmapを取得します。

```python
        rectSize = QApplication.desktop().screenGeometry()
        p.drawPixmap(rectSize, self.originalPixmap)
```

そしてその画像をpaintEventで描画させます。

画面のキャプチャー方法は、以前とは多少変わっていて

```python
QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
```

QPixmapにある glabWindowを使っていましたが、今は非推奨で
上のサンプルのように、 QScreenからgrabWindowで取得するのが正解とのこと。

あとは、マウスをDrag&Dropしている間、切り抜く矩形範囲がわかりやすいように
addRect で矩形を描画しています。
矩形の開始位置はマウスをクリック瞬間にセットして、
それ以降はマウスが動くたびに右下の位置をアップデートさせるようにしています。

あとはマウスの範囲でQPixmapを切り抜いて jpg で保存すれば完了です。

全画面にして現在のWindowを描画するというのはわりと応用が利くので
paintEvent での Qpainter の使い方と併せて勉強すればいろんな事が出来そうです。
