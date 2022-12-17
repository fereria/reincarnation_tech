---
title: 0から始めるUSDPython(3) Primを作る
tags:
    - USD
    - USDPythonTutorial
    - AdventCalendar2022
description: USDをPythonで操作するチュートリアル_Primを作る
---

{{markdown_link('01_start_usdpython')}} と {{markdown_link('02_traverse')}} ではすでに作成されている USD ファイルの読み方と変更方法をやっていきましたが
第 3 回目の今回は、新しい USD ファイルを作り
Prim を作っていきます。

## 新しいステージを作る

まず、空のステージを作るのですが、
新規シーンを作る方法はいくつかあります。
1 つ目が、ファイル名を指定して新規で作る場合。

```python
stage = Usd.Stage.CreateNew('./newScene.usda')
```

CreateNew では、引数に保存先のファイルを指定し
新規ファイルを作成してから、その USD ファイルをロードします。

こうすると、CreateNew した段階で USD ファイルが作成されるメリットがありますが
すでにファイルがある場合は CreateNew の場合はエラーになります。

```python
stage = Usd.Stage.CreateInMemory()

layer = stage.GetRootLayer()
layer.Export("./newScene.usda")
```

もう 1 つが、CreateInMemory です。
この CreateInMemory は、ファイルを作成することなくメモリ上にだけファイルを作成します。
この場合はファイルが既にあったとしてもエラーになりませんが、
保存するまえはファイルが作成されないのに注意が必要です。

## Prim を作る

ステージができたので、次はこのステージに Prim を作ります。

```python
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim("/newPrim")
stage.GetRootLayer().Export("./newScene.usda)
```

Prim とは、データを入れるためのコンテナ（入れ物）です。
DefinePrim をすると、引数で指定したパスに指定の名前で Prim を作成します。

![](https://gyazo.com/444c60a56fd5d7ffede53f09ac320de6.png)

作成した Prim を usdview で開くと Prim が作成できているのがわかります。
しかし、Type を見ても何も入っていませんし、

![](https://gyazo.com/a92337042b8914a10148a9badee60dff.png)

Property を見ても、BoundingBox や LocalToWorldXform 等はあるものの
情報がありません。

これは Prim とは「あくまでも入れ物」でしかなく、それがどういったものなのかとか
どういう Property が入っているかが入っているわけではありません。
あくまでも階層構造をもった入れ物です。

なので、実際は「こういうデータ構造が入っているよ」という型指定をする必要があります。
USD では、このデータの型を定義するための構造を「{{markdown_link('18_schema','スキーマ')}}」と呼びます。

```python
from pxr import UsdGeom
cube = UsdGeom.Cube.Define(stage,'/sampleCube')
```

スキーマを定義した Prim を作成する場合は、 UsdGeom(UsdGeometrySchema)や
UsdLux(UsdLightSchema)のようなスキーマクラスの Define 関数を使用します。

![](https://gyazo.com/b66ed18caa3d044205946bed7e3ec60e.png)

スキーマで定義すると、先ほどとは違い Type が指定されているのがわかります。

![](https://gyazo.com/57e18eb4e2e58bcb90f1cebe438f2d65.png)

Property も、Cube を定義するのに必要な size のようなアトリビュートが
指定されています。

```python
# >> UsdGeom.Cube(Usd.Prim(</sampleCube>))
```

スキーマクラスを使用して Prim を定義した場合は、 Usd.Prim ではなく
UsdGeom.Cube のような、スキーマのオブジェクトが帰ってきます。

```python
print(cube.GetSizeAttr().Get())
# >> 2.0
```

スキーマオブジェクトは、そのスキーマに関連する機能が用意されています。
たとえば、UsdGeomCube であれば、CubeSize を取得したりセットするような関数が
用意されています。

```python
prim = cube.GetPrim()
```

スキーマオブジェクトではなく、Prim を取得したい場合は、 GetPrim で取得します。

```python
cube = UsdGeom.Cube(cubePrim)
```

Prim からスキーマオブジェクトを取得する場合は、このようにクラスに Prim
を渡します。

## Light を作る

これまでは Cube を作っていましたが、次は Light を作ってみます。
とはいえ、ライトもスキーマによって定義されているので
同様の方法で作成できます。

```python
from pxr import UsdLux
light = UsdLux.DistantLight.Define(stage,'/dLight')
# Intensityを取得したい場合 セットなら Get～
print(light.GetIntensityAttr().Get())
```

DistantLight を作る場合はこのようになります。
このように、3DCG に関連するデータを作成するには指定の定義（スキーマ）を
作成し、そこに指定の Property を設定することで作成できます。
