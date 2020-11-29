---
title: USDとは
---

# USD とは

## はじめに

今年(2019 年)の SIGGRAPH に参加して、あらゆるパイプライン系セッションで USD という名前を聞きました。  
日本ではまだあまり導入はされていない USD ですが  
海外ではある意味スタンダードなものになりつつあります。  
また、今年発表された Houdini18 からは USD がネイティブサポートされ、  
Blender 等でも USD 関係の記事がでてきたり、  
Maya の Plugin も出てきたり（ビルドがめんどくさいけど）で、導入までの難易度が下がり、  
日本でも徐々に感心が上がってきているのではないかと思います。

ですが、あまり日本語の記事としては USD 関係の資料はあまりなく  
そもそも USD とはなにで、  
導入することでなにが出来るのか、  
あまりわかりにくいのが実情な気がしています。

かくいう私も、SIGGRAPH ですごい名前は出てくるけれども  
具体的にどういったものなのか、よく分からなかったので  
色々と調べたり、聞いたりして理解したことなどをまとめて行ければとおもいます。

なお、この説明の多くは
元開発者の一人でもある手島さんが公開している

- [CEDEC2017 Pixar USD 入門](https://www.slideshare.net/takahitotejima/usd-79288174)
- [USD(ユニバーサルシーンディスクリプション)](https://qiita.com/takahito-tejima/items/3c2fa4a4a83aa04b9a0e)
  でも詳しく書かれていますので  
  併せてみて頂けると良いかなと思います。

## USD とは

![](https://gyazo.com/37673716a79f059efdc3d16be734b9a2.png)

USD とは、Universal Scene Description の略で、  
Pixar 社が GitHub 上で公開しているオープンソースプロジェクトのライブラリになります。

では、どのようなライブラリなのかというと  
**シーングラフ（描画要素を管理するためのデータ構造）を扱うことのできるライブラリ**  
になります。  
シーングラフとは、Maya 使い的に言えばアウトライナやハイパーグラフに表示されているノードツリー  
の構造で、つまりは「シーンのデータ構造を扱うことができる」ものになります。

現在同じようなライブラリ・ファイルフォーマットとしては FBX、DAE（COLLADA)、OBJ  
キャッシュデータとしては Alembic  
Web 関係では glTF、あるいは等がほぼ同じようなライブラリとしてあげられます。

では、それらのフォーマットと USD はなにが違うのか（なにが凄いのか）  
導入することでなにが出来るのかを説明していきたいと思います。

## 現行の問題点

現在、いろいろな DCC ツールを行き来する場合は  
多くの場合 FBX を使用してソフトウェアを行き来することが多いかと思います。

しかし FBX の場合、

![](https://gyazo.com/48dd92c60827906844ad1aa48d257fb0.png)

- FBX 内にモデルデータも含まれてるためモデルが変更になった場合いろいろ大変  
  （FBX には外部参照、いわゆるリファレンスが存在しない）
- 持って行けないアトリビュート情報が出てきてしまう
- Autodesk に結局依存

等の問題が発生することがあります。

ソフトをまたがず Maya だけで完結した場合でも、
モデリングをして、リギングまでしたモデルや BG をアセットデータとして保存し、  
それをリファレンスで読み込み、アニメーションを行い、  
モデルが更新されたらリファレンス先を更新することでモデリングとアニメーションを  
同時並行して行うフローなどがあります。  
が、リファレンスで読んだ場合に

- データが破損したり、破損したり、破損したり
- 多重リファレンスしたらデータがおかしくなったり
- そもそも重かったり、リファレンスしたデータは追加編集ができなかったり

かなり制限が多いワークフローになってしまいます。  
（そもそも Maya に完全に依存してしまう）

最近だと、Maya や Houdini の行き来だったりで DCC ツールをまたいでのフローが増えてきており  
FBX を使用したフローは限界があります。  
~~というか Maya 触りたくないし、FBX も...~~

## というわけで....

映像制作における  
**複数ソフトウェアをまたぐ、かつ大人数同時並行を行うために作成されたフォーマット**  
として作られたのが、この USD になります。

大規模な開発のときに問題になるのが、多人数での編集時のデータのアップデートです。  
上に書いたように、Maya 単体の場合はこの問題を  
モデルはリファレンスで読み込みすることで、あとでモデルのアップデートをできるような  
使い方をすることが多いです。

しかし、複数のソフトウェアをまたいでしまうとリファレンスは使えません。  
現在一般的に使われている FBX でも出来ません。

しかし、USD は Maya のリファレンスとは比較にならない強力な合成機能が備わっています。  
それが、 **「コンポジションアーク」** と呼ばれる 複数の usd ファイルの合成になります。

このあたりの合成については、あとでソレ単体で詳しく説明します(詳しく説明すると長くなる)ので、  
今回は概要のみざっくりと説明します。

![](https://gyazo.com/3bb5bf1d5c2e56f3ed09cde278832504.png)

こちらが、USD を使用した場合のシーン構成の一例になります。

3DCG のワークフローは、すごーくざっくり分けると

モデリングをして  
セットアップして  
レイアウトして  
アニメーションをして  
ライティングして  
レンダリングする

という形で、ある程度担当（者）が分かれます。  
最近だと、上に書いたパート内でも担当者がさらに細分化していることもあります。

その場合、あるファイルを編集したら下流の工程は再度ファイルのアップデートが必要になります。

しかし、USD を使用する場合、各工程ごとに別ファイルとしてデータを保存して  
それを合成することができます。

ので、「モデリング」工程でのモデル USD ができて、
その「モデリング」データに対して「セットアップ」した「セットアップ情報」の USD（モデルはモデル USD を参照）
その「セットアップした USD」をレイアウトしたレイアウト情報の USD ができて  
キャラクターのアニメーションをつけて、アニメーション情報だけの USD ができて...  
そんなかんじで

モデルの USD  
セットアップ情報の USD  
レイアウト情報の USD  
アニメーションデータの USD  
レンダーセッティングの USD  
ライティングの USD

という細かいデータに分かれた物を、最終的なレンダリングに使用する USD に合成して  
レンダリングすることで、  
各工程のデータが更新されても、非破壊で編集・アップデートが出来るようになります。  
重要なのは、この「合成できること」と「非破壊である」という 2 点で  
複数人で作業をしていても、  
前後の作業関係なくアップデートしても（ルールに沿ってさえいれば）  
入れ替え作業だったり、同時作業の衝突だったりを気にしないで  
作業を行うことが出来ます。

最近、何人かに USD の話をしたときに

**モデルを出力するためのフォーマットだと思っていた**  
**アニメーション作業には関係ないと思っていた**

と言われたことがありましたが、そういうわけではなく  
USD は、  
モデリングから、最後のレンダリングに至るまでのパイプラインの基盤になるもので  
すべてのパイプラインを、自分たちが設計したフローで行うための  
基幹になるものであるといえます。

## USD でできること・できないこと

そんな感じで、全力で USD を押してきましたが  
メリットデメリットも軽く触れておきます。

### できること・メリット

#### DCC ツールをまたいでのファイルフォーマットとして

まずは、3DCG の各種モデルやアニメーションのファイルフォーマットとして使用できます。  
おそらくこれが一番イメージされている使われ方ではないでしょうか。  
FBX や GLTF のような汎用フォーマットとして、DCC ツールのフォーマットに縛られず  
3DCG のデータを扱うことが出来ます。  
また、モデル以外にもキャッシュデータ（Alembic など）も扱うことが出来ます。

#### JSON や XML、YAML、TOML のようなフォーマットの代替

FBX のようなファイルフォーマットと思われがちの USD ですが、  
あくまでのファイルフォーマットなので  
DCC ツールなどにかかわらず、汎用ファイルフォーマットとして使用することができます。

#### 拡張できる

今後説明する「スキーマ」を自分で定義することで、  
自社のパイプライン用に自由に拡張することができます。

#### Autodesk に縛られない

FBX とは違い、Autodesk にに縛られずに扱うことが出来ます（重要）

### できないこと・デメリット

#### リグが持てない

当初、USD の説明を色々聞いていたときに一番？？？だった出来ないことが  
「リグが持てない」  
ということでした。

自分のイメージだと、「リグ」とは、スキニングされたモデルのジョイントに対して  
コントローラーをつけて、コンストレインやらを使ってジョイント（あるいはデフォーマ）を  
動かすための機能のことを指していると思っていましたが  
こと USD に関しては意味合いが異なります。

そもそも Pixar のモデルはジョイントでアニメーションしているわけではなく（この時点で衝撃だった）  
ものすごい大量のデフォーマによって、頂点制御でアニメーションを行っているような物...  
らしいです。

なので、この場合のリグとは、
デフォーマなどの実行「ロジック(プログラムで書かれた処理）」部分のことであり、  
**「なんらかの計算をして結果を出す」**  
の事を指しています。

あくまでも、USD 自体はファイルフォーマットなので  
何かしらのロジック（処理）が記載されているわけではありません。  
なので、デフォーマなどの処理を作成する場合は、  
スキーマを定義して、そのスキーマを解釈するためのロジックを  
DCC ツール側のプラグインとして実装する必要があります。（多分）

#### 決まった使い方があるわけではない

これはメリットの裏返しではりますが、  
USD 自体は  
「あらゆるパイプラインにフィットさせる事が出来る柔軟さをもったフォーマット」  
なので、ただ普通に FBX の代わりとして使用した場合は  
その恩恵を受けることはあまりできません。

どのようなパイプラインを敷いて、どのようなシーン構成をするのかは  
使用者がきちんと設計をする必要があります。

## そんなかんじで...

文字多め、説明多めで微妙に分かりくい説明になったかもしれませんが  
とにかく USD は、すごいファイルフォーマットで  
それをつかうと色々できるよ！！！  
という事が言いたかったです。

はい。

概要はこのくらいにして、次回からスクリプトベースにしつつ  
コンポジションの説明やら、データ構造の説明を

詳しく書いて行こうと思います。

先は長い！！！