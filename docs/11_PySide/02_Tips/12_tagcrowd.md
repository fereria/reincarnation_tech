---
title: PySideでタグクラウドっぽいWidgetを作る
tags:
    - PySide
    - Python
---

[前回](11_custom_layout.md) 作った FlowLayout を利用して、今度は実践として
ウェブページなどでよく見かけるタグクラウドっぽい Widget を作ってみようかと思います。

[全コードはこちら](/65_SampleCode/PySide/tagCrowd)
FlowLayout 部分は前回と同じなので、説明は省きます。

## 基本機能

![](https://gyazo.com/3409ed47c2ec59da71ab656e4befeb43.png)

今回作るタグクラウドでは、まずこのようなシンプルな表示のみをする機能と、

![](https://gyazo.com/5e2e751dbf782fc6d46f4368290c264b.gif)

一覧のタグを追加・削除することができる機能、
そして現在のタグの一覧を取得できるようにします。

## Tag 部分

```python
class Tag(QFrame):

    deleteTag = Signal(object)

    def __init__(self, name="", color: QColor = QColor(200, 200, 200), deletable=True, parent=None):
        super().__init__(parent)

        css = f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});border-radius: 5px;"
        self.setStyleSheet(css)
        self.label = QLabel(name)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(10, 5, 10, 5)

        if deletable:
            self.button = QPushButton()
            icon = QIcon()
            icon.addPixmap(QPixmap("D:/work/py37/PySide/icons/batu.png"), QIcon.Normal, QIcon.On)
            self.button.setIcon(icon)
            self.button.setFlat(True)
            layout.addWidget(self.button)
            self.button.clicked.connect(self.delete)

    @property
    def name(self):
        return self.label.text()

    def delete(self):

        self.deleteTag.emit(self)
```

![](https://gyazo.com/77bb6bef1469f25d8f1041c39fa67488.png)

最初はタグ部分。
ベースは QFrame を使用します。
背景色や、エッジを少し丸くするのは、QSS を Frame に対して指定することで作成しています。
そして、この Frame に対して HBoxLayout で Label とボタンを配置するようにします。

タグのマージンは、LayoutHBoxLayout と QFrame 自体に存在しているのですが
両方入っているとコントロールしにくいので、レイアウト自体のマージンは 0 にしたうえで
QFrame のマージンでいい感じになるように調整しています。

そして、タグを削除するとき用に Delete のシグナルを追加します。
シグナルでは、削除するタグ（自分自身）を渡すようにします。
これは、この Tag 側で削除してしまうと、レイアウトの更新的によろしくないので
このシグナルを受け取った TagCrowd 側で削除します。

タグの色は引数で変えられるようにしておきます。

## TagCrowd

```python
class TagCrowd(QWidget):

    def __init__(self, addNewTag=True, deletetable=True, parent=None):
        super().__init__(parent)

        self.layout = FlowLayout(3, 5, 5)
        self.setLayout(self.layout)

        self.addNewTag = addNewTag
        self.deletable = deletetable

        if addNewTag:
            self.button = QPushButton(self)
            self.button.clicked.connect(self.showAddEdit)
            icon = QIcon()
            icon.addPixmap(QPixmap("D:/work/py37/PySide/icons/plus.png"), QIcon.Normal, QIcon.On)
            self.button.setIcon(icon)
            self.button.setFlat(True)

        self.tags = []

    def getTagNames(self):

        return [x.name for x in self.tags]

    def showAddEdit(self):

        editor = PopupEdit(self)
        editor.send.connect(self.addTag)
        editor.show()

    def deleteTag(self, widget):

        self.tags = [x for x in self.tags if x.name != widget.name]
        widget.deleteLater()

    def addTag(self, name):

        self.layout.clear()
        currentTags = [x.name for x in self.tags]

        if name not in currentTags:
            tag = Tag(name, deletable=self.deletable)
            tag.deleteTag.connect(self.deleteTag)
            self.tags.append(tag)

        for i in self.tags:
            self.layout.addWidget(i)

        if self.addNewTag:
            self.layout.addWidget(self.button)
```

続いてタグクラウド本体。
構造はシンプルで、先ほどの Tag ウィジェットを FlowLayout を利用して配置します。
FlowLayout 側で配置しているオブジェクトの管理や増減をするか迷ったのですが
現在のタグ一覧を取得したり、削除したり追加したいする挙動は TagCrowd 側でやりたかったので
addTag 時にレイアウトへの追加は毎回クリア → 追加するようにします。

![](https://gyazo.com/fc08defecc01e20dd0308f031b57fb1c.png)

タグ追加ボタンは、FlowLayout の最後尾に追加するようにしたいので、
addTag でクリア →Tag オブジェクトを追加した最後に FlowLayout に対して addWidget しています。

削除は、Tag のシグナルで削除されたときに deleteTag を呼ぶようにします。
そして該当タグを tags から削除して、自分自身を deleteLater で削除します。
（deleteLater してから Tag オブジェクトを削除するとレイアウトがぶっ壊れるので注意）

```python
class PopupEdit(QDialog):

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

    def Submit(self):
        # Enterしたら文字をEmitして閉じる
        self.send.emit(self.edit.text())
        self.close()
```

addTag するときの Dialog は、{{markdown_link('02_completer')}}の時のコードを流用して、Popup で表示＋閉じるときに Emit する簡単な入力を作りました。

## 使ってみる

```python
class SampleUI(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = QUiLoader().load(f"{CURRENT_PATH}/scroll.ui")

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.ui)

        self.crowd = TagCrowd()
        self.ui.scrollArea.setWidget(self.crowd)

        self.crowd.addTag('aaa')
        self.crowd.addTag('bbb')
        self.crowd.addTag('ccc')

        self.ui.pushButton.clicked.connect(self.showTags)

    def showTags(self):
        print(self.crowd.getTagNames())

```

[sroll.ui](https://gist.github.com/fereria/036b2ee82789c33a204dfa3308ee2d59)は前に使ったものにボタンを追加しています。

## まとめ

FlowLayout と合わせてよく使いそうなタグクラウドウィジェットができました。
あとは、これにタグ追加シグナルやタグ削除シグナルを追加したり
個別にタグの色を変更できるようにするといったことを追加すると、さらに便利になるのでは？と思います。
