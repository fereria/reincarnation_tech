---
title: Specifier
tags:
    - USD
    - AdventCalendar2021
---


[Universal Scene Description AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 19日目は、
USDの Specifier についてです。

## Specifierとは？

Specifierとは、PrimSpecに対して指定されるメタデータで
PrimSpecがどのようにコンポジションされて、どのように解釈されるのか指定するものです。

https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/21_stage_layer_spec/

USDは、レイヤーに書かれている「Spec」と呼ばれる主張をコンポジションすることで
最終的案ステージを構築します。
このコンポジションをするときに、各レイヤーに記述されたPrimSpecを
どのように解釈して最終的なPrimにするか
Specifierによってコントロールすることができます。

このSpecifierには３種類あります。

* def
* over
* class

この３つを詳しく見ていきます。

## def

defは、Primを定義するもので
多くの場合PrimSpecは「def」で定義されます。

```python
from pxr import Usd

stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim('/sample')
```

{{'271af5c1a8117467d67d55ae319fb053'|gist}}

レイヤーに def で定義された PrimSpecは、

![](https://gyazo.com/8ed673ef78f9aa9096fd4dd7ba5a84de.png)

最終的にこのようにPrimとして作成されます。

## over

次が over
overは、defとは違い over があるだけではPrimは作成されず
コンポジションによってあるPrimを編集したい場合に、「上書き」をすることを目的にした
PrimSpecを作成します。

```python
stage = Usd.Stage.CreateInMemory()
prim = stage.OverridePrim('/sample')
```

{{'3ae2ea2525ac8870919123639718ed54'|gist}}

例として、このような overだけが定義されているレイヤーを作成します。

![](https://gyazo.com/f7510c34ff94e17eff21d627ac939718.png)

作成後、usdviewで確認しても、Primはありません。
over は、すでに def Prim がある場合に Primの値を上書きするので、
overだけの場合、StageにはPrimはありません。

```python
# ベースのレイヤーを作成
base = Usd.Stage.CreateInMemory()
defprim = base.DefinePrim("/sample")
defprim.CreateAttribute('value',Sdf.ValueTypeNames.Bool).Set(False)
base.Export("D:/base.usda")

# ベースのレイヤーをサブレイヤーで合成
stage = Usd.Stage.CreateInMemory()
layer = stage.GetRootLayer()
layer.subLayerPaths = ['D:/base.usda']
prim = stage.OverridePrim('/sample')
primB = stage.OverridePrim('/sampleB')
prim.GetAttribute('value').Set(True)

layer.Export("D:/sample.usda")
```

では、以下のようにサブレイヤーを使用して
別のレイヤーで def によってPrimSpecがある場合、over で定義された値はオーバーライドされます。

{{'2c3281d4f4082a38e8039aacec1ddbc2'|gist}}

{{'fb1465dfe54ff56a34d0c7d76a9c973a'|gist}}

![](https://gyazo.com/c220e9d71d4a02bf49c10497aefe6ed7.png)

base.usda に sample Prim がDefineされているので
サブレイヤーされたレイヤー側に「over」を記述することで
over に定義されている value = True が、合成されます。

Stageで開いて、現在のTargetLayerに対して編集した場合、
自分より強い主張が別レイヤーに存在する場合は、 over 扱いになります。
これがどういうことかというと
例えば自分より強いレイヤーの def Prim が削除された場合
overだった場合は、 over Primは適応されず Primが削除されます。
対して、over ではなく 編集時も def の場合、強いレイヤーの def Primが削除されても
Primは削除されず、Stageには残ります。

これはとても重要なことで、
例えば レイアウトで配置したあるモデルに対して 次の工程の作業者がマテリアルの調整を
したとします。
しかし、そのモデルが削除された場合
マテリアルの編集は「なかったこと」になってほしいはずです。
defで編集されていた場合は、上流工程で削除されていてもPrimは残り続けます。

Specifierは、Primが最終的にどのように解釈されて解決されるのか。
コンポジションの順序なども重要ですが、 PrimがどのSpecifier を持つかによって
最終的に解決されるStageも変わってくるというのには注意が必要です。
（とはいえ、多くのツールは良しなに計らってくれるし、PythonAPIもそこまで意識しないでも大丈夫ではある）

## class

最後に class
classはプラグラミングにおけるクラスと同じで、ある別のPrimにInherits（継承）するための
Primを定義するために使用します。

```python
stage = Usd.Stage.CreateInMemory()
layer = stage.GetRootLayer()
cls = stage.CreateClassPrim('/__class__')
```

{{'9c53e934655105717136cbabcf4328bb'|gist}}

例えば、このように \_\_class\_\_  を class で定義します。
これを usdview で確認した場合は、 over と同様にPrimはありません。

![](https://gyazo.com/760d9d3b799fe03899497e40517cb20d.png)

```python
stage = Usd.Stage.CreateInMemory()
layer = stage.GetRootLayer()
cls = stage.CreateClassPrim('/__class__')
cls.CreateAttribute('value',Sdf.ValueTypeNames.Bool).Set(False)

prim = stage.DefinePrim("/sample")
prim.GetInherits().AddInherit(cls.GetPath())
```

![](https://gyazo.com/e76cb1d44cfb2b88f875d54e1e8d3528.png)

![](https://gyazo.com/cb17fd7aaa327714952f2d16c42cdc58.png)

しかし、この class Primは Inherits することで、別のPrimに継承することができます。

継承については別途[こちらで解説](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/07_comp_arc_inherits/)していますので、そちらを参照してください。

def を Inherits することも可能ですが、
class として定義するのはあくまで「共通定義」であることが多く（例：共通のライト、マテリアル等）
そういった共通パラメーターは Traverse や GetChildren で検索には入ってほしくありません。
（overも同様）

そういった場合に、 class で定義することでInheritsするための 定義用Primを
作成することができます。

## まとめ

以上 Specifier についてでした。
Stage/Layer/Spec の回で「Spec」について解説しましたが、このSpecifierはPrimSpecから
Primに、Stageに構築する際に「最終的にどのようなPrimになるか」解釈するのに重要な要素になりますので
Stageの記事と合わせて、Specifierについても理解できると
よりUSDのコンポジションを理解できるのではないかと思います。