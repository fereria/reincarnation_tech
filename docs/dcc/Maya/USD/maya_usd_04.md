---
slug: /maya/maya_usd/04
title: MayaのUSDReferenceを理解する
description: Mayaでアニメーション作業をする手順
sidebar_position: 4
---

今回は、Maya でアニメーション作業をしながら USD を扱う場合の手順について解説していきます。

## 全体の構造

まず、USD の重要なポイントとして「USD はリグを持てない」というものがあります。  
この「リグ」というのが何を指すかというと、内部で何かしらの計算をするようなもの全般を指していて  
唯一スケルトンとウェイトなどは入っていますが、それ以外は基本的には入っていません。  
なので、USD を使用してキャラクターアニメーションを扱う場合は  
スケルトンにアニメーションをベイクするか、ジオメトリキャッシュを作成するかの 2 択になります。

ですが、USD を使う以上は非破壊かつプロシージャルな構築がしたいよね？ということで  
Maya では Reference を使用した Maya と USD のワークフローが用意されています。

ので、順番に試していきます。

### Reference する

まず、何かしらセットアップ済のモデルが必要なので、

https://mox-motion.com/freerig/

今回は、MoxMotion 様のモモちゃん RIG で試してみます。（多分ほかのモデルであっても同様にできると思います）

