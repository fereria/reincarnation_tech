---
title: SOLARISの sopimportを攻略する
tags:
    - SOLARIS
    - Houdini
    - AdventCalendar2022
description: sopimportを使ってSOPのGeometryをLOPに持ち込む方法
---

![](https://gyazo.com/d09240a437e3e7c0926a2c6a2ed405d5.png)

[Houdini Advent Calendar 2022](https://qiita.com/advent-calendar/2021/houdini) は、SOLARIS のノード「sopimport」の使い方を、できる限り調査していきたいと思います。

## sopimport ノードとは

sopimport ノードは、その名の通り SOP で作成したジオメトリを LOP の世界に持ち込むことができるノードです。
このノードを使用することで、SOP の usdexport ノードでファイルを出力することなく
シームレスにジオメトリデータを LOP に持ち込むことができます。

似たようなことを、{{markdown_link('02_sop2lop')}} こちらの記事で実行していますが
こちらはかなりイレギュラーな手段で、
Python ノードを使用して自力で Prim を生成していますが、
ことジオメトリに関して言えばこんなめんどくさいことをせずに
ほぼだいたいのことを sopimport ノードを使用することで実行できます。

## 基本

まずは基本的な使い方。

![](https://gyazo.com/f7bf67dab5e9d56302f04297849e8663.png)

SOP Network を作成し、

![](https://gyazo.com/d0b8def247053967bfc1bbe2d4c07683.png)

シンプルな Pighead モデルと OUTPUT ノードを作成します。

![](https://gyazo.com/447a74034a4f94a15f142a1104cc14ef.png)

SOP Path を、sopnet 内の OUTPUT になるようにしておきます。

![](https://gyazo.com/f656108c72e157641f4d66f3da5b42e5.png)

まずはこれで Mesh を持ち込むことができます。

![](https://gyazo.com/d3be3eb1eb72d0e42181f4a79b39bd89.png)

この時の importPrimitive は、デフォルトでは sopimport ノード名になっています。

![](https://gyazo.com/d0d2ca0bdfc5bcd8822f75975fb4a947.png)

無事ジオメトリが持ち込み出来ました。

## Reference

![](https://gyazo.com/c8fd47dc1fb299e7c08e417dbde1c3b0.png)

基本的な持ち込み方法では、データはそのままメモリ上のレイヤーにインポートされ、
レイヤーを分離して保存したとしてもサブレイヤー扱いになります。
そうではなく、Reference で持ち込みたい場合は Load As Reference にチェックをいれます。
この場合、Layer Save Path で指定したレイヤーを「Reference」でロードするようになります。
サブレイヤーとは違い、SOP 側で作成したジオメトリと階層構造を
指定のパス（PrimitivePath）に読み込むことになるのが大きく異なります。

## Copy Contents into Editable Layer

![](https://gyazo.com/896bbba8ce3f4af48a5c1843eddf9803.png)

sopimport でモデルを読み込もうとした場合、そのままだと Warning が表示されます。
出ていてもモデルは持ち込めますが、Warning を確認します。

![](https://gyazo.com/88fdd907845a7d722807249dcd43c7ed.png)

sopimport で SOP からインポートした場合、レイヤーが保存されてないよ。
SOP ノードのレイヤーは、その Houdini のパスあ k ら生成された
ファイルパスに出力されるよ。

ということのようです。

SOP と LOP の行き来をテストしていたときに気が付いたことですが
LOP Node には Editable Stage と Stage と 2 種類取得方法があります。

SOP から LOP のノードにアクセスしようとした場合、
取得は可能だが変更不可な read-only の stage として取得できます。

ということを踏まえて、現状だと read-only の stage として取得されてる
状態なので、変更可能な保存先に入れておいてね？ということだと解釈して

![](https://gyazo.com/bc1c87d0df5ee2b0e114936f734549ac.png)

Copy Contetents into Editable Layer オプションを押して
現在の LOP 側の EditableLayer（編集可能レイヤー）に構造をコピーして
LOP のレイヤーとして扱うことにすれば、Warning は消えます。

## Group

Import 時の指定だと、ある SOP のノードを指定して
その段階の Geometry を取得していますが、そこから条件を指定して
一部だけ読み込みたいケースもあるでしょう。

その場合、SOP の Group を指定して一部だけ持ち込むことができます。

![](https://gyazo.com/48d41f9dabaf504e095b4f4a2df7b6ac.png)

Import Group で、SOP 側で指定した Group を指定すると、

![](https://gyazo.com/4e92bbef204917ea60c4267590dca459.png)

指定した Group のモデルだけを LOP 側にインポートできました。

## SubsetGeom

SubsetGeom とは、USD で Face 単位のマテリアルアサイン等をするときに使用するものです。
詳細は {{markdown_link('06_shader')}} このあたりに書いたので合わせてみてもらえればですが、

![](https://gyazo.com/5daffb80355fc78263f770593130e981.png)

Subset Groups で、SOP 側の Group を指定すれば、

![](https://gyazo.com/3db457c2d1ac0418d242a710cd91d3f3.png)

GeomSubset が作成され、Group で指定した Face に対してマテリアルアサインを
するなどが可能になります。

## Point

![](https://gyazo.com/cca87afb5194b5e5d3e33cbee357da06.png)

デフォルトで SOP から持ってこれるのは Primitives ですが、 Import Group Type で「Points」を選ぶことで、Point としてもインポートが可能です。

![](https://gyazo.com/e3974a321aa1eeebcb33cf283f30c839.png)

Points として読み込むと、UsdGeomMesh ではなく UsdGeomPoints として読み込むことができます。

![](https://gyazo.com/7cd1d5c768401eda0a59a8069c4a7e3b.png)

表示した結果。

## Path 指定

特に何もせずにインポートすると /nodename/mesh_0 のような名前で Mesh が生成されますが {{markdown_link('00_usdexport')}} このあたりは、SOP の USDExport ノードのルールと同様に、
指定の Attribute を指定することで SOP 側で指定することができます。

![](https://gyazo.com/4bac97fb9a120672e16a44e4329563ec.png)

AttributeWrangle を作成し、

![](https://gyazo.com/46f9f2539869e332726917aa5045115c.png)

GroupType を Primtives に変更し、
path アトリビュートに、LOP 側の SdfPath を指定します。

![](https://gyazo.com/7bef3552ddfd009b8b48a51b5bfb59b8.png)

こうしておくと、 sopimport で LOP に読み込んだ時の SdfPath を
SOP 側でコントロールすることができます。

## Instance

次にインスタンスを作成したい場合。
インスタンスを使うには、PackedPrimitives を使用します。

![](https://gyazo.com/d8624b905efbaa4b854ec357cb906d2c.png)

SOP の Copy and Transform ノードで「Pack and Instance」で複製してみると、

![](https://gyazo.com/18dc6871b34ba495fb72a3cf6c300f06.png)

インスタンスのもとになっているジオメトリは「Prototypes」として作成され
青文字になっている部分はインスタンス扱いとして作成されます。

PackedPrimitive になっているものはインスタンス扱いになりますが

![](https://gyazo.com/b04b0319a2fb7993078bdf4d28cee83b.png)

sopimport の Packed Primitives でどのように持ち込むかを変更できるので
あえてインスタンスにしたくない場合だったり、PointInstancer で持ち込みたい場合は
設定で変更が可能です。

## Layer Save Path

sopimport で SOP から持ち込まれるデータは、基本的にジオメトリオブジェクトです。
ので、この部分だけを別レイヤー扱いにしておいたほうが都合がよいので、
sopimport で、レイヤーパスを指定します。

![](https://gyazo.com/0176a346ed9ac01f93ce893f93862b3d.png)

Layer Save Path に、保存先を指定すると、

![](<https://gyazo.com/f6ff629ec951feb20584e37b3e94c16b.[](.png)>)

USD ROP ノードを作成します。

![](https://gyazo.com/34fdaf3f33b82a2e51fb157afbc41f39.png)

その結果、sopimport 段階のデータとそれ以外とでレイヤーを分離できます。

これで USD への出力がコントロールできました。

## Attribute

SOP では、各頂点や Primitives に対して GeometrySpreadSheet で Attibute をつけることができます。
特に指定がない場合は、USD の Attribute としては持ち込めませんが

![](https://gyazo.com/f6bf8986545472db8ccdd767ca0c6369.png)

sopimport の USD custom Attribute で読み込みたい Attribute を指定できます。
アスタリスクの場合は、どんなアトリビュートでも全部持ってくるという意味になりますし

![](https://gyazo.com/2d59ef1b1ea4ca54b006f9b81d87ddb6.png)

usd*\*のようにすると、頭が usd*のアトリビュートのみを USD のアトリビュートとして
インポートできます。

![](https://gyazo.com/9e365091ef7b142264b2aa799fd2acd7.png)

れいとして、これは usd\_\*でインポートした場合。

![](https://gyazo.com/a3721e2502ee01666689a5c0f8dc9236.png)

*で読み込んだ場合。
*だとより多くのアトリビュートが持ち込めているのがわかります。

### Point の場合

先ほどの例は Primitives に対してのアトリビュートでしたが
Point に対してもアトリビュートが付加できます。

![](https://gyazo.com/3a7adae62570a4f2cb301d9a6de410c7.png)

試しに、全頂点にランダムな値を入れておきます。

![](https://gyazo.com/67406de973b82da06ec4f1efd95a7ad9.png)

これを持ち込んだ結果はこちら。
primvars として頂点分の配列を持ち込むことができました。

この rpimvars とは primitive variables の略で、
Primtives の各頂点単位で指定され、主に material などで頂点間で値を補完して扱うものです。

![](https://gyazo.com/ae2413905acd352fcd99c9507c0b98b8.png)

例えば、SOP 側で Color ノードを使用して頂点カラーを指定した場合。

![](https://gyazo.com/2c61012fcbd790871d121256fadc2305.png)

displayColor としてインポートされます。
各頂点ごとに指定された値によって、間の Face カラーは補完されて表示されます。

といった感じで、SOP 側で頂点に対して指定した値は primvar として出力され
自由に扱えるようになるというのがわかりました。

![](https://gyazo.com/2dd417352c787f2818b4579c361346bb.png)

primvar はデフォルトだと全部インポート扱いになっていますが
Attributes で、Primitives 同様に持ち込むパラメーターを制御できます。

## アニメーション

![](https://gyazo.com/a449d9b63ab8d4713b6cea0c675bfe96.png)

SOP 側でアニメーションを追加した場合は、デフォルトで SOP 側に TimeSampling が追加されます。

![](https://gyazo.com/dac9d32262bff6e99817c6e7361c450e.png)

USD ROP が、デフォルトだと単一フレームなので、 Valid Frame Range を
Render Specific Frame Range に変更すれば、アニメーション付きで Export できます。

## まとめ

この記事を投下する前に {{markdown_link('01_importlop')}} や {{markdown_link('02_sop2lop')}} のようなトリッキーな手法を書いてしまったのですが
多くの場合はそんなことをせずに、sopimport ノード１つで
たいていのデータは LOP に持ち込み、そして USD アセットとして扱えるようになります。

SOP のプロシージャルモデリングと、TOP を使用してのバッチ処理
LOP を使用しての USD のセットアップを組み合わせれば
大量委のアセットをまとめて USD 化なども簡単にできるので
ぜひとも Houdini を活用して
大量のアセットを作成していけるといいなーと思います。

今回は取り上げませんでしたが、Agent（Skel 周り）や Curve 周りなども
持ち込んだり、
[Scene Import LOP object translator plugin](https://qiita.com/K240/items/d3d0fa8a632bc06cfda5) のような、さらに痒い所に手が届く機能もあるので
今回書けなかった部分も含めて検証を進めていければなーと思います。
