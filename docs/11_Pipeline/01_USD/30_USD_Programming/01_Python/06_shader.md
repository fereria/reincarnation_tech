---
title: UsdPreviewSurfaceを使う
tags:
    - USD
    - UsdShade
    - UsdPreviewSurface
    - Python
description: Pythonを使用してUsdPreviewSurfaceを構築する
---

[SOLARISでのUsdPreviewSurface以前](https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/12_usd_preview_surface/)の記事を書いたのですが
今回はPythonをベースにPreviewSurfaceをまとめてみようと思います。

## 基本構造

![](https://gyazo.com/d9576c9061fcdeb24117c432243b3964.png)

UsdPreviewSurfaceを使用する場合は、 MaterialとShaderの２つのPrimを使用します。

![](shader.drawio#0)

ルート以下の構造はこのようにします。

必要に応じて変えても良いですが、

* マテリアルはLooks
* ジオメトリなどはGeom
* レンダーセッティングはRender
  
が、比較的スタンダードな構造かとおもうので今回はこれで説明します。

![](shader.drawio#1)

Mesh、Material、Shaderの関係性はこのようになります。

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

それを、Pythonで書くとこのようになります。

![](https://gyazo.com/a1951837651322ab11c24e445a06e0b1.png)

結果できあがったusdaをusdviewでひらくと、このように赤いSphereができあがります。

次は、MaterialとShaderをもう少し詳しく見ていきます。

## UsdShadeMaterial

UsdShadeMaterialは、MayaでいうところのShadingGroupのような役割を持つPrimです。
レンダーターゲットとなるPrim（Mesh等）とシェーダーとをつなぐ働きをします。

![](https://gyazo.com/0140601734293f7728cdd922a04198d5.png)

MaterialとMeshとはリレーションで接続されています。

Meshに対してMaterialをBindするには、UsdShadeMaterialBindingAPIを使用します。

```python
UsdShade.MaterialBindingAPI(sphere.GetPrim()).Bind(mat)
```
BindingAPIがアサインするMesh、そしてBind(materialPrim)でアサインすることができます。


## UsdShadeShader

次にシェーダー。

USDのシェーダーは、
https://graphics.pixar.com/usd/docs/UsdPreviewSurface-Proposal.html
公式Helpのこちらに一覧があります。

ShaderPrimとまとめられていますが、ShaderPrimは id を指定することで
Mayaでいうところのマテリアルであったり、ファイルノードであったり、Place2DTextureのような
ノードの働きをします。
そして、それらには Inputs/Outputs のアトリビュートがあり、
ShaderPrim同士を接続することができます。

### UsdPreviewSurface

```python
shader = UsdShade.Shader.Define(stage, matPath.AppendChild('SampleShader'))
shader.CreateIdAttr('UsdPreviewSurface')
shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1,0,0))
mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
```

まずは、シンプルなシェーダーを作成します。
CreateIdAttr というのが、このShaderがどう振る舞うものかを指定するものになります。
「UsdPreviewSurface」が、いわゆるPixarがデフォルトで用意しているPBRシェーダーです。

そのシェーダーに対して、アトリビュートを追加します。
アトリビュートのうちなにが指定できるかは Helpページの Core Nodes / Preview Surface 以下に
まとめてあります。

> Inputs (name - type - fallback)
>  * diffuseColor - color3f - (0.18, 0.18, 0.18)
>     When using metallic workflow this is interpreted as albedo.

CreateInput(～)でアトリビュートを作り（idを指定したからといってアトリビュートがデフォルトで用意されているわけではない）
その作成したアトリビュートに対して、色をセットします。

![](shader.drawio#4)

そして、シェーダーとマテリアルを接続します。
ConnectToSourceは 
接続先.ConnectToSource(接続元.ConnectableAPI(),'接続するアトリビュート')
です。

!!! note 
    ShaderPrimのUsdShadeConnectableAPI は、シェーディングパラメーターの入力と出力
    の間の接続を行うための共通インターフェースを提供するAPIスキーマです。
    USDのUsdShadeMaterialの CreateSurfaceOutput().ConnectToSourceや、
    サンプルコードを見ると ConnectableAPI() を使わずに shader, "surface"  となっているが
    それだと現状はエラーになってしまいます。
    Input/Outputの接続処理全般を扱うのであれば、UsdShadeConnectableAPIを使うのが推奨なのかも？
    

### UsdUVTexture / UsdPrimvarReader

基本的な色の指定ができた次は、テクスチャを指定してみます。

UsdPreviewSurfaceを使用する場合は、UsdShadeShaderPrimに対して UsdPreviewSurfaceをIDに指定しましたが
テクスチャを使用する場合は、UsdShadeShaderPrimに対して別のIDを使用することで
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

テクスチャを使用するには、 UsdUVTextureを使用するのですが
テクスチャを貼るには、Mayaで言うところのPlace2DTextureのように
UV座標を取得して来る必要があります。

### UsdGeomMeshのUV

USDのUVは「Primvar」と呼ばれるアトリビュートで指定することができます。
Primvarとは、レンダラーに渡すための特別なアトリビュートです。

![](shader.drawio#5)

例えばUVの場合。
st PrimvarはいわゆるあるVertexに対応するUV座標を保持しています。
これは各Vertexごとに指定されていますが
その頂点間に関しては、表面や体積に応じて「補完（Interpolate）」されます。

!!! info
    デフォルトだとPrimvarのIndexはDirect（VertexとUVのIndexが同じ）モードですが
    １頂点に対して複数UV指定がある場合は UsdGeom.Tokens.faceVarying にします。
    ![](shader.drawio#3)
    その場合は、primvarsのindicesにMeshのpointsと同じ並びのアトリビュートを追加し
    そのアトリビュートには、対応するUV（primvar:st）のIndexを指定します。
    

で。
このUVを使用してテクスチャをマテリアルにアサインしたいので
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

まず、MaterialとShaderを作成します。
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
 そしてファイルパスやUV座標をInputで受け取り、その結果を rgb でOutputで渡します。
 そのOutputの結果を、UsdPreviewSurfaceのdiffuseColorアトリビュートに接続します。
 
 UV座標を取得するのが UsdPrimvarReaderです。
 これが、その名の通りメッシュに指定してあるPrimvarのアトリビュートを参照するためのノードで
 UVの場合は float2 なので、IDは UsdPrimvarReader_float2 を指定します。
 
 Inputsの「st」は、Materialにある stPrimvarName で指定した名前です。
この名前は、いわゆるUVSetの名前です。
```python
texCoords = billboard.CreatePrimvar("st", 
                                    Sdf.ValueTypeNames.TexCoord2fArray, 
                                    UsdGeom.Tokens.varying)
```
MeshにPrimvarを指定したときの名前がUVSetNameで
任意の名前を指定できます。（複数のUVを作ることができる）
その、複数あるUVのうち
どのUVを使用するのか指定するのが、この PrimvarReader の varname アトリビュートです。

サンプルでは、Materialにアトリビュートを作成して
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

また、diffuseColor以外のアトリビュートに別のテクスチャを指したい場合も基本と同じで
CreateOutputであるチャンネルのみを取得して、
指定のアトリビュートに対してConnectToSourceで接続すればOKです。

!!! info
    これ以外にも、Transform2dが使用可能です。
    Transform2dを使用すると、テクスチャ座標系でイメージを移動・リサイズ・回転をすることができます。

## Face単位のアサイン

Primを指定すると、１Meshに対して１Materialをアサインします。
そうではなく、Face単位でアサインしたい場合はどのようにするかというと
Subsetを使用してBindします。

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

実行すると、Meshの子PrimとしてUsdGeomSubsetPrimが作成されます。
UsdGeomSubsetは、その名の通りUsdGeomのサブセットで
メッシュのインデックスを保持します。
これを利用することで、あるメッシュのうちの指定のFaceにマテリアルをアサインすることができます。

![](https://gyazo.com/f5de0e93f09774bbac22339c5c1ba70a.png)

アサインした結果、インデックスが 0 のFaceにのみマテリアルがアサインできました。

![](https://gyazo.com/a1ce09026d42f97e2e186ff98cf1e967.png)

GeomSubsetのアトリビュートをみると、インデックスと アサインされているマテリアルがmaterial:binding のリレーション
が含まれていることがわかります。

```python
subset.GetPrim().GetRelationship("material:binding").GetTargets()
```

Pythonでマテリアルを取得する場合は、
subsetからPrimを取得して、そのPrimのリレーションからターゲットを取得できます。

## まとめ

これで、USDの基本的なシェーダーの構築方法がわかりました。
https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/12_usd_preview_surface/
SOLARISのUsdPreviewSurfaceなどを使用すればもう少し楽に作れると思いますが
PrimvarReaderや、Fileノードなどの構造はUSDの構造をベースにしているので
[こちら](https://graphics.pixar.com/usd/docs/UsdPreviewSurface-Proposal.html)とあわせて確認すると扱いやすいのではないかとおもいます。