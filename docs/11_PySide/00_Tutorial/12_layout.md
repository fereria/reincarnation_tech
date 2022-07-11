---
title: 基本的なレイアウトを使おう
tags:
    - PySide
    - Python
description: VBoxLayout/HBoxLayout/GridLayoutの使い方
---

PySideで、ウィンドウの上にウィジェットを縦や横、格子状に配置して
ウィンドウサイズの変更に応じてレイアウトしたい場合は
「QLayout」を使用します。

![](https://gyazo.com/b499a2dbc5d276a802343021d1660d90.png)

レイアウトは、Designerを使用するときにでも使用しますが
今回はDesignerを使用せずコードのみで書いた場合の使い方などを説明していきます。

## QVBoxLayout/QHBoxLayout

```python
class SampleUI(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.setLayout(layout)
```

例として、QDialogに対して、レイアウトを配置する場合。
Widgetは、基本 setLayoutを使用することで
レイアウトを指定することができます。

![](layout.drawio#1)

図に表すとこのようになっていて、
あるWidget(QDialog)上に、ウィジェットを配置するためのスペースが準備されます。

```python
        for i in range(5):
            btn = QPushButton(f"Sample {i}")
            layout.addWidget(btn)
```

![](https://gyazo.com/52503ecce656e91bf7b50b7eeaaa23e9.png)

配置した結果はこのようになります。

![](https://gyazo.com/078c0c7c98555b6eff502d1eae92d089.gif)

このレイアウトに対してWidgetを配置すると、  
QDialogのサイズに合わせて均等にレイアウトすることができます。

このように縦方向にレイアウトしたい場合は、「QVBoxLayout」を使用します。

同じように横方向に配置したい場合は「QHBoxLayout」を使用します。
使い方はVBoxLayoutと同様で、

```python
class SampleUI(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        self.setLayout(layout)
        
        for i in range(5):
            btn = QPushButton(f"Sample {i}")
            layout.addWidget(btn)
```

![](https://gyazo.com/ed91246e56bbb3e9ff72ee507145befc.png)

QVBoxLayoutを使用していたところを、QHBoxLayoutに変更すれば、
横方向に並べることができます。

### SpacerItem

QLayoutを使用すると、縦・横方向に並べられることがわかりましたが   
Dialogのサイズが変更されても、均等ではなく配置してるWidgetは固定したい場合があると思います。
その場合は、QSpacerItemを使用します。

```python
class SampleUI(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

          layout = QVBoxLayout(self)
          spacerItem = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        for i in range(5):
            btn = QPushButton(f"Sample {i}")
            layout.addWidget(btn)

        layout.addItem(spacerItem)
        self.setLayout(layout)
```

![](https://gyazo.com/5ca1c8d0fec912daf10f225b36fc6e4e.gif)

QSpacerItemを使用した場合の例はこのようになります。

SpacerItemとは、その名の通り、レイアウトに対してスペースを配置します。  

![](layout.drawio#0)

見えていないですが、視覚化するとこのようになります。

#### SizePolicy

QSpacerItemは、引数で SpacerItemのデフォルトの大きさとSizePolicyを渡します。  
これは、ウィンドウを変更したときの振る舞いを表していて、  
Minimumならば、最小の値で固定し Expandingならば、ウィンドウサイズに応じて幅が変動するようになります。  

[詳細はこちら](https://doc.qt.io/qtforpython/PySide6/QtWidgets/QSizePolicy.html#PySide6.QtWidgets.PySide6.QtWidgets.QSizePolicy)参照ですが、この中からいくつか使いそうなものを紹介します。
  
デフォルトはMinimumになっていて、これはSpacerItemを使わなかった場合と同じ挙動になります。

##### Expanding

```python
spacerItem = QSpacerItem(0, 200, QSizePolicy.Minimum, QSizePolicy.Expanding)
```

![](https://gyazo.com/5ca1c8d0fec912daf10f225b36fc6e4e.gif)

Expandingにすると、SpacerItemの範囲がウィンドウサイズに応じて拡張されます。
Spacer以外は元のサイズ（SizeHintの大きさで）固定になります。

##### Fixed

```python
spacerItem = QSpacerItem(0, 200, QSizePolicy.Minimum, QSizePolicy.Fixed)
```

![](https://gyazo.com/6103bbf10ea8293cbf6d2a87c09fd254.gif)

Fixedにすると、指定のSpacerItemで（SizeHintの大きさで）固定され  
レイアウトに配置してWidgetは均等に配置されます。

## QGridLayout

VBoxとHBoxを使用すると、縦・横に配置できましたが、  
そうではなくExcelのように格子状にウィジェットを配置したい場合もあります。

その場合は、QGridLayoutを使用します。

```python
class FormUI(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout()
        self.setLayout(layout)

        btn = QPushButton("SampleA")
        layout.addWidget(btn, 0, 0)
        btn = QPushButton("SampleB")
        layout.addWidget(btn, 0, 1)
        btn = QPushButton("SampleC")
        layout.addWidget(btn, 1, 0)
        btn = QPushButton("SampleD")
        layout.addWidget(btn, 1, 1)

        btn = QPushButton("SampleE")
        layout.addWidget(btn, 2, 0, 1, 2)

        btn = QPushButton("SampleF")
        layout.addWidget(btn, 3, 0, 2, 1)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        btn = QPushButton("SampleG")
        layout.addWidget(btn, 3, 1)
        btn = QPushButton("SampleH")
        layout.addWidget(btn, 4, 1)
```
GridLayoutを使用したサンプルです。


GridLayoutは、レイアウトに対して addWidget(配置したいWidget,Row,Column)で  
指定したグリッドにWidgetを配置することができます。

#### 基本的なグリッド配置

```python
        btn = QPushButton("SampleA")
        layout.addWidget(btn, 0, 0)
        btn = QPushButton("SampleB")
        layout.addWidget(btn, 0, 1)
        btn = QPushButton("SampleC")
        layout.addWidget(btn, 1, 0)
        btn = QPushButton("SampleD")
        layout.addWidget(btn, 1, 1)
```

![](https://gyazo.com/d5612891938017ac77d6b076e7c69a35.png)

![](layout.drawio#4)

まずは、シンプルに格子状に配置したい場合。
Row と Column のインデックスを指定することで、  
その位置に配置できます。

#### グリッドの結合


![](https://gyazo.com/bcf9265132d87819dcf76d2cde6627ca.png)

![](layout.drawio#5)

次は、そのグリッドを結合したい場合。
結合したい場合は、 addWidget(配置するWidget,Row,Column,RowSpan,ColumnSpan)
のように、縦・横それぞれいくつ結合するかを引数で指定します。

例えば、横方向に結合している「SampleE」のボタンの場合、

```python
        btn = QPushButton("SampleE")
        layout.addWidget(btn, 2, 0, 1, 2)
```

2,0,1,2 なので、 ColumnSpanが2になっています。  
なので、2つ分のグリッドを結合したレイアウトにボタンが配置されます。

```python
        btn = QPushButton("SampleF")
        layout.addWidget(btn, 3, 0, 2, 1)

        btn = QPushButton("SampleG")
        layout.addWidget(btn, 3, 1)
        btn = QPushButton("SampleH")
        layout.addWidget(btn, 4, 1)
```

縦の場合も同様で、この場合はRowSpanを2にします。  

##### SizePolicy（おまけ）

![](https://gyazo.com/203f8aac14324d0cea672324af9d5afd.png)

```python
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
```
デフォルトの場合、ボタンサイズは縦方向は固定されているのですが  
これをレイアウトにフィットさせたい場合は
先程説明したSizePolicyを、ボタンに対して指定します。


## まとめ

https://snippets.cacher.io/snippet/39af914aa31fd8e7e282

インポート含めてのサンプルコードはこちらです。

VBoxとHBoxはネストすることができるので  
これを組み合わせることで複雑なGUIを作ることも可能です。

それ以外にも、
https://fereria.github.io/reincarnation_tech/11_PySide/02_Tips/11_custom_layout/
PySideではカスタムレイアウトを作成することもできるので、
もっと複雑なレイアウトを作りたい場合などは、QLayoutを継承したおオレオレレイアウトを  
作ることもできます。