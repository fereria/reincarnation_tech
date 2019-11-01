---
title: PySideで単独アプリケーションを作る
---
# PySideで単独アプリケーションを作る

まずは、Mayaではなく単独のPySideのGUIツールを表示します。  

## インストールする

まず、PySideをインストールします。  
今回はPySide2、Pythonは3.6を使用します。

```bat
pip install pyside2
```

インストールするには、pipを使用します。  
（Anacondaやpipenvでも同様に「pyside2」をインストールすればOK）  

!!! info 
    PySideには、1と2がありますが  
    説明はPySide2準拠で説明します。  
    （Maya用に両方対応した書き方もありますが、それは別途解説します）
    

## 基本的な構造

![](https://gyazo.com/90d2467621845bcf23ca552174b0ed68.png)

<script src="https://embed.cacher.io/81523b875d61f812a8fe469b5f2413f32b0ef812.js?a=261ec51543734b7edb4beef13abbfb8f"></script>

まず、PySideでUIを作成するには、  
このサンプルのような基本構造を作成します。  

### Applicationの作成

まず、PySideでUIを作る場合は「[QApplication](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QApplication.html)」を作成します。  

![](https://gyazo.com/d0ad62876373374abd8f3eaafd35676d.png)

PySideは、ざっくりと分けるとApplicationとウィンドウ部分（QtWidgets）の2つで  
構成されていて、  
PySideでアプリを作る場合は、まずApplicationを作成し  
そのアプリ上で表示したいウィンドウを作成します。  
  
今回のサンプルは、Applicationを作成し  
QDialogというシンプルなウィンドウを継承したクラスを作成し、  
表示をしています。  
  
この構造が、PySideの最も基本的な形で  
この構造に対していろいろなパーツ（Widget）を乗せていくことで  
UIを作成していきます。  
  
!!! info
    解説的にはクラス継承しないで作成しているものもありますが  
    継承してから作った方が後々わかりやすいので  
    今回は、継承して使う前提で解説します。