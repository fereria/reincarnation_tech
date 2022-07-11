---
title: 基本Widgetを使ってみる(2):RadioButton
tags:
    - PySide
---

# 基本 Widget を使ってみる(2):RadioButton

複数の選択肢からなにかを選ぶときに使用するのが RadioButton。  
その基本的な使い方を解説。

![](https://gyazo.com/6cf831e4fe126a407870f8b82bde509e.png)

完成した UI はこんな感じ。  
選択した CheckBox の文字を、「SelectCheck」ボタンを押すとプリントしてくれます。

使用している ui ファイルは
https://snippets.cacher.io/snippet/82070300e6a8c34b8f12
こちら。

<script src="https://embed.cacher.io/d6026a815967a314a1f845970c294ea62e59fc17.js?a=abcd6b52889638d633a3f71e5bb228a9"></script>

## 基本的な使い方

まず、使用する Button を「ButtonGroup」でまとめてから使用します。

```python
        self.grpA = QtWidgets.QButtonGroup()
        self.grpA.addButton(self.ui.radioButton_4, 1)
        self.grpA.addButton(self.ui.radioButton_5, 2)
        self.grpA.addButton(self.ui.radioButton_6, 3)
        self.grpA.button(1).setChecked(True)
```

この ButtonGroup は AbstractButton クラスを継承して作成されている Button を  
グルーピングすることができます。  
使い方は、上のコードのように、addButton に対して Button のオブジェクトをセットするだけ。  
その時に、アクセス用の ID を指定しておきます。

以降は、ButtonGroup.button( **id** )で、  
Group に含まれる Button のオブジェクトの取得を行うことができる。

そして、取得方法は

```python
self.grpA.checkedButton()
```

ButtonGroup の checkedButton で選択中の Button のオブジェクトを  
取得することができます。

## それ以外の使い方

ButtonGroup の Signal の中には、クリックしたときに  
クリックしたボタンを取得する関数があります。

```python
self.grpA.buttonClicked.connect(self.checkButtonA)
```

使い方は、このようなシグナルを作成し、

```python
    def checkButtonA(self,btn):
        print(btn.text())
```

スロットの関数には Button のオブジェクトを受け取るための引数を  
用意しておきます。  
こうしておくと、Button をクリックしたときに  
今選択した Button オブジェクトを受け取って、何かしらの処理をはさむことができます。

同様な処理で buttonPressed buttonReleased などがありますが  
使い方は同じなので、用途に応じて差し替えます。

参考の Help は
ButtonGroup  
https://doc.qt.io/qtforpython/PySide2/QtWidgets/QButtonGroup.html#PySide2.QtWidgets.PySide2.QtWidgets.QButtonGroup.checkedButton
RadioButton  
https://doc.qt.io/qtforpython/PySide2/QtWidgets/QRadioButton.html  
ただし、RadioButton はほぼ AbstractButton を継承したものなので  
https://doc.qt.io/qtforpython/PySide2/QtWidgets/QAbstractButton.html#PySide2.QtWidgets.QAbstractButton  
Button に関数は、AbstractButton 側のヘルプを参照すると良いです。
