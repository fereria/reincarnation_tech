# QtDesignerでUIを作る

<!-- SUMMARY:QtDesignerでUIを作る -->

次は、[PySideで単独アプリケーションを作る](01_start.md) で作成したApplicationに、QtDesignerで作成したGUIを  
追加していきます。  
  
QtDesignerとは、PySideのレイアウトツールです。  
QtDesignerを使用すると、WidgetをWindowに対して視覚的にわかりやすく並べることができます。

## Designerを起動する

PySide2をインストールすると、PySide2のインストールフォルダにQtDesignerがインストールされます。  
インストールされる場所は、Python3.6の場合C直下ではないので
```
where python
```
これでPythonのインストール場所を探し、  
where で表示されたPython##のインストールフォルダ以下の  

```
Python36\Lib\site-packages\PySide2
```

このフォルダ以下にある  

![](https://gyazo.com/b6fbbba102e33eda115f5b74c6e5bac4.png)

designer.exeを実行します。  
  
## UIを作る

![](https://gyazo.com/b813450957af6cba07c31a82f58caa7f.png)

QtDesignerを起動したら、「新しいフォーム」画面が表示されます。  
その表示された画面内の「MainWindow」を選択します。  
  
![](https://gyazo.com/0da33f951253d576109261630167dee2.png)

このような空のWindowが表示されます。  
次に、このWindowに対してWidgetを配置していきます。

### Widgetを配置する

![](https://gyazo.com/ccb709bd55a99cc994a5dabaf13d7511.gif)

左側の「ウィジェットボックス」からWindowに対して配置したいWidgetをDrag&Dropします。  
こうすると、ウィンドウにWidgetを置くことが出来ます。  
  
### レイアウトする

Drag&Dropしたままだと、ボタンは任意の場所に配置されただけで  
ウィンドウサイズが変更された場合もその場所に置かれたままになります。  
それだけだととても微妙な感じになってしまうので「レイアウト」機能を使用して  
作成したWindowに対して  
Widgetを配置していきます。  
  
![](https://gyazo.com/148e380d0d368461c441aa3fe82c975e.png)

まずは、作成したウィンドウに対してぴったりになるように配置してみます。  
その場合は、Windowの空いているところで右クリックし、  
「レイアウト」からどのようにレイアウトをするかを指定します。  
今回は、「垂直に並べる」に変更してみます。  
  
![](https://gyazo.com/429c0bb0e5fd52bdc1537f03dac5b1d3.png)

垂直にすると、このようにウィンドウにフィットするようにボタンが配置されます。  
  
![](https://gyazo.com/a43f869d7b053eb139ddb07bd72ce39d.gif)

垂直にすると、Widgetを増やすごとに垂直に新しく追加されるようになります。  
  
とりあえず、QtDesigner上でWidgetを配置できたので  
このファイルを保存してPython側からロードしてみます。  
  
## Python側で .ui ファイルをロードする

.uiファイルは、pythonファイルと同じ階層に保存をした前提とします。  
サンプルコードは以下の通り。  


<script src="https://embed.cacher.io/d1526b890b34a348aca2129108284ea17f09fa43.js?a=694a47dfe8b93fb38ee1d5576f52ea54"></script>

### ロードする

前回からの大きな変更点として、「作成したuiファイルを読み込む」行が追加されました。  
  
```python
self.ui = QUiLoader().load(os.path.join(CURRENT_PATH, 'sample_btn_ui.ui'))
```
追加する行はこの行になります。  
この「UiLoader」とは、QtDesignerで作成したUIを  
「複数のWidgetを使って作ったカスタムWidget」として読み込むための関数になります。  
そして、その作ったWidgetをGUI上に配置します。  
その配置をしているのが「setCentralWidget」です。  

![](https://gyazo.com/51ae38c79f85e05d1ab4dde0381daefe.png)  

今回のサンプルでは「QMainWindow」を継承したクラスで作成していますが  
このQMainWindowのWindow内は↑のようなレイアウトになっています。[詳しくは公式Help参照](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QMainWindow.html#detailed-description)  
なので、QtDesignerで作成したカスタムWidgetを  
この「CentralWidget」部分に配置します。  
  
### ボタンを押したときの動作を作成する  
  
PySideで「ボタンを押す」のようなGuiの動作に対して指定の処理を起こしたい場合には  
Signal-Slotと呼ばれる機能を使用します。  
詳細は次回説明します。  
  
```python
self.ui.pushButton.clicked.connect(self.click_btn)
```
QUiLoaderを使用してUIを読むときに「self.ui」にロードをしています。  
ので、この場合は「self.ui.####」という形で、Designerで作成したWidgetにアクセスをすることができます。  
  
![](https://gyazo.com/dd496d9e609e3b7b54e336a4df500e45.png)

この名前はどこで指定するかというと、  
QtDesignerの「プロパティエディタ」内の「QObject->objectName」で変更をします。  
シンプルな場合は問題ないかもですが、複雑なUIになると  
わかりにくくなってしまうので、名前は随時付けておくほうが良いです。  
  
「ボタンを押したとき」という動作をしたい場合は、  
self.ui.objectName.指定の動作.connect(実行したい関数名)  
のように記述をします。  
今回は「押したとき」なので clicked を使用します。

![](https://gyazo.com/9f60bf83b145f096d0d4fe9e23073756.png)

ボタンを押すと、こんな感じでclick_btn関数が呼ばれます。  
  
次は、このボタンを押したときの動作、  
PySideの「キモ」となるSignal-Slotについて説明します。  
