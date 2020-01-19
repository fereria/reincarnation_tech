---
title: UILoaderで.uiをロードする
---

# UILoaderで.uiをロードする


PySide1と2を併用することが多い都合、今までやっていた .py へコンバートしてから  
使う方法はなにかと不便だったので、あらためて.uiファイルのまま使用する方法を調べました。

```python
# -*- coding: utf-8 -*-

import sys
import os
import os.path

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

class UISample(QtWidgets.QDialog):
    
    def __init__(self,parent=None):
        
        super(UISample,self).__init__((parent))
        self.ui = QUiLoader().load(os.path.join(CURRENT_PATH,'graphicsView.ui'),self)
        layout  = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.ui)
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = UISample()
    a.show()
    sys.exit(app.exec_())
```

.uiを使用する場合は、QUiLoaderを使用します。  
このUiLoaderを使用すると、uiファイルを「Widgets」として読み込んでくれます。  
このWidgetsを show() することでも使えなくもないのですが、  
それはそれで拡張するときには不便なので、上のようにQDialogあるいはQMainWindowを継承したクラスを作成し  
そのクラス内で一端メンバ変数に対してロードし、そのロードしたWidgetsをDialogに配置するようにします。

![](https://gyazo.com/8c1ec3d9783b8a41473341d30a023710.png)

PySideは、ざっくりと分けると　Window（Dialog/Mainwindow)とWidget(GUIの部品)とソレを配置するLayout  
に分けられます。  
Designerで作成したUIというのは、複数のWidgetを並べた1つのWidgets（カスタムWidgets） なので  
Loaderでよみこんだuiファイルは、

![](https://gyazo.com/483c35a420d4893e8beda4234da2506c.png)

QWidgetsオブジェクトになります。  
なので、QDialogに乗せたい場合は、Windowに対してLayoutを配置し  
そのLayoutに対して読み込んだ.uiファイルのWidgetを addWidgetを使用して配置します。  
  
こうしておけば、Designerで配置した各種Widgetsにアクセスするときは  
self.ui.hogehoge.clicked.connect(####) のようにすればOKになります。  
  
