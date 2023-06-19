---
slug: /usd/render_context
title: USDのRenderContextについて
description: Materialに対して指定できる「RenderContext」とは
sidebar_position: 30
---

USD のマテリアルには「RenderContext」と呼ばれる Material に接続される Shader に対して「修飾する」機能が用意されています。  
今回はそれがどんなもので、どんな意味があるかを説明していきます。

USD は、「ユニバーサルな」シーン記述という名前の通り、  
あらゆる環境で共通して解釈可能なデータフォーマットになっています。  
USD は [スキーマ](/usd/schema) と呼ばれるデータ構造を用いることで、一般的に 3DCG で使用しているデータ型を定義し扱っています。  
ですが、メッシュデータやライトなどはそれでも何とかなりますが、  
マテリアルに関してはその限りではありません。

MaterialX などを用いて、マテリアルの定義の共通化の取り組みは行われていますが  
まだまだレンダラー固有の情報も多く、1 つのシェーダーだけですべてをまかなうことができません。

これを解決するのが RenderContext です。

## Mesh と Material と Shader の関係

USD における「Material」とはなにかというと、

:::note Material
A Material provides a container into which multiple "render targets" can add data that defines a "shading material" for a renderer.
:::

とあるとおり、レンダラーの「シェーディングマテリアル」を定義するデータを追加するための **コンテナ** を提供します。
それに対して、Shader とは、

:::note Shader
Shaders are the building blocks of shading networks.
While UsdShadeShader objects are not target specific,
each renderer or application target may derive its own renderer-specific shader object types from this base, if needed.
:::

いわゆる「シェーディングネットワーク」を提供し、各レンダラーで使用するシェーダーを定義しています。

関係性をあらわすならば、

![](https://gyazo.com/f5484a202836643c616b8e0e8c1d4578.png)

ざっくりとこのような関係になっています。
Mesh は、単一の Material に対してアサインされます。
この Material が、Shader に接続されマテリアル情報を参照します。
この時、Material と Shader の関係は 1 対 1 ではないというのが重要です。

## RenderContext

というわけで、ここからが本題です。
USD の Material は、複数の Shader を持つことができます。
それを Blender の Export を使用してテストしてみます。

![](https://gyazo.com/cdf5392e25fc3705f91a8ea4d0c982bc.png)

Blender の USD Export のオプションには「Export Cycles Shaders」というオプションが存在しています。  
それと同じく、「Convert to USD Preview Surface」が用意されています。  
これは、Blender のレンダラーである Cycles でレンダリングする場合に使用するシェーダーを出力しつつ  
PreviewSurface（どのツールでもある程度使用できる共通のマテリアル）も出力するということになります。

![](https://gyazo.com/c5fb390c711a2618a8c8eda18068d5ca.png)

個のシーンを、SOLARIS や usdview で開くと、Material 以下に「cycles」「mdl」「preview」という３つのスコープが
出力されます。

![](https://gyazo.com/4b3a135bc858bd40f5ba9e1e7e428886.png)

Material の Property を確認すると、outputs:###:surface というアトリビュートがあり、

![](https://gyazo.com/801d12b3c9537e59d273565dfed6ad81.png)

outputs:surface は、 preview のスコープ以下の Shader に接続しているし、

![](https://gyazo.com/ab78b10d018e8e6124801b175b646c0d.png)

outputs:cycles:surface は、 cycles 以下のスコープの Shader に接続しているのがわかります。

今回は Blender でしたが、SOLARIS で試すと、 karma というネームスペースが追加されているのがわかります。

この cycles や preview のように、ある Material に対して指定されている SurfaceOutput（シェーダーの出力）を  
修飾するときに使用するのが「RenderContext」です。  
これをしようすれば、1 つのシーンのなかに、複数のレンダラー用の Shader を持ちつつも  
指定がなければデフォルトを使用する...そういったことが可能になります。

```python
from pxr import UsdShade

prim = stage.GetPrimAtPath('/root/materials/Material')
mat = UsdShade.Material(prim)

print(mat.ComputeSurfaceSource())
```

この RenderContext によって複数の Shader をもつ Material から  
Python を使用して何かしらの Shader を取得したい場合。  
「ComputeSurfaceSource」という関数が用意されています。  
これは「Compute」とある通り、単純に SurfaceSource を取得するのではなく  
RenderContext を指定して取得することができます。

上の例だと何も指定していないのでデフォルト(outputs:surface) に接続されている Shader を取得します。

```python
print(mat.ComputeSurfaceSource('cycles'))
```

これに、RenderContext を指定した場合、
この場合は outputs:cycles/surface に接続されている Shader が取得でいます。

```python
print(mat.ComputeSurfaceSource('karma'))
```

ですが、「karma」のように、現在のシーンに存在していないものを取得しようとした場合どうなるかというと  
デフォルトである outputs:surface に接続されている Shader が取得されます。

## まとめ

このような USD のシェーダーアサインになっていることで、  
Mesh と Material の Assign 情報は維持しつつも、複数のレンダラーに対応できるのがわかりました。  
いずれは MaterialX 等を使用してマテリアルも共通化がされていくかと思いますが  
現段階でもこの RenderContext をうまく利用することでマテリアルの設定だけを差し替えることが可能なので  
USD でシーンを構築するときは、有効活用できるのでは？と思います。
