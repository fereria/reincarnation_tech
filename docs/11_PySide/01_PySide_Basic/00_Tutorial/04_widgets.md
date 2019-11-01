---
title: Widgetとカスタムウィジェットを作成する 
---
# Widgetとカスタムウィジェットを作成する

前回サクッとQtDesignerを仕様してUIを作って見ましたが  
度々でてくる「Widget」というものがなにを指しているのか  
まずは改めて説明をしたいと思います。  
  
## Widget

Widgetとは、PySideのUIを構成するパーツの1単位です。  

![](https://gyazo.com/2f2c60008cf42db6a861eb985f01669d.png)

QtDesignerの画面を見てみると、ウィンドウに配置するためのパーツは  
「ウィジェットボックス」に並べられています。  
この１つづつがいわゆる「Widget」で、ここにあるものはPySideがデフォルトで  
用意してくれているGUIのパーツになります。  
  
![](https://gyazo.com/718b061f312f49173b0c6e8e9095156a.png)

PySideにある各種パーツはすべて「Widget」扱いになっていて  
Windowも配置するためのLayoutもButton等のパーツもすべてWidgetです。  

![](https://gyazo.com/2dcdbfb6dc6f467b99aca95a0b85c875.png)

それのなにが重要かというと  
すべてのWidgetは「QWidget」クラスを継承していて、このQWidget内の関数を  
共通して使用することができるのです。  
  
このQWidgetは、すべてのGUIのイベント（マウス、キーボード、その他諸々）を受け取って  
処理をする機能と、描画をする機能を持っています。  
なので、このクラスを継承している各Widgetは  
それぞれ固有の機能と描画を持たせて、配置することでGUIを構成するようになります。  

## 親子化

Widgetは親子化されて構成されています。
  
![](https://gyazo.com/728357bda05243652c41a71210b61c54.png)
  
どのように構成されているかは、オブジェクトインスペクタをみるとわかりやすいです。  
この例の場合 Window > Layout > LineEdit のように構成されているのがわかります。  
  
親子化すると、Show/Hide時はまとめて適応されたり、  
関数を使用して子のWidgetをリストしたり、  
まとめて操作したりすることができます。

## Window

上記の通り、Widgetは親子化されていますが  
一番親のルートに当たるWidgetは「Window」と呼ばれます。

## カスタムウィジェット  
  
![](https://gyazo.com/8cfc9cea59ae66ac125c61cb76b2b248.png)

PySideでは、自分でカスタマイズしたWidgetを作成することができます。  
作成するのには、まずは QtDesignerのWidgetからUIを作成します。  

作成するのは、ファイルパスをセットするためのWidget。  
このカスタムWidgetはLabelとLineEditとToolButtonを並べただけです。
  

https://snippets.cacher.io/snippet/c916ee4236b639c38cee  
UIファイルはこれ。  
コードは以下の通り。

<script src="https://embed.cacher.io/d65e3e855a3aab44adad16c60a7813f4795aae44.js?a=c1e5f1af51506fbd021ac66f46b04a85"></script>
  
カスタムウィジェットを作成すると、よく使うGUIパーツを使い回しできるようになります。  

![](https://gyazo.com/a65ea06687163cec414b15af2048eb1c.png)

実行すると、このようになります。  

![](https://gyazo.com/88cf995b3e7f139bbac47d40f48c82b1.png)

カスタムウィジェット単体では、このようになっています。  
  
カスタムウィジェットを作成する場合は、QWidgetクラスを継承したクラスを作成します。  
作成したら、そのクラス内でuiファイルをロードし、Layoutに配置します。  
あとは、ボタンを押したときのSignal-Slotを作成します。  
  
最後に、作成したカスタムウィジェットをWindowで作成して配置します。  
  
今回のようなファイルをセットするUIなどは  
どのUIでも使用するので、カスタムウィジェットとして共有化しておくと  
とても便利です。  