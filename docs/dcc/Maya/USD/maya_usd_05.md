---
slug: /maya/maya_usd/05
title: MayaUSDでマテリアルを扱おう
description: LookDevXの基本的な使い方
sidebar_position: 5
---

MayaUSD の基本、Bifrost など見てきましたが MayaUSD の基本編最後は「マテリアル」です。  
以前は、マテリアルアサインもろくにできないような惨状でしたが  
2025 では一通りの作業ができるようになっていたので、順番に見ていきます。

:::warning

今回は MaterialX でのマテリアルの作り方などには触れません。  
あくまでも Maya ＋ USD でどのように扱われているかを詳しく調べる回になりますので  
ご注意ください！！

:::

## シンプルなマテリアル作成・アサイン

まず、最も基本的な手順を見ていきます。  
あらかじめ、UsdProxyShape を作成し、Sphere を作成しておきます。

![](https://gyazo.com/495e61b4e5ece1ab8868a3712c24e74a.png)

作成方法は、Maya 世界で Sphere を作り  
選択＞ Duplicate As USD Data で、送りたい USD 世界を選択します。

![](https://gyazo.com/0a79f9b18150e8aaca4b1c366e9c3199.png)

そのあと、Sphere を選び「Assign New Material」から USD ＞ USD Preview Surface  
を選択します。

![](https://gyazo.com/2c3fe7858723f76b5bbd9f24ca09eb69.png)

これで、USD の世界に PreviewSurface の Material/Shader が作成されました。

![](https://gyazo.com/16c04bed6967ae7ba1ef527f5e8e7511.png)

作成した Shader を選ぶと（Material ではない）  
このように AttributeEditor で、マテリアルを編集することができます。

![](https://gyazo.com/5ef76bd61ed91e6564c05fadfcd67e23.png)

DiffuseColor を赤にすると、  
このようにマテリアルがアサインされていることが確認できます。

おおむね、これまでの Maya での作業と同じ感覚でマテリアルを作成・アサインできるようになっています。

## LookDevX

シンプルなものであれば以上で終了なのですが、実際にはもう少しちゃんとマテリアルを設定したくなるはずです。  
そうした場合は、これまでの HyperShade とは別のツールで「LookDevX」と呼ばれる  
<Marker>USD と MaterialX のシェードグラフを作成する</Marker>ツールを使用します。  
＞＞ [LookdevX について](https://help.autodesk.com/view/MAYAUL/2024/JPN/?guid=GUID-5C076445-22FB-4C74-9147-43672BCF88CD)

![](https://gyazo.com/2e4a5de8aab46e04a55bbe2f3bfff68f.png)

まず、LookdeVX を開きます。

![](https://gyazo.com/7560de15d0315cd88ec3d94fcf86991c.png)

開くとこのような画面になります。  
まずは USD で作成してみます。

「USD」ボタンを押して、編集画面に入ると、

![](https://gyazo.com/97e9649347ec88fc8313802af66542ce.png)

Tab ＞ USD ＞ USD Preview Surface を選択します。

![](https://gyazo.com/9e8cf2f54ded1465b528ea5e896b46b9.png)

すると、このように PreviewSurface のマテリアルノードが作成されます。

![](https://gyazo.com/b2204078e565b9263e881808c015d882.png)

作成した PreviewSurafce は、自動的に現在の MayaUsdProxyShape に Material/Shader を作成します。

![](https://gyazo.com/15d7d19a40062d25bc13914e090755f4.png)

Material ノードをダブルクリックすると、ノードの編集 UI に入ることができます。  
この中は、いわゆる UsdShadeShader ノードで構成されていて  
この中でテクスチャを定義したりなど、USD でマテリアルネットワークを  
作成できます。

![](https://gyazo.com/27c19e2dbaae3c97b42c5ed4ebed0f58.png)

まずは簡単なマテリアルということで、Texture をアサインしてみます。  
その場合は USD UV Texture を選びます。

![](https://gyazo.com/81d9054c05c536179c307e2e0a463e43.png)

選ぶと、UsdPrimvarReader と UsdUVTexture が自動で作成され（PrimvarReader はもろもろ指定もされた状態）

![](https://gyazo.com/b65236156e91cf5f3afdedeea1fc2c4c.png)

一応できましたが、Maya のビューポート（Hydra）だと微妙な壊れ方をするし  
Arnold にすると Maya が 100%落ちます。  
がんばれ！！Maya！！！

![](https://gyazo.com/0a791163dd6dfd8fe2c1fe5aa5251de9.png)

Houdini で見ると正しくアサインできているので、おそらく大丈夫だと思います。

![](https://gyazo.com/998c6ca2b585be89a57034496cbc58fc.png)

すでにある PreviewSurface を編集したい場合は、  
対象の Material を選び Show in LookdevX で開くことができます。

## MaterialX

ここまでは USD の世界だけでしたが、LookDevX は USD というよりどちらかというと  
MaterialX を使用するのがメインなのではないかと思います。

MateiralX がなにかというと

> シェーディングネットワークを記述するためのオープンソース規格です
> 参考： https://www.sidefx.com/ja/docs/houdini/solaris/materialx.html

とあるとおり、シェーディングネットワークを記述するための形式です。

https://openusd.org/release/api/usd_mtlx_page_front.html

USD には、MaterialX を USD で読むための FileFormatPlugin が用意されているので  
USD とは別のシステムではありますが、USD とセットで語られがちです。  
くわしくは、<AutoLinkTitle url="/usd/materialx" />あたりで USD と MaterialX は書いてありますのでこちらを参照してください。

![](https://gyazo.com/45b7bed10fb68bfa00012fdedfdf9057.png)

まず、作成から MaterialX Stack を選び作成します。  
これは、USD における mayaUsdProxyShape と同じようなものの MaterialX 版で  
<Marker>「このノード以下が MaterialX の世界」</Marker>になります。  
※このノードは、LookdevX プラグインの仕様らしい※

![](https://gyazo.com/1fdb0503eb5eb166933afdfb40c6028e.png)

アウトライナー上にはこのように表示されます。  
まず、さすがに何もないとわからないので MaterialX のサンプルを読み込んでみます。

https://matlib.gpuopen.com/main/materials/all

使用するサンプルは、AMD の GPUOpen MaterialX Library です。  
このサンプルを Maya のシーンの MaterialXStack に読み込みます。

![](https://gyazo.com/aa64800969cd716b87bc82d8d9246e95.png)

まず、Create MaterialX Document で、Document を作成します。  
MaterialX の Document とは、ファイル全体のルートノードを表すオブジェクトです。  
なので、まずはこの Document を作成する必要があります。

![](https://gyazo.com/4028266e0b459e73ef7ac3f76527e236.png)

Document のノードを選び、Create MaterialX Document を選びます。

![](https://gyazo.com/270f6e2dc39150e555e971d588da25f6.png)

選ぶと、このように materialXStack にインポートできます。

![](https://gyazo.com/b74294a24bc3cac3b24a16aa4b7a4e62.png)

これを LookDevX で開くとこのようになっています。

![](https://gyazo.com/0f1d55b91b2196b756aaf798d5bd56fc.png)

NG_Oblong_Indigo_Wallpaper 内はこのようになっています。  
materialXStack でみたときの親子関係＝ノードでまとめられている単位になっているようです。

LookdevX で表示できましたが、これだけだと MaterialX の世界でだけマテリアルが存在している状態になっているので  
このままだと使用できません。

さらに、どうやらマテリアル単体でのコンバート（Duplicate As USD Data はあるけれども、空の Prim が作られるだけで使えない？）  
ということにここまで書いて気が付きました。なんてこった。

さすがにあんまりなので、単体で持って行く以外の方法を考えます。  
この MaterialXStack にあるものは、USD の世界ではなく Maya 世界の Mesh に対して  
アサインが可能です。

![](https://gyazo.com/d1eba6538ba1c71c2cdc8ec46522aa3c.png)

Assign Existing Material に MaterialXStack にある StandardSurface が表示されているので、これを選びます。  
![](https://gyazo.com/0eb3f7d2157c3b5eb6686470d5f9150e.png)
![](https://gyazo.com/5d73ce120d31c8aca1f5ec94f1657862.png)
結果、これまでのマテリアルと同様に ShadingEngine 経由でマテリアルがアサインされます。

![](https://gyazo.com/78bd9e0b62d1e862312b353847704632.png)

この MaterialX の StandardSurface をアサインした Mesh を  
Duplicate As USD Data で USD の世界に送ります。

![](https://gyazo.com/982e2da45e2bbd146385c64b25ba55bf.png)

Options...に「MaterialX Shading」のチェックがあるので、これを ON にしておきます。  
![](https://gyazo.com/63f72ade5582e51963a426cdf8b2adaa.png)

結果、USD の世界にインポートすることができました。  
ただ、見ての通りすべてのノードがインポートできるわけではない  
（USD の FileFormatPlugin のドキュメントなどにも制限事項が書かれている）  
ので、その点だけ注意が必要です。

![](https://gyazo.com/46e91ea708f027b34c5a9c93da1940ac.png)

さらに、どうやらエラーになっているので、まだまだこの辺りは検証が必要そうです。  
MaterialX 自体の仕様もちゃんと理解しないとダメそうなので  
この辺りは次の宿題にしたいと思います。

## まとめ

ネイティブ USD と MaterialX をノードベースで編集できる機能である LookDevX ですが  
おそらく 1 からマテリアルを作る場合などは大丈夫かもしれませんが  
既存の mtlx を持ってきたり、USD と合わせていろいろやると途端に怪しくなる気がします。

とくに MaterialXStack 側（MaterialX の世界）と MayaUsdProxyShape 側（USD の世界）  
と Maya の世界とが平行で「ノード」という形でラップして存在しているので  
どこがどうつながっていて、どうやって出力するのかがわかりにくいです。

このあたりは、もうすこし MaterialX や OpenPBR 周りの基礎知識が必要だなと感じたので  
継続的に学習していきたいと思います。
