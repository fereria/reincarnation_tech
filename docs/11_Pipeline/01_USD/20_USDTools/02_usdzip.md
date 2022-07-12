---
title: USDの便利なツールたち (3) usdzip
tags:
    - USD
    - AdventCalendar2021
description: usdzipの作り方
---

[USD AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 18 日目は USD に付属する便利ツール usdzip について
紹介したいとおもいます。

## usdzip について

usdzip とは、usd ファイルから usdz パッケージを作成することができるコマンドラインツールです。

### usdz

https://graphics.pixar.com/usd/release/wp_usdz.html

USD のアセット（usd ファイル、テクスチャなどを含む）を zip で１つのファイルにアーカイブしたものです。
Apple の ArKit で使用されていたり、iPhone の 3d Scanner App などからはテクスチャとスキャンしたモデルを
出力するためなどに使用されています。

{{'https://twitter.com/fereria/status/1350777261335564288'|twitter}}

以前 3d Scanner App を使用してモデルをスキャン＆PC にもってきて usdview で眺めてみた例。
この例だと、 usdz にはスキャンしたときのテクスチャも含まれていて
usdview でみると、テクスチャも表示された状態になります。

こんなかんじで、 usdz はテクスチャ等も含んだアセットのパッケージとして
使用することができて、この usdz を作成することができるツールが usdzip です。

## つかってみる

実際に使ってみます。

```
usdzip D:\usdzSample\sample.usdz D:\usdzSample\sample.usd
```

最もシンプルな使い方は、
usdzip ＜ usdz の出力先＞ ＜ USD ファイルパス＞
このように、usdz にしたいファイルを指定します。

### フォルダを指定する

上の例の場合は、単一の usd ファイルが usdz ファイルになりますが、Kitchen_set のように
複数のアセットを含むデータを usdz にしたい場合は、以下のようにします。

```
usdzip D:/kitchen_set.usdz D:\Kitchen_set -r
```

inputPath をディレクトリにした上で、 -r (recursive) のフラグを入れると
指定のフォルダ以下をすべて usdz にすることができます。
(指定しない場合、assets 以下のサブディレクトリは usdz に入らないので注意)

![](https://gyazo.com/9f3ea9f4e76cb93c8ab6809c0247bbf4.png)

usdzip にすると、Reference の AssetPath は usdzip 内の Path になります。

![](https://gyazo.com/ae7995b486322659107a11f80d1152fb.png)

usdz は、最初に説明した通り zip ファイルなので
zip にリネームすると中身を除くことができます。

### usdz のデータに含まれるファイルを確認する

```
usdzip -l D:\kitchen_set.usdz
```

usdzip を使用すれば、 usdz 内にどんなファイルが含まれているのか確認することができます。

### resolver との組み合わせ

usdzip にしている Path は、 --asset ASSET_PATH と指定することで
Resolver を経由した Path から usdz を作成できます。

!!! info
ただし usdResolverExample だと Resolve ですべてを解決されたファイルが取得できないので
usdzip --asset asset:Buzz/Buzz.usd D:/buzz.usdz
は上手くいかないので、ResolverPlugin での \_Resolve の実装をやる必要がある

## Python で実行する

usdzip の内部実装をみると、Python からも実行できることがわかるので試しにやってみます。

```python
from pxr import Usd,Ar,Sdf

with Usd.ZipFileWriter.CreateNew("D:/usdzSample/sample.usdz") as usdwriter:
    usdwriter.AddFile('D:/usdzSample/sample.usd')
```

作成方法は、 Usd.ZipFileWrite を使用して、
usdz に入れたいファイルを AddFile すればＯＫです。

```python
zipFile = Usd.ZipFile.Open("D:/usdzSample/sample.usdz")

for fileName in zipFile.GetFileNames():
    fileinfo = zipFile.GetFileInfo(fileName)
    print(fileinfo.dataOffset)
    print(fileinfo.size)
    print(fileinfo.uncompressedSize)
```

usdz 内のファイル情報は、 ZipFile.Open して、 GetFileNames() から取得できます。

```python
stage = Usd.Stage.Open("D:/usdzSample/sample.usdz")
print(stage.ExportToString())
```

ファイルの情報ではなく Stage を取得したい場合は、
通常の usd ファイルと同様です。

> pxr/usd/bin/usdzip/usdzip.py

usdzip はすべてのコードが Python なので、
このコードを見ると、何が行われているかわかります。

## まとめ

以上 usdzip の使いかたと Python での usdz の作り方でした。
usdzip を使用して、アセットを usdz にすると
テクスチャを含めたアセットを１つのパッケージとして扱えるようになります。

また、usdzip には arKit 用のオプションも用意されていて
その場合は UsdUtils.UsdUtilsCreateNewARKitUsdzPackage で指定の処理がされるようになっています。
（コンポジションがある場合、Flatten して usdc にして Export？）

デフォルトで付属している usdzip だと、ディレクトリ以下を usdz にするだけですが
事前に収集して usdzip するなど自動化したり
AssetResolver と組み合わせて usdzip 化すると、データを配布したり
するのがやりやすくなるのでは？と思います。
