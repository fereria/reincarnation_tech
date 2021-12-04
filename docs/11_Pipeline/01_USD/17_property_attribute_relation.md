---
title: Property/Attribute/Relationship
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description](https://qiita.com/advent-calendar/2021/usd) 3日目。
今回は、今までしっかり説明指定していなかった、USDの「Propertyの基本」について説明していこうと思います。

## Propertyとは

USDのPropertyとは、

> Properties are the other kind of namespace object in USD (Prims being the first).
> 引用: https://graphics.pixar.com/usd/release/glossary.html#usdglossary-property

とあるとおり、USDのネームスペースを構成する一種で、Primに指定される実データをを含む値のことです。
（MayaでいうところのAttribute）

USDのPropertyは、 **「Attribute」** と **「Relationship」** の種類があります。

### Attribute

AttributeはいわゆるMayaのAttributeのように、
Primに定義された「TimeSampleすること」「コンポジションアークによって合成」ができるパラメーターです。
[昨日のこちらの記事のアトリビュートについて](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09) でも触れられていましたが、
一般的に、3Dで使われる型など[DataType](https://graphics.pixar.com/usd/release/api/_usd__page__datatypes.html)で指定されたものが使用できます。

jsonやtoml、yaml、xmlといったフォーマットとは違い、Attributeに対しては必ず型指定必用なのが特徴です。

```python
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim('/samplePrim')
attr = prim.CreateAttribute('sampleValuer',Sdf.ValueTypeNames.Bool).Set(True)
print(stage.ExportToString())
```

```
#usda 1.0
(
    doc = """Generated from Composed Stage of root layer 
"""
)

def "samplePrim"
{
    custom bool sampleValuer = 1
}
```

シンプルなPrimを作成して、Attributeを追加・指定した例。
CreateAttributeで指定した型でAttributeが追加されていることがわかります。

> 余談ですが、このAttributeの型指定は、Pythonから指定する場合公式のDataTypesページのどこにも書かれていないという罠があります。
> https://fereria.github.io/reincarnation_tech/11_Pipeline/10_USDTips/01_usd_py_docs/#usdattributetype
> そんなトラップを回避するために、過去頑張って調べた一覧がこちら。
> PythonとC++（Help記載の内容）だと違うという罠がごくまれにあるのがUSDの悲しいところ。

#### TimeSamplingとInterpolation

USDのAttributeでは、TimeCodeを指定することで、TimeSampling　いわゆるアニメーションを
させることができます。
以下、シンプルなAttributeを作成して、動作を確認してみます。

```python
stage = Usd.Stage.CreateInMemory()

prim = stage.DefinePrim('/samplePrim')
attr = prim.CreateAttribute('intValue',Sdf.ValueTypeNames.Float)
attr.Set(0,0)
attr.Set(10,10)
print(stage.ExportToString())
```
```
#usda 1.0
(
    doc = """Generated from Composed Stage of root layer 
"""
)

def "samplePrim"
{
    custom float intValue
    float intValue.timeSamples = {
        0: 0,
        10: 10,
    }
}
```
Setするときに、 Set(\<Value\>,\<Timecode\>) とすることで、Attributeに対してキーを追加できました。
この状態で、

```python
print(attr.Get(5))
```
> 5.0


.Get(\<TimeCode\>) とすると、指定のTimeCodeの値を取得することができます。
GetしているのはKeyを打っていない5フレーム目ですが、0フレーム目と10フレーム目のちょうど中間
TimeCodeとTimeCodeの間が補間された値が取得されました。

AttributeのTimeSampleは、UsdStageのSetInterpolationTypeで指定することができます。
サポートされているのは Held と Linear の２つ。

デフォルトは Linearで、TimeCodeとTimeCodeの間をリニアに保管します。
Heldの場合は、MayaでいうところのStepTangentで、次のTimeCodeまでAttributeの値を一定に保ちます。

```python
stage.SetInterpolationType(Usd.InterpolationTypeHeld) # デフォルトは、UsdInterpolationTypeLinear 
prim = stage.DefinePrim('/samplePrim')
attr = prim.CreateAttribute('intValue',Sdf.ValueTypeNames.Float)
attr.Set(0,0)
attr.Set(10,10)

print(attr.Get(5))
```
> 0.0

Holdに変えた場合の結果、補間されず直前の値が取得されました。

#### CustomAttribute

最後にCustomAttributeについて。
空のPrimに対して CreateAttributeをした場合、ExpotToStringをしてみると、Attributeの前に「custom」
が付いていることがわかります。
この custom がなにかというと、
その名の通りそのAttributeがSchemaによって定義されたものかユーザーによって定義されたものかどうか区別するためのものです。

まず、Schemaによって定義されたものとはどういうものかというと、
以下のKitchen_setにあるBall.usdで見てみます。

![](https://gyazo.com/786954f7a9dfca11223458c9759c3413.png)

BallにあるMeshPrimは、UsdGeomMeshスキーマが指定されたPrimです。
USDのソースコード以下 USD/pxr/usd/usdGeom/generatedSchema.usda を読み進めると、Meshスキーマの classがあり
その中に、Meshスキーマに定義されたAttributeがあります。
これが、スキーマによって定義されているAttributeで たとえレイヤーにAttributeの記述がなかったとしても
スキーマで定義された値がフォールバック値として設定されます。

![](https://gyazo.com/2c3347b7c11c5c69fa8499f34513a294.png)

例として、 doubleSided。
Ball.usd内には doubleSided Attributeに値をセットする記述はありませんが、usdviewを見ると
セットされていることがわかります。

```
stage = Usd.Stage.CreateInMemory()
layer = stage.GetRootLayer()
layer.subLayerPaths = [r"D:\Kitchen_set\assets\Ball\Ball.usd"]

prim = stage.GetPrimAtPath('/Ball/Geom/Ball')
prim.GetAttribute('doubleSided').Set(True)

prim.CreateAttribute('sample',Sdf.ValueTypeNames.Int).Set(0)

print(layer.ExportToString())
```
```
#usda 1.0
(
    subLayers = [
        @D:\Kitchen_set\assets\Ball\Ball.usd@
    ]
)

over "Ball"
{
    over "Geom"
    {
        over "Ball"
        {
            uniform bool doubleSided = 1
            custom int sample = 0
        }
    }
}
```

このようなAttributeに値をSetした場合は custom にはなりません。

```python
prim.GetAttribute('doubleSided').IsCustom()
```
> False

IsCustomで確認しても、Falseになります。

```python
prim.GetAttribute('sample').IsCustom()
```
> True

対する、スキーマにはないAttributeの場合は
customが追加され、 IsCustomで確認してもTrueになります。

### Relationship

Relationshipとは、その名の通り、あるPrimへの「リレーション」を持つプロパティのことです。

```python
stage = Usd.Stage.CreateInMemory()

basePrim = stage.DefinePrim('/samplePrim')
primA = stage.DefinePrim('/primA')
primB = stage.DefinePrim('/primB')
# Relationを作成
rel = basePrim.CreateRelationship('sample')
rel.AddTarget(primA.GetPath())
rel.AddTarget(primB.GetPath())
print(stage.ExportToString())
```

```
#usda 1.0
(
    doc = """Generated from Composed Stage of root layer 
"""
)

def "samplePrim"
{
    custom rel sample = [
        </primA>,
        </primB>,
    ]
}

def "primA"
{
}

def "primB"
{
}
```

同じPropertyですが、Attributeとは違いリレーションは指定のPrimまでのSdfPathを持ちます。
上の例でいうと、 basePrimの sampleプロパティは primA と primB へのRelationshipを持ちます。

```python
# Relationで接続したPrimを取得できる
print(rel.GetTargets())
# そのPathから、Primを取得
for path in rel.GetTargets():
    print(stage.GetPrimAtPath(path))
```

Relationshipは、ターゲットまでのSdfPathを持っているので
このように、別のPrimとのコネクションを作成できます。（Property - 複数Primの関係）

このRelationshipは、主に[MaterialAssign](https://fereria.github.io/reincarnation_tech/60_JupyterNotebook/USD/Material/USDMaterial_02/)や[Collection](https://fereria.github.io/reincarnation_tech/60_JupyterNotebook/USD/APISchema/USDCollectoinSample/)といった、あるPropertyによって指定のPrimとを関連付けるときなどに
使用します。

## Namespace

最後にPropertyのNamespaceについて。
USDのProperty名には Namespace:PropName = Value のように、 : を使用することでNamespaceを指定することができます。

```python
stage = Usd.Stage.CreateInMemory()

prim = stage.DefinePrim('/samplePrim')
attr = prim.CreateAttribute('sampleA:hoge',Sdf.ValueTypeNames.Bool).Set(False)
attr = prim.CreateAttribute('sampleA:ns:fuga',Sdf.ValueTypeNames.Bool).Set(True)
attr = prim.CreateAttribute('sampleA:ns:fugaB',Sdf.ValueTypeNames.Bool).Set(True)

attr = prim.CreateAttribute('sampleB:foo',Sdf.ValueTypeNames.Bool).Set(False)
attr = prim.CreateAttribute('sampleB:bar',Sdf.ValueTypeNames.Bool).Set(True)

print(prim.GetPropertiesInNamespace('sampleA'))
print(prim.GetPropertiesInNamespace('sampleA:ns'))
print(prim.GetPropertiesInNamespace('sampleB'))

print(stage.ExportToString())
```

このNamespaceをつけると何ができるかというと、指定のNamespace以下のPropertyを GetPropertiesInNamespaceできるようになります。
サンプルのように、１つだけでなく複数Namespaceをつけることもできるので
これを利用して、Propertyをグループとして扱うなどができます。


## まとめ

まとめると、PropertyとはPrimに指定された実データを含む値のことで

![](https://gyazo.com/183b5cd7bbf695a0eda49a9ef22bb3a2.png)

AttributeとRelationshipの２種類が存在しています。

Attributeは、型をもった値(実データ)で、任意のTimeCodeを与えることでTimeSampling（アニメーション）することができます。
TimeSamplingがある場合、Stageで指定されたInterpolation（補間）でTimeCodeとTimeCodeの間が補間されます。
そして、Attributeは、Schemaによって定義されたものと、ユーザーによって定義されたもの２種類が存在し、
Schemaによって定義されたものはレイヤーに値が設定されていない場合でもデフォルトが指定されます。

Relationshipは、

![](https://gyazo.com/2dd700fff71f07fc4ef050e00b360006.png)

あるPrimへのリレーションを作ることができます。
これを利用して、MaterialAssignやCollectionといったような他Primとのコネクションを
表現することができます。

以上が Property/Attribute/Relationshipの基本でした。

このあたりは、コンポジションがかかわってきた場合さらにいろいろややこしくなりますが、[こちらの記事](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09) で技師長師匠に盛大に丸投げされてしまったので、近いうちに別途詳しく書こうと思います。
