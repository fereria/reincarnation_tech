---
title: PySideでFontAwesomeを使う
tags:
    - PySide
    - Python
description:
---

https://fontawesome.com/

Fontawesome とは、無料で使用できる Web アイコンフォントで
よく使いそうなアイコンを簡単に使用することができます。

PySide の GUI を作るときに、アイコンを用意するのはいろいろ手間がかかりますが
この Fontawesome を使えば、PySide でもお手軽にアイコンを使えます。

## インストールする

まずはインストール

```bat
pip install qtawesome
```

pip で qtawesome をインストールします。

```python
# -*- coding: utf-8 -*-
import sys
# from PySide2.QtCore import ()
# from PySide2.QtGui import ()
from PySide2.QtWidgets import (QApplication, QMainWindow, QDialog, QListWidget, QListWidgetItem)
import qtawesome as qta


class SampleUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        listWidget = QListWidget()
        self.setCentralWidget(listWidget)
        # Listにアイテムを追加する
        for i in ['a', 'b', 'c', 'd', 'e']:
            item = QListWidgetItem(i, listWidget)
            icon = qta.icon('fa.angle-left')
            item.setIcon(icon)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = SampleUI()
    ui.show()
    sys.exit(app.exec_())
```

![](https://gyazo.com/5a57d2861859a29036fb39b33edaa2f5.png)

実行結果。

qta.icon(～～～)を使用することで、QIcon で Fontawesome のアイコンを使用できます。

![](https://gyazo.com/124f44c19c44fd3fb76e9c1098bb2e67.png)

```
 qta-browser
```

使用可能なアイコンは qta-browser をコマンドプロンプトなどで実行すると一覧することができて
使うときの名前を調べることができます。

![](https://gyazo.com/5c92a7160a686111aca62ac422776e91.png)

たとえば、この github のアイコンを使用するなら、

```python
icon = qta.icon('ei.github')
```

こうすると

![](https://gyazo.com/98c67b77440a2fa368bbecc148093f63.png)

このようにできます。

これを活用すれば、PySide の GUI をお手軽に飾ることができるので
おすすめです。

## 参考

-   https://github.com/spyder-ide/qtawesome
