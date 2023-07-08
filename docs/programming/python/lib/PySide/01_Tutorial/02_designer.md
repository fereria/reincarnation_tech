---
slug: /python/pyside/tutorial/02
title: QtDesigner で UI を作る
tags:
    - PySide
sidebar_position: 1
---

# QtDesigner で UI を作る

次は、[PySide で単独アプリケーションを作る](/python/pyside/tutorial/02) で作成した Application に、QtDesigner で作成した GUI を  
追加していきます。

QtDesigner とは、PySide のレイアウトツールです。  
QtDesigner を使用すると、Widget を Window に対して視覚的にわかりやすく並べることができます。

## Designer を起動する

PySide2 をインストールすると、PySide2 のインストールフォルダに QtDesigner がインストールされます。  
インストールされる場所は、Python3.6 の場合 C 直下ではないので

```
where python
```

これで Python のインストール場所を探し、  
where で表示された Python##のインストールフォルダ以下の

```
Python36\Lib\site-packages\PySide2
```

このフォルダ以下にある

![](https://gyazo.com/b6fbbba102e33eda115f5b74c6e5bac4.png)

designer.exe を実行します。

## UI を作る

![](https://gyazo.com/b813450957af6cba07c31a82f58caa7f.png)

QtDesigner を起動したら、「新しいフォーム」画面が表示されます。  
その表示された画面内の「MainWindow」を選択します。

![](https://gyazo.com/0da33f951253d576109261630167dee2.png)

このような空の Window が表示されます。  
次に、この Window に対して Widget を配置していきます。

### Widget を配置する

![](https://gyazo.com/ccb709bd55a99cc994a5dabaf13d7511.gif)

左側の「ウィジェットボックス」から Window に対して配置したい Widget を Drag&Drop します。  
こうすると、ウィンドウに Widget を置くことが出来ます。

### レイアウトする

Drag&Drop したままだと、ボタンは任意の場所に配置されただけで  
ウィンドウサイズが変更された場合もその場所に置かれたままになります。  
それだけだととても微妙な感じになってしまうので「レイアウト」機能を使用して  
作成した Window に対して  
Widget を配置していきます。

![](https://gyazo.com/148e380d0d368461c441aa3fe82c975e.png)

まずは、作成したウィンドウに対してぴったりになるように配置してみます。  
その場合は、Window の空いているところで右クリックし、  
「レイアウト」からどのようにレイアウトをするかを指定します。  
今回は、「垂直に並べる」に変更してみます。

![](https://gyazo.com/429c0bb0e5fd52bdc1537f03dac5b1d3.png)

垂直にすると、このようにウィンドウにフィットするようにボタンが配置されます。

![](https://gyazo.com/a43f869d7b053eb139ddb07bd72ce39d.gif)

垂直にすると、Widget を増やすごとに垂直に新しく追加されるようになります。

とりあえず、QtDesigner 上で Widget を配置できたので  
このファイルを保存して Python 側からロードしてみます。

## Python 側で .ui ファイルをロードする

.ui ファイルは、python ファイルと同じ階層に保存をした前提とします。  
サンプルコードは以下の通り。

<script src="https://embed.cacher.io/d1526b890b34a348aca2129108284ea17f09fa43.js?a=694a47dfe8b93fb38ee1d5576f52ea54"></script>

### ロードする

前回からの大きな変更点として、「作成した ui ファイルを読み込む」行が追加されました。

```python
self.ui = QUiLoader().load(os.path.join(CURRENT_PATH, 'sample_btn_ui.ui'))
```

追加する行はこの行になります。  
この「UiLoader」とは、QtDesigner で作成した UI を  
「複数の Widget を使って作ったカスタム Widget」として読み込むための関数になります。  
そして、その作った Widget を GUI 上に配置します。  
その配置をしているのが「setCentralWidget」です。

![](https://gyazo.com/51ae38c79f85e05d1ab4dde0381daefe.png)

今回のサンプルでは「QMainWindow」を継承したクラスで作成していますが  
この QMainWindow の Window 内は ↑ のようなレイアウトになっています。[詳しくは公式 Help 参照](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QMainWindow.html#detailed-description)  
なので、QtDesigner で作成したカスタム Widget を  
この「CentralWidget」部分に配置します。

### ボタンを押したときの動作を作成する

PySide で「ボタンを押す」のような Gui の動作に対して指定の処理を起こしたい場合には  
Signal-Slot と呼ばれる機能を使用します。  
詳細は次回説明します。

```python
self.ui.pushButton.clicked.connect(self.click_btn)
```

QUiLoader を使用して UI を読むときに「self.ui」にロードをしています。  
ので、この場合は「self.ui.####」という形で、Designer で作成した Widget にアクセスをすることができます。

![](https://gyazo.com/dd496d9e609e3b7b54e336a4df500e45.png)

この名前はどこで指定するかというと、  
QtDesigner の「プロパティエディタ」内の「QObject->objectName」で変更をします。  
シンプルな場合は問題ないかもですが、複雑な UI になると  
わかりにくくなってしまうので、名前は随時付けておくほうが良いです。

「ボタンを押したとき」という動作をしたい場合は、  
self.ui.objectName.指定の動作.connect(実行したい関数名)  
のように記述をします。  
今回は「押したとき」なので clicked を使用します。

![](https://gyazo.com/9f60bf83b145f096d0d4fe9e23073756.png)

ボタンを押すと、こんな感じで click_btn 関数が呼ばれます。
