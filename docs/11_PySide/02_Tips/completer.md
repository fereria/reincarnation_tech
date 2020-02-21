---
title: QCompleterでLineEditに予測変換を入れる
---

PySid の LineEdit に予測変換を入れたいみたいな事がでてきたので  
やり方を調べてみました。

## 基本編

まず、やりたかったのは
「Tab キーを押したら小さな Menu が出てきて、検索みたいな事ができるようにしたい」
です。
なので、QDialog に LineEdit を入れて、setWindowFlags を Popup にした UI をつくります。

![](https://gyazo.com/719a8365f414216337483d89f5fe8537.gif)

こんな感じ。
Twitter で最初のテストを Up したときは、マウス位置が Window の左上で
Edit 部分が見づらかったので、マウス位置が画面右下になるようにしたのと
サンプル時は LineEdit をそのまま show()していたのを QDialog に置き換えました。

```python
class PopupSerchEdit(QDialog):

    send = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)

        self.edit = QLineEdit(self)
        layout.addWidget(self.edit)
        self.setLayout(layout)
        # 現在のマウス位置にGUIを出す
        size_x = 200
        size_y = 50
        pos = QCursor().pos()
        self.setGeometry(pos.x() - size_x,
                         pos.y() - size_y,
                         size_x,
                         size_y)

        self.edit.returnPressed.connect(self.Submit)
        self.edit.setFocus()

        # SimpleなAutoCompleteを作る
        comp = QCompleter(self)
        comp.setModel(QStringListModel(['hogehoge', 'fugafuga', 'foo', 'bar']))
        # 全部表示: UnfilteredPopupCompletion
        # Inlineに候補を表示: InlineCompletion
        # POPUP表示: PopupCompletion
        comp.setCompletionMode(QCompleter.InlineCompletion)
        self.edit.setCompleter(comp)

    def Submit(self):
        # Enterしたら文字をEmitして閉じる
        self.send.emit(self.edit.text())
        self.close()
```

コードがこちら。

で、今回のおにに書かれた「AutoComplete」自体はどうするかというと
デフォルトで「QCompleter」クラスが用意されているのでこれを使用します。

この QCompleter は、引数で受け取った Model を利用して、予測変換をだしてくれます。
上の例はもっとも簡単な例として、QStringList を利用して候補の List を受け渡しています。

### setCompletensionMode

CompletensionMode とは、予測のリストをどういう風に出すかのオプションです。
これには、大きく分けて 3 種類あって

![](https://gyazo.com/eb587fdbe9cc1765a096333d2cb906c9.png)
InlineCompletion が、Inline 上に候補をこんな感じにだすもの

![](https://gyazo.com/71bc7fb2175c76518f4c5046b3ad6a5f.png)
PopupCompletion が、候補を Popup 表示するもの

![](https://gyazo.com/5f358bdf58139011924478ddb6449c23.png)
UnfilteredPopupCompletion が、すべての候補を出すもの　になっています。

使いやすいのはPopupかな...ということで、以降はPOPUPを使用します。

### 基本の形

```python
        # SimpleなAutoCompleteを作る
        comp = QCompleter(self)
        comp.setModel(QStringListModel(['hogehoge', 'fugafuga', 'foo', 'bar']))
        # 全部表示: UnfilteredPopupCompletion
        # Inlineに候補を表示: InlineCompletion
        # POPUP表示: PopupCompletion
        comp.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.edit.setCompleter(comp)
```
AutoCompleteに必要なのがこの部分。
構造は簡単で、候補に出したいModelをsetMomdelでセットし
（今回は特別に作っているけど、別のViewでつかってるModelを入れても良い）
予測をだしたいLineEditに対してCompleterを setCompleterでセットすればOKです。

このモデル部分に QDirModel を使うことで、フォルダの予測変換なども作る事が出来ます。

## カスタムモデル予測変換

以上が基本型でしたが、例えばカスタムで作ったTreeViewで予測を出したいとなった場合は
このQCompleterをカスタマイズする必要があります。

ということで、こちらではテストつくってるUSDのSceneGraphのTreeViewで
予測変換を作ってみます。

### モデル側の設定

まず、予測変換時に使用する文字列はどのように設定されているかというと
Modelのdataの「EditRole」の値が使用されます。（DisplayRoleではないのに注意）
なので、Modelを
```python
    def data(self, index, role):

        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.DisplayRole:
            return item.data(index.column())
        if role == Qt.UserRole:
            return item
        if role == Qt.EditRole:
            return item.data(0)
        return None
```
こんな感じに、DisplayRoleと同じPrimNameを返すようにしておきます。

### Completeのカスタマイズ

次に、QCompleterを継承したカスタムQCompleterを作ります。

```python
class CustomQCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setCompletionMode(self.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)

    def setModel(self, model):
        self.srcModel = model
        self.proxyModel = QSortFilterProxyModel(self)
        self.proxyModel.setSourceModel(self.srcModel)
        super(CustomQCompleter, self).setModel(self.proxyModel)

    def splitPath(self, path):
        return re.sub("^/", "", path).split("/")

    def pathFromIndex(self, index):
        # SdfPatにに置き換える
        item = index.data(Qt.UserRole)
        return item.data(2)
```

重要な所は2つで「**splitPath**」と「**pathFromIndex**」です。

### splitPath
splitPathとは、LineEditで入力した値を引数で受け取り
その値がTreeViewの階層とどのように対応するか（予測されるか）を配列で返します。

デフォルトの場合どのようになるかというと、
/test/hoge/fuga を検索したかったとして、LineEditに /test/hoge と入れても fugaは予測に出ません。
これは、それぞれの予測は、各TreeViewのEditRoleの文字にを使用しているからで
/test/hoge/fuga を予測したい場合は test -> hoge -> fuga という順に
TreeViewの階層を見つけなければ行けません。

ので、この辺をコントロールするのが splitPath で
各ツリーの階層ごとのマッチさせたい文字列を配列で返すようにします。

今回のサンプル例だと、UsdのSefPathは / で区切られるので / で入力パスを分割して
[test,hoge]という配列を受け渡すようにします。

### pathFromIndex
次に pathFromIndex。
こちらは、予測変換された結果、LineEditに入力される文字列を返します。
splitPathと同じように、デフォルトの場合は各要素のEditRoleでかえされた値しか
返してくれません。
なので、TreeViewのように、各Treeの要素すべてを含む値を入力させたい場合は
別途カスタムする必要があります。

ので、今回はSdfPathをpathFromIndexで返すようにしました。

![](https://gyazo.com/a6b015c08022588ce33cabbea999e0bd.gif)

結果。
pathFromIndexで受け取る値は現在のItemのSdfPathなので
予測変換している場合、頭に / が入ります。

一応全コードは
https://snippets.cacher.io/snippet/579ea1daa316875bd869
こちら。

## まとめ

予測変換とかどうやるんだろうと前から疑問ではあったのですが
調べてみたら思いのほか簡単にできたので、もう少し早くやっておけば良かったです。

はまりポイントとして、CustomModelの時の変に使うRoleがEditRoleだったこと
（調べた情報によってはCompleterRoleとかあったけどPySideにはなかった）
splitPathとpathFromIndexでなにを返せば良いのかの関連性がつかみにくいこと。

しかしわかってしまえば、各種Modelと組み合わせて色々拡張できそうなのが良いです。

参考によってはProxyModelと併用して正規表現での絞り込みをしたりとかしてたので
次の機会には対応してみようと思います。

## 参考

- https://stackoverflow.com/questions/5129211/qcompleter-custom-completion-rules
- https://kiwamiden.com/how-to-make-autocomplete-of-pass-input

