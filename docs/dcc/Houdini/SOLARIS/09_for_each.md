---
slug: /houdini/solaris/for_each
title: ForEachの使い方
description: ForEachの使い方を調べる
sidebar_position: 9
---

SOKARIS の ForEach ノードは、特定の Prim に対してや、指定の回数分、バリアントセットにたいして
その名の通り繰り返しを実行したい場合に使用するノードです。

![](https://gyazo.com/578a497b43c02f47189fd90e7a0f95f5.png)

![](https://gyazo.com/c3b82152842aa5369b2e47843af46f77.png)

ノードを作成すると、このように Begin/End ノードが作成されます。
このノードの間に追加されたノードを、End ノードでの指定した数だけ繰り返すようになります。

## 基本

### Prim の数だけ繰り返す

まずは基本として、シンプルなシーンを作ります。

![](https://gyazo.com/5f6e3d5ef18b1c01fb201e4163cf53c2.png)

シーンには A B C の 3 つの Prim があります。
この 3 つに対して何かを処理したい場合。

![](https://gyazo.com/c9d58ef8d76e1f5e8bec11e82030e95f.png)

ForEach で指定の数だけ Python で処理を実行します。

![](https://gyazo.com/398a89178ae783895dcac55adc4d856d.png)

ForEach の条件は End ノード側にあります。
指定が必要なのは Iteration Method、これはその名の通り何を対象に繰り返すのか。
今回は Input に接続されたノードの数だけ繰り返します。

Primitives は、IterationMethod で入力された Stage のうち、対象となる Prim を何にするかを指定します。 \*の場合は、無条件ですべての Prim に対して繰り返します。

```python
node = hou.pwd()
stage = node.editableStage()

print(hou.contextOption("ITERATIONVALUE"))
print(hou.contextOption("ITERATION"))
```

Python ノードの中身はこのようにします。
ForEach で繰り返しているときの何回目か、であったり、現在の PrimPath は ContextOption で取得できるので
hou.contextdOption を使用すれば Python ノード内で使用できます。

![](https://gyazo.com/c9ea75d7f1864938cd615ba54bc7c87a.png)

その結果がこちら。
すべてのノードの数だけ Python ノードを実行できました。

### 文字列分だけ繰り返す

Iteration Method には For Each String in Parameter があるので、Iterate OverStrings を指定することで  
strings の数だけ繰り返すような処理を作れます。

![](https://gyazo.com/941a60b2129736432dc7a0ee1a9d634d.png)

書き方は、スペースで区切ることで複数の文字列を指定できます。

![](https://gyazo.com/e7a12576a4854ada821661d356649069.png)

スペースが欲しい場合は ダブルクォートにすると、スペースアリの文字列も作ることができます。

### Variant

ある Prim の Varinat に対して処理をする場合も、ForEach ノードで指定できます。

![](https://gyazo.com/2afaaeba5b25e750895d1c4190c49fc3.png)

サンプルで KitchenSet の Cup を試してみます。  
子のアセットは、１つの Prim に対して複数の VarinatSet があります。

![](https://gyazo.com/dd665ba0a17ad22f33110421e47a98f1.png)

ForEach の IterationMethod には、Variant は「Variant」と「Variant Set」と似たようなものが 2 種類あります。
Variant Set というのは、shadingVariant や modelingVariant のような  
Prim に指定された VariantSet の数だけ繰り返します。  
Variant は、VariantSet 内にある選択肢の数だけ繰り返します。

![](https://gyazo.com/63be96b65ef91327598d561e5c99d88d.png)

なので、すべての Variant を繰り返したいのであれば、ForEach をネストさせます。

![](https://gyazo.com/27ff250e76042e1f170ab6d650bf678c.png)

繰り返し中の現在の値は contextOption に入ります。  
ネストする場合は、同じ名前だと上書きされてしまうので、Value Option Name を VARINAT_SET にして、

![](https://gyazo.com/ac6c52d5fc6377d5cd3226c78f03ce07.png)

内側の ForEach は、 For Each Variant in First Input にして、VariantSet を @VARIANT_SET にします。

![](https://gyazo.com/1bc15772a124ca614963d8e6b70cb1dc.png)

これで、すべての VariantSet の数だけループで実行できます。
