---
slug: /maya/maya_usd/01
title: MayaUSDの基本構造
description: MayaでのUSDの扱われ方を理解する
sidebar_position: 0
---

[USD アドカレ 2024](https://qiita.com/advent-calendar/2024/usd) 1 日目は、MayaUSD の基本構造です。

これまで、あまり MayaUSD については触れていませんでしたが、Maya2025 になって  
だいぶ使えるようになってきた気がするので、  
何回かに分けて Maya での USD の構造や作法についてを調査していきたいと思います。

## Plugin

https://github.com/Autodesk/maya-usd

MayaUSD は、プラグインとして提供されていて、コードは上記の Github で公開されています。

![](https://gyazo.com/265455b0130ca32d8cf1b45b42380e94.png)

特にビルドする必要はなく、Maya をインストールすると対応しているバージョンの MayaUSD プラグインがインストールされています。  
今回テストしているバージョンは、Maya2025.3、MayaUsd のバージョンは 0.30 です。

## Maya シーングラフと USD シーングラフ

まず、Maya で USD を使用する場合は「Maya のシーングラフ」と「USD のシーングラフ」の 2 つが存在していることを  
最初に理解する必要があります。  
まず、通常の Maya のシーングラフを軸に説明していきます。

この 2 つは、それぞれ別のものですが　 Maya の機能としてそれぞれのシーングラフに「コンバート」を介して  
切り替えるような構造になっています。

![](https://gyazo.com/e6a941bf43d0057559c3abd553053a3a.png)

Maya のシーングラフとは、いわゆる「これまでの Maya」の構造部分で  
良く見慣れた Maya のノードのことを指します。  
Maya は、すべてのノードが「何かしらのノード」によって定義されていて  
このノードが親子かかリレーションによって接続された DAG として構成されています。

![](https://gyazo.com/9b5115935de024e6443c1d491eaddc96.png)

このシーンに対して、ファイル＞読み込み...を使用して、USD ファイルをインポートします。

![](https://gyazo.com/4ac6d39f160177abdfda3ac576c2eacc.png)

例として、Kitchen_set をロードしてみます。

![](https://gyazo.com/3587bad725361bf63e285d94b52ca04c.png)

このように、Maya シーン内に USD をロードすることができました。

![](https://gyazo.com/c71d7c2a671465658d99b397a5e22f16.png)

が、ロードはできましたが  
このノードは「Transform」ノードや「Mesh ノード」として読み込まれていて  
いわゆる「Maya のシーングラフ」として読み込まれています。  
これは、「USD を Maya のシーングラフとしてインポート」しただけであって  
USD のシーングラフではありません。  
元の USD がアップデートされたとしても、USD ファイルとは関係性が完全になくなっているため  
変更は反映されません。

つまりは、このように Maya に読み込むような手順を取ると、  
これまでの FBX などと同じ扱いになるため、あまり USD の恩恵を得ることができません。

## mayaUsdProxyShape

Maya で USD を USD として扱う場合は、UsdProxyShape を経由してロードする必要があります。

![](https://gyazo.com/8f02594bbf60b8a669b257e87c2753f5.png)

mayaUsdProxyShape から読む場合は、  
作成＞ UniversalSceneDescription（USD）＞ Stage From File... を選びます。

![](https://gyazo.com/2845a1625e5a506f479cf06726e98760.png)

この方法で読み込むと、このように USD アイコンぽいノードが作成されます。

![](https://gyazo.com/f98e593580f77c6bf65feef72d1a22e5.png)

この方法で USD をロードすると、ルートノードに「mayaUsdProxyShape」ノードと呼ばれる  
特殊なノードが作成されます。  
このノードは、その名の通り USD のステージを Maya で表示するための特殊なノードで  
ある１つの USD レイヤーをオープンした「USD ステージ」を表します。  
この例なら Kitchen_set.usd を開いた USD ステージになっています。

![](https://gyazo.com/56946d6f3c2c1890d3221c8082786fd3.png)

ProxyShape 以下は、<Marker>「Maya のシーングラフ」ではなく「USD のシーングラフ」</Marker>です。  
なので、AttributeEditor を見ても Transform ノードや Mesh ノードは存在せず  
「データモデル＝ UniversalSceneDescription」のようになっています。

![](https://gyazo.com/dd4e0a4e2e96232f13b26f7f1114d5d9.png)

つまり、このアウトライナーで表示されている「ノードのようなもの」は  
USD の用語でいうと、「Prim」が表示されているものであって  
Maya のノードではありません。

この USD のシーングラフと Maya のシーングラフは、アウトライナー上では同じようなものとして  
共存しているように見えますが、 <Marker>それぞれが別の世界</Marker> となっています。  
そのため、Maya の Mesh ノードを、mayaUsdProxyShape 以下に移動しようとしても  
移動することはできません。  
また、その逆もしかりです。

とても大事なことなので、繰り返しになりますが <Marker>「それぞれは全く別の世界」</Marker> です。  
なので、この USD のシーングラフを扱う場合は  
双方をどのように行き来するのか、今どちらを操作しているのかを理解しないと  
全く分からないという状態に陥ってしまいます。

ので、まずは「別世界である」という前提に、何を編集して保存しているのかを１から確認していきます。

## mb と USD

ここまでで、Maya の世界と USD の世界がそれぞれ存在していることがわかりましたが  
では、具体的にそれぞれが何を編集しているかを確認していきます。

Maya のシーングラフは、当然のことながら Maya のデータであり  
データを保存するのも Maya バイナリー、またはアスキーです。  
開くときも、このシーンファイル（MB/MA）をファイルオープンで  
Maya シーンとして開きます。

では、上記で説明した mayaUsdProxyShape はどうでしょうか。

![](https://gyazo.com/8ee41fc92b7033433d1ad85821cca9e8.png)

この ProxyShape 内の世界は Maya の世界ではありません。  
なので、編集を加えた場合は「Maya の世界の情報」としては記録されません。

![](https://gyazo.com/eb0991f0fe362b32d8f13ca7f6ce7975.png)

Maya としての情報は mayaUsdProxyShape を作成し、  
「ロード対象の USD ファイル」の情報のみです。

この ProxyShape 以下のノードは「USD の世界を編集している」わけですから  
保存先も「USD」であってほしいわけです。

![](https://gyazo.com/063bdab0e81b81f96bd1f0a08a7bf738.png)

![](https://gyazo.com/0e98741ea73461e0e022801f5c96306c.png)

そのため、ProxyShape 以下を編集した場合は、Maya シーンを保存しようとすると  
上記のようなダイアログが表示されます。  
これは、Maya シーンではなく USD の世界が編集されているので  
Maya シーンだけではなく USD 側も保存するかを確認するダイアログです。

この、編集対象が USD である　というのが、USD を扱う場合は重要なポイントになります。

どのようなときに意味を持つかというと、それはツールをまたいで作業する場合や、違う人と共同作業をする場合です。

![](https://gyazo.com/cb3c3f24938972f88f26ffc0bf0e8099.png)

試しに、Maya で開いている USD を、Houdini 側で開きます。  
開く場合は「SubLayer」ノードを使用します。

![](https://gyazo.com/24981116dd9593ed5f3b9cff0a8aed98.png)

ConfigureLayer で新しいレイヤーを作成し、

![](https://gyazo.com/676d94b4b3fae752dd4dc73f9fedb2c8.png)

別レイヤー化します。

![](https://gyazo.com/34aaf7785e95144bd81f62f252392365.png)

この状態で、Maya 側で編集して　シーンを保存しつつ USD も更新します。

![](https://gyazo.com/abd27536c1f688c8658a69504fe47f05.jpg)

Houdini 側でリロードすると、  
Maya で編集した結果が反映さているのがわかります。

これは、繰り返しになりますが mayaProxyShape 内の世界が「USD」で  
保存先が「USD」になっているからこのような結果になります。

## まとめ

ここまでで Maya での USD の扱われ方、Maya と USD の世界についての基本部分を書いていきました。  
今までのフローだと、Maya シーンを「Export Selection...」などして  
別のフォーマットに出力する、という手順でしたが  
USD はそうではないというのがわかってきたのではないかと思います。

ので、次回は「レイヤー」という概念を説明しつつ  
Maya での USD 編集と <Marker>どの USD ファイルを編集しているのか</Marker>をベースにいろいろ USD を編集していきたいと思います。
