---
title: USDの便利なツールたち (2) usdcat
tags:
    - USD
    - AdventCalendar2021
---

[USD AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 6日目は USDに付属する便利ツール usdcatについて
紹介したいとおもいます。

## usdcatとは

usdcatは、
https://graphics.pixar.com/usd/release/toolset.html#usdcat
USDツールの１つで、引数で受け取った usdファイルを、テキストとして標準出力・またはファイルに出力します。

```
usdcat D:/sample.usd
```

![](https://gyazo.com/40fb6fb0b1aec7a89d60dceee2d3bc56.png)

使用方法は、コマンドプロンプトから usdcat 確認したいusdファイルを指定します。
指定すると、上のように指定したusdファイルの中身を表示してくれます。

### USDA - USDC変換

引数を指定しない場合は、標準出力でusdファイルの中身を表示するだけですが、
引数を指定することでアスキーとバイナリの変換をすることができます。
```
usdcat D:/sample.usd --usdFormat usdc -o D:/sample2usdc.usd
```
アスキーのファイルをバイナリに変換した例。逆の場合は usdFormat を usda にすることで変換できます。

## flatten/flattenLayerStack

usdcatの機能に flattenという機能があります。
これは、指定のusdのコンポジションをすべてベイクした状態で出力する機能です。

{{'8601a03b53c0293879b56c396ea8ce09'|gist}}

たとえばこんなCubeのusdファイルを、

{{'9b0587728f5729d2b740f502e4271f1d'|gist}}

このようにリファレンスしたファイルを usdcat を用意します。

![](https://gyazo.com/2f51800dadeffaeb17da29eb21ccc97f.png)

```
usdcat D:/root.usda
```

--flattenをつけずに実行すると、指定したusdaの中身をそのまま（コンポジションなどの情報も含んだまま）
表示されます。

対して、--flatten するとどうなるかというと

![](https://gyazo.com/2c8e77ad215eee73215dacfcfc72783c.png)

--flattenした場合、コンポジションの情報はなくなり１つのusdで完結する状態になりました。
コンポジションがあった部分（refCubeに cube.usdaの cubePrimがリファレンスされている）はなくなり
コンポジションの結果のPrimになっているのがわかるかとおもいます。

```python
stage = Usd.Stage.Open("D:/root.usda")
print(stage.ExportToString())
```

--flattenLayerStackはすべてをFlattenするのではなく、サブレイヤー部分だけをFlattenします。

{{'58bba26aa3bc46ba85f3668d2f6250e6'|gist}}

{{'e2442096f1e6201a1d7bb5423e41ff0a'|gist}}

こんな感じにサブレイヤーにして実行すると

![](https://gyazo.com/57a176cc72c22841559fd01306b8f08c.png)

このようになります。
サブレイヤーだけFlattenされていますが、リファレンスは残っているのがわかります。

### mask

maskは、 [PopulationMask](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/19_population_mask/) で説明したOpenMaskで指定したPath以下だけをロード・表示する機能です。

{{'8bad7d6f561150fc1ee197be85d11c85'|gist}}

こんな感じでファイルのうち /a のみロードする場合

```
usdcat --mask /a --flatten D:\root.usda
```

![](https://gyazo.com/d324e3a1a9b4a1e2654e5fb8627b4034.png)

このようになります。

## まとめ

以上が usdcat でした。

usdcatは usdcをusdaに変換したりまたその逆をしたりする場合や
手書きのusdaのフォーマットが正しいか確認したり、コンポジションの結果を確認したり
大量のレイヤーに分けられたusdを１つにまとめたりといったことが可能になります。

usdcheckerと同様、とても便利なツールなのでぜひともお試しください。