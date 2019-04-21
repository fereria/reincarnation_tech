# Vtx Point Primitive Mesh Polygon について

<!-- SUMMARY:Vtx Point Primitive Mesh Polygon について -->

Houdini を調べていると、Maya 以上に細かくノードやコンポーネントに  
名前が付いていて？？？になることが多いです。

![](https://i.gyazo.com/9cc9f56715d8e1666158de9b675eadc6.png)

とくに分からなかったのが、 Polygon と Mesh の違い。  
Maya 使い的には「同じじゃね？？？」になりましたが  
別の物として区別されている。ということはこれには意味があるはず。

ということでまとめてみました。

## Geometry の要素

まず、Geometry。  
Maya 的に言えば Geometry は Shape ノードに近い？

![](https://i.gyazo.com/2b520a48117ce829d3eb1d9cb65df3a1.png)

そして Geometry は、 Point Vertices Primitives を持っている。

Maya の場合は、  
**Vertex - Edge - Face**  
このような関係になっているのが、

Houdini の場合、  
**Point - Vertex - Primtive - Detail**
このようになっている。

また、この Point Vertex Primitive のように Geometry を構成する要素のことを「エレメント」と呼ぶ。

### Vertex と Point

![](https://i.gyazo.com/2adac0b985a90ae253e601ea4039f556.png)

Point が Maya の Vertex に近い。  
Vertex は、Face 単位の Vertex で、複数の Vertex→Point のような構造になっている。

![](https://i.gyazo.com/5e9b9fc936c1cec1f98e4f0a1b395275.png)

GeometrySpreadSheet を確認すると、Vertex はいずれかの PointNum と対応した構造になっている。

### Primitive

Primitive は、Maya でいうところの Face にあたる部分。  
いろいろな意味合いをふくんでいて  
「ポリゴン・カーブ・サーフェイス・メタボール・パーティクル・ボリューム」  
など、を含んでいる。  
Face にあたると書いたけれども、
ポリゴンの場合は 1Face=1Primitive になるが、サーフェイスの場合は複数面=1 プリミティブ扱いでもある。

### Detail

Detail は、Point・Vertex・Primitive の要素をすべて含む単位のこと。

## Mesh と Polygon

Point - Vertex - Primitive の構造を理解したところで、  
Mesh と Polygon の違いとはなにか？という話。

ありがたいことに、Twitter 上で教えて頂きました。

<blockquote class="twitter-tweet" data-lang="ja"><p lang="ja" dir="ltr">TAさんならHoudiniのからシンプルなGridとかをGeoアスキーファイル出力して中身眺めるのも面白いと思いますよ。ジオメトリスプレッドシートでも良いですが。</p>&mdash; Ryu (@dragonboy765) <a href="https://twitter.com/dragonboy765/status/1109015302619062272?ref_src=twsrc%5Etfw">2019年3月22日</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

まず、内部の構造がどう違うのか確認します。

### Polygon

![](https://i.gyazo.com/3150e3ab000768be436682a240aefcd4.png)

Polygon の表示を見ると、 <PrimitiveNum:ID -> PointNum> のように表示されます。

![](https://i.gyazo.com/613985eacbe029f8f3559330205fe531.png)

それぞれの Primitive ごとに ID が振られていて、それが結線情報になっています。

### Mesh

![](https://i.gyazo.com/b657c2a5636fbefc28936bec51ffbbe5.png)

対して、Mesh の場合は 1 つの Primitive のみ。

![](https://i.gyazo.com/4513c183d2c4f671b8dd014a45540308.png)

ID を確認してみても Primitive の ID は１つのみで、Point が 9 点あるのみになっています。

### Polygons and Meshes のヘルプを確認

> Polygons are shapes constructed from a series of straight edges.

Help を確認すると、Polygon についてはこういう記述があります。  
いわゆる Maya のポリゴンと Houdini のポリゴンは同じニュアンス。

> A mesh is a collection of polygons with guaranteed ordering.
> It is much more efficient that the equivalent polygons,
> and unlike most regular polygons you can convert it directly to NURBS.

Mesh とは、順番の決まったポリゴンの集まりで、ポリゴンより効率的。  
そして、そのまま NURBS に変換することができる。

さらに、Twitter で教えていただきました。

<blockquote class="twitter-tweet" data-lang="ja"><p lang="ja" dir="ltr">Houdiniでいうメッシュは実体がNURBSで表示がポリゴンのことです。<br>なのでNURBS系ツールで制御可。<br>ポリゴンはポイントを結んでできた面のことです。ポリゴン系ツールを使って制御可。<br>ポリゴンメッシュはメッシュとポリゴンの中間で実体がポリゴンだけどNURBSのようにサーフェスUVを持っています。</p>&mdash; Kaz-Kitaguchi (@kit2cuz) <a href="https://twitter.com/kit2cuz/status/1109134546052640768?ref_src=twsrc%5Etfw">2019年3月22日</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<blockquote class="twitter-tweet" data-lang="ja"><p lang="ja" dir="ltr">フェースが複数あるけれど、それを一枚のサーフェスとして扱うものとしてポリゴンスープというものがあります。データ量が軽くできるものの、個々のフェース情報を持ちません。水のようなポリゴンの表現に適しています。</p>&mdash; Kaz-Kitaguchi (@kit2cuz) <a href="https://twitter.com/kit2cuz/status/1109135297277648896?ref_src=twsrc%5Etfw">2019年3月22日</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

つまりは、Mesh とは Maya でいうところの History を維持した状態の Surface to Mesh Convert した  
オブジェクトのこと。

![](https://i.gyazo.com/784be6bb75393d4903c6e468341f7766.png)

Cube の Primitive Type を Polygon にした場合は、

![](https://i.gyazo.com/f5278821c4c297f9c636885830c3470f.png)

ポリゴン系ツールが使用できるので、ベベルの効果がかかっているが  
Type を Mesh にした場合は、ベベルの効果はかからない。

![](https://i.gyazo.com/4158fbdf2ee3407a63be6e5ab7abaf40.png)

このように、Mesh から Polygon に変換すれば

![](https://i.gyazo.com/4fee5cd5b57ccf551a37ef4c82a7b499.png)

効果がかかる。  
なるほど。

## まとめ

PolygonMesh と PolygonSoup はまだ使いどころが来ていないのでまたこんど。

データ構造は Point > Vertex > Primitive > Detail それぞれを Geometry を構成するエレメントと呼ぶ。

Mesh は、内部的には NURBS で１つのサーフェースとして扱われているので  
プリミティブは１つ、また Polygon 系ノードは使用できず NURBS 系のノードが使用できる。  
Polygon は Maya の Polygon と同等で、ポイントを結んでできた面を指す。

GeometrySpreadSheet で構造を確認すると、Mesh と Polygon では構造の持ち方が違う。  
Polygon は、１つの面がプリミティブで、Point から Face が構成されている。  
Mesh は、内部的には NURBS からサーフェイスが作られていて、サーフェイス自体が１つのプリミティブとして  
扱われているので、Primitive は１つしか存在しない。

## 参考

- https://www.kickbase.net/entry/houdini-component
- https://houdini.prisms.xyz/wiki/index.php?title=Points_and_Verts_and_Prims
