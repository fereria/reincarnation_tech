---
title: OpenMasked（PopulationMask）について
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description](https://qiita.com/advent-calendar/2021/usd) 5日目は、USDのファイルオープンの
機能の１つ、PopulationMask（OpenMasked）について紹介します。

USDは、コンポジションを使用することで巨大なシーンを扱うことができますが、
巨大なシーンを毎回すべて開くと時間がかかるので
指定した一部分だけをロードしたい...ということが多々あります。

その場合、Payloadを使用してアンロードしておいた状態から指定Primをロードする事もできますが
それ以外にも [UsdStagePopulationMask](https://graphics.pixar.com/usd/release/api/class_usd_stage_population_mask.html) という機能を使用することで
部分的なロードができるようになります。

## 使い方

まず、普通にロードした場合。

```python
from pxr import Usd

stage = Usd.Stage.Open(r"D:/Kitchen_set/Kitchen_set.usd")
```

Usd.Stage.Open(ファイルパス)をすることで、ロードすることができます。
この場合は、すべてのPrimがロードされます。

```python
stage = Usd.Stage.Open(r"D:/Kitchen_set/Kitchen_set.usd",Usd.Stage.LoadNone)
```

次にUnload状態でロードした場合。
この場合は、すべてのPayloadがアンロードされた状態になります。


では、実際にPopulationMaskを使用した場合について。


![](https://gyazo.com/db398e3d8478280a9fa7b7c961db5d08.png)


Kitchen_setのうち、冷蔵庫だけをロードしてみます。

```python
mask = Usd.StagePopulationMask().Add('/Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1')
stage =  Usd.Stage.OpenMasked(r"D:/Kitchen_set/Kitchen_set.usd",mask)
```

この場合は、ロードしたいSdfPathをPopulationMaskに追加して
Usd.Stage.Openのかわりに OpenMasked を使用します。
こうすると、 冷蔵庫の指定Path以下にあるPrimだけがロードされます。

```
usdview D:\Kitchen_set\Kitchen_set.usd --mask /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
```

![](https://gyazo.com/a422223a382b4c8d2b89833eb98fd9db.png)

PopulationMaskは usdview で使用することができて、引数に --mask PrimPath を追加すれば
指定のPath以下のPrimだけロードされた状態になります。

## 現在のStageのPopulationMaskを取得

次に、取得方法。

```python
mask = stage.GetPopulationMask()
for path in mask.GetPaths():
    print(path)
```

現在のStageのPopulationMaskがどうなっているか、またどんなPathが含まれているのかも確認が可能です。

## PopulationMaskを変更する

PopulationMaskはロード時だけではなく、ロード後にも変更ができます。

```
#usda 1.0

def "a"{}
def "b"{}
def "c"{}
```

このようなシンプルなUSDファイルを用意して、 sample.usdaという名前で保存しておきます。


```python
mask = Usd.StagePopulationMask(['/a'])
stage = Usd.Stage.OpenMasked("D:/sample.usda",mask)
print(stage.ExportToString())
maskB = Usd.StagePopulationMask(['/b'])
stage.SetPopulationMask(maskB)
print(stage.ExportToString())
```
最初に a PrimだけをPopulationMaskを使用してロードしたときは、Primは a のみになります。
そのあと、 b Prim のPopulationMaskをセットすると
Stageは再構築され、b のみロードされたシーンになります。


## PopulationMaskのさらなる使い方

PopulationMaskを使用すればStageの一部だけをロードできることがわかりました。

今までは、Add等で１つあるいは複数のPathを追加するだけの使い方でしたが、
PopulationMaskは、それ以外にもSdfPathをSet（集合）として扱うことができます。

先度帆の simple.usda で動作をみていきます。

このファイルのうち、 a Primだけをロードしたい場合は、

```python
mask = Usd.StagePopulationMask().Add('/a')
stage = Usd.Stage.OpenMasked("D:/sample.usda",mask)
print(stage.ExportToString())
```
このように、 a をPopulationMaskに入れてOpenMaskedで開けばOKです。

### 複数のSdfPathを指定する場合

```python
mask = Usd.StagePopulationMask().Add('/a')
mask.Add('/b')

# あるいは
mask = Usd.StagePopulationMask(['/a','/b'])
```
複数の場合は、StagePopulationMaskの引数に配列で指定するか、
PopulationMaskにAddすることで複数指定が可能です。

### 複数のPopulationMaskから新しいPopulationMaskを作る場合

```python
# 複数の異なるMaskを結合する場合
maskA = Usd.StagePopulationMask().Add('/a')
maskB = Usd.StagePopulationMask().Add('/b')
# PopulationMaskを結合
union = Usd.StagePopulationMask().Union(maskA,maskB)
# これでもOK
 maskA.GetUnion(maskB)
```

### 両方のPopulationMaskに含まれるSdfPathのみにしたい

```python
maskA = Usd.StagePopulationMask(['/a','/b'])
maskB = Usd.StagePopulationMask(['/c','/b'])
print(Usd.StagePopulationMask().Intersection(maskA,maskB))
```

### 指定のSdfPathを含むか確認したい

```python
maskA = Usd.StagePopulationMask(['/a','/b'])
maskB = Usd.StagePopulationMask(['/b'])
print(maskA.Includes(maskB))
```

このように、すでにあるPopulationMaskを組み合わせることで別のPopulationMaskを作成すれば
柔軟にシーンの部分ロードが可能になります。

## まとめ

Payloadをすることで大規模なシーンでも一部だけロードする...といったことが可能でしたが
PopulationMaskを使用すると、さらに細かく
SdfPathを個別に指定しながら一部だけのロードが可能になります。
また、PopulationMaskは、Setsのような使い方ができるので
これを利用して様々な条件でも柔軟に部分ロードができます。

巨大なシーンを扱う場合、一部だけ修正・確認をしたいような場合にぜひお試しください。