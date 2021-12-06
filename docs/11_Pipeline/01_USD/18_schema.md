---
title: Schemaについて
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description](https://qiita.com/advent-calendar/2021/usd) 7日目は、Schema(スキーマ)についてです。

## Schemaとは

> USD defines a schema as an object whose purpose is to author and retrieve structured data from some UsdObject. 
> 引用: https://graphics.pixar.com/usd/release/glossary.html#usdglossary-schema

とあるとおり、ある**UsdObject（Prim）に対して共通の機能・特性を指定するもの**です。

たとえば、UsdGeomMeshなら、このPrimにはMeshを作るのに必要なPropertyが定義されているから
表示するツールはMeshとして扱っていいよ
このUsdGeomXformなら、これはいわゆるTransformNodeだからそのつもりで扱っていいよ
というような、各Primに対して役割（構造）を与えます。

当然、DCCツールからデータをExportする時には、Primに対してはSchemaが定義されています。
そのため、Schemaやその分類については意識しなくても大丈夫ですが、
Python等でUSDを操作しようとした場合はその限りではありません。

```python
stage.DefinePrim('/hogehoge')
```

たとえば、このように UsdStageからDefinePrimした場合。
構造化されていない野良データになります。

その場合、[ツールによってはTypeの解釈がうまくいかなくて問題になったりする](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09#prim-%E3%81%AB%E3%81%AF%E5%9E%8B%E3%82%92%E3%81%A4%E3%81%91%E3%82%89%E3%82%8C%E3%82%8B)ので
Schemaは定義するようにしましょう。

## Schemaの種類

なんとなくSchemaがどんなものか理解できてきたとおもいますが、
Schemaと一言で言っても、様々な種類があります。

![](https://gyazo.com/dc0620ed573da2cdc339ca19d297bc35.png)

分類すると、このようになります。

多くの場合 **はPrim Schemaと呼ばれる Primに対して指定するSchema** ですが
このPrimSchemaも、役割や対象によって細かくいくつかの種類に分かれます。
さらに理解を深めるために、分類について見ていきます。

### Prim Schema

PrimSchemaは、その名の通りPrimに対して指定されるSchemaのことを指します。
多くの場合、SchemaはこのPrimSchemaです。

```python
# 野良Primを作った場合
stage.DefinePrim("/noraPrim")
```

最初に説明した通り、UsdStageからDefinePrimした場合は、Schemaの定義されていない空の野良Primになります。
このPrimに対してType（Prim Schema）を指定します。

作成するには、各SchemaのクラスのDefineからPrim作成を実行します。
すると、指定されたSchemaでPrimを定義することができます。

例として、Cubeを作成したい場合。

```python
stage = Usd.Stage.CreateInMemory()
geom = UsdGeom.Cube.Define(stage,'/sample')
print(stage.ExportToString())
```

このように **UsdGeomCube**を **Define**すると、
Primは指定したSchemaのPrim(UsdGeomCube)になります。

![](https://gyazo.com/e601ec4885edbce8422ed314002dba99.png)

{{'450695a7cdbd2b32e88abcf21879e858'|gist}}

このCubeSchemaを適応したPrimを作成すると、ほかになんの指定がなかったとしても
このような例のように、 **Primに機能を与えるものがPrimSchema** です。

Xformなら[UsdGeomXform](https://graphics.pixar.com/usd/release/api/class_usd_geom_xform.html)、Meshなら[UsdGeomMesh](https://graphics.pixar.com/usd/release/api/class_usd_geom_mesh.html)など、デフォルトでよく使われる機能は
デフォルトで用意されていますし、もちろん自分で定義することも可能ですが
そのあたりの詳細はまた別途書こうと思います。

> 多くの場合がPrimSchemaと書きましたが、
> UsdGeomPrimvar UsdShadeInput は例外で、PropertySchemaと呼ばれます。


## IsA Schema / API Schema

Prim Schemaは、さらに２つに分類することができます。
それが、 IsA Schema と API Schema です。

### IsA

IsA とは、その名の通り **AはBです という = の関係になるようなSchema**です。
別名を Typed Schemaと呼びます。

例えば、「このPrimはCubeです」「このPrimはMeshです」
のように、 Prim の定義を（このPrimは ### です）のように決めます。

つまりは、MayaのNodeType（mesh transform 等）のようにPrimのTypeを表すのがこのIsASchemaになります。

#### APIで扱う場合の分類

普通に扱う場合はIsA Schema がある　というのを理解していればよいですが、
PythonやC++などでAPIを扱う場合は、このIsA Schemaは２つに分けることができます。

それが、 **Abstract Schema** と **Concrete Schema** です。

たとえば、UsdGeomCubeを例に見た場合、
UsdGeomCubeはIsASchemaです。

![](https://gyazo.com/13ff0894df322db5dc21f9701e8bc096.png)

このUsdGeomCubeの Inheritance diagram を見てみると、 UsdGeomCube の親クラスに ～ableといった
クラスが存在しているのがわかります。

![](https://gyazo.com/6f4a941cbe77713488f47d60c1c73c90.png)

このような、～able となっているクラスは、「abstract schema」と呼ばれるいわゆる基底クラスで
あるIsASchemaに対して機能を追加するものになります。
たとえばImageableならレンダリングしたり、ビジュアライゼーションする必要があるPrimに対して指定されるものだし
Xformableなら、TransformできるようにするPrimに対して指定される...といった複数のSchemaに対して共通する機能を
与えるためのクラスが、AbstractSchemaです。

このAbstractSchemaは、Primを（インスタンスを）つくることができません。

対して、実際に **Primを作成できるものを Concrete Schema** と呼び、

```python
geom = UsdGeom.Cube.Define(stage,'/sample')
```

このように、Stageに対してDefineすることができます。


## API Schema

API Schema は、IsAとは違いある一連のデータをオーサリングしたり抽出したりするためのインターフェースとして
機能するPrim Schemaのことです。
APISchemaは、 [IsA](https://ja.wikipedia.org/wiki/Is-a) に対して [HasA](https://ja.wikipedia.org/wiki/Has-a) Schemaとも呼ばれます。

```python
stage = Usd.Stage.CreateInMemory()
geom = UsdGeom.Cube.Define(stage,'/sample')

xformAPI = UsdGeom.XformCommonAPI(geom.GetPrim())
xformAPI.SetTranslate([0,100,0])
```

シンプルな例として、スケール・回転・移動などのオーサリングや取得をすることができる XformCommonAPを
みてみます。
このAPIは、指定のPrim（ samplePrim ) に対して、Y方向に100移動する処理を適応しています。

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

このほかに、 UsdShadeMaterialBindingAPI のように、あるMeshに対してMaterialをAssignする
といったような操作のインターフェースも、このAPI Schemaを使用します。

API Schema にも、大きく分けると non-applied single-apply multi-apply の３種類があります。

XformCommonAPIや、UsdShaderMaterialは Single-Apply APISchemaです。
これはその名の通り１つのPrimに対して１つしか適応できないものだからです。
例えば１つのMeshには複数のマテリアルはアサインできないし、
複数のXformを適応することはできません。

### non-Applied

non-applied は、プロパティをセットするためなどに存在するAPIで、PrimTypeや定義には影響しないもののことを指します。
例として、 UsdModelAPI 等があり、[Kindの指定](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/11_kind_modelhierarchy/) などで、

```python
from pxr import Usd
api = Usd.ModelAPI(usdviewApi.prim)
api.SetKind('chargroup')
```
Primに対してKindを指定していますが、これはあくまでも決められた値をセットするためにあるもので
APISchemaが適応されているわけではありません。

### Multi-Apply

最後のMulti-Apply は、あるPrimに対して複数適応することができるAPISchemaです。

MultiApplyのAPISchemaの例としては、 UsdCollectionAPI があげられます。
詳細は、過去に [UsdCollectionを使おう](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/14_usdCollection/)にまとめたのでそちらをみればわかるかと思いますが、
Collectionは、１つのPrimに対して複数のCollectionを適応することができます。（いわゆるSets）



## まとめ

以上USDSchemaについてでした。

USDを扱っていると、デフォルト容易されているSchemaだけではなかったり
不空数のPrimに対してなにかしらのオーサリングをするときについかの拡張をしたいケースが出てくると思います。
そうでなかったとしても、PythonやC++からUSDのシーングラフを扱う場合、
専用のカスタムSchemaを定義したい場合などは、
このSchemaの定義、Property関連を理解しておくと公式のAPIドキュメントがかなり理解しやすくなると思います。