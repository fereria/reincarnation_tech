---
title: Houdini18で追加されたLOPノードを調べてみた
tags:
    - USD
    - SOLARIS
    - Houdini
    - HoudiniAdventCalendar
---

# Houdini18 で追加された LOP ノードを調べてみた

[Houdini Advent Calendar 2019](https://qiita.com/advent-calendar/2019/houdini) 20 日目は  
Houdini18 から追加された SOLARIS の Stage ネットワーク内で使用する各種ノードの挙動を調べてみよう です。

ただし、追加されたノードはかなり膨大なので全部を 1 度でやるのはムリなので  
コンポジションアーク、Light のノード以外で、使いそうな物をいくつかピックアップして  
アドカレ締め切り日までに書けるだけかいてみるようにします。  
また、とりあえず最初なので、1 つづつは深掘りせず基本的な使い方のみです。  
  
検証してたらやっぱり違うかもしれない...ということもあるかもしれませんが  
そのあたりはご容赦ください。

## 調べ方

Stage ネットワークはノードを作成することで、USD のシーングラフを操作することができます。  
そのため、今回はノードを使用することでどういう挙動になるのかを  
**LOP Actions / Scene Graph Path / Scene Graph Detail** の 3 つを使用して確認しながら  
各種オプションの補足などをしていきます。  
詳しく見ていく前に、この確認する 3 つについて軽く説明していきます。

### LOP Actions

![](https://gyazo.com/361923aff93434d24f3ad36ed9387976.png)

LOP Actions は、そのノードを実行したことで生成される USD のアスキーファイルを  
見ることが出来る機能です。  
SOLARIS では、カレントノードは現在の最新のアクティブレイヤーを編集している事になります。  
そしてそのアクティブレイヤーは前レイヤーまでとの差分（メモリ内ツリー用と思われる ～　 Layers は除く）  
を保持することになります。  
なので、この LOP Actions を確認することで「どういう編集が追加されたか」を  
アスキーファイルとして見ることが出来ます。

### Scene Grapth Path

![](https://gyazo.com/858b398e70a69c2bf981e43d50ca496e.png)

Scene Graph Path は前回触れましたが、これは現在選択されている段階の「合成結果のシーングラフ」  
を確認出来る画面です。  
つまり、ノードを使用してどのような Primitive が作られたのか、シーングラフのツリーが  
どう編集されたのかを  
この画面を見ることで確認できます。

### Scene Graph Detail

![](https://gyazo.com/a7c0da511ad7b84205f0896951bf204b.png)

最後の Detail は、Scene Graph Path で選択中の Primitive の詳細を確認することが出来ます。  
確認出来るのは、Primitive の

- Value
- Metadata
- Layer Stack
- Composition

この 4 つです。  
が、、、、ここだけでもちゃんと説明書こうとするとかなりのボリュームになるので  
なとなく Primitive の詳細を見れるという認識で OK です。

## LOP ノードを見ていこう

というわけで、本題。  
実際に LOP 用に新しく追加されたノードを見ていきたいと思います。

今回はとりあえずざっくりと概要や設定項目を触れていく形にしてみます。  
それぞれもうちょっと掘り下げたいなぁというものは  
今回以降に個々のページで検証をしていこうかと思います。

### SOP->LOP 関係

SOLARIS空間にSOPのジオメトリを持ち込む方法はいくつかあります。

#### SOP import

![](https://gyazo.com/23523170781cf45294c0d689b1f11f16.png)

まず sopimport  
その名の通り、SOP 世界からジオメトリを LOP 内に持ち込むことが出来ます。

![](https://gyazo.com/02ad7d59ddc060ce8aeb28d813673f8f.png)

sopimport では、ノードを指定して  
その段階のジオメトリを読み込むことが出来ます。

![](https://gyazo.com/16a8214da3b97a01f6a9d18f6930208a.png)

読み込むジオメトリは、 Import Path Prefix で指定した Path に対してロードされます。

![](https://gyazo.com/bdf15ffeac3cbc996d5c9063f8437157.png)

シーングラフはこうなります。

![](https://gyazo.com/ef147d7273c2ea40fe7b2be9d7d610d0.png)

SOP import を使用する場合、Reference ノードを使用することなく Load As Reference のチェック  
を ON にすることで、リファレンスで読み込みができます。

![](https://gyazo.com/869cc0cd5ed58ba141f8a178fa19cfd8.png)

リファレンス ON の場合、SOP のモデルは自動で usd ファイルとしてエクスポートされ  
SOP path の下に usd ファイルで保存されます。

#### SOP Create

![](https://gyazo.com/c1cd6fc15a67cf2e4f53893606f95e9a.png)

SOP Create は importと違いこのノード内でSOPネットワークを作り、  
そのOUTPUTをSOLARIS上で使用することができます。  
  
![](https://gyazo.com/d43ccb2cd59e8525c4b3106d8f3dbe39.png)

例として、このように SOP Create のサブネットワーク内でノードを作ると  

![](https://gyazo.com/7b35b415b468cc384ecf116de89c2088.png)

このように、Outputの結果がSOLARIS上に持ち込まれます。  
  
この画像を見てもらうと分かりますが、デフォルトだとマテリアルアサインがされません。  
  
![](https://gyazo.com/2a02faf39796491776f642bc68a1c6c5.png)

マテリアルは、SOP CreateノードのMaterialsタブをクリックし、「Auto-fill Materials」をクリック  
すると、  
  
![](https://gyazo.com/89620a098d279492da5437f44ce9104d.png)

マテリアルも一緒に持ち込めるようになります。

細かいところは、 SOP import と設定部分は同じです。  
  
![](https://gyazo.com/31c39831d7d8e44e7a60813f2b275581.png)

SOLARIS上でも、SOPと同じようにTestジオメトリをロードできますが、  
  
![](https://gyazo.com/da6d34788395a29da0e97714f3ea4184.png)

Testジオメトリは、このSOP Createで持ち込んだものになります。  

#### scene import

![](https://gyazo.com/da1dd698dfdb5c56a1c9a5e29dbcf438.png)

scene improt は、 sopimport とは違い、Houdini の SOP ネットワーク内の全ジオメトリを  
まとめて LOP 内に持ち込むことが出来ます。

![](https://gyazo.com/a5cbf5f0a6ee2aca806cadea995673fd.png)

指定するのは、 SOP の読み込みたいノードの RootPath。

![](https://gyazo.com/a1acc8ceb6c66b8b23d9c9d48f5d7a84.png)

その SOP のジオメトリを、Destination Path 下にリファレンスでロードします。

![](https://gyazo.com/a981778b5eaa8418fe909c35ad6729b4.png)

sopimport の Reference と同様に、USD ROP で Export すると  
SOP Path 下に usd ファイルが出力されます。

SOP 内でシーンを構築して、まとめて ROP に持ち込んでライティングをしたい場合は  
import(All)を使用するのが良さそうです。

### 作成関係

#### Primitive

![](https://gyazo.com/a9abb5f181021e5bb7541c73494dc232.png)

Primitive ノードは、USD のシーングラフ Prim を作成するノードです。

![](https://gyazo.com/7932e69a5e6ba143acd5e46deb492a84.png)

Prim とは、 Scene Graph Path に表示されるこれの事。  
このノードを使用すれば、指定のタイプの Prim を指定の階層でつくることができます。

![](https://gyazo.com/20e9cb9130061238a41dd17a312ab971.png)

たとえば、このような Primitive Paths で作成すると

![](https://gyazo.com/59fbeff1e1a1c5cbf1e887d7da2c70a3.png)

シーングラフ上ではこのようになります。

![](https://gyazo.com/2f07fc46089bf8c62b945bb8640c82aa.png)

途中の Path の PrimitiveType は、 Parent Primitive Type で指定することが出来ます。  
違いは Transform 出来るかどうか（だとおもう）  
単純にまとめるためとして使用するなら Scope で良いのかなと思います。

![](https://gyazo.com/18d8cfa67ed0864e1fcd26e17201b1f8.png)

このノードの特徴は、Primitive Type を自分の指定した Type で作成できます。  
なので、Cube にすれば Cube がつくれるし Material にすれば Material ノードを作成することができます。

![](https://gyazo.com/40e4361ffa41d445fbdf812fcf36d124.png)

もう 1 つ、このノードの特徴として  
作成する Primitive の Specifier(指定子)を変更することが出来ます。

指定子とは

```usda
def Xform "hoge"
{
}

class Xform "fuga"
{
}

over Xform "homu"
{
}
```

このような USD の定義が会った場合の「def/class/over」の部分のことです。  
種類は 3 つあり、通常の Primitive は def で、  
def [PrimitiveType] [name] とすると、定義した Type の Primitive を作る事が出来ます。

class とは、まさにプログラムのクラスと同様に継承するための「定義」になります。  
この場合、シーングラフ上には
![](https://gyazo.com/6d454b690b4b78c015d03b7e13c653f3.png)
このようなマークの Primitive が表示されますが  
ビューポートにノード等は表示されません。  
これらは、いわゆる定義なのでコンポジションアークの「継承」をするための  
継承元（共通定義）のような扱いになります。

このあたりは、コンポジションアーク解説として別途詳しく書こうと思います。

#### PointInstancer

![](https://gyazo.com/34d236cd32aac5132a2a64626e8172a6.png)

PointInstancer は、Point に対して指定のオブジェクトをインスタンスで配置する機能です。  
例えば、草だったり石ころだったり  
背景などに無数にばらまかれているようなオブジェクトを  
広いフィールドにランダムに配置したい場合、このノードを使用します。

作り方は色々あるっぽいですが、比較的ベーシックっぽいやりかたのみ。

まず、Instancer で配置するための Point を SOP ネットワーク内で作成します。  
今回は Grid を Point にしたのみ。

![](https://gyazo.com/ba7675af37b0f6f9580ed6e7541a7e35.png)

作成した Point は、 External SOP の SOP Path で指定をします。

![](https://gyazo.com/7890a5ce51bde4f2d686621e357fcfef.png)

次に実際に配置したいインスタンスオブジェクトを指定します。  
今回は Second Input に入力した Primitive をランダムで配置するようにします。  
なので Prototype Source を Second Input に変更し  
Use Entire Stage 　のチェックを OFF にします。

これが ON の場合、入力のステージを 1 つのインスタンスオブジェクトとして認識するようになります。

![](https://gyazo.com/1bc794c15b6135f65bc87f25b7c112d3.png)

あとは、Merge ノードでオブジェクトをマージして、Second Input にさします。

![](https://gyazo.com/3dd2925d21969002d6c2f015fe5d6928.png)

結果はこちら。

![](https://gyazo.com/b9e280a58ca75667a83fb8399524feb8.png)

ポイントに対してオブジェクトがインスタンスで配置されました。

このあたりも、近いうちにもうちょっと深く掘り下げて検証してみようと思います。

#### Collections

![](https://gyazo.com/ef55f762bbc0b1836078195702d7cfc0.png)

Collection とは、USD のオブジェクトの識別用のグループのようなもの（北口(@kit2cuz)さんの [USD 日本語訳説明はこちら](https://usd.prisms.xyz/intro/USD-Glossary.html#collection)）  
この Collection は、指定のパターンマッチングを使用して動的にグループを作ることが出来て  
コレを利用することで、大量のオブジェクトをコンパクトに管理できるようになるらしい。  
パターンマッチングのルールはこちら。  
https://www.sidefx.com/docs/houdini/solaris/pattern.html

![](https://gyazo.com/0bda759b24222e89e7f8341f20980f85.png)

このような構造があったとして、

![](https://gyazo.com/e7de8f673aaa4903a3cb10e8102406e2.png)

シーングラフはこうなります。

例えば、この中から「Cube」という名前がつくオブジェクトのみ選べる Collection をつくってみたいとします。

![](https://gyazo.com/39fd88416227ca07d9ffd386816e8d8b.png)

その場合はこのようにします。  
Target Rule に、この Collection に含めるための条件を追加します。  
今回は Cube という名前がついているオブジェクトをコレクションにいれたいので  
/cube\* のようにしました。

![](https://gyazo.com/de48f202bbbbd64143f8753dc44fa8bf.png)

名前だと Cube じゃないものも含まれたりしますので、Type でまとめたい場合は  
Primitive Type を条件にすることもできます。

![](https://gyazo.com/fc2be11ae9eb6bda82e6ed4e9e5132f2.png)

正しくコレクションができているか確認したい場合は、  
SceneGraphPath で作成した CollectionPrimitive を選択して、SceneGraphDetail の Tree View で「collection:selected:includes」 をみてみます。  
見ると、無事 Cube のみがコレクションにはいったことがわかります。

この「collection:～～～:includes」 の　～～～　部分は、Collection Name と呼ばれる部分で  
自分で指定することができます。

![](https://gyazo.com/6a11add1f7fbf02a06e18339a05035d9.png)

たとえば、Collection Name を hogehoge にしてみると、

![](https://gyazo.com/956c237b2249a9ce82ffac0903c61ec8.png)

このように変化します。

```usda
def "collections" (
    apiSchemas = ["CollectionAPI:hogehoge"]
)
{
    uniform token collection:hogehoge:expansionRule = "explicitOnly"
    rel collection:hogehoge:includes = [
        </cube1>,
        </cube2>,
        </cube3>,
    ]
}
```

usda を確認するとこうなっています。  
Collection は、リレーションで定義されているので  
Python 等からアクセスする場合も色々とやりやすそうです。

このあたりも、いずれ別途詳しくリサーチしようと思います。

### 編集関係

#### Edit

![](https://gyazo.com/695248a329110373a96ad0a059a9d5ed.png)

Edit ノードは、SOLARIS 上で Primitive の Rotate/Transalte/Scale を編集したときに  
作成されるノードです。  
自分で作ると言うより、選択したノードを動かしたときに自動で作られることの方が多いかもしれません。

![](https://gyazo.com/8e8aab5abc65c4b7ab1c9b7c27a81bc2.png)

操作対象の Primitive は、手で動かした場合は Primitives に自動で PrimitivePath が設定されますが  
手動で作った場合は空の状態になるため  
値をいれてもなにも動かなくなったりします。  
固定の名前ではなく、Input の Primitive を動かしたい場合は、 \`lopinputprims('.', 0)\` にすると  
最後に編集された Primitive をセットすることができます。

#### Duplicate

![](https://gyazo.com/6acabd0b54bbe8a4c524d51a069a971e.png)

Duplicate は、その名の通り  
指定の Primitive を複製します。

![](https://gyazo.com/efa18904ad21131a71a3b4a416e9586a.png)

作ったノードをグループにまとめたい場合は、 Destination Primitives を指定すると

![](https://gyazo.com/0a9f8d5e339f5403572897e068afae11.png)

その下にノードをまとめてくれます。  
まとめるノードは Xform か Scope かも指定することができます。

![](https://gyazo.com/fc40e776a033d3889b7c35c2ff0ad859.PNG)

入力のノードの Primitive（あるいは指定の Primitive）を指定の数指定の名前で  
複製してくれます。

![](https://gyazo.com/a8035aac536bd655b9372df2f57f7d16.png)

どの形式で読み込むかは変更することが出来て  
デフォルトだと Reference として複製されます。

![](https://gyazo.com/cfeef89ab29835e1747afb26b040a4c1.png)

また、複製した Primitive を Collection に入れることが出来ます。  
Collection Primitive は、Path を入れるとその場所に Primitive も自動で作ってくれます。

![](https://gyazo.com/a61dc9519179c9b43e20227d3c76070e.png)

作成した Primitive をまとめて処理したい時などは Collection 化しておくと便利かもしれません。

### ツリー操作

ツリー操作系のノードは、 Merge は Sublayer Graft は Reference Switch は Variant  
それぞれ USD の操作に似た形の挙動をとります。  
しかし、似たような挙動をとりますが微妙に差異があります。

このあたりは書き始めると、コレ単体で 1 つの記事になりそうなので  
別途記事にまとめようと思います。

#### Merge

![](https://gyazo.com/49ae3084a8d4b0ac52314fe6692f5cb9.png)

Merge ノードは、SOP にある Merge とほぼ同じ挙動で  
入力の Primitive やその他もろもろをすべて結合し、  
その **結合した結果の Primitive すべて** を返します。

例えば上の画像の例だと、Cube と Cone の Primitive を結合し  
その 2 つの結果を Output に出力します。

「すべて」というのがミソで、これがどのようなときに関係するかというと、

![](https://gyazo.com/a3e26fcf09f8cf3e112d864684d71030.png)

instancetopoints で Point に対してインスタンス配置をしたい場合。  
Prototypes は指定の入力のノードを Inputs として受け取りますが

```
`lopinputprims('.', 1)`
```

デフォルトのこの lopinputprims で取得出来るのは「最後に編集した結果」の Primitive
です。  
ランダムで配置する場合、複数 Primitive を入れたい場合  
この編集結果が「複数」でないと、正しい挙動になりません。

このあたりが、Sublayer ノードと挙動が異なるので  
注意が必要です。（私は当初バグか何かだと思った）

![](https://gyazo.com/5a91ad529823a8bda84fca7a5f8a5e11.png)

もう 1 つ Merge ノードで注意が必要なのが、 Merge Style です。

![](https://gyazo.com/bd9cb215a71b39d578289a5b387573ce.png)

これは USD のコンポジションの解決順序にかかわることですが  
Merge をするときに、同じ Primitive が会った場合  
どちらを優先するのか　というのが決められています。  
入力が 0 側が弱く、右に行くにつれてつよくなっていきます。

![](https://gyazo.com/efed7fdf0c3330001f789d940902972d.png)

その編集順序は「レイヤースタック」というかたちで保持されます。  
このレイヤースタックでレイヤーの順序が保持されている状態が「Separate Layers」です。

![](https://gyazo.com/b5c8a5c899ff6c5d1fb0232ca5d6a248.png)

このように、ノードの右下に～～ Layers と表示されているのが  
現在のレイヤースタック（サブレイヤーで重ねたレイヤーをあつめたもの）

![](https://gyazo.com/4c8b73a48ddc3676cd7c53d5f502e315.png)

これを Flatten Layers に変更するとどうなるかというと  
レイヤースタックが「つよい」レイヤーにまとめられていることが分かります。  
つまりはそれまで維持していたレイヤースタックを結合することで  
レイヤーのコンポジットを「結合」したような状態になります。

どういうときに意味があるかなぁと考えてましたが  
複数の大量のレイヤーをコンポジットしていく場合の AE のプリコンポーズに近いのかな？  
と思います。  
どのような順序で編集を適応するか、処理を確定するようなイメージ？

#### Graft

![](https://gyazo.com/26b8989ba884c093840e2c756a6b8aba.png)

Graft ノードは、挙動としては Reference のように「1 つめの Inputs（あるいは指定の Path）」に対して  
MultiImputs に入力された Primitive を「接ぎ木」するようにマージします。

![](https://gyazo.com/625be0116191aa39a50a027031b9cabf.png)

デフォルトの状態で 2 つのノードをセットすると、このようになります。  
ParentPrimitiveType が「Xform」の場合、
自動で Xform ノードを作ってくれます。

![](https://gyazo.com/1a9699420a75633f04c53bccd3d68f01.png)

接ぎ木先の Primitive は Destination Path Defaults で指定することができて  
通常は opinput 下に接ぎ木されますが、自分で指定もできて  
サンプルのようにすると

![](https://gyazo.com/8d1522d2e256b5854ca0b93ae024d960.png)

このように、個別の Primitive を指定のルールで接ぎ木できます。

![](https://gyazo.com/e43b31d3fc832932e5733e9eb5547af7.png)

接ぎ木先は、個別の入力単位でも指定できて

![](https://gyazo.com/925f8adf5f8309cf3cc79aa34e7d9b70.png)

このようにすると、

![](https://gyazo.com/430c5fb70d4e4f87c088ab0d8951270e.png)

個別に接ぎ木先の Path を設定できます。

挙動はほぼ Reference ですが、Reference とは違い、  
すべて実体のノードとしてシーングラフが構築されます。

![](https://gyazo.com/4556d47c3ee1b20548f695e5de3787b5.png)

もちろん、入力が Reference の場合は

![](https://gyazo.com/f2925b9f6a6f500af2ef8579597b6056.png)

Reference のまま接ぎ木処理になります。

シーンをノードで構築する場合は、この Graft ノードを使用することで  
かんたんにツリー構造を構築することが出来ます。

#### Switch

![](https://gyazo.com/42354b7c361fe0752d56a9ab9e8955ad.gif)

Switch ノードは、Varitnt Set のように複数の入力から 1 つの入力に「スイッチ」することができるノードです。

![](https://gyazo.com/668381c22357f75a8da0a218bcbaa4b6.png)

Variant Set に比べると構造はシンプルで、入力に対して  
どの Input を使用するかのスイッチがあるだけです。

ですが、Variant Set となにが違うかというと  
こちらはあくまでも切り替えた結果の Primitive を返すだけで  
USD の構造としての Variant Set は持ちません。

```
def Cube "cube2" (
    customData = {
        int HoudiniPrimEditorNodeId = 65
    }
)
{
    double size = 2
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]
}
```

なので、この Switch ノードの結果の usda を確認しても  
含まれているのは Switch で選択されている Primitive 情報のみです。

あくまでも、SOLARIS 内で入力を切り替えたい・スイッチしたい場合にのみ使うのが  
この Switch ノードということかとおもいます。

#### prune

![](https://gyazo.com/28f423dff229866a96f21589800ea281.png)

pruneは、入力のPrimitiveのうち **「条件に当てはまる」** Primitiveを無効 or 非表示にします。  

![](https://gyazo.com/c6cfba365d4d3dde8a4bc4ef1f1fd533.png)

Pruneノードの条件を指定すると

![](https://gyazo.com/4667a9b6bbb63a549a7a66e12cdabeb1.png)

条件に当てはまるノードが非表示になります。  

![](https://gyazo.com/ef0b0e5de945cd5915defccab24a3965.png)

デフォルトだと Make Invisible の場合は「非表示」になるし Deactivate だと「無効」になります。

出力されるUSDファイルは、非表示なら
```
over "cube1"
{
    token visibility = "invisible"
}
```
無効なら
```
over "cube1" (
    active = false
)
{
}
```
こうなります。


### Material 関係

#### materiallibrary

![](https://gyazo.com/4779def23714d785095ca81b09f89c8b.png)

materiallibrary は、VOP ネットワークで作られた（/mat 下)マテリアルを  
SOLARIS の世界に Import するためのノードです。

![](https://gyazo.com/b76a03ede976b08ebf40b35485351b79.png)

例として、  
このようなシンプルなシェーダーを /mat 下でつくったとします。

しかし、作っただけでは SOLARIS 上では使用することが出来ません。  
ので、 materiallibrary で読み込みます。

![](https://gyazo.com/f314352cd6487ccf5be798166e10e017.png)

Container Path は

![](https://gyazo.com/548d2a23f1c1753593d5c4df191c158c.png)

Scene Graph Path 内のどの空間に Import するかの設定です。  
USD では、マテリアル関係も同じシーングラフ上に構築されますが  
どこにおくかは指定されていないので、自分で決めることが出来ます。

あとは、 Material VOP に、先ほど /mat 内でつくったシェーダーを指定すれば  
USD の Material/Shader として Import することができます。

![](https://gyazo.com/b2ee0911cd843eeed0a331ac437a0dc5.png)

Geometry Path にアサインしたい Primitive を指定すると  
自動でアサインまでしてくれます。

#### assignmaterial

![](https://gyazo.com/668c7cd8899883f83821daec8df54b20.png)

assignmaterial は、現在の SceneGraphPath 内にある Material を、指定の Primitive に対して  
アサインします。

注意点は、VOP などで作成したマテリアルは、 materiallibrary の説明にもある通り  
自動では import されません。  
ので、使用する場合は事前に materiallibrary でマテリアルを import する必要があります。

![](https://gyazo.com/2ca886211f0082c4291586acd0327cdd.png)

アサインするには、 Primitives に、対象の Primtive 名を設定し  
アサインしたい対象の Material Path をセットします。

なお、 Scene Graph Path の Material をターゲットに対して Drag&Drop することでも  
この assignmaterial ノードを自動作成＆アサインをすることができます。

### そのほか

#### python

![](https://gyazo.com/bf60ffd43b76ea320763ae433838aaf6.png)

最後に紹介するのは Python Script。  
このノードは、これまで構築したシーングラフのステージを Python の pxr モジュールの Stage で受け取り、  
直接編集することが出来ます。

```python
node = hou.pwd()
stage = node.editableStage()
```

デフォルトではこのようになっています。  
後はどうぞご自由に。。。。という感じですね。  
  
http://graphics.pixar.com/usd/docs/api/index.html  
  
USD は Python からほぼ 100％自由に操作することができます。  
関連する関数群も充実というかとんでもない物量で、私もできる限りドキュメントを読んでいますが  
未だに全容を把握することが出来ません。

しかし、シーングラフの操作に関してはかなり扱いやすく  
関数やクラスの設計も直感的でわかりやすいです。  
この充実度だけとっても USD を全力で使っていきたいと思える大きな理由でもあります。

```python
from pxr import Usd

collectionPrim = stage.GetPrimAtPath("/collections")
colAPI = Usd.CollectionAPI.GetCollection(collectionPrim,"selected")
for prim in colAPI.GetIncludesRel().GetTargets():
    # なんか処理を書く
```

例として。  
この Python ノードの前段階までで指定した Collection に含まれる Primitive を取得。  
取得したノードにたいして処理したい場合なんかは  
このようにすることで、指定の Primitive に対して編集を行うことが出来ます。  
  
やっかいなのは、ドキュメントが C++版なので多少の脳内変換が必要なのと  
用語関係は USD の用語で書かれているので Houdini 側と一致しないこと。  
あとは、USD のデータ構造はある程度把握しておく必要があるので  
若干敷居は高いかもしれません。（Collection は Relation で扱われてる...等）

https://fereria.github.io/reincarnation_tech/11_Pipeline/10_USDTips/02_usd_py_cheatsheets/

よく使う Pyton コマンド集は別途ページを作成してあります。

## まとめ

とりあえずアドカレ締め切りの日までにざっくり調べたノードの使い方でした。  
  
検証して分かったことは、  
SOLARIS のノード（コンポジションアーク系ノード以外）は USD の細かい仕様だったりを  
いいかんじに Houdini 風にラップして  
ユーザーに USD をそこまで学習しなくても、直感的にシーンを構築できるように  
出来ているなと感じました。  
（特に、コンポジションの解決順序とかをほぼ意識せず直感的に操作できるのが素晴らしい）

個人的に調べていて勉強になったのが Merge/Graft/Switch。  
この3つとかコンポジションアークのノードと挙動が同じでなにが違うんだろう？？？？？と  
ずっと疑問でした。  
ですが、調べたらどう違うのかが分かったし  
結果どういうシーングラフが作られるのか理解出来たのが収穫でした。

今回までに調べたノードの中だと、やはり Merge Graft Swith などでのシーングラフ構築と  
sopimport sceneimport materiallibrary 等の、今まであった Houdini の世界から  
オブジェクトを持ってくるあたりがよく使うノードになるのではと思います。  
  
なので、USD とはなんぞや？というのはとりあえず横に置いておいて  
sopimport や scene import で、SOP で作ったモデルを持ち込んで  
Graft や Merge でシーンのツリーを構築して、ライトをおいてみてレンダリングしてみたり、
PointInstancer で、Point に対して大量のモデルを配置してみる（Point 配置自体は SOP でやる）  
などで SOLARIS に慣れつつ、  
それ以外のノードで複雑なシーンなどを作ってみると良いのではないかと思います。

対して、今回説明しなかった Sublayer/Reference/Variant 等のノードは  
別途リサーチ記事にまとめようかと思いますが  
今回説明したノード群と違い、より USD のマニュアル操作 的な理解が必要という印象があります。  
細かいところまで自分の思うとおりにマニュアル操作したい！という場合などは  
これらのノードも併せて使用することで  
より、USD を手軽に、より細かく扱えるようになるのでは？と思いました。

（そして最後は Python + inlineUSD でマニュアル操作の世界へ...)

というわけで SOLARIS と USD の検証はまだまだ続く.....
