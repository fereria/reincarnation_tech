---
title: USD と MaterialX
tags:
    - USD
    - AdventCalendar2022
    - MaterialX
description: USDでMaterialXを使用した場合の話
---

[Universal Scene Description AdventCalendar2022](https://qiita.com/advent-calendar/2022/usd) 日目は、 USD の MaterialX です。

## MaterialX とは？

MaterialX とはなにかというと、

> シェーダーグラフの定義や material のアサインメントを XML 形式のファイルによって
> 異なったＤＣＣツール間でデータ交換するしくみ
> 参考: https://qiita.com/kit2cuz/items/d4459493248b147f4ea6

です。
USD が、異なるツール間のシーングラフを行き来するためのフォーマットであるのに対して
MaterialX は、それのマテリアル版ともいうべきものです。

似たようなものとして、nVidia の MDL 言語や、Open Shading Language(OSL)と呼ばれるものが存在していますが、
MaterialX は Houdini の Karma や AMD の ProRender、ArnoldRender といった各種レンダラーによってサポートされ
スタンダードなフォーマットになりつつあります。

このあたりの MaterialX についてのもろもろは、 2021 の Houdini アドカレで、 @kit2cuz さんが [MaterialX で遊ぶ](https://qiita.com/kit2cuz/items/d4459493248b147f4ea6)という記事内で、とても分かりやすくまとめられているのでそちらを参照してみてください。

## USD と MaterialX

そんな MaterialX ですが、USD でも扱うことが可能です。

USD にも Material や Shader を表現するための構造は存在していますが
デフォルトで用意されているのは UsdPreviewSurface のみだし、ネットワークの表現に関しても足りていません。

そういった事情から、現時点では USD の ShadingNetwork を使用するというよりも
マテリアル部分に関しては MaterialX を使用するような構造になっています。

どのような対応になっているかというと、対応方法はざっくり 2 種類あります。
1 つ目が、 UsdMtlx (MaterialX FileFormat and Shader Plugins) を使用して、 mtlx ファイルを USD のシーングラフとして取り込み

![](https://gyazo.com/3f056ecc90f9f19f59222d9f86102542.png)

UsdShadeShader の id によって、MaterialX のノードを表現する方法です。

以前にも {{markdown_link('fileformat_plugin')}} という記事を書いたのですが、
1 つ目の例の場合、mtlx ファイルを USD の FileFormatPlugin が USD のシーングラフとして解釈し
USD で扱える形にインポートしています。

2 つめが、mtlx のファイルパスを Attribute として保存し、レンダラはこの filePath の mtlx を解釈して使用するパターンです。
https://zenn.dev/remiria/articles/18c724e281c164
過去に書いた記事で Blender の UsdHydraAddon がこの形式になっていて
この場合だと、USD の FileFormatPlugin が未対応のマテリアルも対応できます。
ただし、最近調べた ProRender だと外部ファイルとしてではなく USD のシーングラフとして MaterialX の構造を
構築していたので、今後は 1 つ目の方式に統一されていくのではないかと思います。

## 読んでみる

ということで、ここまでで概要は説明できたので実際に usdview で確認してみます。
デフォルトのビルドだと MaterialX はビルドされていないので、オプションを入れて USD をビルドします。

```bat
python build_scripts\build_usd.py --materialx C:\USD
```

MaterialX の Plugin ありでビルドする場合は --materialx を入れておきます。

ビルドできたら、usdview で MaterialX のサンプルデータを開きます。
サンプルは、
https://github.com/AcademySoftwareFoundation/MaterialX
Github のリポジトリ以下に、 resources/Materials/Examples/UsdPreviewSurface というのがあるので
これを開いてみます。

```
usdview resources\Materials\Examples\UsdPreviewSurface\usd_preview_surface_glass.mtlx
```

拡張子やファイルフォーマットは USD ではありませんが、上のように usdview にそのまま投入します。

![](https://gyazo.com/69889187dbb67b8c5581abe94639f1c2.png)

MaterialX のプラグインがビルドされていれば、このようにロードができました。

![](https://gyazo.com/79f7fc0a8cbf7276a872ebcfab32f246.png)

UsdPreview 以外のものも開いてみます。
ShaderPrim は、それぞれ id によって MaterialX のノードに対応されていて
USD の構造で、MaterialX が表現されているのがわかります。

### 対応関係を見る

#### input output

何がどのノードに対応しているか、どのように解釈されるかは
公式の UsdMtlx ドキュメント以下にまとめられています。
https://graphics.pixar.com/usd/release/api/usd_mtlx_page_front.html
そこを見ながら確認すると

![](https://gyazo.com/5958b3d529ae545d8a5fab90ee710766.png)

このように、 <input ～ となっているものは、inputs:～のアトリビュートとして追加されます。
これは、以前 {{markdown_link('06_shader')}} で詳細は書いているのですが
USD のマテリアルのネットワークを作成するときは input と output を作成し
それを ConnectToSource で接続することで ShadingNetwork を構成しています。

#### nodegraph

![](https://gyazo.com/adf08643fbaeaf47698c9d0f7e7d449e.png)

nodegraph であれば、

![](https://gyazo.com/f7bfd0b4ebf90ca0f7e8b4093a9afb56.png)

UsdShadeGraph によって表現されます。

以前は、開こうと思ってもエラーになってしまうことがおおい印象でしたが
現在は問題なく FileFormatPlugin で変換できるようです。

#### Houdini の場合

Houdini の場合、Karma のマテリアルは MaterialX で構築できます。

ボーンデジタル社による [Solaris で MaterialX ファイルを保存して、再利用する](https://support.borndigital.co.jp/hc/ja/articles/13156119863705) という記事でこのあたりの内容が書かれていますが、

![](https://gyazo.com/65100479d4340fd5512b9fd827a249ca.png)

通常、MaterialX で作ったネットワークは、

![](https://gyazo.com/20ddcbda3745df172b4bc17a6ed2ddee.png)

USD のシーングラフとして、このように Material そして Shader として表示されていますが
別途、このファイルを使いまわすことも可能で、その場合 mtlx で出力し
File ノードでインポートしています。

File ノードでインポートしてるのは、今回説明した FileFormatPlugin を使用して
mtlx を USD の形式に再度解釈することでインポートさせています。

このあたりの Houdini の USD との相性の良さはさすがだなぁと思います。

## まとめ

そんな感じで、USD と MaterialX の関係性をまとめてみました。
MaterialX がすべてのレンダラーで同じように使用できるようになるまでは、
まだ時間がかかるとは思います。
しかし、近い未来には USD がシーングラフの共通言語になっていったように
MaterialX も業界の標準として共通化されるのでは？とおもっています。
（USD + MaterialX が標準になるのだろうか）

そんな未来を見据えて、MaterialX 側ももう少し現況していこうかなと思います。

## 参考

-   https://support.borndigital.co.jp/hc/ja/articles/13156119863705
-   https://qiita.com/kit2cuz/items/d4459493248b147f4ea6
