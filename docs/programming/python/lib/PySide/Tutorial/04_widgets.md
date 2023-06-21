---
slug: widgets
title: Widgetとカスタムウィジェットを作成する
tags:
    - PySide
    - Python
sidebar_position: 4
---

# Widget とカスタムウィジェットを作成する

前回サクッと QtDesigner を仕様して UI を作って見ましたが  
度々でてくる「Widget」というものがなにを指しているのか  
まずは改めて説明をしたいと思います。

## Widget

Widget とは、PySide の UI を構成するパーツの 1 単位です。

![](https://gyazo.com/2f2c60008cf42db6a861eb985f01669d.png)

QtDesigner の画面を見てみると、ウィンドウに配置するためのパーツは  
「ウィジェットボックス」に並べられています。  
この１つづつがいわゆる「Widget」で、ここにあるものは PySide がデフォルトで  
用意してくれている GUI のパーツになります。

![](https://gyazo.com/718b061f312f49173b0c6e8e9095156a.png)

PySide にある各種パーツはすべて「Widget」扱いになっていて  
Window も配置するための Layout も Button 等のパーツもすべて Widget です。

![](https://gyazo.com/2dcdbfb6dc6f467b99aca95a0b85c875.png)

それのなにが重要かというと  
すべての Widget は「QWidget」クラスを継承していて、この QWidget 内の関数を  
共通して使用することができるのです。

この QWidget は、すべての GUI のイベント（マウス、キーボード、その他諸々）を受け取って  
処理をする機能と、描画をする機能を持っています。  
なので、このクラスを継承している各 Widget は  
それぞれ固有の機能と描画を持たせて、配置することで GUI を構成するようになります。

## 親子化

Widget は親子化されて構成されています。

![](https://gyazo.com/728357bda05243652c41a71210b61c54.png)

どのように構成されているかは、オブジェクトインスペクタをみるとわかりやすいです。  
この例の場合 Window > Layout > LineEdit のように構成されているのがわかります。

親子化すると、Show/Hide 時はまとめて適応されたり、  
関数を使用して子の Widget をリストしたり、  
まとめて操作したりすることができます。

## Window

上記の通り、Widget は親子化されていますが  
一番親のルートに当たる Widget は「Window」と呼ばれます。

## カスタムウィジェット

![](https://gyazo.com/8cfc9cea59ae66ac125c61cb76b2b248.png)

PySide では、自分でカスタマイズした Widget を作成することができます。  
作成するのには、まずは QtDesigner の Widget から UI を作成します。

作成するのは、ファイルパスをセットするための Widget。  
このカスタム Widget は Label と LineEdit と ToolButton を並べただけです。

https://snippets.cacher.io/snippet/c916ee4236b639c38cee  
UI ファイルはこれ。  
コードは以下の通り。

<script src="https://embed.cacher.io/d65e3e855a3aab44adad16c60a7813f4795aae44.js?a=c1e5f1af51506fbd021ac66f46b04a85"></script>

カスタムウィジェットを作成すると、よく使う GUI パーツを使い回しできるようになります。

![](https://gyazo.com/a65ea06687163cec414b15af2048eb1c.png)

実行すると、このようになります。

![](https://gyazo.com/88cf995b3e7f139bbac47d40f48c82b1.png)

カスタムウィジェット単体では、このようになっています。

カスタムウィジェットを作成する場合は、QWidget クラスを継承したクラスを作成します。  
作成したら、そのクラス内で ui ファイルをロードし、Layout に配置します。  
あとは、ボタンを押したときの Signal-Slot を作成します。

最後に、作成したカスタムウィジェットを Window で作成して配置します。

今回のようなファイルをセットする UI などは  
どの UI でも使用するので、カスタムウィジェットとして共有化しておくと  
とても便利です。
