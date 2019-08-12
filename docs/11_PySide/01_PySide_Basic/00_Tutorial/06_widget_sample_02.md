# 基本Widgetを使ってみる(2):RadioButton

<!-- SUMMARY:基本Widgetを使ってみる(2)_RadioButton -->

複数の選択肢からなにかを選ぶときに使用するのがRadioButton。  
その基本的な使い方を解説。  
  

![](https://gyazo.com/6cf831e4fe126a407870f8b82bde509e.png)

完成したUIはこんな感じ。  
選択したCheckBoxの文字を、「SelectCheck」ボタンを押すとプリントしてくれます。  
  
使用しているuiファイルは
https://snippets.cacher.io/snippet/82070300e6a8c34b8f12
こちら。  
  

<script src="https://embed.cacher.io/d6026a815967a314a1f845970c294ea62e59fc17.js?a=abcd6b52889638d633a3f71e5bb228a9"></script>

## 基本的な使い方

まず、使用するButtonを「ButtonGroup」でまとめてから使用します。  

```python
        self.grpA = QtWidgets.QButtonGroup()
        self.grpA.addButton(self.ui.radioButton_4, 1)
        self.grpA.addButton(self.ui.radioButton_5, 2)
        self.grpA.addButton(self.ui.radioButton_6, 3)
        self.grpA.button(1).setChecked(True)
```
このButtonGroupはAbstractButtonクラスを継承して作成されているButtonを  
グルーピングすることができます。  
使い方は、上のコードのように、addButtonに対してButtonのオブジェクトをセットするだけ。  
その時に、アクセス用のIDを指定しておきます。  
  
以降は、ButtonGroup.button( **id** )で、  
Groupに含まれるButtonのオブジェクトの取得を行うことができる。  
  
そして、取得方法は  
  
```python
self.grpA.checkedButton()
```
ButtonGroupのcheckedButtonで選択中のButtonのオブジェクトを  
取得することができます。  
  

## それ以外の使い方

ButtonGroupのSignalの中には、クリックしたときに  
クリックしたボタンを取得する関数があります。
```python
self.grpA.buttonClicked.connect(self.checkButtonA)
```
使い方は、このようなシグナルを作成し、
```python
    def checkButtonA(self,btn):
        print(btn.text())
```
スロットの関数にはButtonのオブジェクトを受け取るための引数を  
用意しておきます。  
こうしておくと、Buttonをクリックしたときに  
今選択したButtonオブジェクトを受け取って、何かしらの処理をはさむことができます。  
  
同様な処理で buttonPressed buttonReleased などがありますが  
使い方は同じなので、用途に応じて差し替えます。  
  
参考のHelpは
ButtonGroup  
https://doc.qt.io/qtforpython/PySide2/QtWidgets/QButtonGroup.html#PySide2.QtWidgets.PySide2.QtWidgets.QButtonGroup.checkedButton
RadioButton  
https://doc.qt.io/qtforpython/PySide2/QtWidgets/QRadioButton.html  
ただし、RadioButtonはほぼAbstractButtonを継承したものなので  
https://doc.qt.io/qtforpython/PySide2/QtWidgets/QAbstractButton.html#PySide2.QtWidgets.QAbstractButton  
Buttonに関数は、AbstractButton側のヘルプを参照すると良いです。  
  
