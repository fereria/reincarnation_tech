---
title: Specifier
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 19 日目は、
USD の Specifier についてです。

## Specifier とは？

Specifier とは、PrimSpec に対して指定されるメタデータで
PrimSpec がどのようにコンポジションされて、どのように解釈されるのか指定するものです。

{{markdown_link('21_stage_layer_spec')}}

USD は、レイヤーに書かれている「Spec」と呼ばれる主張をコンポジションすることで
最終的案ステージを構築します。
このコンポジションをするときに、各レイヤーに記述された PrimSpec を
どのように解釈して最終的な Prim にするか
Specifier によってコントロールすることができます。

この Specifier には３種類あります。

-   def
-   over
-   class

この３つを詳しく見ていきます。

## def

def は、Prim を定義するもので
多くの場合 PrimSpec は「def」で定義されます。

```python
from pxr import Usd

stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim('/sample')
```

{{'271af5c1a8117467d67d55ae319fb053'|gist}}

レイヤーに def で定義された PrimSpec は、

![](https://gyazo.com/8ed673ef78f9aa9096fd4dd7ba5a84de.png)

最終的にこのように Prim として作成されます。

## over

次が over
over は、def とは違い over があるだけでは Prim は作成されず
コンポジションによってある Prim を編集したい場合に、「上書き」をすることを目的にした
PrimSpec を作成します。

```python
stage = Usd.Stage.CreateInMemory()
prim = stage.OverridePrim('/sample')
```

{{'3ae2ea2525ac8870919123639718ed54'|gist}}

例として、このような over だけが定義されているレイヤーを作成します。

![](https://gyazo.com/f7510c34ff94e17eff21d627ac939718.png)

作成後、usdview で確認しても、Prim はありません。
over は、すでに def Prim がある場合に Prim の値を上書きするので、
over だけの場合、Stage には Prim はありません。

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
別のレイヤーで def によって PrimSpec がある場合、over で定義された値はオーバーライドされます。

{{'2c3281d4f4082a38e8039aacec1ddbc2'|gist}}

{{'fb1465dfe54ff56a34d0c7d76a9c973a'|gist}}

![](https://gyazo.com/c220e9d71d4a02bf49c10497aefe6ed7.png)

base.usda に sample Prim が Define されているので
サブレイヤーされたレイヤー側に「over」を記述することで
over に定義されている value = True が、合成されます。

Stage で開いて、現在の TargetLayer に対して編集した場合、
自分より強い主張が別レイヤーに存在する場合は、 over 扱いになります。
これがどういうことかというと
例えば自分より強いレイヤーの def Prim が削除された場合
over だった場合は、 over Prim は適応されず Prim が削除されます。
対して、over ではなく 編集時も def の場合、強いレイヤーの def Prim が削除されても
Prim は削除されず、Stage には残ります。

これはとても重要なことで、
例えば レイアウトで配置したあるモデルに対して 次の工程の作業者がマテリアルの調整を
したとします。
しかし、そのモデルが削除された場合
マテリアルの編集は「なかったこと」になってほしいはずです。
def で編集されていた場合は、上流工程で削除されていても Prim は残り続けます。

Specifier は、Prim が最終的にどのように解釈されて解決されるのか。
コンポジションの順序なども重要ですが、 Prim がどの Specifier を持つかによって
最終的に解決される Stage も変わってくるというのには注意が必要です。
（とはいえ、多くのツールは良しなに計らってくれるし、PythonAPI もそこまで意識しないでも大丈夫ではある）

## class

最後に class
class はプラグラミングにおけるクラスと同じで、ある別の Prim に Inherits（継承）するための
Prim を定義するために使用します。

```python
stage = Usd.Stage.CreateInMemory()
layer = stage.GetRootLayer()
cls = stage.CreateClassPrim('/__class__')
```

{{'9c53e934655105717136cbabcf4328bb'|gist}}

例えば、このように \_\_class\_\_ を class で定義します。
これを usdview で確認した場合は、 over と同様に Prim はありません。

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

しかし、この class Prim は Inherits することで、別の Prim に継承することができます。

継承については別途 {{markdown_link('07_comp_arc_inherits','こちらで解説')}} していますので、そちらを参照してください。

def を Inherits することも可能ですが、
class として定義するのはあくまで「共通定義」であることが多く（例：共通のライト、マテリアル等）
そういった共通パラメーターは Traverse や GetChildren で検索には入ってほしくありません。
（over も同様）

そういった場合に、 class で定義することで Inherits するための 定義用 Prim を
作成することができます。

## まとめ

以上 Specifier についてでした。
Stage/Layer/Spec の回で「Spec」について解説しましたが、この Specifier は PrimSpec から
Prim に、Stage に構築する際に「最終的にどのような Prim になるか」解釈するのに重要な要素になりますので
Stage の記事と合わせて、Specifier についても理解できると
より USD のコンポジションを理解できるのではないかと思います。
