---
title: Houdiniの群衆をSOLARISに持って行ってみよう(1)
---

浜タコさん（@hamatako）の群衆勉強会で群衆のパイプラインワークフローを色々聞いていたら
Houdiniの群衆をSOLARISに持って行くと、
AgentがUsdSkelになるというのを聞いたので
どういう形で出てくるのかをチェックしてみました。

## サンプルを開く

![](https://gyazo.com/c21bb05d6fe5ffe936d9aa15fb86e8d8.png)

まずは、群衆のサンプルシーンを開きます。
開くには「Crowd」タののギフトボッククスっぽいものをクリックすると
群衆サンプルシーンを開くことができます。

![](https://gyazo.com/81208ab88b2b8fe5de5ca0b47975f9d6.png)

読み込むと、こんな感じのシーンを開くことが出来ます。

![](https://gyazo.com/8dd6607c3b22e600d75c93e52d7be62d.png)

Streetなので、こんな感じのシーンです。

## SOLARISに持って行く

![](https://gyazo.com/cd964b08f3676bc6aaecca82eeff6aea.png)

読み込んだら、シーンをSOLARISにもって行きます。
StageNetworkに移動して、SceneImport(all)ノードを作ります。
このノードを使用すると、Houdiniの世界をそのままSOLARISに持ち込むことが出来ます。

## usdviewで表示

持ち込むことができたら、とりあえずusdviewで見れるように出力します。
![](https://gyazo.com/9ecb724ec6995f61f837133e735e7993.png)

USDROPを使用して、usdファイルとして出力してみます。

![](https://gyazo.com/dbbe29718fe122a4dcf3d8e73944e26a.png)

ValidFrameRangeがデフォルトだとCurrentFrameだけでアニメーションが出力されないので
Render Specific Frame Range にしておきます。

![](https://gyazo.com/7c5ae4719fca6d7a02e584616be0a0ec.png)

完了すると、指定フォルダにusdファイルが出力されます。
出力されたファイルはusdviewなどでも開くことができるようになります。

## もう少し詳しく見てみる

出力はできたようなので、実際どのような構造USDとして出力されているのか細かく見ていってみます。

### 全体

まず、全体のシーングラフ。
これはHoudiniの構造がそのままUSDのシーングラフとして出力されます。

![](https://gyazo.com/cbef024cd72e8fdc049b1167efd6f676.png)

こちらがHoudini

![](https://gyazo.com/e2f2bd7c37018123f7451adc09a6c27b.png)

USDはこちら。

大きな違いは「crowd_sim(DOP Network)」が出力された側には存在しません。
あくまでも出力されているのはSOP Networkのノードのようです。

### Agent

![](https://gyazo.com/2c02014d098384bb3434fcd2eb5dc0c0.png)

エージェントは個別のモデルデータです。

![](https://gyazo.com/a4baddd171daddf0d604cb254e1c1a5d.png)

個別のAgentは、それぞれusdとしてMeshが出力されます。
しかし注目はこのモデルには **SkelもWeightもはいっていない** です。
あくまでもTスタンスのMeshのみが各Agent名のフォルダに出力されます。

![](https://gyazo.com/f53eff552a7f0b8bc1b2cffe85ef3935.png)

各モデルは、出力されている usda ファイル直下に読み込まれています。
しかし、あくまでもこれはHoudiniのシーングラフと同じ場所に同じように出力されているだけで
このモデルは並べるのには使用されていません。
なので、全シーンをSOLARISに持ち込んだ場合、このモデルが持ち込まれますが
Agent関係のPrimは本来は不要になります。

### crowdsource

では、実際のモデルの組み立てがどこで行われているかというと

![](https://gyazo.com/56cb81572ed1b4f37359af5f5736cc6a.png)

実際のCrowdSimをしているであろうcrowdsourceで

![](https://gyazo.com/92c7a0ae9e305cb0112220a7a680b78d.png)

USD側もSkelとMeshの組み立てが行われています。

![](https://gyazo.com/737dff65a6dfdb86f7459833d7d59afc.png)

agentdefinitions内で、Mesh（Meshはshapelibrary内にある）とSkelがReferenceで構築され、

![](https://gyazo.com/c2b6f6c4df40241d504ecf0b2e6f8cac.png)

個別のagentでReferenceで読み込まれます。
注意点としては、このRefernceは「現在のレイヤー内にあるMeshやSkeletonPrimをReferenceしている」
ということです。
SOLARISから出力されたときに個別のusdとして出力されていますが
このファイルは外のAgentは読み込んでいません。

### Group

![](https://gyazo.com/92c79c31843083fc64ea42ed1ea8161e.png)

シミュレーションはcrowdsourceで構築されていたようですが、最終的な出力は別のGeometryで出力されています。

![](https://gyazo.com/d3151c4651778e4ab66a4e30151e9f5e.png)

これは、crowdsourceから、objectMergeを使用して
指定のGroup名になっているAgentだけになるようにしています。

![](https://gyazo.com/4794e7cb23b727f16682d7f527a87160.png)

このobjectMerge分も個別のusdになっています。
注意が必要なのは、このcrowdsourceを読み込んでいるobjectmergeのusdはcrowdsourceは見ていなくて
個別のデータになっていることです。
あくまでも、このobjectMergeのデータ内でのみ完結しています。

## というわけで...

SOLARISにAllで読み込むことで
群衆をSOLARISに持ち込むことが出来ますが、その場合不要のノードが大量に読み込まれてしまいました。
なので、Improt Scene(All)は不味い。

さてどうするかと思ったのですが

![](https://gyazo.com/45fec36eac893ebf798fe2d251648d2d.png)

素直にsopimport で各グループのジオメトリにしている object_mergeのノードを sopimportでロードして
USD ROPで持ち込むのが正解のようです。

![](https://gyazo.com/a8c710f46bb790377309e61de2219b93.png)

結果。
各Agentとアニメーション、Setupをしているagentdefinitionsだけが出力されました。

Import Allだとほんとうに全部Importしてしまうので、
不要なもの（GeometryのDisplayFlagがOffになっているもの）がある場合は気をつけないといけなそうです。

## おまけ

![](https://gyazo.com/7e1a4eefe24244fe711c4579853bdc12.png)

なにかの不具合か、Skeletonがエラーになる模様。

![](https://gyazo.com/a7dd848f74b109706453b6ad980c785a.png)

MakeInstanceすると壊れる模様（Houdiniもお亡くなりに...）

ひととおりの挙動は理解できましたが、どうあるべきかはまだまだ考える余地はありそうです。