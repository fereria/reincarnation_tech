---
title: BlenderのAssetLibrary
tags:
    - Blender
    - Asset
description: BlenderでのAssetLibraryの基本的な使い方
---

Blender の AssetLibrary システムは、Blender3.0 から新しく追加されました。
Blender で Asset をレイアウトしたりする場合などに扱える機能ですが
それがどういうもので、どう扱うのかまずは基本的なところから書いていこうと思います。

## Blender の Asset とは

まず、Blender における「Asset」が何を指しているのかというと

> An asset is a data-block with meaning.

意味をもつ「Data-Block」のことを指します。
この場合の Data-Block とは、Blender のオブジェクトやマテリアル、テクスチャなどを指します。
この Data-Block に対して Asset とマークをすることで
AssetLibrary からレイアウトしたりすることが可能になるのが、
こんかい解説する AssetLibrary になります。

## ライブラリに追加する

Blender の Library に登録するには、登録したい Asset のオブジェクトに「Mark as Asset」で Mark を入れます。

![](https://gyazo.com/81a91b867b7551004138bc948faab3ae.png)

![](https://gyazo.com/bd096b3d680a22ed6c2c7a1793ade85f.png)

追加すると、

![](https://gyazo.com/ab88dd557c10e0351c142859235a6980.png)

Browser の Current File に、ObjectName で新しく Asset が追加されます。

![](https://gyazo.com/6516ef36ed7e2f82700fa22cf7720445.png)

Asset にしたものは、レイアウトのもとになるデータになるので、
別の Collection 以下に移動して、デフォルトでは非表示にしておきます。

![](https://gyazo.com/4ec8f93faaab1a8c87ba49777a80d789.gif)

準備ができたら、AssetBrowser からレイアウトしたい Asset を Viewport に Drag＆Drop します。
登録した Asset をレイアウトできるようになりました。
↑ の動作を見ればわかる通り、配置しているオブジェクトに設置する形で
オブジェクトを配置できるようになっているのがわかります。

![](https://gyazo.com/f72c6bedcc5e7ce5589a3bd652e9af8f.png)

オブジェクト以外でも、Asset に登録することができて、
Material からも登録することができます。

![](https://gyazo.com/165cb41e8cb9ebfa64b5832a23e3d2e2.png)

登録されたマテリアルはこのようになります。

## 別ファイルの Asset を配置する

Asset 管理をする場合、同じファイルでアセットを作るのではなく
Asset は別のファイルに Asset データを作成し、レイアウトファイルに配置をしたくなります。

![](https://gyazo.com/5e485d90cd19e8505bdddde2e51d2b30.png)

Asset は、Preferences の File Paths に Asset の Blender ファイル置き場を指定して
その下の Blender ファイルを Asset のロード元にすることができます。

https://www.blender.org/download/demo-files/

試しに、Blender のサンプルファイル Asset Demo Bundles の Cube Diorama を、

![](https://gyazo.com/31fdbccd0fe480fcd7d933fcb27210d7.png)

指定の AssetLibraries の Dir 下に置きます。

![](https://gyazo.com/15a6e6f5fc791eab9f04221bb283be3b.png)

AssetLibraries に追加した Path は、AssetBrowser で切り替えることができます。
今回の場合、User Library に .blend ファイルを配置したので、 User Library に切り替えます。

![](https://gyazo.com/be85b55cc1196136b594c78c4fa36e52.png)

切り替えると、指定 Dir 下にある blend 内にある Asset データを、Browser に表示することができます。

## Reuse

別ファイルの Asset を読み込んだ場合、配置するオブジェクトの扱いを切り替えることができます。

![](https://gyazo.com/7967cbf16042b0ee2deaa4f6efe0a611.png)

デフォルトだと、 Append(Reuse Data)になっています。

![](https://gyazo.com/011a509d527b2e30dac15a9651ea6877.png)

Reuse Data の場合は、いわゆるインスタンスのような状態になっていて、同じ Data-Block の Mesh などを共有
するように配置されます。

## まとめ

Blender ファイルに Asset マークを付けるだけで、簡単に Asset 化できることがわかりました。
Data-Block を Asset として扱えるこの AssetLibraries は Blender でアセット作成からレイアウト、ライティングなどの一連の
工程を行うのに非常に便利な機能に思えました。
