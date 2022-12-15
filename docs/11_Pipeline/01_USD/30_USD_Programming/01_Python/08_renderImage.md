---
title: RenderImageでUSDをレンダリングしよう
tags:
    - USD
description:
---

USD には、 UsdAppUtils と呼ばれる
USD の画像を表示したり記録するためのユーティリティを持つ機能をもつクラスが
用意されています。

これを利用すると、Python を利用して USD のシーンをレンダリングすることができます。

今回は、この機能を使用してレンダリングをしてみます。

## 準備

まず Python 環境を準備する必要がありますが、この時に注意が必要なのが
UsdAppUtils は pip install でインストール可能な usd-core には含まれていないため
この機能を使用したい場合は自前でビルドして置く必要があります。

ので、 {{markdown_link('00_install_USD')}} このあたりを参考に、USD をビルドしておいたうえで
Path を通しておきます。

### サンプルシーンを作る

次に、サンプル用のシーンを用意します。

![](https://gyazo.com/199d8d99ed0353787c83e98f961789ff.png)

今回はシンプルに、Cube とカメラだけあるようなシーンをあらかじめ Houdini で用意しておきます。

![](https://gyazo.com/4de5cc8814633291d6077f331c18c18e.png)

こんな感じのカメラを作りました。
これを保存しておきます。

## レンダリングしてみる

準備ができたら、Python でコードを書いていきます。

```python
from pxr import UsdAppUtils,Usd

from PySide2 import QtOpenGL
from PySide2.QtWidgets import QApplication
```

必要になるのが、UsdAppUtils と Usd
あとは、OpenGL で描画するためのビューポートを用意するために PySide をインポートします。

```python
stage = Usd.Stage.Open("D:/sample/cube.usd")
usdCamera = UsdAppUtils.GetCameraAtPath(stage,"/sampleCamera")
```

次に、レンダリングしたいステージを開き、そのステージ内にあるレンダリング用のカメラ Prim を取得しておきます。

```python
application = QApplication()

glFormat = QtOpenGL.QGLFormat()
glFormat.setSampleBuffers(True)
glFormat.setSamples(4)
glWidget = QtOpenGL.QGLWidget(glFormat)
glWidget.setFixedSize(640,480)
glWidget.makeCurrent()
```

そして、描画用の OpenGLQGlWidget を作ります。

```python
frameRecorder = UsdAppUtils.FrameRecorder()
frameRecorder.SetImageWidth(640)
```

画像を出力するのに使うのが「FrameRecorder」クラスです。
これはその名前の通り、指定のフレームを指定のカメラで記録して、画像に出力できます。

```python
frameRecorder.Record(stage, usdCamera, 0, "./sample.jpg")
```

使い方は簡単で、Record 関数に、ステージ、カメラ、フレーム数、保存先を渡すと
指定場所に画像を出力してくれます。

![](https://gyazo.com/2be0a2dd7985051d5dde23f1b405035e.png)

結果はこちら。
無事画像を出力できました。

今回はデフォルトのStormでレンダリングしていますが、
RenderDelegateに対応したレンダラーであれば、同様の方法でレンダリングが可能（なはず）です。
pxr/usdImaging/bin/usdrecord/usdrecord.py 
サンプルとして、USDのリポジトリ以下の usdrecord.py のソースコードを見ると
どのように実装されているか詳しく理解することができます。

## JupyterNotebook での応用

画像が出力できたので、これを利用してJupyterNotebookでレンダリング結果を
表示したくなります。

やり方は簡単で、

```python
from IPython.display import Image
Image("./sample.jpg")
```

IPython.display にあるImageで、Recordで保存しておいた画像を指定すればOKです。

![](https://gyazo.com/dda2a138570b51b4d7fd3a5140991826.png)

結果。

これを利用すれば、Pythonでいろいろ操作して、その結果を簡単にNotebookで
確認するといったことも可能になります。
