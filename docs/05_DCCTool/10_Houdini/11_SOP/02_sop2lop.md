---
title: SOPから無理やりデータを持ってくる
tags:
    - USD
    - AdventCalendar2022
    - SOP
description: 普通だと持ってこれないSOPのパラメーターをLOPに持ち込む方法
---

[USD AdventCalendar2022](https://qiita.com/advent-calendar/2022/usd) 9 日目は
{{markdown_link('01_importlop')}} で無理やり LOP から持ち込んだデータを
SOP で編集してから LOP 側に戻してみます。

![](https://gyazo.com/83384553e0fc63c5079fe9fa30ff638c.png)

前回は、Python を使用して USD のアトリビュートを、Prims の Attrib として
持ち込みをしてきました。
その時に、 : は \_\_ に置換しているので、そのあたりもカバーしつつ
返さなければいけません。

![](https://gyazo.com/c33e4cd9aa030276e6d00f71759a7b4e.png)

さらに、特殊な PrimitiveType だとそのまま戻すことはできないようなので
それを踏まえて対策をする必要があります。

ので、今回は Python を使用して SOP のデータを持ち込みつつ
USD の Prim として扱えるようにします。

![](https://gyazo.com/74011fb07504fb0f5be013c11ae4295b.png)

まずは、このように LayerBreak ノードを作成し、その次に PythonScript ノードを作ります。

この「LayerBreak」ノードは、
このノード以前のノードの Define をせずに
LayerBreak ノード以降の変更点のみを「Over」で出力します。

![](https://gyazo.com/7b891a806981807673edd700b0ea5ce9.png)

通常、LayerBreak がない場合は、Prim は「def」で定義されています。
def の場合は、現在のノードの上流に定義がなかった場合は作成するし
すでにある場合は上書きします。

![](https://gyazo.com/60ef9582d19d5a2499772438d7fd5b81.png)

対して LayerBreak がある場合は「Over」で出力されます。
この Over の場合、上流のノードに Prim がない場合は
合成されても Prim は作成されなくなります。

![](https://gyazo.com/f79b8a580b8ccce4ec4b370e66eff553.png)

つまりは、この SOP からデータを持ってくる差分だけの結果のレイヤーが作成されます。
こうすると、LOP 側の処理で Prim の Namespace が変化したり、削除したあとに
SOP での編集結果を合成した場合にも
削除した Prim は SOP での編集は無効扱いにできます。

で、次に Python ノードで SOP のデータを持ち込みます。

```python
node = hou.pwd()
stage = node.editableStage()

# Add code to modify the stage.
# Use drop down menu to select examples.

sop = hou.node('/stage/sopnet1/output0')
geo = sop.geometry()

for prim in geo.prims():
    usdPrim = stage.GetPrimAtPath(prim.attribValue('path'))
    for attr in geo.primAttribs():
        attrName = attr.name().replace("__",":")
        if usdPrim.HasAttribute(attrName):
            usdPrim.GetAttribute(attrName).Set(prim.attribValue(attr.name()))

```

方法はシンプルで、
SOP の output ノードのジオメトリを取得し
そこにあるアトリビュートを取得します。

アトリビュート名は \_\_ を : に置換して、USD 側の Prim に Attribute がある場合は
その Attribute に SOP の Geometry の Attrib の値をセットすることで
SOP のデータを持ち込みできます。

![](https://gyazo.com/5e61e9367e103483da2513b1340cc8fe.png)

試しに SOP 側の intensity を編集してみます。

```
@inputs__intensity = 100;
```

SOP の wrangle で値を変更してみます。

![](https://gyazo.com/cdf04a69ad937c5aa7fa6bfa794b657f.png)

LOP の Python ノードの結果をみてみると、 intensity = 100 に書き換えできました。

## メモ

データの行き来を Python を経由していて初めて知ったこととして

![](https://gyazo.com/5ba1c5e32ce2fe83aa1c458bb1657c20.png)

LOP 側の Python で SOP のジオメトリノードを取得した場合は、 read-only になります。
逆に、SOP 側で LOP の Stage を読む場合も read-only になります。
よく考えてみたら、たしかに別の世界からアクセスできてしまうと
大変面倒なことになりそうなので、それぞれ独立しているのは
まぁ当然だよな…と思いました。

![](https://gyazo.com/879b1bc452605b51813f2aaa02272e99.png)

今回は、特殊な方法で SOP がわの Geometry の attrib に持ち込んでしまったので
トリッキーな手段を取りましたが、
USD の Mesh を SOP 側に持って行って、その結果を取得したいのなら
![](https://gyazo.com/879b1bc452605b51813f2aaa02272e99.png)
SOPImport ノードという有能ノードがありますので、これを使えば問題ありません。
アトリビュート名の置換のようなことをしなければ SOPImport で事足ります。

これ以外に、去年のアドカレで
https://qiita.com/K240/items/d3d0fa8a632bc06cfda5
Scene Import LOP object translator plugin という手段もありましたので
こちらを使ってみるのもありかなぁと思いました。

## まとめ

かなりトリッキーな方法ですが、 hou.node で、SOP と LOP のノードを取得すれば
必要な値を SOP にまとめて送って、加工して戻すみたいなこともできるということがわかりました。

だいたいのことは Python を使えばできそうだな…というのはわかったものの
あまりやると Houdini らしさがなくなってしまうので
もうちょっと Houdini を勉強しつつ、より良い SOP-LOP の行き来を目指したいと思います。

今回のサンプルは [こちら](https://1drv.ms/u/s!AlUBmJYsMwMhhqU-12teloYHazoBxQ?e=fQse03)
