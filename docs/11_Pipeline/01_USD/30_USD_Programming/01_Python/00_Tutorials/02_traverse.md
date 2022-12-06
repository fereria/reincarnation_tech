---
title: 0から始めるUSDPython(2) ステージを検索しよう
tags:
    - USD
    - USDPythonTutorial
    - AdventCalendar2022
description:
---

[前回](01_start_usdpython) で USD を Python で開いて、指定の Prim の Attribute を編集して
保存するという処理を書いてみましたが
多くの場合、Prim を固定パスで取得して何か編集する…というよりも、
ステージに含まれる特定の条件の Prim にたいしてなにか処理をすることのほうが多いと思います。

今回は、
**USD のステージを検索（Traverse）して条件にマッチした Prim に対して処理を実行する**
ようにしてみます。

## 全ノード検索

UsdStage には、現在のステージにある Prim すべてを取得できるイテレーターが用意されていますので
自前で再帰処理を書かなくても簡単に書けます。
それが [UsdStage の TraverseAll()](https://graphics.pixar.com/usd/dev/api/class_usd_stage.html#a71559921b1e48949207817b2fd8bd01b) です。
ので、まず前回も使用した Kitchen_set.usd を使用して
すべてのノードをプリントしてみます。

```python
from pxr import  Usd

stage = Usd.Stage.Open("D:/Kitchen_set/Kitchen_set.usd")

for prim in stage.TraverseAll():
    print(prim)
```

![](https://gyazo.com/bb1e117e09a3d2afbe81d9b7f59277c6.png)

実行すると、このようにシーンに含まれる Prim が大量にプリントされるかと思います。

### Attribute の値が条件に合致している場合に何かしたい

これだと、ただ全 Prim を for で繰り返ししているだけでなにもしていないので
ここで前回非表示にしたノードを print するようにしてみます。

```python
# シーンにあるPrimの数だけ繰り返す
for prim in stage.TraverseAll():
    if prim.GetAttribute('visibility').Get() == 'invisible':
        print(prim)
```

Attribute に値をセットするときは .Set(Value) としていましたが、
Get() すると、Attribute の値を取得できます。
ので、非表示の場合（ visibility が invisible の Attribute の Prim を取得する場合は
上のように if 文を書けば、指定の Prim にだけ処理をするというのが
書けるようになります。

では、処理をしたい Prim が if 文を使用することで取得することができたので、
非表示にした Attribute を表示して、上書き保存してみます。

```python
from pxr import  Usd

stage = Usd.Stage.Open("D:/Kitchen_set/Kitchen_set.usd")

for prim in stage.TraverseAll():
    if prim.GetAttribute('visibility').Get() == 'invisible':
        prim.GetAttribute("visibility").Set("inherited")

stage.GetRootLayer().Save()
```

値を変更するときは、GetAttribute(AttributeName).Set(Value) とすればよいので
致した Prim に対して値をセットするにはこのように書けば OK です。

### 指定の Type に対して処理をしたい

条件は、これ以外にもいろいろと作ることができます。
ので、別の例で「指定の Prim のタイプ（スキーマ）のみ処理をする」というのを
書いてみます。

![](https://gyazo.com/5ec584cdd6c95b1b78c66fde75edcdd0.png)

USD の Prim には、「スキーマ」と呼ばれる型が定義されています。
これは、いわゆる Maya のノードタイプ（Mesh や Transform 等）のように
この Prim がどのようにふるまうのかを定義するものです。

![](https://gyazo.com/b46318a1ecdd6a1d97850154beb53b29.png)

サンプルの Kitchen_set のカップのモデルは、Mesh だったり
移動をするための Group は Xform だったり、

![](https://gyazo.com/cd27ed63643acc747eb793b66bbfee2e.png)

ライトだと、 DistantLight SphereLight DiskLight のように
3DCG で使用する各種データごとにこの Prim が指定されています。

なので、たとえば「シーンにある SphereLight に対して何かをしたい、値を取得したい」
だったり、「シーンにある Mesh に対してなにかしたい」のように
型ごとに処理を分けたい場合はこの Type を使用すればできます。

今回は、Kitchen_set に含まれる Mesh Prim に対して実行したい場合を書いてみます。

```python
for prim in stage.TraverseAll():
    if prim.GetTypeName() == "Mesh":
        #何かしらの処理
        pass
```

prim がどのスキーマを使用しているのかは、 [UsdPrim.GetTypeName()](https://graphics.pixar.com/usd/dev/api/class_usd_prim.html#a8cc8a084710338ce2de6eeba7872c194)で取得できます。
基本は Attribute で条件を指定していたところを GetTypeName を実行したい Type で
条件指定するのに変えただけです。

## まとめ

これで、Path を固定することなく USD のステージ上に含まれる「何かしらの条件」にだけ
実行するといった処理が書けるようになりました。

複雑な条件だと、多少工夫する必要はありますが（特定のマテリアルにアサインされている Mesh だけ等）
基本はこの for prim in stage.TraverseAll() を使用することで
USD のステージにある特定の Prim（ノード）に何かをするということが書けるようになります。

今回紹介した GetAttribute や GetTypeName 以外にも
たとえば、指定の Attribute がある場合なら ( [UsdPrim.HasAttribute()](https://graphics.pixar.com/usd/dev/api/class_usd_prim.html#a6092b2a26c8f94cf68eb77e45bd1f8d5) ) バリアントセットが指定されている場合 ( [UsdPrim.HasVariantSets()](https://graphics.pixar.com/usd/dev/api/class_usd_prim.html#a87443b32a72f95ca96d960b4e96cbf02) )のように
UsdPrim のドキュメントをを見ると、ほかの条件でも検索を書けると思うので
試しに別の条件で Prim を検索を試してみると良いかもしれません。

次回、Prim 作成編に続く。
