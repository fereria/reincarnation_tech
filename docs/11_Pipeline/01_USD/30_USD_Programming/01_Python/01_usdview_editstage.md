---
title: USDViewPluginで自作GUIを追加しよう
---

[前回](00_usdView_tutorial.md) で pluginInfo.json を書いて usdview にプラグインを追加することができたのですが、
今回はただ Print するだけではなく、今開いている Stage をゴニョゴニョするような処理を
Plugin を利用して書いてみます。

フォルダ構成や plugInfo.json は前回と共通なのでスキップして本体のみ解説。
長いけど全コード

```python
from pxr import Tf, UsdGeom
from pxr.Usdviewq.plugin import PluginContainer

from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton


class TestDialog(QDialog):

    def __init__(self, usdviewApi):
        super().__init__(usdviewApi.qMainWindow)

        self.resize(400, 200)

        self.usdviewApi = usdviewApi

        layout = QVBoxLayout()
        self.setLayout(layout)
        btn = QPushButton('ShowSelection')
        btn.clicked.connect(self.showSelection)
        layout.addWidget(btn)
        btn = QPushButton('SnapShot')
        btn.clicked.connect(self.viewportCapture)
        layout.addWidget(btn)
        btn = QPushButton('createPrim')
        btn.clicked.connect(self.createPrim)
        layout.addWidget(btn)

    def showSelection(self):

        print(self.usdviewApi.dataModel.selection.getPrims())

    def viewportCapture(self):

        img = self.usdviewApi.GrabViewportShot()
        img.save("D:/capture.jpg")
        self.usdviewApi.PrintStatus("Save Image -> D:/capture.jpg")

    def createPrim(self):

        prim = self.usdviewApi.stage.GetPrimAtPath("/createPrim")
        if not prim.IsValid():
            prim = self.usdviewApi.stage.DefinePrim("/createPrim")

        childSize = len(prim.GetChildren())

        xform = UsdGeom.Xform.Define(self.usdviewApi.stage, prim.GetPath().AppendChild(f"ChildNode_{childSize+1}"))
        self.usdviewApi.dataModel.selection.setPrim(xform)


def printMessage(usdviewApi):

    win = TestDialog(usdviewApi)
    win.show()


class TutorialPluginContainer(PluginContainer):

    def registerPlugins(self, plugRegistry, usdviewApi):

        self._printMessage = plugRegistry.registerCommandPlugin(
            "TutorialPluginContainer.printMessage",
            "TestGUI",
            printMessage)

    def configureView(self, plugRegistry, plugUIBuilder):

        tutMenu = plugUIBuilder.findOrCreateMenu("Tutorial")
        tutMenu.addItem(self._printMessage)


Tf.Type.Define(TutorialPluginContainer)
```

usdview の Plugin に必要なのは

1. PluginContainer を継承したクラス
2. 上のクラスを Tf.Type.Define

この２つです。
この Container 内で Menu に新しい GUI を表示するコマンドを追加してみます。

![](https://gyazo.com/c94221845730bcf4fb6747c6e4d9f29e.png)

この Menu を実行すると、

![](https://gyazo.com/cbc02418fd38c7a9fd886b6433772341.png)

こんな感じの GUI が表示されます。

### MainWindow を受け取る

usdview は Maya などと同じく PySide を利用して作られているので
カスタム GUI を作りたい場合も Maya と同じく MainWindow を取得して
その MainWindow を親にした Dialog を作成すれば OK です。

plugRegistry.registerCommandPlugin で登録した関数には
引数で pxr.Usdviewq.usdviewApi.UsdviewApi クラスオブジェクトを受け取ります。
このオブジェクトには、現在の USDView で開いている Stage や Window の情報、
CurrentFrame の値、View 設定などが含まれていて
これらを利用して処理を書くことができます。

```python
super().__init__(usdviewApi.qMainWindow)
```

PySide の MainWindow は usdviewApi.qMainWindow で取得できます。
今回は QDialog で Stage に対して色々操作をしたかったので
QDialog には UsdviewApi オブジェクトを渡して
\_\_init\_\_に対してそのオブジェクトの qMainWindow を渡すようにしました。

### TreeView の Item を追加・選択

usdView の TreeView に対して何かをしたい場合は self.usdviewApi.dataModel を利用します。
この dataModel を使用すれば、選択中の Prim オブジェクトを取得したり、
指定の Prim を選択状態にしたりできます。

```python
    print(self.usdviewApi.dataModel.selection.getPrims())
```

選択中の Prim は、 selection.getPrims() で取得ができます。

![](https://gyazo.com/a91faa582e88b6020517f786f43e0812.png)

ここで取得できるのは USD の Prim なので
あとは単独のツールで書くのと同じく処理を書けば OK です。

```python
        prim = self.usdviewApi.stage.GetPrimAtPath("/createPrim")
        if not prim.IsValid():
            prim = self.usdviewApi.stage.DefinePrim("/createPrim")

        childSize = len(prim.GetChildren())

        xform = UsdGeom.Xform.Define(self.usdviewApi.stage, prim.GetPath().AppendChild(f"ChildNode_{childSize+1}"))
        self.usdviewApi.dataModel.selection.setPrim(xform)
```

self.usdviewApi.stage で、現在の Stage を取得することができるので
新しい Prim を追加する場合などは、取得した Stage に対して DefinePrim であったり
UsdGeom.Define(stage,"<PATH>")
を利用してPrimを追加することができます。

TreeViewに増やしたPrimを選択状態にしたい場合は、
```python
self.usdviewApi.dataModel.selection.setPrim(xform)
```

selection.setPrim(\<primObj\>)

このように setPrim で、選択したいPrimを指定します。

### ViewPortのScreenShotをつくる

この usdvieApiを利用すると、現在のViewportのスクリーンショットをかんたんに取ることができます。

```python
        img = self.usdviewApi.GrabViewportShot()
        img.save("D:/capture.jpg")
        self.usdviewApi.PrintStatus("Save Image -> D:/capture.jpg")
```

GrabViewportShot() で、Viewportの QImageオブジェクトを取得できます。
ので、あとは save(Path) で

![](https://i.gyazo.com/ee182d4498896a8625079f7c48337d6b.jpg)

こんな感じで現在のスクショが保存できます。

## まとめ

Menu登録した関数の引数で、いろんな情報を受け取れるオブジェクトが渡されるので
あとは stageから中をTraverseしたり、選択Primになにかしたり
かんたんにできることがわかりました。

https://graphics.pixar.com/usd/docs/Creating-a-Usdview-Plugin.html

usdviewApi で受け取れる内容については、公式Docs の Using the Usdview APIに
まとめがあります。

usdView自体はデフォルトだと編集することが難しい（Pythonコマンドががんばるしかない）
ですが、拡張を入れればできることがかなり増えるので
いろいろな使い方できそうです。