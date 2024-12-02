---
slug: /maya/maya_usd/03
title: BifrostUSD基本編
description: BifrostでUSDを編集する基本的な部分を理解する
sidebar_position: 2
---

今回は、MayaBifrost を使用した USD 編集について、基本的な手順や構造などを理解していきたいと思います。

## 起動する

![](https://gyazo.com/e7c59696179ee5fd2c5ea6718c6bb96b.png)

まず、Bifrost を起動してみます。  
起動するには、Window から BifrostGraphEditor を開きます。

![](https://gyazo.com/8c002acd78c22d72e059b6d0193f6cd7.png)

開いたら、CreateGraph で新しく Graph を作ります。

![](https://gyazo.com/4652fe9b2803299a2f181c8e26cce556.png)

作成すると、このような bifrostGraphShape がシーン内に作成されます。

![](https://gyazo.com/78343d284d7e562c3c895346a74ccc43.png)

この状態からスタートします。

## Bifrost と Maya と USD の関係性を理解する

まず、操作していくうえで「Bifrost」「Maya」「USD」のそれぞれが  
どのような関係性になっているのか見ていきます。

Bifrost は、Houdini の HDA や Subnet のように Graph 内で何かしらの処理をノードを使用して  
記述することができます。  
今回は USD の処理を中心に試しますが、USD 以外のことももちろんできます。

![](https://gyazo.com/122f500d188f95e69a76f3ed954732cd.png)

USD を操作したい場合は、USD に必要なノードが揃っています。

つまり、3 つの中で「処理の記述」をするのが Bifrost の役割になります。

### Bifrost から USD を出力する

前回の記事で、Maya での USD には「Maya の世界」と「USD の世界」が存在すると書きました。  
この考え方は Bifrost を使用した場合にも非常に重要になる概念です。

まずは Maya を忘れて Bifrost と USD で考えます。

![](https://gyazo.com/4d4d02e7685ec598d8613fdb5c3fd7ca.png)

add_to_stage ノードを Output に接続します。

![](https://gyazo.com/37789e6549b67200fa93d3b2e5e02df9.png)

結果、UsdProxyShape が作成され、bifrost.usd が自動的に作成されます。  
この UsdProxyShape とは「USD の世界」です。  
つまり、Bifrost で編集した情報が USD の世界として出力され「bifrost.usd」という形で  
レイヤーに出力されているわけです。

![](https://gyazo.com/a5c7b11d3e3b63ec24ed4ce2ebc8fbfc.png)

さらに DefineMesh ノードを使用して、MeshPrim を追加します。  
AddToStage ノードは、指定の Input の PrimDefinition（定義）を Stage に追加する効果なので

![](https://gyazo.com/abad1ab9a8503f94823144124adae404.png)

USDMesh 内に MeshPrim が生成されました。

### Maya から Bifrost に読み込む

以上の手順だと、Bifrost 起点で USD にデータを出力できましたが  
当然それだけではなく Maya から Bifrost に Mesh やその他いろいろなノードを  
読み込むことができます。

![](https://gyazo.com/52749905e9a88bb712e6b6916dea1a62.png)

試しに、Maya 側で Sphere を作成し、これを GraphEditor の UI にドラッグ＆ドロップします。

![](https://gyazo.com/1497d98449c3efb5a27a3aee200962ed.png)

これで、Bifrost に Maya の Mesh を持ち込むことができました。

![](https://gyazo.com/2b0116e4dc6cab4c161a126f206dec51.png)

この Shape を、Define Mesh ノード > Add to Stage ノードとつないで Output すると、

![](https://gyazo.com/d902f87984e7e0deb333c44f1bf65ee1.png)

UsdProxyShape 内に Mesh を読み込むことができます。

このように Bifrost を経由すると、 Maya の世界と USD の世界をリアルタイムに接続することができて  
この状態で Maya 側の Mesh を操作すると、自動的に USD 側の Mesh も変形できます。

### USD から MayaMesh へ

同じように、USD から Bifrost 経由で Maya の世界に Prim を持ってきます。

![](https://gyazo.com/2a225da13985ca77807226adb94cf37b.png)

OpenStage で Kitchen_set を開き、ReadUsdMeshes ノードを使用して、特定の Path の Prim を  
Mesh に変換します。  
この時の「Mesh」とは「BifrostMesh」を指します。MayaMesh ではないことに注意が必要です。  
この Mesh を、Output で出力すると

![](https://gyazo.com/7837b6a7434b9e007c1db057f5ef1853.png)

BifrostGraph ノードに出力メッシュが表示されます。  
ここからさらに MayaMesh に変換します。

![](https://gyazo.com/75f6a95b3e66d6fc814637e2fc5479b0.png)

Maya のノードエディタで、 BifrostGraph ノードの Mesh→BifrostGeoToMaya ノード →Mesh の InMesh へ  
つなぐことで

![](https://gyazo.com/82b7a34e599bf5e1a09d231fca771f79.png)

Maya 側に Mesh を持ち込むことができました。  
できるけど、とてつもなくめんどくさいことがわかりました。

![](https://gyazo.com/6453e4bc8000bb1c623e477c90132b44.png)

以上のことから、自分なりの解釈でまとめるとこのような関係性になります。  
Bifrost 内では、USD の Stage と BifrostMesh の両方があるので  
どちらで扱っているかは注意しないと混乱しそうです。

雑な理解だと、

![](https://gyazo.com/560e08e967e5ffee4c69a3778b4a754f.png)

アイコンが USD の場合は、USD を扱っているというルールになっています。  
しかし、Output はそのノードの処理に応じて USD か BifrostMesh かは変わります。
ReadUsdMeshes の場合「Mesh」は BifrostMesh のことを指すので  
Stage を入力で BifrostMesh を出力します。

![](https://gyazo.com/a7b1ea8be032e0a97a6c80086ce9238a.png)

input は、Maya の Mesh を BifrostMesh として読み込むものなので  
Input はなく、Output が BifrostMesh になります。

![](https://gyazo.com/e506d136c5c2913afb4849d1600f26d9.png)

DefineMesh と AddToStage も両方 USD アイコンで、USD を扱います。  
DefineMesh は、BifrostMesh を USD に変換するノードなので、入力して BifrostMesh を受け取りますが、後の処理は USD です。

## まとめ

![](https://gyazo.com/94b2866ecd03b0f7a0b220c8012c8bad.png)

何となく操作方法や考え方はわかってきたので  
アトリビュートの追加をするネットワークを作ってみましたが、  
1ノード＝USDのコマンド１つとほぼほぼ対応していて、APIをわかってさえいればまぁ直感で  
理解できるかな？と思います。  
しかし、アトリビュート追加してセットするだけでも結構な長さになるので  
使いどころはなかなか難しいです。  
  
利点としては、MayaのMeshをリアルタイムでUSDに持ち込むことができるので  
プロシージャルな配置をしつつモデルを作成する等の使い方はできるのかな？と思います。  

