---
title: Houdini 写経 01 RBD_ClueConstraint
---

[Houdini ビジュアルエフェクトの教科書](https://www.amazon.co.jp/dp/4844367609/ref=cm_sw_r_tw_dp_U_x_Dt3KCbRA0MCTX)の内容を写経しながら Houdini のノードの挙動などを調べていきます。  
基本的な手順は本に書いてあるので省いてます。  
自分が気になった所をメモ。

![](https://i.gyazo.com/9fe25da90224b1d0543743207e73464a.gif)

完成図はこんな感じで、地面に落下すると割れるようにします。

## モデルを割る

まず、シミュレーションをする前に  
モデルを　 voronoifracture を使用して割ります。

![](https://gyazo.com/14200356a195b27d9a01c6f5a9d13b90.png)

ネットワークはこんな感じ。  
基本本の通りに組んであります。

メッシュからヴォロノイ用のポイントを作り（scatter）、出力する...と言う流れ。  
メインの部分は OK として初心者的にものすごい疑問になったのが

**なんで最後 Null に刺してるんだろう？**

これ以外のモデルをなにかしているもの（出力したりなにかしたりする場合の最後のノード）  
は最後が Null。  
なんでだろう？

https://www.sidefx.com/forum/topic/45602/?page=1#post-203566

調べたらありました。  
超意訳ですが、明示的に「これがおわりの部分ですよ」「ここからはなにもしてないよ」  
という目印だったり、なにかしらの動作をフックさせるためのアンカーとして  
慣例になっているぽいですね。

![](https://i.gyazo.com/cd1da4c0685720d47fe17598030a69fc.png)

別のオブジェクト内で別のノードのアウトプットを使いたい時など  
Null で出力させたい部分を指定しておいて、  
ObjectMerge で Null を指定させるような使い方をするようです。  
なるほど。

## シミュレーションをする

![](https://i.gyazo.com/da44220c95cab4078a8d49b7250e07d0.png)

まず、衝突用の地面を作成します。  
Collisions -> Ground Plane を作成します。  
そして、

![](https://i.gyazo.com/229106d432766e3334a2623bcb4607b2.png)

RBD Glued Objects をクリックします。  
RBD は「Rigid Body Dynamic」の略です。

実行すると、Geometry オブジェクトノード内の Null 以下に

![](https://i.gyazo.com/ffe582bddac4b917c642d6313b64dfd3.png)

こんな感じで自動でノードが追加されます。

RestPositionSOP とは、デフォルトの位置を記録したもの。  
Assemble は、オブジェクトをパーツ分けしているノード。  
DOPImport が、シミュレーションにモデルを引き渡している？はず、です。

## AutoDopNetwork

そして、シミュレーションの本体になっているのが AutoDopNetwork オブジェクト。

![](https://i.gyazo.com/0f51335cee8008640a7864a77f0bdf5b.png)

中身はこんな感じ。

大きく分けると、左側がシミュレーションをしている構造で  
右側の Glue というのが、地面に衝突してもモデルを全部割らずに接着したままにしてくれる  
GlueConstraint の設定部分になります。

## RigidBody シミュレーション

### RPDPackedObject

![](https://i.gyazo.com/7202f25a9dccdc45ad66aeaca48b0d3f.png)

まず、RigidBody でシミュレーションするモデルは RPDPackedObject で取得する。

![](https://i.gyazo.com/2d84e4f0cdbe140aca1856af41376150.png)

アトリビュートを確認してみると「SOP Path」が、↑ で指定した DOPImport ノードになっています。  
Help を見ると

> Creates a single DOP object from SOP Geometry that represents a number of RBD Objects.

SOP ジオメトリから DOP 用のオブジェクトを生成しているノードが RBDPackedObject。

### solver

次がソルバ。
毎フレームなにかしらの計算を行うノード。  
ヴォロノイで割ったモデルに対して RigidBody の計算を付加しているのが「RigidBodySolver」  
RigidBody 以外にも StaticSolver と SOPSolver があるのだが  
どちらもこの部分でシミュレーションをしている形かな。

### Merge

Merge は、複数のジオメトリを１つにまとめる機能をもっている。  
と、Help には書いてるのですが  
このサンプルの場合地面と破壊モデルを Merge しているので  
Maya のモデルを結合するというよりも、個別のシーンだったものを１つに取りまとめる  
的なニュアンスなのだと思います。

### Glue Constraint

![](https://i.gyazo.com/fb16a8065fb0be79cefd7efd67cbfeab.png)

GlueConstraint は、ヴォロノイで分割しているモデルをある一定の衝撃が加わらない限り  
くっつけておく事が出来るコンストレイン。  
設定本体は「Glue Constraint RelationShip」ノードで、ここでどのぐらいの衝撃まで  
結合しておくか等を指定することができる。

### Constraint Network

これは GlueConstraint にかぎらず、RBD 内でコンストレインを使用する場合に使用するノード。

![](https://i.gyazo.com/606a4ff0b755dd4403c008d1fa7d8612.png)

Constraint Network 内で SOPPath を指定していて、そのよみさきは  
Geometry 側で新しく追加された CONTRAINTS の Null。

![](https://gyazo.com/d8c4ac422c5a505c5dd86291794a9a6e.png)

この CONSTRINTS はこうなっていて、Geometry 同士の結線情報？のようになっている。  
その後に Attribute が追加されているのは、Glue コンストレインを行うのに必須のパラメーターを追加している。

## まとめメモ

Houdini のネットワークは、子に行くにつれて徐々にノードの効果を付加している。  
複数の系統があっても、出力は 1 つ。  
系統をまとめているのが Merge。

## 参考

-   http://houdini.indyzone.jp/blog/dop%E5%9F%BA%E7%A4%8E-1/
-   http://houdini.indyzone.jp/blog/assemble-sop/
-   http://naniwa-cg83.blog.jp/archives/295498.html
-   http://houdini.indyzone.jp/blog/solver%E3%83%8E%E3%83%BC%E3%83%89%E3%81%AE%E4%BD%BF%E3%81%84%E6%96%B9/
