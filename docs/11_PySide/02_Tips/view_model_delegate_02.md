# PySideのTableViewでDelegateを使う(2) paintする

<!-- SUMMARY:PySideのTableViewでDelegateを使う(2) paintする -->

前回の [TableViewでDelegateを使う（1）](view_model_delegate_01.md) のデータをすこし修正して  
各セルごとの描画やらを色々作ってみました。  
  
全コードはかなり長いので  
https://snippets.cacher.io/snippet/9efc9751db929a15c9a2  
こちらを参照。  
今回はuiファイルは使用していません。  
  
![](https://i.gyazo.com/eef30e75ba7e29d5dc1ce35e8d6e0df7.gif)

実行結果はこんな感じ。  
今回のサンプルのポイントは

* セルを見やすくするために背景色を変更
* チェックボックスを画像で作成
* ステータス部分を描画で見やすくしてみる
* Viewのセルサイズを自動フィットさせる

この3つです。  
  
前回のDelegateで説明したとおり、Delegateのpaint関数をオーバーライドすることで  
見た目の描画を自由に作成することができます。  
今回はこの描画部分でテストしていたときにけっこうハマった所をメモっておきます。

## 背景色を変更する

```python
# Painter COLOR ----- #
BACKGROUND_BASE_COLOR_A = QtGui.QColor(255, 255, 255)
BACKGROUND_BASE_COLOR_B = QtGui.QColor(240, 240, 240)
STATUS_FONT_COLOR = QtGui.QColor(255, 255, 255)
 
BACKGROUND_SELECTED = QtGui.QColor(204, 230, 255)
BACKGROUND_FOCUS = QtGui.QColor(240, 248, 255)
 
FONT_BASE_COLOR = QtGui.QColor(0, 0, 0)
```

まず、paint内で使用する色は別途変数で定義をしておきます。  
なんで直書きしないかというと、コード内でどこにどの色を使用しているのかわかりやすくするためです。  
私はなんとなくですがpythonファイルのあたまにまとめて記載するようにしています。  
  

```python
    def paint(self, painter, option, index):
 
        # 背景色を指定する
        data = index.data()
 
        bgColor = BACKGROUND_BASE_COLOR_A
        if (index.row() % 2) != 0:
            bgColor = BACKGROUND_BASE_COLOR_B
 
        if option.state & QtWidgets.QStyle.State_Selected:
            bgColor = BACKGROUND_SELECTED
        if option.state & QtWidgets.QStyle.State_HasFocus:
            bgColor = BACKGROUND_FOCUS
 
        brush = QtGui.QBrush(bgColor)
        painter.fillRect(option.rect, brush)
```

まず、背景色について。  
paint内で描画する場合は、引数で渡される「painter（QPainter）」を使用します。  
  
このpaintは、セルごとにセルの数分実行されます。  
どのセルの処理をしているかは「index」で取得することが出来ます。  
  
今回は奇数行と偶数行で色を変えて見やすくしたかったので  
まずはそのいずれかの色を指定します。  
さらに、「選択されてる」あるいは「ドラッグ中」の場合は別の色を表示するように  
QStyleを使用して判定をします。  
  
引数の option は、セルごとの様々な設定情報を受け取るためのもので  
option.state は、現在のセルのステータスを  
option.rect は、現在のセルの矩形を  
それぞれ取得することができます。  
  
指定のセル色を決めたら、 fillRect で　指定色でセルを塗りつぶします。  
  
このpainterで何かをしたい場合は、  
1. 塗りつぶし色をsetBrushで指定
2. 線の色をsetPenで指定
3. 描画する

という順番で処理を書きます。  
一度セットすると、次の処理でもセットされた色や塗りつぶし方法の指定が引き継がれるのに  
注意が必要です。  
  
## チェックボックスを画像で描画する

次にチェックボックス。  
一応デフォルトでもチェックボックスボタンは用意されているのですが  
それだと位置調整とか色々めんどうだったのと  
画像でやれば見た目もおしゃれにしやすいので画像でつくってみます。  
  
まず、チェックのONとOFFの画像を用意しておきます。  
私のサンプルは  
http://modernuiicons.com/  
このサイトのアイコンを使用しました。  
  
```python
        if index.column() == 1:
            if data:
                pix = QtGui.QPixmap(CHECK_IMG)
            else:
                pix = QtGui.QPixmap(UNCHECK_IMG)
 
            rect = self.getCheckBoxRect(option)
            painter.drawPixmap(rect, pix)
```
まずpaint内の描画。  

```python
    def getCheckBoxRect(self, option, imgSize=30):
 
        return QtCore.QRect(option.rect.left() + (option.rect.width() / 2) - (imgSize / 2),
                            option.rect.top() + (option.rect.height() / 2) - (imgSize / 2),
                            imgSize,
                            imgSize)
```

ボタンの表示位置は、QRectで設定するのですが、  
描画部分以外にも「ボタンを押した」処理を位置で判定するのに使用したいので  
別途関数にしておきます。  
位置は、現在のセルの中央にimgSizeの大きさで表示するようにします。  
  
そして、画像を drawPixmap で表示します。  
  
```python
    def editorEvent(self, event, model, option, index):
 
        if index.column() == 1:
            if self.getCheckBoxRect(option).contains(event.pos().x(), event.pos().y()):
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    currentValue = model.items[index.row()].data(index.column())
                    model.setData(index, not currentValue)
                    return True
        return False
```

クリックしたときの挙動は基本前回と同じです。  
画像表示位置と同じ矩形でマウス位置が範囲内かどうかを判定して、  
範囲内でクリックされている場合は、セルのBool値を変更します。  
  
この部分も若干処理から変更していて  
前回は
```python
model.items[index.row()].setData(index.column(), not currentValue)
model.layoutChanged.emit()
```
このように、modelのitems(表示しているオブジェクトの配列)のsetData で値を指定していましたが  
modelのsetData関数をオーバーライドした関数を作成し、  
そちら経由で値を登録するようにしました。  
  
```python
    def setData(self, index, value, role=QtCore.Qt.EditRole):
 
        if role == QtCore.Qt.EditRole:
            index.data(QtCore.Qt.UserRole).setData(index.column(), value)
            self.headerDataChanged.emit(QtCore.Qt.Vertical, index.row(), index.row())
            self.dataChanged.emit(index, index)
```

今までは、値を変更したときにViewをアップデートする良い方法が layoutChanged しか思いつかず  
もっと良い方法はないか探していたのですが  
setDataでセットして、 dataChangedとheaderDataChangedするほうが色々と都合が良い（あとで詳しく説明）  
のが分かったので、この方式にしました。  
  
### ステータス部分を色をつけて見やすくする  
  
![](https://gyazo.com/93e3a1a85d1eed32523408e0775355c5.png)

こんな感じのLabelっぽい表示をしたかったので、Itemにステータスを追加して  
それに応じて表示を変更するようにしました。  
  
```python
class Status(IntEnum):
 
    WAITING = auto()
    RUN = auto()
    FINISH = auto()
    ERROR = auto()
 
 
class StatusItem:
 
    def __init__(self, name, color):
 
        self.name = name
        self.color = color
        
STATUS_BG_COLOR = {
    Status.WAITING: StatusItem("待機中", QtGui.QColor(0, 0, 205)),
    Status.RUN: StatusItem("実行中", QtGui.QColor(148, 0, 211)),
    Status.FINISH: StatusItem("完了", QtGui.QColor(46, 139, 87)),
    Status.ERROR: StatusItem("エラー", QtGui.QColor(255, 0, 0))
}        
```

まず、StatusのEnumを作成（EnumはPython3から追加されたっぽい）  
そして、どのStatusがどの色で文字なのかを指定するためのクラスとDictを作成しておきます。  
  
```python
        # Status表示
        if index.column() == 3:
            statusSizeX = 60
            statusSizeY = 20
            brush = QtGui.QBrush(data.color)
            painter.setPen(QtCore.Qt.NoPen)
            rect = QtCore.QRect(option.rect.left() + (option.rect.width() / 2) - (statusSizeX / 2),
                                option.rect.top() + (option.rect.height() / 2) - (statusSizeY / 2),
                                statusSizeX,
                                statusSizeY)
            painter.setBrush(brush)
            painter.drawRoundRect(rect)
            painter.setPen(STATUS_FONT_COLOR)
            painter.setFont(QtGui.QFont("メイリオ", 9))
            painter.drawText(rect, QtCore.Qt.AlignCenter | QtCore.Qt.TextWordWrap, data.name)
```
そしてpaint内で描画処理を書きます。  

## セルのサイズをコントロールする

最後に一番ハマったのがセルサイズ。  
今回は縦横サイズは固定で作りたかったので  
固定にしつつも、中の情報に応じて大きさを変更するようにします。  
  
```python
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
```
まず、MainWindowでtableViewを作っているところで  
HeaderサイズのResizeModeをResizeToContentsに変更します。  
このモードにすると、DelegateのSizeHintsをもとにした大きさに  
セルのサイズが固定されるようになります。  
  
```python
    def sizeHint(self, option, index):
 
        if index.column() == 1:
            return self.getCheckBoxRect(option).size()
 
        if index.column() == 2:
            return QtCore.QSize(200, 30)
 
        if index.column() == 3:
            return QtCore.QSize(90, 30)
 
        if index.column() == 4:
            document = QtGui.QTextDocument(index.data())
            document.setDefaultFont(option.font)
            return QtCore.QSize(document.idealWidth() + 50, 15 * (document.lineCount() + 1))
 
        return super(TableDelegate, self).sizeHint(option, index)
```

次に、DelegateのsizeHintをオーバーライドにします。  
このsizeHint関数も、セルの数分繰り返され、セルの縦・横サイズがreturnしたサイズになります。  
  
ProgressBarのように固定サイズならそのまま固定のSizeを返せばよいのですが  
複数行の文字などは文字の行に応じて変更したい。  
  
その方法として、 [QFontMetrics](https://doc.qt.io/qtforpython/PySide2/QtGui/QFontMetrics.html?highlight=fontmetrics#PySide2.QtGui.QFontMetrics) というクラスが存在しているのですが、  
この場合改行（\n）は考慮されないので  
QTextDocument を使用して行を取得し、その行に応じてそれっぽい縦・横になるようにしています。  
この辺もうちょっとうまい方法ありそうです。  
  
idealWidth() が改行ありでの横サイズっぽいのですが  
それだと若干キツキツだったので、＋で余白分を指定しています。  
  
で。  
これでセルのサイズ変更はできたのですが  
デフォルトだと行数が変更されてもSizeHintが変更されませんでした。  
  
文字が変更されたときに、SizeHintをアップデートしたい場合はどうしたらいかというと  
modelの headerDataChanged のシグナルをすれば良いので  
値が変わった時などに自動でアップデートされるように  
オーバーライドした setData 関数内で、headerDataChanged と dataChanged を呼ぶようにしています。  
（おかげでlayoutChangedをDelegate側でemitする必要がなくなりました）  
  
だいぶこれでDelegateを使用したTableViewの拡張ができてきた気がします。  
ので、次は中の項目をDrag＆Dropで入れ替えたりするやり方を調べてみようかと思います。