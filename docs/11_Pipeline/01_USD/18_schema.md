---
title: Schemaについて
tags:
    - USD
    - AdventCalendar2021
    - CEDEC2022
---

[Universal Scene Description](https://qiita.com/advent-calendar/2021/usd) 7 日目は、Schema(スキーマ)についてです。

## Schema とは

> USD defines a schema as an object whose purpose is to author and retrieve structured data from some UsdObject.
> 引用: https://graphics.pixar.com/usd/release/glossary.html#usdglossary-schema

とあるとおり、ある**UsdObject（Prim）に対して共通の機能・特性を指定するもの**です。

たとえば、UsdGeomMesh なら、この Prim には Mesh を作るのに必要な Property が定義されているから
表示するツールは Mesh として扱っていいよ
この UsdGeomXform なら、これはいわゆる TransformNode だからそのつもりで扱っていいよ
というような、各 Prim に対して役割（構造）を与えます。

当然、DCC ツールからデータを Export する時には、Prim に対しては Schema が定義されています。
そのため、Schema やその分類については意識しなくても大丈夫ですが、
Python 等で USD を操作しようとした場合はその限りではありません。

```python
stage.DefinePrim('/hogehoge')
```

たとえば、このように UsdStage から DefinePrim した場合。
構造化されていない野良データになります。

その場合、[ツールによっては Type の解釈がうまくいかなくて問題になったりする](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09#prim-%E3%81%AB%E3%81%AF%E5%9E%8B%E3%82%92%E3%81%A4%E3%81%91%E3%82%89%E3%82%8C%E3%82%8B)ので
Schema は定義するようにしましょう。

## Schema の種類

なんとなく Schema がどんなものか理解できてきたとおもいますが、
Schema と一言で言っても、様々な種類があります。

![](https://gyazo.com/dc0620ed573da2cdc339ca19d297bc35.png)

分類すると、このようになります。

多くの場合 **は Prim Schema と呼ばれる Prim に対して指定する Schema** ですが
この PrimSchema も、役割や対象によって細かくいくつかの種類に分かれます。
さらに理解を深めるために、分類について見ていきます。

### Prim Schema

PrimSchema は、その名の通り Prim に対して指定される Schema のことを指します。
多くの場合、Schema はこの PrimSchema です。

```python
# 野良Primを作った場合
stage.DefinePrim("/noraPrim")
```

最初に説明した通り、UsdStage から DefinePrim した場合は、Schema の定義されていない空の野良 Prim になります。
この Prim に対して Type（Prim Schema）を指定します。

作成するには、各 Schema のクラスの Define から Prim 作成を実行します。
すると、指定された Schema で Prim を定義することができます。

例として、Cube を作成したい場合。

```python
stage = Usd.Stage.CreateInMemory()
geom = UsdGeom.Cube.Define(stage,'/sample')
print(stage.ExportToString())
```

このように **UsdGeomCube**を **Define**すると、
Prim は指定した Schema の Prim(UsdGeomCube)になります。

![](https://gyazo.com/e601ec4885edbce8422ed314002dba99.png)

{{'450695a7cdbd2b32e88abcf21879e858'|gist}}

この CubeSchema を適応した Prim を作成すると、ほかになんの指定がなかったとしても
このような例のように、 **Prim に機能を与えるものが PrimSchema** です。

Xform なら[UsdGeomXform](https://graphics.pixar.com/usd/release/api/class_usd_geom_xform.html)、Mesh なら[UsdGeomMesh](https://graphics.pixar.com/usd/release/api/class_usd_geom_mesh.html)など、デフォルトでよく使われる機能は
デフォルトで用意されていますし、もちろん自分で定義することも可能ですが
そのあたりの詳細はまた別途書こうと思います。

> 多くの場合が PrimSchema と書きましたが、
> UsdGeomPrimvar UsdShadeInput は例外で、PropertySchema と呼ばれます。

## IsA Schema / API Schema

Prim Schema は、さらに２つに分類することができます。
それが、 IsA Schema と API Schema です。

### IsA

IsA とは、その名の通り **A は B です という = の関係になるような Schema**です。
別名を Typed Schema と呼びます。

例えば、「この Prim は Cube です」「この Prim は Mesh です」
のように、 Prim の定義を（この Prim は ### です）のように決めます。

つまりは、Maya の NodeType（mesh transform 等）のように Prim の Type を表すのがこの IsASchema になります。

#### API で扱う場合の分類

普通に扱う場合は IsA Schema がある　というのを理解していればよいですが、
Python や C++などで API を扱う場合は、この IsA Schema は２つに分けることができます。

それが、 **Abstract Schema** と **Concrete Schema** です。

たとえば、UsdGeomCube を例に見た場合、
UsdGeomCube は IsASchema です。

![](https://gyazo.com/13ff0894df322db5dc21f9701e8bc096.png)

この UsdGeomCube の Inheritance diagram を見てみると、 UsdGeomCube の親クラスに ～ able といった
クラスが存在しているのがわかります。

![](https://gyazo.com/6f4a941cbe77713488f47d60c1c73c90.png)

このような、～ able となっているクラスは、「abstract schema」と呼ばれるいわゆる基底クラスで
ある IsASchema に対して機能を追加するものになります。
たとえば Imageable ならレンダリングしたり、ビジュアライゼーションする必要がある Prim に対して指定されるものだし
Xformable なら、Transform できるようにする Prim に対して指定される...といった複数の Schema に対して共通する機能を
与えるためのクラスが、AbstractSchema です。

この AbstractSchema は、Prim を（インスタンスを）つくることができません。

対して、実際に **Prim を作成できるものを Concrete Schema** と呼び、

```python
geom = UsdGeom.Cube.Define(stage,'/sample')
```

このように、Stage に対して Define することができます。

## API Schema

API Schema は、IsA とは違いある一連のデータをオーサリングしたり抽出したりするためのインターフェースとして
機能する Prim Schema のことです。
APISchema は、 [IsA](https://ja.wikipedia.org/wiki/Is-a) に対して [HasA](https://ja.wikipedia.org/wiki/Has-a) Schema とも呼ばれます。

```python
stage = Usd.Stage.CreateInMemory()
geom = UsdGeom.Cube.Define(stage,'/sample')

xformAPI = UsdGeom.XformCommonAPI(geom.GetPrim())
xformAPI.SetTranslate([0,100,0])
```

シンプルな例として、スケール・回転・移動などのオーサリングや取得をすることができる XformCommonAP を
みてみます。
この API は、指定の Prim（ samplePrim ) に対して、Y 方向に 100 移動する処理を適応しています。

```python
stage = Usd.Stage.CreateInMemory()
rootLayer = stage.GetRootLayer()

# Mesh作成
sphere = UsdGeom.Sphere.Define(stage, '/test/sphere')

matPath = Sdf.Path("/Model/Material/MyMat")
mat = UsdShade.Material.Define(stage, matPath)

# ～もろもろ略～

# Bind
UsdShade.MaterialBindingAPI(sphere.GetPrim()).Bind(mat)
```

このほかに、 UsdShadeMaterialBindingAPI のように、ある Mesh に対して Material を Assign する
といったような操作のインターフェースも、この API Schema を使用します。

API Schema にも、大きく分けると non-applied single-apply multi-apply の３種類があります。

XformCommonAPI や、UsdShaderMaterial は Single-Apply APISchema です。
これはその名の通り１つの Prim に対して１つしか適応できないものだからです。
例えば１つの Mesh には複数のマテリアルはアサインできないし、
複数の Xform を適応することはできません。

### non-Applied

non-applied は、プロパティをセットするためなどに存在する API で、PrimType や定義には影響しないもののことを指します。
例として、 UsdModelAPI 等があり、[Kind の指定](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/11_kind_modelhierarchy/) などで、

```python
from pxr import Usd
api = Usd.ModelAPI(usdviewApi.prim)
api.SetKind('chargroup')
```

Prim に対して Kind を指定していますが、これはあくまでも決められた値をセットするためにあるもので
APISchema が適応されているわけではありません。

### Multi-Apply

最後の Multi-Apply は、ある Prim に対して複数適応することができる APISchema です。

MultiApply の APISchema の例としては、 UsdCollectionAPI があげられます。
詳細は、過去に [UsdCollection を使おう](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/14_usdCollection/)にまとめたのでそちらをみればわかるかと思いますが、
Collection は、１つの Prim に対して複数の Collection を適応することができます。（いわゆる Sets）

## まとめ

以上 USDSchema についてでした。

USD を扱っていると、デフォルト容易されている Schema だけではなかったり
不空数の Prim に対してなにかしらのオーサリングをするときについかの拡張をしたいケースが出てくると思います。
そうでなかったとしても、Python や C++から USD のシーングラフを扱う場合、
専用のカスタム Schema を定義したい場合などは、
この Schema の定義、Property 関連を理解しておくと公式の API ドキュメントがかなり理解しやすくなると思います。
