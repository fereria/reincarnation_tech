---
title: USDの便利なツールたち (1) checker
tags:
    - USD
    - AdventCalendar2021
description: USDのデータをチェックする機能の使い方
order: 0
---

[USD AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 4 日目は USD に付属する便利ツール usdchecker について
紹介したいとおもいます。

USD には、シーングラフを扱うライブラリ以外にも、[様々なコマンドライン・GUI ツールセット](https://graphics.pixar.com/usd/release/toolset.html)が多数用意されています。
usdview は、様々な場所で紹介されているので知っている人も多いかとおもいますが、それ以外にも
非常に便利なものが多いので、何回かに分けて便利なツールを紹介していこうと思います。

初回は、USD のデータエラーをチェックしたい場合に使用できる usdchecker を紹介します。

## usdchecker とは

https://graphics.pixar.com/usd/release/toolset.html#usdchecker

usdchecker とは、その名の通り usd または usdz ファイルを検証して、問題がないかをチェックするための
コマンドラインツールです。
その指定のアセットが、Hydra によってレンダリングで可能であるかを
実行することで確認できます。

## 使い方

まず使用方法。
チェックしたい usd ファイルをコマンドプロンプトなどで以下のように指定します。

```bat
usdchecker D:/sample.usda
```

{{'c9b5d59bd398f9a87fdc2dd6a1d453b8'|gist}}

たとえばこんな感じの usda を書いたとしましょう。
こんな Prim 定義して大丈夫なのかよ...と思うかと思いますが、

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

こんな不届きな usda は絶対に、絶対に許さない と、usdchecker に怒られます。

{{'721b03ee90083c0373ebf27020fe6eb6'|gist}}

２バイト文字など許されるわけではない、ということで名前を変えてもう一度確認してみます。

```
[91mStage does not specify an upAxis. (fails 'StageMetadataChecker')[0m
[91mStage does not specify its linear scale in metersPerUnit. (fails 'StageMetadataChecker')[0m
[91mStage has missing or invalid defaultPrim. (fails 'StageMetadataChecker')[0m
Failed!
```

まだ許されませんでした。
ログをみると、**upAxis を指定しろ、metersPerUnit を指定しろ、defaultPrim がない**と怒られているのがわかります。

{{'e429922483916c6da418182495819a50'|gist}}

いわれたとおりに修正して、もう一度実行してみます。

```
Success!
```

ようやく許してもらうことができました。
ありがとう usdchecker。

## usdchecker の引数

チェックしたいファイル以外にも引数を指定することができます。

| 引数                    | 効果                                                                                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| --dumpRules             | 引数を追加すると、チェック項目の詳細を Dump してくれます。                                                                                             |
| --out -o \<outputPath\> | 指定の outputPath に、チェック結果を保存てくれます                                                                                                     |
| --skiVariants           | 現在の選択されているバリアントのみチェックします                                                                                                       |
| --rooPackageOnly        | 指定のパッケージ以下にネストされているデータはスキップします                                                                                           |
| --arkit                 | arkit 用のより厳しいチェック（ARKitRootLayerChecker）をします。<br>例として、upAxis が Y か、usdc かどうか、等。                                       |
| --noAssetChecks         | Asset 用のチェック（DefaultPrim が指定されているかなど）のような<br>後述のチェックルールのうち、AssetLevelCheck 向こうのチェックルールはスキップします |

たとえば、アセットではなくレンダリング用アセットを配置した USD ファイルをチェックして、その結果を
指定ファイルに保存したい場合。

```
usdchecker --noAssetChecks --o c001_results.txt c001_render.usda
```

このようになります。
レンダリングする前など、アセットをパブリッシュする前などに この usdchecker を挟むことで
ミスを防ぐことができるかと思います。

## 実装をみる

最後に、サクッと実装をみてみます。
USD ツールのソースコードは、

> USD/pxr/usd/bin

以下にあります。
usdchecker であれば bin 以下の usdchecker/usdchecker.py
が、元になります。

チェック本体は、UsdUtils モジュールから実行することができます。

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

チェック本体は、この ComplianceChecker.py で、BaseRuleChecker を継承したクラスを定義し
チェックしたい項目（Stage/Layer 等）の指定の名前でチェック関数を定義。
そして GetBaseRules または GetARKitRules に、定義したクラスを指定しています。

実装までは試せていないですが、定型化されているので必要に応じてオリジナルのチェック項目を
簡単にできそうです。

usdchecker に限らずですが、USD のツールセットはすべて USD リポジトリ以下にソースコードがあります。
このコード類は、USD を使わなかった場合でも自社ツールを開発するうえでも非常に参考になるサンプルなので
興味がある人はツールを使うだけではなくソースコードも覗いてみるのをお勧めします。

## まとめ

以上、USD ツール紹介第一弾 usdchecker でした。
レンダリングした後にデータのミスが見つかり、もう一度レンダリングをし直す...というのは
CG 屋あるあるだと思います。
そういった悲劇を防ぐためにもデータのチェックはとても大切です。
USD を使用したパイプラインを構築する場合は、ぜひとも導入したいツールの１つです。
