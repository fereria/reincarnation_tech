---
title: LineEditに入力チェック・修正機能を入れる
---

![](https://i.gyazo.com/59d3c3755cdf1a70be495f990160e4f1.gif)

Webページによくある、電話番号やクレカの入力で
入力の値が正しいかチェックして、変更するような処理をPySideでできるか
試してみました。

## 標準機能でチェック

入力した値をチェックして、NGならば編集に入れない。。。みたいなことをする場合は  
QValidatorを使用します。  
このValidatorには、標準で QRegExpValidator, QDoubleValidator, QIntValidator があり、  
これを使うとかんたんに入力チェックをすることができます。

```python
class UISample(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.edit = QLineEdit()
        self.edit.setValidator(QIntValidator())
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.setLayout(layout)
```

使い方は、LineEdit.setValidator()を使用して、使いたいValidatorをセットすればOKです。  
上の例だと、IntValidatorなので「Intのみ」セットすることができます。

Intだけ、Doubleだけ、、、ではなく、もう少しチェックの幅を広げたい場合は  
QRegexpValidatorを使用します。

```python
self.edit.setValidator(QRegExpValidator('[^A-Z]+'))
```
これは、その名の通り正規表現で入力できるかどうかチェックすることができます。  
この例だと大文字は禁止...という意味になります。

こんな感じで、標準のValidatorでも入力させない...というのはかんたんに作れますが  
入力させないだけではなく、
「間違っていた場合は修正する」みたいなことをしたい場合もあると思います。
そういうときは、QValidatorクラスを継承して、新しいValidatorを作ります。

### カスタムなValidatorを作る

というわけで、試しに「携帯の電話番号を入力する」LineEditをテストで作ってみます。
携帯電話の場合は ###-####-#### という形で、途中に - が入ってほしい。  
そしてそれ以外は数字である...という条件にしてみます。

つまりは
1. 数字以外は入力させない
2. 4文字目と9文字目のときは - のみ許可
3. ただし - 以外の数字が入力されたら、勝手に - を挿入する
という挙動としてみます。

以下コード。
```python
class SampleValidator(QValidator):

    def __init__(self, parent=None):
        super().__init__()
        self.edit = parent

    def fixup(self, input):

        self.edit.setText(input[:-1] + "-" + input[-1])

    def validate(self, input, pos):
        # 入力の文字列が正しいかを判定する

        # 空OK
        if pos == 0:
            return QValidator.Acceptable

        if pos in [4, 9]:
            if input[pos - 1] == "-":
                return QValidator.Acceptable
            self.fixup(input)
            return (QValidator.Invalid, input, pos)

        # 電話番号入れ終わったら、以降は入力させない
        if pos > 13:
            return QValidator.Invalid

        # 数字限定
        if re.search("[0-9]", input) is None:
            return QValidator.Invalid

        return QValidator.Acceptable
```

QValidatorは、Virtual関数として「validate」と「fixup」が用意されています。  
まずは validate。
こちらは、入力がされると自動的に呼ばれる関数です。

この中で、Inputの文字列が正しいかどうかチェックして  
入力を許可する場合は Acceptable 許可できない場合は Invalid を返すようにします。

validateのInputは、１つめが、LineEditに入力された文字列。  
２つめが、今の入力している文字の位置になります。
文字の位置が０の場合は、入力が空を意味します。

上の例の場合、全てがからの場合。
つまりは一度入力したあと、LineEditを空にした場合は入力を許可します。
これをしないと、１文字目を削除することができません。

次に４文字目と９文字目は「-」にしたいので、そのチェックをします。
すでに - を手動で入力している場合は許可し、そうでない場合は
ｰをいれるように修正します。

修正したいときに呼ぶのがこの fixup()で、
文字列を渡して、その中で値を修正して、LineEditにセットし直します。

注意が必要なのは、こうして修正をしたときは再度チェックをしなければいけないところで  
その場合は、fixupしたあとに 

```python
    self.fixup(input)
    return (QValidator.Invalid, input, pos)
```

こんなふうに、結果以外に input pos をあわせて tupleを渡す必要があります。
これをしないと、無限ループになってしまいエラーになります（すごいハマった）

次に、電話番号の桁数以上に入力があったら許可しません。
そして、数字以外の入力だったら許可せず、

その先に残った値を許可しています。

今回は、間に - を挿入する...というので試しましたが  
例えば大文字は許容しないみたいなことをしたい場合や、指定文字列がきたら修正する
のようなことをこの fixupを使うことで、Validationする途中に値を修正する...
といったGUIを作ることができます。

工夫次第で色々できそう？

参考用の全コードは
https://snippets.cacher.io/snippet/4577f23a56f7e563e50c
こちら。

## 参考

* https://doc.qt.io/qtforpython/PySide2/QtGui/QIntValidator.html
* https://stackoverflow.com/questions/16067893/how-does-qvalidator-fixup-works-in-pyside
* https://unpyside.wixsite.com/unpyside/post/2018/12/20/%E3%80%90mayapyside%E3%80%91qlineedit%E3%81%A7%E6%95%B0%E5%80%A4%E3%81%AE%E3%81%BF%E3%81%AE%E5%85%A5%E5%8A%9B%E3%81%95%E3%81%9B%E3%82%8B%E6%96%B9%E6%B3%95