![](https://gyazo.com/402e073fbdce0e83f3b6e671adc3f88c.png)

まず、作成＞ UniversalSceneDescription で、UsdProxyShape を作成します。

![](https://gyazo.com/d5ff7e1a92585c36f7a1f30c24e592de.png)

作成したら、AnonymousLayer だとまずいのでまずレイヤーを保存します。

![](https://gyazo.com/dbf5c4003e24475a3660be65de1eae36.png)

保存したら、ProxyShape に対して「Add New Prim」で XformPrim を作り  
名前を「Root」とします。

![](https://gyazo.com/4d19558b5b5503a1fb75cdcdb054a50c.png)

作成するとこのようになります。

![](https://gyazo.com/9c59f02a33e0dba0d14c986ff37b4bff.png)

そして、この RootPrim を選択したうえで「Add Maya Reference...」を選びます。  
ProxyShape に直接だと NG ですので、かならず Prim を作りましょう。

Add Maya Reference...でモモちゃん RIG の Maya シーンを選択します。

![](https://gyazo.com/b4c8af8978ab29db9206c0d21428f23d.png)

このように、キャラクターを読み込むことができました。

![](https://gyazo.com/e0a7a0ffe2f8b5c1eacefb727426b090.png)

アウトライナーを確認すると、このようになっています。  
なんかムズムズする感じは置いておいて、最初に作った「Prim」以下に  
リグ付きのアニメーション用モデルが Maya リファレンスされているのがわかります。

※以降、紛らわしいので Maya 側のリファレンスは「Maya リファレンス」、  
USD のコンポジションのリファレンスなら「リファレンス」と呼称します※

![](https://gyazo.com/0957974e2fa73ea70c646f053456611a.png)

HyperGraph 上ではこのようになっています。  
**mayaUsd**ノードという特殊なノード以下に、リファレンスが読み込まれています。

これでアニメーション作業の準備ができました。

## アニメーションする

現在の状態は、しいて言うならば「Maya モード」と呼ばれる状況下にあります。  
Maya モードなので、Maya の機能でリギングされたキャラクターは  
Maya で扱うのとまったく同じ状態になっていて  
これまでの Maya と同じ感覚でアニメーションをつけることができます。

![](https://gyazo.com/bdff708c391855e91590975ddb78000b.png)

凄く適当で申し訳ないですが、こんな感じでポーズを変更してみました。  
ここまでだと特に変化はありません。

## USD モード

ここで、新しい要素が「USD モード（私が勝手に命名）」への切り替えです。  
アニメーション作業までの段階では、  
ProxyShape 以下にノードはあるものの、基本的には Maya のシーングラフです。

USD の世界のデータではないので、他のツール（Houdini 等）には持って行くことができません。

なので、このアニメーション用のシーンに対して USD の世界を作成します。

![](https://gyazo.com/dc0079f839823ae51851780b52926e0d.png)

MayaReference の階層を選んで右クリックすると「Cache to USD...」というメニューがあるので  
これを実行します。  
これは、その名の通り　現在のキャラクターの Mesh や Skel を USD の世界にキャッシュ  
してくれます。

実行すると、ファイルを保存する場所を聞かれるので  
アニメーションの保存場所を指定します。  
※ここで指定した場所に、アニメーションデータが出力されることになります※  
今回は、ProxyShape を保存したフォルダに、 anim.usd という名前で保存しました。

![](https://gyazo.com/77e9dad6473330b9c1f3a441ea29a94a.png)

保存するときには、USD キャッシュをどのように作成するか聞かれるので  
アニメーションの場合は Animation タブ以下の Frame Range Start/End で  
キャッシュしたいフレームを指定します。  
デフォルトは 1Frame だけなので、アニメーションが出力されないので  
<Marker>必ず設定してください</Marker>（私は忘れてはまりました）

![](https://gyazo.com/3b05e778e9039235abfa5f39094a3663.png)

キャッシュを作成すると、このように Maya のコントローラーが消えます。

![](https://gyazo.com/abf2aa7077d2ffbc26ca33b9c21bac39.png)

UsdProxyShape を見ると、Maya のリファレンスは消えて USD のシーングラフになっているのがわかります。  
![](https://gyazo.com/75d496a5005dbeeb3d7f746067ecf253.png)
Maya リファレンスは、このように無効化されています。

## Maya モードと USD モード

一度キャッシュを取ったらもう戻れないのか？というとそういうわけではありません。

![](https://gyazo.com/cbd23ae9f02d36318bc80420fb100471.png)

Root ノード（Maya リファレンスを追加した Prim）を右クリックし、  
Variant Set ＞ Representation 　と選んでいくと「Cache」と「MayaReference」が  
選べるようになっています。

ここが、USD モードと Maya モードの切り替え場所で  
Cache だと USD、MayaReference だと Maya モード扱いになります。

MayaReference に切り替えてみます。

![](https://gyazo.com/94466acfe5850bcb8f6e949fe0a99706.png)

切り替えると、Maya モードに戻りました。  
これで、アニメーション作業を再開することができます。

## 他ツールとの連携

上記の USD シーンを Houdini で読んでみます。  
読むのは、UsdProxyShape で読んでいる base.usd です。

![](https://gyazo.com/485b5109efc9b2cdece3baf3d3156fd1.png)

こちらも MayaReference と Cache のバリアントセットがあり  
MayaReference では何もノードがありませんが「Cache」を選択すると

![](https://gyazo.com/3d74e46daff4a5dc1b5571e6ea61e70b.png)

Houdini 側でもキャラクターアニメーションが Skel にベイクされた形で  
出力されます。

## 構造を理解する

最後に、どのような構造になっているか  
USD シーンを確認してみます。

![](https://gyazo.com/05ed1d012a19204ac06375f814f4f347.png)

UsdProxyShape で読み込んでいる USD レイヤー（base.usd）を確認すると  
このようになっています。  
MayaUSD の機能として、MayaReference スキーマに mayaReference アトリビュートがあると  
USD の世界を介して Maya のモデルをロードします。

そして、CacheToUSD で USD にキャッシュした場合は、キャッシュ（今回の anim.usd )  
に対して、モデルのエクスポートとアニメーションのエクスポートを行います。  
これを、VariantSet を Cache に切り替えるたびにキャッシュが行われ  
結果、別ツールで見た場合は「USD のデータとして」アニメーションを  
扱えるようになります。

Maya シーン側のアニメーションデータなどは、
![](https://gyazo.com/f8be01cbf6c864b37bad7ef1decdb482.png)
従来の Maya リファレンスと同様です。

USD キャッシュ化時の動作は、MayaExport で USD を選択した時とおそらく同様の挙動ですが  
今回の手順でリファレンスを作成した場合  
USD 側に Maya のモデルとの依存関係を持つことになるので  
Maya での作業と他ツールでの作業の一貫性を保つことができます。

また、Maya シーン内でライティングやレンダリングをしたい場合  
Cache に切り替えたデータは USD の世界のデータ扱い（Maya ノードではない）  
になるので、シームレスで USD でのオーサリングやライティングなどが可能になります。

個人的にはかなり怖い感じがしますが、  
とはいえアニメーション作業をする環境も他にはないため、USD を使ってアニメーションをする際の選択肢になるのでは？と思います。
