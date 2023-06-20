---
slug: signal_slot
title: SignalとSlotについて(1)
tags:
    - PySide
    - Python
---

# Signal と Slot について(1)

Button 等の Widget を作成した場合、  
「ボタンを押したら###する」だったり「リストを選択したら###する」  
だったりと、GUI に対してのアクションに対して何かしらの動作を指定する必要があります。  
それを PySide で作成する場合は「Signal-Slot」の機能を使用します。

Signal と Slot とは、その名の通り **「なにかアクションがあった」** 時に Signal を発して  
**「それに対応した動作を実行」** するための機能です。

![](https://gyazo.com/81cfadb19f08e3b4237bf525b50275a6.gif)

例として前回の「ボタンを押す」をみてみます。  
この場合「ボタンを押す」というのが Signal  
push!!をプリントするのが Slot になります。

```python
class UISample(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UISample, self).__init__(parent)

        self.ui = QUiLoader().load(os.path.join(CURRENT_PATH, 'sample_btn_ui.ui'))
        self.setCentralWidget(self.ui)
        # Signal作成
        self.ui.pushButton.clicked.connect(self.click_btn)

    def click_btn(self):
        # 押したときの動作
        print("push!!")
```

前回のサンプルを再度みてみます。  
ボタンを押したときに実行する（push!!をプリントする）関数がいわゆる Slot になります。  
この関数と Widget を紐づけているのが

```python
self.ui.pushButton.clicked.connect(self.click_btn)
```

この部分で、  
Widget のオブジェクト Signal.connect(Slot の関数)  
このように書きます。

## Signal

この Signal 部分は、Widget ごとに固有のものがあります。  
（自分で作成もできます）  
Widget にどのような Signal があるかは Help を確認するとわかります。

![](https://gyazo.com/d461329897a67cd0bd34fedc024f8b06.png)

まずは、QtDesigner の「オブジェクトインスペクタ」のクラスを確認してみます。  
これが配置した Widget のクラス名になります。

https://doc.qt.io/qtforpython/PySide2/QtWidgets/index.html

使用しているクラス名がわかったら、公式 Help の QtWidgets 下から  
クラス名を探します。

!!! info
QtWidgets の下にあるのが、QtDesigner で Window に対して配置する  
 パーツがまとめられているモジュールです。

https://doc.qt.io/qtforpython/PySide2/QtWidgets/QPushButton.html

その中から PushButton を開いてみます。  
この下を開いてみても、それっぽい関数はありません。

![](https://gyazo.com/d23f18972755a2d1acc95ee9a8d7f435.png)

こういう場合は、ページの上にあるこの図を確認してみます。  
この図は、いわゆるクラスの継承図で  
左に行くほど親クラスになります。  
Help を見て、調べている Widget のページにそれっぽいものがない場合は  
親クラス側にそれらしいものがないかをさがします。

今回の場合は、「QAbstractButton」がそれっぽいものなので  
クリックして

https://doc.qt.io/qtforpython/PySide2/QtWidgets/QAbstractButton.html#qabstractbutton

AbstractButton のページを確認します。

!!! info
Abstract というのは、抽象クラスと呼ばれるもので  
 このクラスを継承して使用するのを前提としたクラスです。  
 この「AbstractButton」の場合、「ボタン」に関係する  
 Widget を作成する場合はこの AbstractButton を継承しています。

![](https://gyazo.com/3f376e7af0db7bd8bdf036d20e12fc34.png)

このページ下を確認すると「Signals」というカテゴリがあります。  
ここが Signal 部分に入れる関数名です。  
Signal は、その後ろには .connect() を入れて使用します。

## 引数付きの Signal

![](https://gyazo.com/6296441ef24bca7fdeea06576808ae6b.png)

Signal を実行したときに、一緒に引数を送ることができる機能があります。

![](https://gyazo.com/5052ac9c7136206c09b4bcd36f7bf60e.png)

引数を送ることができる場合、Help には arg\_\_1 のような引数が記入してあります。  
例として、LineEdit を使用してみます。

```python
class UISample(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UISample, self).__init__(parent)

        self.ui = QUiLoader().load(os.path.join(CURRENT_PATH, 'sample_btn_ui.ui'))
        self.setCentralWidget(self.ui)
        # Signal作成
        self.ui.lineEdit.textChanged.connect(self.changeText)

    def changeText(self, text):
        # 押したときの動作
        print(text)
```

![](https://gyazo.com/8a4e8b99afaa63e6c4262c366265ba35.gif)

LineEdit には「テキストが変更された」ときに実行する textChanged があります。  
この Signal は、引数として現在の入力されているテキストを受け取ることが出来るので  
Slot の関数に受け取り用の引数を指定しておきます。

こうすることで、Signl が発生して Slot の関数が実行されたときに  
引数が送られて、Slot の関数内で使用することができます。

## まとめ

この Signal-Slot が、PySide で UI を作成するときの  
GUI を操作したときに動作を作成するための基本になります。

各 Widget の Help には対応する Signal-Slot が書かれているので  
その Help を参考に動作を作成していきます。
