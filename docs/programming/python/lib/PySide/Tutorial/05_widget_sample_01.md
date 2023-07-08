---
slug: /python/pyside/tutorial/05
title: 基本Widgetを使ってみる(1):LineEdit
tags:
    - PySide
sidebar_position: 5
---

# 基本 Widget を使ってみる(1):LineEdit

widget を説明したところで、PySide でよく使う Widget の参考を色々書きながら  
頻出な関数などを紹介していこうと思います。

まずは LineEdit。

![](https://gyazo.com/f954cfa0ad20bf416f6a72155b58708b.png)

いわゆる 1 行の入力欄になります。

```python
#!python3
# -*- coding: utf-8 -*-
import sys
import os.path
from PySide2 import QtCore, QtGui, QtWidgets

class UISample(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(UISample, self).__init__(parent)
        # カスタムUIを作成
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.lineEdit = QtWidgets.QLineEdit()
        self.btn = QtWidgets.QPushButton("Push")
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.btn)

        self.btn.clicked.connect(self.pushBtn)

    def pushBtn(self):
        """
        LineEditに書かれた内容を取得する
        """
        print(self.lineEdit.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = UISample()
    a.show()
    sys.exit(app.exec_())
```

このコマンドを実行すると、LineEdit に入力されている文字列をプリントすることができます。

## Widget の機能を使う方法

### 取得・セット

「値を取得する」だったり「セットする」だったり  
追加した Widget に対して何かしたい場合は、その Widget のオブジェクト（インスタンス？）  
にアクセスすれば OK です。

```
self.lineEdit.text()
```

上のサンプルの場合、この部分です。  
使いたい Widget を知りたければ、とりあえず公式 Help を開きます。  
https://doc.qt.io/qtforpython/PySide2/QtWidgets/QLineEdit.html  
LineEdit のヘルプはこちら。  
クラスの構造的には QWidet を継承しているだけなので、比較的シンプルな構造です。  
**現在入力されているものを取得** したい場合は text() を使用すれば OK なのが Help を見れば分かります。

次に、デフォルトですでに文字が入っているようにしたい場合はどうすればいいか。

```python
self.lineEdit.setText("Hello World")
```

その場合は、setText を使用します。

![](https://gyazo.com/00f817aa792826f89306399f24c94fd0.png)

実行すると、こんな感じでデフォルトで文字が入った状態になります。

### Enter 押したらなにかする

LineEdit の場合は、Enter を押したらなにかを実行したいケースがでてきます。  
その場合は

```python
        # __init__内に↓を記述
        self.lineEdit.returnPressed.connect(self.pressReturn)

    def pressReturn(self):
        print(self.lineEdit.text())
```

returnPressed のシグナルを追加します。  
シグナルについては [Signal-Slot について](signal_slot)を参照。  
これ以外に LineEdit では textChanged 等を良く使います。

### Widget の Slot を使う

ボタンを押したらなにかをする のように Widget 側をトリガーにする他に  
Widget 側の Slot を使用することができます

![](https://gyazo.com/eb3b6ec69fbee8ec25f8e5bb14dfd4be.gif)

```python
self.btn.clicked.connect(self.lineEdit.selectAll)
```

LineEdit の場合は、 setText や cut copy paste selectAll 等が Slot として用意されています。  
ので、ボタンの connect 先に LineEdit の Slot を指定すれば  
ボタンを押せば～～～する　のような事を行うことが出来ます。

### 何かをセットする

widget に対してなにかをセットする場合は、 set####という名前になっている  
関数を使用します。

```python
self.lineEdit.setMaxLength(10)
```

例としてこんな感じ。

![](https://gyazo.com/f779dd020bfae1f42cc4e1875b6dc039.png)

QtDesigner のプロパティエディタにある Widget の設定項目を、Python 側で編集したい場合は  
この set ～～～～でほぼ設定することができます。

![](https://gyazo.com/ecee7f511346b35bcbaf1e3d19d17f67.png)

設定する値は、Help に書いてある所の arg\_\_1 が引数の数で  
Parameters が その引数をどの型で指定するか...という意味になります。  
この場合、int なので、LineEdit の行数は 10 とか 20 のような int 型で指定  
すれば OK という意味になります。

次はたぶん RadioButton/CheckBox あたり。
