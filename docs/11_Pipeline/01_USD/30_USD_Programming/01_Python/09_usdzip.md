---
title: pythonでusdz
tags:
    - USD
description: Pythonでusdzを作成したり読んだりする
---

[USD AdventCalendar2022](https://qiita.com/advent-calendar/2022/usd) 23 日目は、python で usdz を扱う話です。

usdz とは、 usd ファイル、画像、オーディオデータを zip ファイルでパッケージングしたファイルフォーマットです。

## サンプルをみてみる

まずはサンプルを見てみます。

https://github.com/usd-wg/assets

USD の主にスキーマのテスト用アセットなどを公開している[ASWF USD WG](https://wiki.aswf.io/display/WGUSD)にある、 full_assets/ElephantWithMonochord を見てみます。

:fa-external-link: [Usdz File Format Specification](https://graphics.pixar.com/usd/release/spec_usdz.html)

![](https://gyazo.com/66e9d9f9262e2dbb0a5f99ebdcf5256d.png)

このサンプルには、usd 本体以外に、テクスチャとオーディオデータも含まれています。

![](https://gyazo.com/f2cae81be8af0922e70eb82bf37ad5c3.png)

オーディオデータを見ると filePath に mp3 が指定されていたり、

![](https://gyazo.com/70bf403251bac3e855e9d0052cf42599.png)

Texture には png が使用されているのがわかります。

![](https://gyazo.com/5de92a315af940fe5b0537ed54879395.png)

usdz は zip ファイルなので、拡張子を zip に変更すると中身を見ることができます。

![](https://gyazo.com/4b11ef1928e852c3c7dd029f08018d0e.png)

zip ファイルをの中をみると、 usdc (usd バイナリー) が置かれています。

![](https://gyazo.com/9b6a1fabf1915cdd5c11aae06c4355d3.png)

0 の中には、テクスチャとオーディオファイルが入っています。

このように、usdz にすることで
3DCG のアセットデータだけではなく、テクスチャ等も含めて 1 つのファイルとして扱えるようになりますので
Apple の [AR Quick Look](https://developer.apple.com/jp/augmented-reality/quick-look/) のように、AR で表示するデータなどのフォーマットとしても使用されています。

## 作る

usdzip を使った作り方等は {{markdown_link('02_usdzip')}} にまとめてありますので
そちらを参照してください。

```python
from pxr import Usd,Ar,Sdf
import os.path

with Usd.ZipFileWriter.CreateNew("D:/sample.usdz") as usdwriter:
    for root,dirs,files in os.walk("D:/usdzSample"):
        for i in files:
            usdwriter.AddFile(os.path.join(root,i))
```

作る場合は Python でも簡単にできます。
UsdZipFileWriter というクラスが用意されていますので、これを利用して
usdz に入れたいファイルを AddFile することで、
usdz 化できます。

## 読み込む

usdz の場合は、usdc や usda と同じように UsdStage で開くことができます。

```python
stage = Usd.Stage.Open("D:/SoC-ElephantWithMonochord.usdz")
```

扱いは他と同じですね。

## 中身を確認する

usd ファイルとしてステージを開くのであれば、 UsdStageOpen で良いですが
そうではなく zip に含まれるファイルを取得したいこともあります。
その場合は、UsdZipFile を使用します。

```python
zipfile = Usd.ZipFile.Open("D:/SoC-ElephantWithMonochord.usdz")

for f in zipfile.GetFileNames():
    print(f)
```

![](https://gyazo.com/11a1707140147387b49a1ce888ea94be.png)

GetFileNames で、usdz に含まれているファイルを確認すると
zip 以下の相対パスで、ファイル名を確認できます。

```python
from PIL import Image,ImageOps
import io

img = zipfile.GetFile("0/Monochord_diff.png")
i = Image.open(io.BytesIO(img))
i
```

![](https://gyazo.com/8049ee25efe4e893fa936afde6a23876.png)

zipfile の GetFile を使用すると、zipfile 内のバイナリデータを取得できます。
ので、これを利用して、Pillow で開き
jupyternotebook で画像を表示することなどができます。

このように、UsdZipFile を使用して開けば
zip に含まれている画像ファイルを Pillow の Image で取得したりもできるので
画像付きパラメーターファイルとして usdz を使用するみたいなことも可能になります。

:fa-external-link: [参考 usdzip の中身を読んでみる](https://github.com/fereria/notebooks/blob/master/USD/UsdZip/load_img__usdzip%E3%81%AE%E4%B8%AD%E3%81%AE%E7%94%BB%E5%83%8F%E3%82%92%E8%AA%AD%E3%81%BF%E8%BE%BC%E3%82%93%E3%81%A7%E3%81%BF%E3%82%8B.ipynb)

## Stage を開いて、テクスチャパスを確認してみる

UsdZipFile を使用して zip の中身を確認したり取得したりできるのはわかりましたが
最後に、Stage からテクスチャのパスがどのようになっているのかみてみます。

```python
prim = stage.GetPrimAtPath("/SoC_ElephantWithMonochord/Materials/Elefant_Mat_68050/PreviewSurface/_MainTex")
texPath = prim.GetAttribute("inputs:file").Get()

print(texPath.resolvedPath)
```

![](https://gyazo.com/28f8df94a5a58e676ddb000291625cc7.png)

テクスチャの inputs:file アトリビュートは [AssetPath](https://graphics.pixar.com/usd/release/glossary.html#asset) タイプで取得できます。
AssetPath は、Resolver によって解決されるもので

```python
texPath.path
```

とすれば

![](https://gyazo.com/5c455b71e24c54b09380d0cd32e42770.png)

未解決の、ファイルに記述されたテキストが取得され、

```python
texPath.resolvedPath
```

だと、

![](https://gyazo.com/3121123bbb5a3bb54d63cfd5fc6abdfd.png)

最終的に解決済のファイルパスを取得できます。
usdz の場合だと、zip 内にファイルが存在しているので
usdz[相対パス] のような形で、resolvedPath を得ることができます。
