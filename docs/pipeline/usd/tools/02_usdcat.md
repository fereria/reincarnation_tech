---
slug: /usd/tools/usdcat
title: USDの便利なツールたち (2) usdcat
tags:
    - USD
    - AdventCalendar2021
description: usda <-> usdc 変換をする方法
sidebar_position: 2
---

[USD AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 6 日目は USD に付属する便利ツール usdcat について
紹介したいとおもいます。

## usdcat とは

usdcat は、
https://graphics.pixar.com/usd/release/toolset.html#usdcat
USD ツールの１つで、引数で受け取った usd ファイルを、テキストとして標準出力・またはファイルに出力します。

```
usdcat D:/sample.usd
```

![](https://gyazo.com/40fb6fb0b1aec7a89d60dceee2d3bc56.png)

使用方法は、コマンドプロンプトから usdcat 確認したい usd ファイルを指定します。
指定すると、上のように指定した usd ファイルの中身を表示してくれます。

### USDA - USDC 変換

引数を指定しない場合は、標準出力で usd ファイルの中身を表示するだけですが、
引数を指定することでアスキーとバイナリの変換をすることができます。

```
usdcat D:/sample.usd --usdFormat usdc -o D:/sample2usdc.usd
```

アスキーのファイルをバイナリに変換した例。逆の場合は usdFormat を usda にすることで変換できます。

## flatten/flattenLayerStack

usdcat の機能に flatten という機能があります。
これは、指定の usd のコンポジションをすべてベイクした状態で出力する機能です。

<Gist id="8601a03b53c0293879b56c396ea8ce09" file="cube.usda" />

たとえばこんな Cube の usd ファイルを、

<Gist id="9b0587728f5729d2b740f502e4271f1d" file="root.usda" />

このようにリファレンスしたファイルを usdcat を用意します。

![](https://gyazo.com/2f51800dadeffaeb17da29eb21ccc97f.png)

```
usdcat D:/root.usda
```

--flatten をつけずに実行すると、指定した usda の中身をそのまま（コンポジションなどの情報も含んだまま）
表示されます。

対して、--flatten するとどうなるかというと

![](https://gyazo.com/2c8e77ad215eee73215dacfcfc72783c.png)

--flatten した場合、コンポジションの情報はなくなり１つの usd で完結する状態になりました。
コンポジションがあった部分（refCube に cube.usda の cubePrim がリファレンスされている）はなくなり
コンポジションの結果の Prim になっているのがわかるかとおもいます。

```python
stage = Usd.Stage.Open("D:/root.usda")
print(stage.ExportToString())
```

<Gist id="58bba26aa3bc46ba85f3668d2f6250e6" file="subLayer.usda" />

--flattenLayerStack はすべてを Flatten するのではなく、サブレイヤー部分だけを Flatten します。

<Gist id="e2442096f1e6201a1d7bb5423e41ff0a" file="root.usda" />

こんな感じにサブレイヤーにして実行すると

![](https://gyazo.com/57a176cc72c22841559fd01306b8f08c.png)

このようになります。
サブレイヤーだけ Flatten されていますが、リファレンスは残っているのがわかります。

### mask

mask は、 {{markdown_link('population_mask')}} で説明した OpenMask で指定した Path 以下だけをロード・表示する機能です。

<Gist id="8bad7d6f561150fc1ee197be85d11c85" file="root.usda" />

こんな感じでファイルのうち /a のみロードする場合

```
usdcat --mask /a --flatten D:\root.usda
```

![](https://gyazo.com/d324e3a1a9b4a1e2654e5fb8627b4034.png)

このようになります。

## まとめ

以上が usdcat でした。

usdcat は usdc を usda に変換したりまたその逆をしたりする場合や
手書きの usda のフォーマットが正しいか確認したり、コンポジションの結果を確認したり
大量のレイヤーに分けられた usd を１つにまとめたりといったことが可能になります。

usdchecker と同様、とても便利なツールなのでぜひともお試しください。
