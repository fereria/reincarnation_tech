---
title: USDの便利なツールたち (3) usdzip
tags:
    - USD
    - AdventCalendar2021
---

[USD AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 18日目は USDに付属する便利ツール usdzipについて
紹介したいとおもいます。

## usdzipについて

usdzipとは、usdファイルからusdzパッケージを作成することができるコマンドラインツールです。

### usdz

https://graphics.pixar.com/usd/release/wp_usdz.html

USDのアセット（usdファイル、テクスチャなどを含む）をzipで１つのファイルにアーカイブしたものです。
AppleのArKitで使用されていたり、iPhoneの 3d Scanner App などからはテクスチャとスキャンしたモデルを
出力するためなどに使用されています。

{{'https://twitter.com/fereria/status/1350777261335564288'|twitter}}

以前 3d Scanner Appを使用してモデルをスキャン＆PCにもってきて usdview で眺めてみた例。
この例だと、 usdz にはスキャンしたときのテクスチャも含まれていて
usdviewでみると、テクスチャも表示された状態になります。

こんなかんじで、 usdz はテクスチャ等も含んだアセットのパッケージとして
使用することができて、この usdz を作成することができるツールが usdzip です。

## つかってみる

実際に使ってみます。

```
usdzip D:\usdzSample\sample.usdz D:\usdzSample\sample.usd
```

最もシンプルな使い方は、
usdzip ＜usdzの出力先＞ ＜USDファイルパス＞
このように、usdzにしたいファイルを指定します。

### フォルダを指定する

上の例の場合は、単一のusdファイルがusdzファイルになりますが、Kitchen_setのように
複数のアセットを含むデータを usdzにしたい場合は、以下のようにします。

```
usdzip D:/kitchen_set.usdz D:\Kitchen_set -r
```

inputPathをディレクトリにした上で、 -r (recursive) のフラグを入れると
指定のフォルダ以下をすべて usdz にすることができます。
(指定しない場合、assets以下のサブディレクトリはusdzに入らないので注意)

![](https://gyazo.com/9f3ea9f4e76cb93c8ab6809c0247bbf4.png)

usdzipにすると、ReferenceのAssetPathは usdzip内のPathになります。

![](https://gyazo.com/ae7995b486322659107a11f80d1152fb.png)

usdzは、最初に説明した通りzipファイルなので
zipにリネームすると中身を除くことができます。

### usdzのデータに含まれるファイルを確認する

```
usdzip -l D:\kitchen_set.usdz
```

usdzipを使用すれば、 usdz 内にどんなファイルが含まれているのか確認することができます。

### resolverとの組み合わせ

usdzipにしているPathは、 --asset ASSET_PATH と指定することで
Resolverを経由したPathからusdzを作成できます。

!!! info
    ただし usdResolverExampleだと Resolveですべてを解決されたファイルが取得できないので
    usdzip --asset asset:Buzz/Buzz.usd D:/buzz.usdz
    は上手くいかないので、ResolverPluginでの _Resolve の実装をやる必要がある
    
## Python で実行する

usdzip の内部実装をみると、Pythonからも実行できることがわかるので試しにやってみます。

```python
from pxr import Usd,Ar,Sdf

with Usd.ZipFileWriter.CreateNew("D:/usdzSample/sample.usdz") as usdwriter:
    usdwriter.AddFile('D:/usdzSample/sample.usd')
```

作成方法は、 Usd.ZipFileWrite を使用して、
usdzに入れたいファイルを AddFile すればＯＫです。

```python
zipFile = Usd.ZipFile.Open("D:/usdzSample/sample.usdz")

for fileName in zipFile.GetFileNames():
    fileinfo = zipFile.GetFileInfo(fileName)
    print(fileinfo.dataOffset)
    print(fileinfo.size)
    print(fileinfo.uncompressedSize)
```

usdz内のファイル情報は、 ZipFile.Openして、 GetFileNames() から取得できます。

```python
stage = Usd.Stage.Open("D:/usdzSample/sample.usdz")
print(stage.ExportToString())
```

ファイルの情報ではなくStageを取得したい場合は、
通常のusdファイルと同様です。

> pxr/usd/bin/usdzip/usdzip.py

usdzipはすべてのコードがPythonなので、
このコードを見ると、何が行われているかわかります。

## まとめ

以上 usdzipの使いかたとPythonでのusdzの作り方でした。
usdzipを使用して、アセットをusdzにすると
テクスチャを含めたアセットを１つのパッケージとして扱えるようになります。

また、usdzip には arKit 用のオプションも用意されていて
その場合は UsdUtils.UsdUtilsCreateNewARKitUsdzPackage で指定の処理がされるようになっています。
（コンポジションがある場合、Flattenして usdc にしてExport？）

デフォルトで付属している usdzip だと、ディレクトリ以下をusdzにするだけですが
事前に収集して usdzip するなど自動化したり
AssetResolverと組み合わせて usdzip 化すると、データを配布したり
するのがやりやすくなるのでは？と思います。