---
title: UsdPreviewSurfaceを使う
tags:
    - USD
    - UsdShade
    - UsdPreviewSurface
    - Python
    - CEDEC2022
description: Pythonを使用してUsdPreviewSurfaceを構築する
---

[SOLARIS での UsdPreviewSurface 以前](https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/12_usd_preview_surface/)の記事を書いたのですが
今回は Python をベースに PreviewSurface をまとめてみようと思います。

## 基本構造

![](https://gyazo.com/d9576c9061fcdeb24117c432243b3964.png)

UsdPreviewSurface を使用する場合は、 Material と Shader の２つの Prim を使用します。

![](shader.drawio#0)

ルート以下の構造はこのようにします。

必要に応じて変えても良いですが、

-   マテリアルは Looks
-   ジオメトリなどは Geom
-   レンダーセッティングは Render

が、比較的スタンダードな構造かとおもうので今回はこれで説明します。

![](shader.drawio#1)

Mesh、Material、Shader の関係性はこのようになります。

```python
from pxr import Usd,UsdShade,Sdf,UsdGeom,Gf

stage = Usd.Stage.CreateInMemory()
rootLayer = stage.GetRootLayer()

# Mesh作成
sphere = UsdGeom.Sphere.Define(stage, '/AssetName/Geom/sphere')

matPath = Sdf.Path("/AssetName/Looks/SampleMaterial")
mat = UsdShade.Material.Define(stage, matPath)
shader = UsdShade.Shader.Define(stage, matPath.AppendChild('SampleShader'))
shader.CreateIdAttr('UsdPreviewSurface')
shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1,0,0))
mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
UsdShade.MaterialBindingAPI(sphere.GetPrim()).Bind(mat)
```

それを、Python で書くとこのようになります。

![](https://gyazo.com/a1951837651322ab11c24e445a06e0b1.png)

結果できあがった usda を usdview でひらくと、このように赤い Sphere ができあがります。

次は、Material と Shader をもう少し詳しく見ていきます。

## UsdShadeMaterial

UsdShadeMaterial は、Maya でいうところの ShadingGroup のような役割を持つ Prim です。
レンダーターゲットとなる Prim（Mesh 等）とシェーダーとをつなぐ働きをします。

![](https://gyazo.com/0140601734293f7728cdd922a04198d5.png)

Material と Mesh とはリレーションで接続されています。

Mesh に対して Material を Bind するには、UsdShadeMaterialBindingAPI を使用します。

```python
UsdShade.MaterialBindingAPI(sphere.GetPrim()).Bind(mat)
```

BindingAPI がアサインする Mesh、そして Bind(materialPrim)でアサインすることができます。

## UsdShadeShader

次にシェーダー。

USD のシェーダーは、
https://graphics.pixar.com/usd/docs/UsdPreviewSurface-Proposal.html
公式 Help のこちらに一覧があります。

ShaderPrim とまとめられていますが、ShaderPrim は id を指定することで
Maya でいうところのマテリアルであったり、ファイルノードであったり、Place2DTexture のような
ノードの働きをします。
そして、それらには Inputs/Outputs のアトリビュートがあり、
ShaderPrim 同士を接続することができます。

### UsdPreviewSurface

```python
shader = UsdShade.Shader.Define(stage, matPath.AppendChild('SampleShader'))
shader.CreateIdAttr('UsdPreviewSurface')
shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1,0,0))
mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
```

まずは、シンプルなシェーダーを作成します。
CreateIdAttr というのが、この Shader がどう振る舞うものかを指定するものになります。
「UsdPreviewSurface」が、いわゆる Pixar がデフォルトで用意している PBR シェーダーです。

そのシェーダーに対して、アトリビュートを追加します。
アトリビュートのうちなにが指定できるかは Help ページの Core Nodes / Preview Surface 以下に
まとめてあります。

> Inputs (name - type - fallback)
>
> -   diffuseColor - color3f - (0.18, 0.18, 0.18)
>     When using metallic workflow this is interpreted as albedo.

CreateInput(～)でアトリビュートを作り（id を指定したからといってアトリビュートがデフォルトで用意されているわけではない）
その作成したアトリビュートに対して、色をセットします。

![](shader.drawio#4)

そして、シェーダーとマテリアルを接続します。
ConnectToSource は
接続先.ConnectToSource(接続元.ConnectableAPI(),'接続するアトリビュート')
です。

!!! note
ShaderPrim の UsdShadeConnectableAPI は、シェーディングパラメーターの入力と出力
の間の接続を行うための共通インターフェースを提供する API スキーマです。
USD の UsdShadeMaterial の CreateSurfaceOutput().ConnectToSource や、
サンプルコードを見ると ConnectableAPI() を使わずに shader, "surface" となっているが
それだと現状はエラーになってしまいます。
Input/Output の接続処理全般を扱うのであれば、UsdShadeConnectableAPI を使うのが推奨なのかも？

### UsdUVTexture / UsdPrimvarReader

基本的な色の指定ができた次は、テクスチャを指定してみます。

UsdPreviewSurface を使用する場合は、UsdShadeShaderPrim に対して UsdPreviewSurface を ID に指定しましたが
テクスチャを使用する場合は、UsdShadeShaderPrim に対して別の ID を使用することで
構築することができます。

```python
stage = Usd.Stage.CreateInMemory()
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

modelRoot = UsdGeom.Xform.Define(stage, "/TexModel")
Usd.ModelAPI(modelRoot).SetKind(Kind.Tokens.component)
billboard = UsdGeom.Mesh.Define(stage, "/TexModel/card")
billboard.CreatePointsAttr([(0,0,0),(9.6,0,0), (9.6,5.4,0),(0,5.4,0)])
billboard.CreateFaceVertexCountsAttr([4])
billboard.CreateFaceVertexIndicesAttr([0,1,2,3])
billboard.CreateExtentAttr([(0,0, 0), (9.6,5.4, 0)])
texCoords = billboard.CreatePrimvar("st",
                                    Sdf.ValueTypeNames.TexCoord2fArray,
                                    UsdGeom.Tokens.varying)
texCoords.Set([(0, 0), (1, 0), (1,1), (0, 1)])
```

まず、アサインするメッシュを用意します。

テクスチャを使用するには、 UsdUVTexture を使用するのですが
テクスチャを貼るには、Maya で言うところの Place2DTexture のように
UV 座標を取得して来る必要があります。

### UsdGeomMesh の UV

USD の UV は「Primvar」と呼ばれるアトリビュートで指定することができます。
Primvar とは、レンダラーに渡すための特別なアトリビュートです。

![](shader.drawio#5)

例えば UV の場合。
st Primvar はいわゆるある Vertex に対応する UV 座標を保持しています。
これは各 Vertex ごとに指定されていますが
その頂点間に関しては、表面や体積に応じて「補完（Interpolate）」されます。

!!! info
デフォルトだと Primvar の Index は Direct（Vertex と UV の Index が同じ）モードですが
１頂点に対して複数 UV 指定がある場合は UsdGeom.Tokens.faceVarying にします。
![](shader.drawio#3)
その場合は、primvars の indices に Mesh の points と同じ並びのアトリビュートを追加し
そのアトリビュートには、対応する UV（primvar:st）の Index を指定します。

で。
この UV を使用してテクスチャをマテリアルにアサインしたいので
そういう場合に使用するのが「UsdPrimvarReader」になります。

```python
material = UsdShade.Material.Define(stage, '/TexModel/boardMat')
pbrShader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/PBRShader')
pbrShader.CreateIdAttr("UsdPreviewSurface")
pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
pbrShader.CreateInput("opacity",Sdf.ValueTypeNames.Float).Set(1.0)
material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")

UsdShade.MaterialBindingAPI(billboard).Bind(material)
```

まず、Material と Shader を作成します。
ここまではテクスチャなしのときと同じです。

```python
stReader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/PBRShader/stReader')
stReader.CreateIdAttr('UsdPrimvarReader_float2')

diffuseTextureSampler = UsdShade.Shader.Define(stage,'/TexModel/boardMat/PBRShader/diffuseTexture')
diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("D:/test.png")
diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')
diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)

pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler.ConnectableAPI(), 'rgb')
stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
stInput.Set('st')

stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)
```

![](shader.drawio#6)

この構造を図に表すとこのようになります。
まず、テクスチャを指定するには UsdUVTexture を使用します。
そしてファイルパスや UV 座標を Input で受け取り、その結果を rgb で Output で渡します。
その Output の結果を、UsdPreviewSurface の diffuseColor アトリビュートに接続します。

UV 座標を取得するのが UsdPrimvarReader です。
これが、その名の通りメッシュに指定してある Primvar のアトリビュートを参照するためのノードで
UV の場合は float2 なので、ID は UsdPrimvarReader_float2 を指定します。

Inputs の「st」は、Material にある stPrimvarName で指定した名前です。
この名前は、いわゆる UVSet の名前です。

```python
texCoords = billboard.CreatePrimvar("st",
                                    Sdf.ValueTypeNames.TexCoord2fArray,
                                    UsdGeom.Tokens.varying)
```

Mesh に Primvar を指定したときの名前が UVSetName で
任意の名前を指定できます。（複数の UV を作ることができる）
その、複数ある UV のうち
どの UV を使用するのか指定するのが、この PrimvarReader の varname アトリビュートです。

サンプルでは、Material にアトリビュートを作成して
その値をコネクションすることで値を設定していますが

```python
# これを
stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)
# こうする
stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).Set('st')
```

これでも同じです。

```python
stReader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/PBRShader/Opacity')
stReader.CreateIdAttr('UsdUVTexture')

diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("D:/sample_opacity.png")
diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')
# Outputは１チャンネルあれば良いので、FloatのOutputを作る
diffuseTextureSampler.CreateOutput('r', Sdf.ValueTypeNames.Float)
pbrShader.CreateInput("opacity",Sdf.ValueTypeNames.Float).ConnectToSource(diffuseTextureSampler.ConnectableAPI(),'r')
```

また、diffuseColor 以外のアトリビュートに別のテクスチャを指したい場合も基本と同じで
CreateOutput であるチャンネルのみを取得して、
指定のアトリビュートに対して ConnectToSource で接続すれば OK です。

!!! info
これ以外にも、Transform2d が使用可能です。
Transform2d を使用すると、テクスチャ座標系でイメージを移動・リサイズ・回転をすることができます。

## Face 単位のアサイン

Prim を指定すると、１ Mesh に対して１ Material をアサインします。
そうではなく、Face 単位でアサインしたい場合はどのようにするかというと
Subset を使用して Bind します。

```python
stage = Usd.Stage.Open(r"plane.usd")
prim = stage.GetPrimAtPath('/Geometry/mesh_0')
path = prim.GetPath()
# PrimからGeomMeshを取得
mesh = UsdGeom.Mesh(prim)

# Materialを作成
matPath = Sdf.Path("/AssetName/Looks/SampleMaterial")
mat = UsdShade.Material.Define(stage, matPath)
shader = UsdShade.Shader.Define(stage, matPath.AppendChild('SampleShader'))
shader.CreateIdAttr('UsdPreviewSurface')
shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1,0,0))
mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

# Subsetを作成して、Subsetに対してMaterialをBind
subset = UsdShade.MaterialBindingAPI(mesh).CreateMaterialBindSubset("SubsetName",[0],UsdGeom.Tokens.face)
UsdShade.MaterialBindingAPI(subset.GetPrim()).Bind(mat)
stage.Export("subset.usd")
```

![](https://gyazo.com/347532f558abdb61a651aaa2a9e4cb9b.png)

実行すると、Mesh の子 Prim として UsdGeomSubsetPrim が作成されます。
UsdGeomSubset は、その名の通り UsdGeom のサブセットで
メッシュのインデックスを保持します。
これを利用することで、あるメッシュのうちの指定の Face にマテリアルをアサインすることができます。

![](https://gyazo.com/f5de0e93f09774bbac22339c5c1ba70a.png)

アサインした結果、インデックスが 0 の Face にのみマテリアルがアサインできました。

![](https://gyazo.com/a1ce09026d42f97e2e186ff98cf1e967.png)

GeomSubset のアトリビュートをみると、インデックスと アサインされているマテリアルが material:binding のリレーション
が含まれていることがわかります。

```python
subset.GetPrim().GetRelationship("material:binding").GetTargets()
```

Python でマテリアルを取得する場合は、
subset から Prim を取得して、その Prim のリレーションからターゲットを取得できます。

## まとめ

これで、USD の基本的なシェーダーの構築方法がわかりました。
https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/12_usd_preview_surface/
SOLARIS の UsdPreviewSurface などを使用すればもう少し楽に作れると思いますが
PrimvarReader や、File ノードなどの構造は USD の構造をベースにしているので
[こちら](https://graphics.pixar.com/usd/docs/UsdPreviewSurface-Proposal.html)とあわせて確認すると扱いやすいのではないかとおもいます。
