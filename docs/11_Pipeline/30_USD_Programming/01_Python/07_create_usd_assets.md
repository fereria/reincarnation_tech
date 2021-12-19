---
title: Pythonで作るUSDアセット
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 20日目は、
以前紹介した [Houdini SOLARISのComponentBuilder](https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/16_component_builder/) に近い内容をPythonでやりながら
Pythonを使用したUSDのコンポジションの作り方を説明していきます。

## 最終的な構成

まず、最終的にどのようになるのかを見てみます。

![](https://gyazo.com/cebf8930f814a9d174b40269e5ef7865.png)

今回はマテリアル回りは省いて、ジオメトリのみの構成です。
Kitchen_setの構造をベースにしつつ、ジオメトリのヴァリエーションは個別のレイヤーに分けつつ
Payloadの構造と、Inheritsの構造をデフォルトで仕込むようにします。

では、順番に処理を見ていきます。

## アセット名の指定など

```python
from pxr import Usd,Sdf,Ar
import glob
import shutil
import os
```

まずは必用なモジュールをImportします。

```python
ASSETS_DIR = "D:/sample/assets"
```

そしてAssetのルートディレクトリを決めておきます。

![](https://gyazo.com/d0a2700028ce196b44e30532eb93d902.png)

各アセット以下はこのような構成になるようにします。
Primやフォルダ名、レイヤー名などには、AssetNameを使用するので
事前に変数で定義しておきます。
（実際に使用する場合は、この辺りは関数にしたほうが良いけど、今回はベタ書きします）

```python
# Asset名を決める
assetName = "sampleAssets"
version = 1.0

assetDir = f"{ASSETS_DIR}/{assetName}"
```

ディレクトリは決まったので、USDのPrimを作っていきます。
最初に、 payload のレイヤーを作り、その中にすでにあるジオメトリのレイヤーを
リファレンスするようにします。

```python
payloadStage = Usd.Stage.CreateInMemory()
payloadsLayer = payloadStage.GetRootLayer()
prim = payloadStage.DefinePrim(f'/{assetName}')
payloadStage.SetDefaultPrim(prim)
rootPath = prim.GetPath()
```

CreateInMemoryで、Stageを作り、空のPrimの作成＋DefaultPrimの設定をします。
新しいレイヤーを作る場合は、いくつかやり方があります。

```python
stage = Usd.Stage.CreateNew(f"{assetDir}/{assetName}.payload.usd")
```

このように、CreateNewする手もありますが
この場合既にファイルがあるとエラーになるので、

```python
payloadLayer = Sdf.Layer.FindOrOpen(f"{assetDir}/{assetName}.payload.usd")
pyaloadStage = Usd.Stage.Open(payloadLayer)
```

FindOrOpenするか、サンプルのように CreateInMemory しておくほうが個人的には好きです。
(CreateInMemory なら、必ず作り直すのでアセットづくりの場合なおのこと。)

### Variant作り

```python
geomVariantDir = "D:/sample/variant"

# Variantを指定する
vset = prim.GetVariantSets().AddVariantSet('assets')
geomPath = rootPath.AppendChild('Geom')
geomPrim = payloadStage.DefinePrim(geomPath)
payloadStage.DefinePrim(geomPath)

variantDir = f"{assetDir}/variant"
os.makedirs(variantDir,exist_ok=True)

# 指定フォルダ以下にあるレイヤーを、VariantSetとして追加する
for f in glob.glob(f"{geomVariantDir}/*.usd*"):
    # Assets以下にコピーする
    basename = os.path.basename(f)
    shutil.copy2(f,f"{variantDir}/{basename}")
    variantName = os.path.splitext(basename)[0]
    vset.AddVariant(variantName)
    # モデルパターンの切り替え用のVariantSetを作る
    vset.SetVariantSelection(variantName)
    with vset.GetVariantEditContext():
        # variant 以下のモデルをReferenceする
        geomPrim.GetReferences().AddReference(f"./variant/{basename}")
        
payloadsLayer.Export(f"{assetDir}/{assetName}.payload.usd")
```

Payload用のStageができたら、その中にVariantSetを作り、
ジオメトリのレイヤーをVariantSetで切り替えできるようにします。

**今回は、指定フォルダ以下にあるレイヤーを切り替えできるようにする**
感じで処理をするので、モデルの置き場所を指定して
Asset以下にコピーしたうえでVariantSetを作ります。
（この辺りはお好みで）

![](https://gyazo.com/1b4f611b3d204416eb55d56a3c963a9a.png)

実行すると、このようなレイヤーが出来上がります。

![](https://gyazo.com/0e366efcb2b2da1a9ca7f8e425e46cf1.png)

payload.usd をusdviewで確認すると、こんな感じになります。
RootPrimにVariantSetが追加され、指定フォルダ以下のLayerがVariantで切り替えできるようになります。

## Inherits作り

次にInheritsするためのレイヤーを用意します。
Referenceは指定Primに対してReferenceするLayerのPath（あるいはSdfPath）を指定しますが
Inheritsは、SdfPathを指定します。
そのため、Inherits用のClassPrimを別レイヤー化したい場合は、
SubLayerと組み合わせる必要があります。

```python
# Inheritsを作る
inheritsStage = Usd.Stage.CreateInMemory()
inheritsLayer = inheritsStage.GetRootLayer()
inheritsStage.CreateClassPrim("/__class__")
inheritsLayer.Export(f"{assetDir}/{assetName}.class.usd")
```

こんな感じで、 __class__ （ Specifierは class ) だけを定義した別レイヤーを作成します。
このように分けておけば、あとで継承したPrimに対して何かしたい場合は
このレイヤーを編集すればOKになります。

## メインのLayerを作る

最後に、実際にレイアウトなどで配置するときに読み込むLayerを作ります。
レイヤー名は、アセット名になるようにして
これまで作成したLayerを読み込みつつ、AssetInfoとKindを指定します。

```python
# Assetsのレイヤーをつくる
stage = Usd.Stage.CreateInMemory()
layer = stage.GetRootLayer()
# そして、AssetsのRoodPrimを作成する
prim = stage.DefinePrim(f'/{assetName}')
rootPath = prim.GetPath()
# Kindを指定
Usd.ModelAPI(prim).SetKind('component')
stage.SetDefaultPrim(prim)

# assetName.usd にはAssetInfoを指定する
assetInfo = {
    "identifier":f"./{assetName}/{assetName}.usd",
    "name":assetName,
    'version':version
}
prim.SetAssetInfo(assetInfo)
# Variantを入れた payload Layer を Payloadする
prim.GetPayloads().AddPayload(f"{assetDir}/{assetName}.payload.usd")

# Inheritsの構造を仕込む
layer.subLayerPaths = [f'./{assetName}.class.usd']
prim.GetInherits().AddInherit('/__class__')

layer.Export(f"{assetDir}/{assetName}.usd")
```

![](https://gyazo.com/ffedff5e328a93184a62ec4ff15b5946.png)

完成した USDファイルを usdview で開いてみます。
Compositionを見ると、Rootになる sampleAssets には SubLayer Inherits Payload Variant
Geomには Reference と、（Specializeを除いた）５つのコンポジションアークを使用した
アセットが出来上がりました。

![](https://gyazo.com/bf39666757b7ee7eb76e7dac2424001c.png)

Meta Data を確認すると、 variant assetInfo kind が指定されています。

## まとめ

以上、Pythonを使用してAssetのセットアップでした。
このようにPythonで書くと、どこで何をして、最終的にどうなるのかが
わかりやすくなるのではと思います。
https://fereria.github.io/reincarnation_tech/60_JupyterNotebook/USD/CompArc/usd-comp-arc/
今回はNotebookで書いたのですが、実際に使う場合は
関数化して、コマンドラインツール化して各種自動化と組み合わせると良いかと思います。
公式のリポジトリの

> USD/extras/usd/examples/usdMakeFileVariantModelAsset/usdMakeFileVariantModelAsset.py

に、今回書いた内容のコマンドラインツールのサンプルがあるので
合わせて確認してみてください。