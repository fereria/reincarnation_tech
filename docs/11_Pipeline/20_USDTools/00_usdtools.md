---
title: USDの便利なツールたち (1) checker
tags:
    - USD
    - AdventCalendar2021
---

[USD AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 4日目は USDに付属する便利ツール usdcheckerについて
紹介したいとおもいます。

USDには、シーングラフを扱うライブラリ以外にも、[様々なコマンドライン・GUIツールセット](https://graphics.pixar.com/usd/release/toolset.html)が多数用意されています。
usdviewは、様々な場所で紹介されているので知っている人も多いかとおもいますが、それ以外にも
非常に便利なものが多いので、何回かに分けて便利なツールを紹介していこうと思います。

初回は、USDのデータエラーをチェックしたい場合に使用できる usdcheckerを紹介します。

## usdcheckerとは

https://graphics.pixar.com/usd/release/toolset.html#usdchecker

usdcheckerとは、その名の通り usdまたはusdzファイルを検証して、問題がないかをチェックするための
コマンドラインツールです。
その指定のアセットが、Hydraによってレンダリングで可能であるかを
実行することで確認できます。

## 使い方

まず使用方法。
チェックしたい usdファイルをコマンドプロンプトなどで以下のように指定します。

```bat
usdchecker D:/sample.usda
```

```usda title="sample.usda"
#usda 1.0

def Mesh "😄"
{
}
```

たとえばこんな感じの usda を書いたとしましょう。
こんなPrim定義して大丈夫なのかよ...と思うかと思いますが、

```
Traceback (most recent call last):
  File "C:\USD\bin\usdchecker", line 148, in <module>
    sys.exit(main())
  File "C:\USD\bin\usdchecker", line 118, in main
    checker.CheckCompliance(inputFile)
  File "C:\USD\lib\python\pxr\UsdUtils\complianceChecker.py", line 957, in CheckCompliance
    usdStage = Usd.Stage.Open(inputFile)
pxr.Tf.ErrorException:
        Error in 'textFileFormatYyerror' at line 3116 in file pxr/usd/sdf/textFileFormat.yy : ''😄' is not a valid prim name at '"😄"' in </> on line 3 in file d:\sample.usda
```

こんな不届きなusdaは絶対に、絶対に許さない と、usdcheckerに怒られます。

```usda title="sample.usda
#usda 1.0

def Mesh "sampleMesh"
{
}
```

２バイト文字など許されるわけではない、ということで名前を変えてもう一度確認してみます。

```
[91mStage does not specify an upAxis. (fails 'StageMetadataChecker')[0m
[91mStage does not specify its linear scale in metersPerUnit. (fails 'StageMetadataChecker')[0m
[91mStage has missing or invalid defaultPrim. (fails 'StageMetadataChecker')[0m
Failed!
```

まだ許されませんでした。
ログをみると、**upAxisを指定しろ、metersPerUnitを指定しろ、defaultPrimがない**と怒られているのがわかります。

```
#usda 1.0
(
    defaultPrim="sampleMesh"
    upAxis = "Z"
    metersPerUnit=1
    
)

def Mesh "sampleMesh"
{
}
```

いわれたとおりに修正して、もう一度実行してみます。

```
Success!
```

ようやく許してもらうことができました。
ありがとうusdchecker。

## usdcheckerの引数

チェックしたいファイル以外にも引数を指定することができます。

| 引数                    | 効果                                                                                                                                                |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| --dumpRules             | 引数を追加すると、チェック項目の詳細をDumpしてくれます。                                                                                            |
| --out -o \<outputPath\> | 指定のoutputPathに、チェック結果を保存てくれます                                                                                                    |
| --skiVariants           | 現在の選択されているバリアントのみチェックします                                                                                                    |
| --rooPackageOnly        | 指定のパッケージ以下にネストされているデータはスキップします                                                                                        |
| --arkit                 | arkit用のより厳しいチェック（ARKitRootLayerChecker）をします。<br>例として、upAxisがYか、usdcかどうか、等。                                         |
| --noAssetChecks         | Asset用のチェック（DefaultPrimが指定されているかなど）のような<br>後述のチェックルールのうち、AssetLevelCheck向こうのチェックルールはスキップします |

たとえば、アセットではなくレンダリング用アセットを配置したUSDファイルをチェックして、その結果を
指定ファイルに保存したい場合。

```
usdchecker --noAssetChecks --o c001_results.txt c001_render.usda
```

このようになります。
レンダリングする前など、アセットをパブリッシュする前などに この usdcheckerを挟むことで
ミスを防ぐことができるかと思います。

## 実装をみる

最後に、サクッと実装をみてみます。
USDツールのソースコードは、

> USD/pxr/usd/bin

以下にあります。
usdcheckerであれば bin 以下のusdchecker/usdchecker.py
が、元になります。

チェック本体は、UsdUtilsモジュールから実行することができます。

```python
from pxr import UsdUtils

arKit = False
rootPackageOnly = False
skipVariants = False
verbose = False
noAssetCheck = False


checker = UsdUtils.ComplianceChecker(arkit=arKit, 
                                         skipARKitRootLayerCheck=False, 
                                         rootPackageOnly=rootPackageOnly, 
                                         skipVariants=skipVariants, 
                                         verbose=verbose,
                                         assetLevelChecks=noAssetCheck)

# 指定ファイルをチェック
checker.CheckCompliance("D:/sample.usda")
# 結果を取得 問題なければ空のリストが帰ってくる
print(checker.GetWarnings())
print(checker.GetErrors())
```
> USD/pxr/usd/usdUtils/complianceChecker.py

チェック本体は、このComplianceChecker.pyで、BaseRuleCheckerを継承したクラスを定義し
チェックしたい項目（Stage/Layer等）の指定の名前でチェック関数を定義。
そして GetBaseRules または GetARKitRules に、定義したクラスを指定しています。

実装までは試せていないですが、定型化されているので必要に応じてオリジナルのチェック項目を
簡単にできそうです。

usdcheckerに限らずですが、USDのツールセットはすべてUSDリポジトリ以下にソースコードがあります。
このコード類は、USDを使わなかった場合でも自社ツールを開発するうえでも非常に参考になるサンプルなので
興味がある人はツールを使うだけではなくソースコードも覗いてみるのをお勧めします。

## まとめ

以上、USDツール紹介第一弾 usdcheckerでした。
レンダリングした後にデータのミスが見つかり、もう一度レンダリングをし直す...というのは
CG屋あるあるだと思います。
そういった悲劇を防ぐためにもデータのチェックはとても大切です。
USDを使用したパイプラインを構築する場合は、ぜひとも導入したいツールの１つです。