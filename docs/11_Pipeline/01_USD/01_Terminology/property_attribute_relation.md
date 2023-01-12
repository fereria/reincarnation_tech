---
title: Property/Attribute/Relationship
tags:
    - USD
    - AdventCalendar2021
order: 1
---

[Universal Scene Description](https://qiita.com/advent-calendar/2021/usd) 3 日目。
今回は、今までしっかり説明指定していなかった、USD の「Property の基本」について説明していこうと思います。

## Property とは

USD の Property とは、

> Properties are the other kind of namespace object in USD (Prims being the first).
> 引用: https://graphics.pixar.com/usd/release/glossary.html#usdglossary-property

とあるとおり、USD のネームスペースを構成する一種で、Prim に指定される実データをを含む値のことです。
（Maya でいうところの Attribute）

USD の Property は、 **「Attribute」** と **「Relationship」** の種類があります。

### Attribute

Attribute はいわゆる Maya の Attribute のように、
Prim に定義された「TimeSample すること」「コンポジションアークによって合成」ができるパラメーターです。
[昨日のこちらの記事のアトリビュートについて](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09) でも触れられていましたが、
一般的に、3D で使われる型など[DataType](https://graphics.pixar.com/usd/release/api/_usd__page__datatypes.html)で指定されたものが使用できます。

json や toml、yaml、xml といったフォーマットとは違い、Attribute に対しては必ず型指定必用なのが特徴です。

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

シンプルな Prim を作成して、Attribute を追加・指定した例。
CreateAttribute で指定した型で Attribute が追加されていることがわかります。

> 余談ですが、この Attribute の型指定は、Python から指定する場合公式の DataTypes ページのどこにも書かれていないという罠があります。
> {{markdown_link('usd_py_docs')}}
> そんなトラップを回避するために、過去頑張って調べた一覧がこちら。
> Python と C++（Help 記載の内容）だと違うという罠がごくまれにあるのが USD の悲しいところ。

#### TimeSampling と Interpolation

USD の Attribute では、TimeCode を指定することで、TimeSampling 　いわゆるアニメーションを
させることができます。
以下、シンプルな Attribute を作成して、動作を確認してみます。

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

Set するときに、 Set(\<Value\>,\<Timecode\>) とすることで、Attribute に対してキーを追加できました。
この状態で、

```python
print(attr.Get(5))
```

> 5.0

.Get(\<TimeCode\>) とすると、指定の TimeCode の値を取得することができます。
Get しているのは Key を打っていない 5 フレーム目ですが、0 フレーム目と 10 フレーム目のちょうど中間
TimeCode と TimeCode の間が補間された値が取得されました。

Attribute の TimeSample は、UsdStage の SetInterpolationType で指定することができます。
サポートされているのは Held と Linear の２つ。

デフォルトは Linear で、TimeCode と TimeCode の間をリニアに保管します。
Held の場合は、Maya でいうところの StepTangent で、次の TimeCode まで Attribute の値を一定に保ちます。

```python
stage.SetInterpolationType(Usd.InterpolationTypeHeld) # デフォルトは、UsdInterpolationTypeLinear
prim = stage.DefinePrim('/samplePrim')
attr = prim.CreateAttribute('intValue',Sdf.ValueTypeNames.Float)
attr.Set(0,0)
attr.Set(10,10)

print(attr.Get(5))
```

> 0.0

Hold に変えた場合の結果、補間されず直前の値が取得されました。

#### CustomAttribute

最後に CustomAttribute について。
空の Prim に対して CreateAttribute をした場合、ExpotToString をしてみると、Attribute の前に「custom」
が付いていることがわかります。
この custom がなにかというと、
その名の通りその Attribute が Schema によって定義されたものかユーザーによって定義されたものかどうか区別するためのものです。

まず、Schema によって定義されたものとはどういうものかというと、
以下の Kitchen_set にある Ball.usd で見てみます。

![](https://gyazo.com/786954f7a9dfca11223458c9759c3413.png)

Ball にある MeshPrim は、UsdGeomMesh スキーマが指定された Prim です。
USD のソースコード以下 USD/pxr/usd/usdGeom/generatedSchema.usda を読み進めると、Mesh スキーマの class があり
その中に、Mesh スキーマに定義された Attribute があります。
これが、スキーマによって定義されている Attribute で たとえレイヤーに Attribute の記述がなかったとしても
スキーマで定義された値がフォールバック値として設定されます。

![](https://gyazo.com/2c3347b7c11c5c69fa8499f34513a294.png)

例として、 doubleSided。
Ball.usd 内には doubleSided Attribute に値をセットする記述はありませんが、usdview を見ると
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

このような Attribute に値を Set した場合は custom にはなりません。

```python
prim.GetAttribute('doubleSided').IsCustom()
```

> False

IsCustom で確認しても、False になります。

```python
prim.GetAttribute('sample').IsCustom()
```

> True

対する、スキーマにはない Attribute の場合は
custom が追加され、 IsCustom で確認しても True になります。

### Relationship

Relationship とは、その名の通り、ある Prim への「リレーション」を持つプロパティのことです。

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

同じ Property ですが、Attribute とは違いリレーションは指定の Prim までの SdfPath を持ちます。
上の例でいうと、 basePrim の sample プロパティは primA と primB への Relationship を持ちます。

```python
# Relationで接続したPrimを取得できる
print(rel.GetTargets())
# そのPathから、Primを取得
for path in rel.GetTargets():
    print(stage.GetPrimAtPath(path))
```

Relationship は、ターゲットまでの SdfPath を持っているので
このように、別の Prim とのコネクションを作成できます。（Property - 複数 Prim の関係）

この Relationship は、主に {{markdown_link('USDMaterial_02')}} や {{markdown_link('USDCollectoinSample')}}といった、ある Property によって指定の Prim とを関連付けるときなどに
使用します。

## Namespace

最後に Property の Namespace について。
USD の Property 名には Namespace:PropName = Value のように、 : を使用することで Namespace を指定することができます。

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

この Namespace をつけると何ができるかというと、指定の Namespace 以下の Property を GetPropertiesInNamespace できるようになります。
サンプルのように、１つだけでなく複数 Namespace をつけることもできるので
これを利用して、Property をグループとして扱うなどができます。

## まとめ

まとめると、Property とは Prim に指定された実データを含む値のことで

![](https://gyazo.com/183b5cd7bbf695a0eda49a9ef22bb3a2.png)

Attribute と Relationship の２種類が存在しています。

Attribute は、型をもった値(実データ)で、任意の TimeCode を与えることで TimeSampling（アニメーション）することができます。
TimeSampling がある場合、Stage で指定された Interpolation（補間）で TimeCode と TimeCode の間が補間されます。
そして、Attribute は、Schema によって定義されたものと、ユーザーによって定義されたもの２種類が存在し、
Schema によって定義されたものはレイヤーに値が設定されていない場合でもデフォルトが指定されます。

Relationship は、

![](https://gyazo.com/2dd700fff71f07fc4ef050e00b360006.png)

ある Prim へのリレーションを作ることができます。
これを利用して、MaterialAssign や Collection といったような他 Prim とのコネクションを
表現することができます。

以上が Property/Attribute/Relationship の基本でした。

このあたりは、コンポジションがかかわってきた場合さらにいろいろややこしくなりますが、[こちらの記事](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09) で技師長師匠に盛大に丸投げされてしまったので、近いうちに別途詳しく書こうと思います。
