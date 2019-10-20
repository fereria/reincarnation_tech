# TableViewの編集画面でDialogを使用する

<!-- SUMMARY:TableViewの編集画面でDialogを使用する -->

![](https://gyazo.com/cd0d297fa4a146f56c0e22470854f343.png)

前回の [TableViewでDelegateを使う（2）](view_model_delegate_02.md)をさらに拡張して  
TableViewの編集画面で、Dialogを表示して編集する機能を追加してみます。  
  
TableViewのセルは、Widgetsオブジェクトの場合はセルの中にぴたっとはまるように  
Widgetsが作成作成されます。  
しかし、TextEditのように長い文章を編集したい場合などは  
セルの中にWidgetsが埋め込まれてしまうととてつもなく編集がしづらくなってしまいます。  
  
![](https://i.gyazo.com/1f3551f880d038912878ceceb6b86475.gif)

ので、今回は、セルをクリックすると編集用Dialogを表示して、セルの中身を編集してくれるようにします。  
  
https://snippets.cacher.io/snippet/ac2de40c53468c8a2f94

全コードはながいので↑にアップしました。  
  
## 解説

### Dialogを作る

```python
class TextEditDialog(QtWidgets.QDialog):

    def __init__(self, uiPos, parent=None):
        super(TextEditDialog, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        self.textEdit = QtWidgets.QTextEdit(self)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

        btn = QtWidgets.QPushButton("Close")
        btn.clicked.connect(self.close)
        layout.addWidget(btn)

        self.uiPos = uiPos

        self.setWindowFlags(QtCore.Qt.Popup)

    def showEvent(self, event):
        self.setGeometry(self.uiPos.x(), self.uiPos.y(), 400, 300)
        super(TextEditDialog, self).showEvent(event)
```

まず、クリックしたときに表示されるDialogを作成します。  
基本は、QDialogに対してTextEditを配置しているだけですが２つポイントがあります。  
  
1つ目が、 setWindowFlags を使用して　Popup　扱いのWindowにしています。  
こうすると、Windowの上のバーの部分がなくなるのと、Windowが選択から外れるとWindowがクローズするように  
なります。  
２つめが、showEventでデフォルトのウィンドウ配置位置を指定しているところ。  
  
今回は、クリックしたセルの上に表示したいので  
起動時にWindow配置位置を引数で指定しているのですが  
__init__の中に setGeometryを入れてもうまく動きませんでした。  
  
かわりに、showEventをオーバーライドして、 setGeometryで配置したい位置を  
セットするようにしています。

### UIを呼び出す

```python
class TableDelegate(QtWidgets.QItemDelegate):

    def __init__(self, parent=None):
        super(TableDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        """
        編集したいCellに対して、編集用のWidgetsを作成する
        """
        if index.column() == 0:
            return QtWidgets.QLineEdit(parent)

        if index.column() == 2:
            spin = QtWidgets.QSpinBox(parent)
            spin.setMinimum(0)
            spin.setMaximum(100)
            return spin
        if index.column() == 3:
            edit = TextEditDialog(parent.mapToGlobal(option.rect.topLeft()), parent)
            return edit
```

作成したUIを呼び出すには、 createEditorでUIオブジェクトを作成し  
returnで返すようにします。  
  
![](https://gyazo.com/b08c701eaa74b6eb5afac34545c90d4a.png)

UIの表示位置は、編集したいセルの左上にぴったり合わせるように表示したいので  
option.rect.topLeft() を使用して座標を取得しています。  
  
しかし、このままだとTableViewのローカル座標扱いになってしまい  
変な位置に表示されてしまいます。  
  
ので、正しい位置に表示されるように parent.mapToGlobal(～～～) を使用して  
グローバル座標の数値を取得し、Dialogに対して表示位置のQPointをセットするようにしています。  
  
### 値をセットする

Model内の関数として、↓を作成

```python
    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if role == QtCore.Qt.EditRole:
            index.data(QtCore.Qt.UserRole).setData(index.column(), value)
            self.headerDataChanged.emit(QtCore.Qt.Vertical, index.row(), index.row())
            self.dataChanged.emit(index, index)
```


```python
    def setModelData(self, editor, model, index):
        """
        編集した値を、Modelを経由して実体のオブジェクトに対してセットする
        """

        value = None

        if index.column() == 0:
            value = editor.text()

        if index.column() == 2:
            value = editor.value()

        if index.column() == 3:
            value = editor.textEdit.toPlainText()

        if value is not None:
            model.setData(index, value)
```

Dialogを閉じると、setModelData関数が呼ばれます。  
ので、あとはほかのWidgetと同じくeditor(これはWidgetのオブジェクト)を  
使用して、値を取得し、モデルに対してセットします。  
  
```python
    def sizeHint(self, option, index):

        if index.column() == 0:
            return QtCore.QSize(100, 30)
        
        if index.column() == 2:
            return QtCore.QSize(200, 30)

        if index.column() == 3:
            document = QtGui.QTextDocument(index.data())
            document.setDefaultFont(option.font)
            return QtCore.QSize(document.idealWidth() + 50, 15 * (document.lineCount() + 1))
```
sizeHintで指定をしておけば、入力した行に応じてセルのサイズを変更できるようになります。  
このあたりの説明は [前回の説明](view_model_delegate_02.md) に説明がありますので  
そちらを参照してください。  
  
### 補足

今回は TextEditを使用しただけですが  
このTableViewから呼ばれるDialogは、通常のUIと同じく好きにWidgetを配置することができます。  
なので、いろいろいい感じにセットするようなGUIを作り、  
setModelDataで、そのDialogからいい感じに情報を取得して  
Modelにセットするようにすれば  
TableViewの各セルをがっつり編集するDialogを作ることなんかもできます。  
  
Delegateはいろいろ拡張すると好き放題できるのが良いですね。