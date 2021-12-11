---
title: ComponentBuilderで遊ぼう
tags:
    - SOLARIS
    - Houdini
    - AdventCalendar2021
---

[Houdini Advent Calendar 2021](https://qiita.com/advent-calendar/2021/houdini) は、Houdini19で新しく追加されたComponentBuilderの使い方を調べてみよう、です。

## ComponentBuilderとは

ComponentBuilderとはなにかというと、
[去年のHoudiniアドカレで書いたUSDアセットを作ろう](https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/13_create_usdAssets_01/)の内容を
もっと簡単にできるようにしたノードです。
つまりは、去年の記事のような複雑なネットワークを作らないでも、
このComponentBuilderを使用すれば汎用アセットをセットアップできるようになります。

まさかの翌年で前年に書いた内容が公式のノードとして用意してるとはHoudini恐ろしい子...

## まずはざっくり

![](https://gyazo.com/bb8b2de7caaa3016ddf2a2e78dbf31d9.png)

まずは、SOLARISのStageで Component Builderを選びます。

![](https://gyazo.com/ddd39553ad7b000d3b36cd073a956ea5.png)

すると、このようなノードができます。
このComponentOutputの結果できあがるシーングラフは、

![](https://gyazo.com/d29e64202edc48286b2187967681f14a.png)

このようになります。

多少違いますが、 [ComponentBuilderを使わなかったときの結果](https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/13_create_usdAssets_01/#_15)と同じような構成になっていて
Payloadの構造、GeometryとMaterialの別レイヤー化などした状態で
USDアセットのセットアップを行ってくれます。

![](https://gyazo.com/17d03acde31d3a1458f31d669df1b9c5.png)

試しにUSDファイルにExportします。
今までだとUSDROPノードでExportしていましたが、ComponentBuilderの場合はComponentOutputノードが
Exportを担当します。

![](https://gyazo.com/ee6b7cd3b4f108c43518941f4159a477.png)
Load from Diskのチェックを入れるとTOPsっぽいものがノードの左側に表示されます。
そしたら、Save to Disk します。

デフォルトだとHipと同じフォルダ以下に出力されるようになっているので、
出力先に指定されたフォルダを覗いてみると、
![](https://gyazo.com/3e6f91938c6153a1d8cedd8ae32b6d66.png)
出力されていました。

![](https://gyazo.com/7458ffed7eabc857083608056ad31c5a.png)

出力した usdcをusdviewで開いてみると

AssetInfo、Kindといったメタデータ、
Payloads、MaterialのVariant、Material・Geometryの分離等含めてすべてされた状態の
USDアセットを出力することができました。

すごい。

> Kindとはなんぞ？という人は
> https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/11_kind_modelhierarchy/
> こちらの記事を参照。
> AssetInfoは近いうちにUSDアドカレに書きます。

## ComponentBuilderの構成

ComponentBuilderは、

* Component Geometry
* Component GeometryVariants
* Component Material
* Component Output

この４つのノードで構成されていますので、それぞれの役割を確認しながら詳しく使っていこうと思います。

### Component Geometry

ComponentGeometryは、その名の通りUSDアセットのうち、Geometry部分のレイヤーを作成するためのノードです。
そして、そのGeometryに対してVariantSet（ヴァリエーション、モデルのパターン）を作成するために使用するのが
Component Geometry Variantsです。

![](https://gyazo.com/3ca90e7a4e77d61a41dedc768ce87aba.png)

![](https://gyazo.com/b76b0f853024e3ab2473f8a46bc208cc.png)

ComponentGeometryを使用することで、USDのGeometryPrim以下の構造を作ってくれます。

![](https://gyazo.com/0d812572371fbc86c58955a2554d796d.png)

Geometryは、ComponentGeometryノードをダブルクリックすると、中にOutputノードが３つ用意されています。

![](https://gyazo.com/a898c9e17771da7d417c5dfd025d5757.png)

このComponentGeometryノード内はSOPNetworkになっていて、SOPでプロシージャルに作成したモデルを
そのまま出力することができます。
使い方は、 output#0 ～ #2 に指定のPurpose（目的）のノードを接続します。

> Purpose（目的）とは
> そのGeometryに対して、レンダリング時にどのような目的を持たせるかを指定するためのAttribute
> デフォルトでは default(役割を持たない) proxy(OpenGL用の軽量Geometry) guide(ガイド表示用)
> が指定できて、それぞれの枠割でどのモデルを表示するかを指定できます。
> 詳しくはまた別の記事で。

![](https://gyazo.com/2b5697b1ff3d1936ebacf32fc43e5012.png)

試しに、defaultにpig proxy に boxを接続します。

![](https://gyazo.com/f03d0d3aee51a9d8504a0adfdbd93196.png)

このようになります。

![](https://gyazo.com/e2d2e354bf7f6dd9666f385861026e42.png)

Stageに戻りビューポートを見ると、Proxyモデルが表示されています。
これはComponentGeometryノードで proxy (OpenGL用の軽量Geometry)のPurposeが指定されている
Geometryが表示されているからです。

![](https://gyazo.com/c6e38640d8bbf4f4faa35b3c2bc4f652.png)

これをKarmaに変更します。

![](https://gyazo.com/ecae8f4501a62df4d51ae115e8bba7e0.png)

変更すると、Pigに変わりました。
Karmaの場合（OpenGLではない場合）はdefaultGeometry表示になります。

![](https://gyazo.com/70d00e3033af8e6a2ce243ed0b2fc8b6.png)

現在のシーングラフはこの通り。
geo以下にproxy/renderの３つのScopeができていて、それが ASSET のXformでまとめられているのがわかります。

ComponentGeometryノード（SOP）で出力した場合は、shapeMesh１つにまとまって出力されます。
このあたりは、以前書いた[PackedPrimitivesとUSDExport](https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOP/00_usdexport/)でMeshを切り分けたり出力先のSdfPathを制御できますので
気になる方はぜひこちらの記事もよろしくお願いします。

#### FaceへのMaterialAssign

ComponentGeometryでMeshを出力した場合、Pack等しない場合は１つのMeshになりますが
その場合どうやって複数のマテリアルをアサインすればいいのか？というと、
![](https://gyazo.com/b18bfb3fd0c52e9b7a1787a3ce950492.png)
SOP側でPrimitivesにGroupを指定します。

![](https://gyazo.com/48a6b7d8f2fd83015b79b66b5f392391.png)
SOPで指定したGroupの名前を、 Subnet Groups に、スペースを空けてグループ名を追加します。

![](https://gyazo.com/b989e7c1f506392feb6a59e1658f256f.png)
Subset Groupsを作ると、UsdGeomSubsetが作成されます。
> UsdGeomSubsetは、その名の通りUsdGeomのサブセットで
> メッシュのインデックスを保持します。

とあるとおり、SOPで指定したPrimitivesのGroupのIndexをUsdGeomSubsetに出力してくれます。
このUsdGeomSubsetに対してマテリアルをアサインすることで、複数マテリアルのアサインができます。

UsdSubsetについては、[UsdPreviewSurfaceを使う](https://fereria.github.io/reincarnation_tech/11_Pipeline/30_USD_Programming/01_Python/06_shader/#face)に説明がありますのでそちらを参照ください。

### ComponentMaterial

次はComponentMaterial。
その名の通りマテリアルをアサインするためのノードです。

![](https://gyazo.com/abfcfb0ff3db960014d5bbfcc7fd14cc.png)

使い方は簡単で、Input0にComponentGeometryをつなぎ、Input1にMaterialLibraryをつなぎ
ComponentMaterialで指定のMeshに対してMaterialLibraryで作成したマテリアルをアサインします。

#### MaterialAssignの方法

![](https://gyazo.com/937da41a82f82658dab4ed26ce71815c.png)

ComponentMaterialは、マテリアルをアサインするPrimitiveと、アサインしたいMaterialのPathを
指定することでアサインが可能です。

![](https://gyazo.com/108c1acd8b809c76ae11c034f84192b0.png)

ComponentGeometryでSubsetGeomを指定していた場合、ComponentMaterialで
SubsetGeomをPrimitivesで指定、アサインしたいMaterialのPathを指定することで

![](https://gyazo.com/6fa971249367b7e90d6431fb5a218dab.png)

Face単位でのアサインができました。

![](https://gyazo.com/15db8e1a39331a629e98d2481042e7a0.png)

Assignの結果、出来上がったシーングラフはこのようになります。
shapeとそのSubset、そしてマテリアルという構造になります。

#### MaterialLibrary

Material Libraryの設定で、指定のVOPからマテリアルをLOPにインポートすることもできますが
それ以外にMaterialLibraryノードをダブルクリックすれば
そこがVOPになっているので

![](https://gyazo.com/ae772e695bbb7746fb030eff7b5f62d4.png)

![](https://gyazo.com/d8de81954d5555fefeea75b1d08d765f.png)

そこでマテリアルを作れば、特に指定をしないでも
Material Path Prefix 以下にMaterialを出力してくれますので、
お好みで使い分けるとよさそうです。

#### ComponentMaterialを使用した場合の特徴

このComponentMaterialを使用しないでも
![](https://gyazo.com/b31c4c08701c17205a41c1848f1024b4.png)

MaterialLinkerを使用して

![](https://gyazo.com/208cf6b58a0b84439b410adadc6ca265.png)

このようにすれば、視覚的にも楽にマテリアルアサインが可能ですが、
ComponentMaterialを使用した場合、大きく以下２つが変わります。

#### Materialの別レイヤー化

![](https://gyazo.com/2a1eab56a846b11becb94d07709c1ed1.png)

のちに説明するComponentOutputで、マテリアルを別レイヤーとしてExportします。

![](https://gyazo.com/3830b785f711e9f359c718ff36f79cce.png)

この時のレイヤーとコンポジションの構造はこんな感じになります。

> MaterialAssignは mtl.usdc側
> リファレンスの順序的でマテリアルレイヤーのほうが強い

#### MaterialAssign ON/OFFのVariantSetの追加

![](https://gyazo.com/a0fc405506081cea76c5009f76512203.png)
マテリアルのアサインをVariantSetを使用してON/OFFする構造を自動で追加してくれます。

> 自分用メモ
> ComponentMaterialのノードをダブルクリックすると、その中はLOP
> InputでStageを受け取り、その中でノードベースでもMaterialAssignができる。
> ここで指定した値は over で mtl.usdcに入る
> ![](https://gyazo.com/ad65b2a11f68aca1d5fa998ca7464d36.png)
> 
> ![](https://gyazo.com/528368a3aef76d904a7eb51e5bdc4a87.png)
> ※ただし、この方法でマテリアルを作ると、ComponentGeometryVariantsで
> 　マテリアルが消失するらしい？

### ComponentGeometryVariants

次にComponentGeometryVariants。
これは、その名の通りGeometryのVariantSetを作成するためのノードです。
ComponentGeometryをInputに接続すると、いい感じにComponentのVariantを作成してくれます。

![](https://gyazo.com/fcb6c63b99363b8b5d567b87b50948eb.png)

ComponentMaterialを追加した後に、ComponentGeometryVariantノードを作成し２つを接続します。
この例だと、CubeとTorusの２つのMeshが作られて、

![](https://gyazo.com/006869fdca7135ec80761b824377a954.PNG)


ASSETノードに対して geo Variants が追加されます。
ここには、ComponentGeometryで指定した名前（デフォルトはComponentGeometryのノード名）でバリアントが作られます。

これで、MaterialAssignと合わせて ASSET Primには、geo と mtl（アサインオンオフ）のVariantSetがある状態になります。

> 自分用メモ
> ComponentGeometryVariantのノードの段階だと、マテリアルのVariantがちょっとおかしい気がする
> ![](https://gyazo.com/3c0d9b6126d503ef075406c093093c57.png)
> mtl.usdc的にはASSETにVariantSetが入っているけど、このノードタイミングだとVariantはあってもVariantにならない。
> ![](https://gyazo.com/d25c8352b757f75e18173469a84efd2c.png)
> （ComponentOutputが入ると正しいので、そういうものなのかもしれない）

### Component Output

![](https://gyazo.com/3a8f28e984b6f4cc69d3677e4d9d313d.png)

最後はComponentOutputです。
これはその名の通り、ここまで作ったUSDAssetを指定のレイヤー構成でExportしてくれます。
Exportする以外に、USDアセット用のメタデータの追加、継承の追加、RootPrimの指定などの構造を
指定します。

#### Exportする

![](https://gyazo.com/6c2bfd65e5b80e9a1eddf82f15c3e56f.png)

まずはOutput。
Caching の Load From Disk をONにして、SaveToDiskを押します。
押すと、デフォルトの場合はHipと同じフォルダ以下の usd/assets/以下にモデルを出力します。

出力すると、

![](https://gyazo.com/00930fcba64e907f9ba732c7699ea3f9.png)

このようなレイヤーが出力されます。
このレイヤーの関係性は以下のようになります。

![](https://gyazo.com/7b102916c5168ffabc384bff62768b15.png)

> 備考
> geo / mtl 内のvariantは
> ![](https://gyazo.com/a96d97b13401cdec7223a3b3b5579d03.png)
> overで定義した ASSET_geo_variant_#/ASSET を AssetName Prim にReference
> このoverそれぞれにVariantが指定されていて、Referenceでそれが合成されている

#### LayoutAssetGalleryに登録する

![](https://gyazo.com/8b504e3bb5b31b66992778c4ae58d9fa.png)
Caching のAdd to AssetGalleryボタンを押すと、

![](https://gyazo.com/11c244f3a7fbb9ffd897c4c1de6ba0dc.png)

簡単に登録できました。

![](https://gyazo.com/ec9a95a5dd7efbdc55bb278fdf8ca018.png)

![](https://gyazo.com/18327791cc0c265d0737db26c5eef09b.png)

作成したアセットは、Layoutノードを使用すると、簡単にレイアウトすることができます。


#### サムネイルを作る

![](https://gyazo.com/07b1d39e34e70139c29c887c3be179b0.png)

Thumbnailの Generator Thumbnailボタンを押すと、Assetフォルダ以下にThumbnail.pngが作成されます。

#### Variantごとの別レイヤー作成

![](https://gyazo.com/61eb367bbc5fb4fe49d304e162bf39eb.png)

Component Output のVariantLayersをONにすると、バリアントを別アセットとして登録することができます。
（別レイヤーですが、本体のAssetName.usdcをリファレンスして、SetVariantしている）

#### AssetInfoやKind

![](https://gyazo.com/f89e3e7f8acdd00ce6bb0db0981ae1f1.png)

Component Outputでは、USDの各種メタデータも指定が可能です。
Kindについては最初にも書いた通り[こちらの記事](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/11_kind_modelhierarchy/)で、どう使うのかを書いたのですが、AssetInfoについてはそこまでふれてないはず
個別にUSDアドカレにて記事を投稿予定です。
（[去年のあどかれのこのあたり](https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/13_create_usdAssets_01/#assetinfo)で言及してた）

以上でモデルとマテリアルを作り、アサインして、出力するまでの構造ができました。

#### Layer名の指定

![](https://gyazo.com/64fb05f6389b1e7c85ae06009c0b6b47.png)

Component Outputを使用すると、ExportOptionsで各レイヤーの名前を変更して出力することができます。
デフォルトだと AssetName.usd payload.usdc geo.usdc mtl.usdc extra.usdc となっています。
ですが、
usdは、中身がアスキーでもバイナリでも大丈夫で、リファレンスが絡んできた場合であってもアスキー・バイナリを簡単にスイッチできるように
しておいたほいがよいため、 usdc ではなく usd としておいたほが個人的には良いと思います。
(この辺りは[アドカレ２日目の記事](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09#%E3%83%A2%E3%83%81%E3%83%99%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3)で技師長師匠が言及しています)

さらに、複雑なコンポジションになってきたときに、どのアセットのどのレイヤーを明示しておいたほうが良いとおもうので、
各レイヤーの頭にアセット名を入れておきます。
（Kitchen_setなども、このようにアセット名が入っていますのでそれ準拠）

![](https://gyazo.com/f36928b169c168d051ee0b9152fe5208.png)

最終的にはこのようなレイヤーになりました。

## サンプル

https://1drv.ms/u/s!AlUBmJYsMwMhhOcoB7mqcctbgbO2GA?e=J2djhB

ComponentBuilderがなかったHoudini18.5で作ったアセットセットアップサンプルと比較すると、

![](https://gyazo.com/53867097178c8e2b8909f420cd8f7a37.png)

これが、

![](https://gyazo.com/8fbb4dd1033e3a5f8051816c5fc5c678.png)

こうなって、以前のUSDをがっつり理解していないとかなり難解なネットワークだったのが、
かなり直感的でシンプルなネットワークになっているのがわかると思います。
（以前のサンプルはVariantSetを入れていなくてもこれだけ複雑）

https://1drv.ms/u/s!AlUBmJYsMwMhhPUHvj3CO9k1O7qsTw?e=mzekNF

一応今回のシンプルなPrimitiveで作ったサンプルファイルをアップロードしておきましたので
構築の参考になれば。

## まとめ

アドカレ公開日までで調べられるところまでやろうとおもったら、
想像以上に機能が多彩で随分と長い記事になってしまいました(多機能すぎる)

ComponentBuilderは、USDアセットを作るのに必用な機能が非常に扱いやすい形でまとめられていると思いました。
今回触り切れなかった機能もまだまだありますので、
余力があればもう少し深堀した記事も書きたいなと思います。

また、Houdini19からはLayout関連がかなり進化していて
LayoutとComponentBuilderを使うことで、以前までとは比較にならないぐらいサクサクレイアウトできるようになりました。
以前までは「ちょっとこれは、すごいけどUSDの構造知らないとちょっと手がだせないかな...」という印象があったSOLARISですが
今回は、そういう印象がなくなり非常に直感的になっています。
これを機会に、ぜひともUSDを使用したアセット作成やレイアウトを試してもらいたいなと思います。
(18.5までとは別物)