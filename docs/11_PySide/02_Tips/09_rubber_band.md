---
title: RubberBandを表示する
---

![](https://gyazo.com/5b6d90c6eddde858c34fcbc0523d9932.git)

PySideでマウスのドラッグ＆ドロップで範囲を表示したい場合は
**QRubberBand**を使用するとかんたんに作ることができます。

```python
# -*- coding: utf-8 -*-

import sys
from PySide2.QtWidgets import QDialog, QRubberBand, QApplication
from PySide2.QtCore import QRect


class RubberBandTest(QDialog):

    rubber_band = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(300, 300)

    def mousePressEvent(self, e):

        self.origin = e.pos()
        if not self.rubber_band:
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
            self.rubber_band.setGeometry(QRect(self.origin, e.pos()).normalized())
            self.rubber_band.show()

    def mouseMoveEvent(self, e):

        self.rubber_band.setGeometry(QRect(self.origin, e.pos()).normalized())

    def mouseReleaseEvent(self, e):

        self.rubber_band.hide()
        self.rubber_band = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = RubberBandTest()
    a.show()
    sys.exit(app.exec_())
```