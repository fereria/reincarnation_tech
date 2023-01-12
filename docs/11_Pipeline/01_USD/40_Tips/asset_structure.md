---
title: USDのアセット構造の話
tags:
    - USD
    - AdventCalendar2022
description: USDのアセット構造を、今までの記事や記事を参考に紹介します
---

[USD AdventCalendar2022](https://qiita.com/advent-calendar/2022/usd) 25 日目は「アセット構造について」です。

USD は、以前に比べるとだいぶ普及して知らないうちに実は使っていた
なんてことも出てきているのではないかと思います。

しかし、何かしらのプロジェクトで実際に使おうとするとそう簡単ではなく
パイプラインの設計などもきちんとやらないといけません。
そうなると、どのように使ったらよいかわからないことが多いのではないでしょうか。

今回は、 [ASWF USD WG](https://wiki.aswf.io/display/WGUSD) の [usd-wg/assets](https://github.com/usd-wg/assets) リポジトリで公開されている Guidelines for Structuring USD Assets をベースにしつつ
過去に書いた記事や、公開されているサンプルなどをもとに解説していきたいと思います。

USD のアセットの構成を考える上で、いくつか考慮しなければいけないことがあります。
ざっくり分けると、以下の 5 つになります。

1. コンポーネントとスコープ
2. アセンブリ
3. ディレクトリ構造
4. USDA or USDC
5. コンポジション構成

それぞれ詳しく見ていきます。

## コンポーネントとスコープ

USD のアセットは、それ単体で使うというよりもアセットをリファレンスやペイロードし
レイアウトして使用することになると思います。
そのため、作成するアセットはリファレンスして使うのを前提にして構築する必要があります。

### defaultPrim

USD のアセットをリファレンス、またはペイロードする場合は USD レイヤーではなく
レイヤー内のある 1 つの Prim を、指定の Prim に対して接ぎ木します。

![](https://gyazo.com/61e61a31ffd12359df5f1262e7a624c9.png)

そのため、たとえばこのようにルート以下に Prim が並んでいるようなデータをリファレンスしようとすると

![](https://gyazo.com/b285073e6ed1fc04619075f57f0ee77a.png)

Warning 扱いになり、

![](https://gyazo.com/f477d0a92d9819070b6c3bffa7bfc702.png)

正しくリファレンスすることができません。

このため、USD でアセットを作る場合は、RootPrim を作成し
これを defaultPrim(リファレンスするときに対象となる Prim)を指定します。

![](https://gyazo.com/8d1e7432e3c78f282f0aeebccbf912aa.png)

このようになります。

この defaultPrim は、リファレンスしてきた先の Prim に「接ぎ木」されるものです。
そのため、レイアウトシーンでアセット情報を付加する場合などは
レイアウトシーンではなくアセット側でつけておく必要がありますが
付加する先はこの defaultPrim である必要があります。

![](https://gyazo.com/7bfe78af8a5f7c2c2b56b09df576b8e2.png)

Kitchen_set の Kitchen.usd を見ると、defaultPrim に対して assetInfo kind documenation が付いています。

![](https://gyazo.com/6ad13a4591a37b8bba626bf2139b9242.png)

Kitchen_set.usd をみてみると、ペイロードで読んでいる Prim に assetInfo kind documentation が指定されています。
{{markdown_link('assetinfo')}} や {{markdown_link('payload_asset_dependencies')}} 等、
アセット情報を defaultPrim に追加しているのは
リファレンス・ペイロードをすることを前提に、シーンの構造を構成しているからになります。

### スコープ

defaultPrim も重要ですが、もう 1 つシーングラフの構造を決めるうえで重要なのがスコープです。
USD は、シーンの階層構造は自由に構成できますが
自由にしすぎるとわかりにくいデータが出来上がってしまいます。
例えば、Mesh 階層下に Material があったり、Material 下に mesh があったりのようになっていると
「シーンに存在するマテリアルを検索したい」みたいなことをしたい場合に
（できるけど）面倒だったり、余計な処理がふえることになります。

ので、そうならないように defaultPrim 以下には「スコープ」と呼ばれる階層を作り
ある程度ルール化しておきます。

![](https://gyazo.com/3a3f63ca865a7629a3edde52c3dec7a4.png)

このスコープは、DCC ツールによって若干の差異はありますがおおむねこのような構造になります。
（Materials が Looks だったり materials だったり \_materials だったりする）

Geom は Mesh データ、Materials は Material と Shader。
そして Render は

![](https://gyazo.com/3600a6f1c4a51db051d9f90f1151c688.png)

RenderSettings 等が配置されます（これは Karma の例）

### Purpose

Geom 以下には proxy や render と呼ばれる構造が配置されます。

USD の Purpose と呼ばれる仕組みがあるのですが、これは OpenGL のビューポートで表示するときには
軽量な Proxy モデルを表示する機能です。

![](https://gyazo.com/8c361388f1f5693318f48e931f765678.png)

この機能で、アセットのモデルを切り替える場合の proxy 用（軽量なモデル）と render 用のモデルを Geom 以下に作成し、

![](https://gyazo.com/7109a90fa3d13dc8bbf403a12cedf0e1.png)
Purpose を指定することで

![](https://gyazo.com/e882d7afc83da58980b90fb144716c31.gif)

前半は Karma でプレビュー、このモデルを OpenGL に切り替えた時は Proxy を表示しています。
これをできるように、Geom 以下には render と proxy のスコープを作成しておきます。

Houdini での作り方などは {{markdown_link('16_component_builder')}} こちら参照。

## Assembly

Assembly とは、個別に作成されたアセットを 1 つにまとめたアセットのことを指します。
たとえば、Kitchen_set アセットは、建物や冷蔵庫、椅子・机などのアセットを 1 つのシーンにレイアウトし
作られていますが、これが Assembly です。

複数の、多ければ数千・数万のアセットをレイアウトした場合、
ある程度ルールを設けなければ意図しない挙動が発生したりする可能性があります。
リファレンスしたアセットの Prim に対して、さらにリファレンスを追加する場合。
構造が変わったら破綻してしまったりする可能性もあります。

そうならないように、ある程度のルールは必要です。
このルールが {{markdown_link('kind_modelhierarchy')}} で説明している kind による component 指定です。

### component とは

component とは、USD のアセットのうちもっとも基本的なアセットのことを指しています。
レイアウト用のアセット、と言い換えてもいいかもしれません。

![](https://gyazo.com/8a90e846a4eac7dffc22a593af5a0430.png)

レイアウトアセットの移動用の XformPrim が component 扱いになります。
そして component 以下は、上で説明したスコープによって各アセットの構造が構成されています。

Assembly するときの各アセットは、リファレンスでロードしたロード先 Prim を component
そしてその component をまとめるのを group
そしてルートプリム（defaultPrim ) が assembly という階層構造を持ちます。
階層は、 assembly > group > component と、component が末端にあたります。
component 以下には component 入れられません。
このようなルールで構成することで、複雑さを防ぐのが基本的な Assembly の構造になります。
これを Model Hierarchy といいます。

Reference するアセットのルートが Component 扱いになるので、
アセットの defaultPrim には kind = component を指定しておきます。

## コンポジション（レイヤー）構成

最終的にどのような階層が出来上がっていればよいかが決まったら、それを適切な単位にレイヤーを分離します。
USD は {{markdown_link('comp_arc')}} にあるとおり、複数のレイヤーを合成して 1 つのシーングラフを構築できます。
アセットは 1 つのレイヤーにまとめても良いですが、決められた構造をセットアップすることで
USD の機能を生かしたアセットにすることができます。

-   {{markdown_link('16_component_builder')}}
-   {{markdown_link('07_create_usd_assets')}}

作成方法は、Houdini の ComponentEditor を使用したパターンと Python を使用したパターンの２つを
以前書いたのでそちらを参照してもらえればよいですが
ここでは、いくつかの重要な要素についてまとめておこうと思います。

![](https://gyazo.com/65e94f6d633d4a6b20532da00045812f.png)

基本となる構成がこのようになります。
AssetName.usd がアセットとして実際に Reference する階層になります。
このレイヤーは、Mesh 等のアセットを構成する実データを持たず
各種メタデータを指定するためのレイヤーになります。

```
#usd 1.0
(
    defaultPrim = "AssetName"
    metersPerUnit = 1
    timeCodesPerSecond = 30
    upAxis = "Y"
)

def Xform "AssetName" (
    prepend payload = @./payload.usd@
    assetInfo = {
        asset identifier = @./AssetInfo.usd@
        string name = "AssetName"
        string version = "1.0"
    }
    kind = "component"
)
{
}
```

スケールや upAxis、defaultPrim に対しては assetInfo や kind の設定など
アセットに必要なメタデータをこのレイヤーに記述し、
頂点データなどの大きなデータは別のファイルに分離し、ペイロードにしておきます。

アセットの段階でこのようにメタデータと本体とを分けておくことで
アンロード状態にしておいても、最低限必要な情報を取得できるようにします。

![](https://gyazo.com/37b4768b88374a83b72ef8ff9c3400cc.png)

VariantSet を含む場合は、payload がこのようになります。
そして、variant の個別の usd は上の図の payload.usd と同じ構造になります。

![](https://gyazo.com/f2351783c6bd3300cc36c7968d83c7f5.png)

geo.usd の中身が、Mesh データです。

### Moana Island Scene をみてみる

ここまでが、Houdini の ComponentBuilder や Kitchen_set の例を参考にした場合の構造例ですが
それ以外に Disney Animation Studio が出しているサンプルデータ [Moana Island Scene](https://www.disneyanimation.com/resources/moana-island-scene/) の構造も、例としてみてみます。

![](https://gyazo.com/fd0890f489cc6a8fae3b76171e57006e.png)

アセット部分を切り出すと、構造はこのようになっています。
基本的にファイル名は異なりますが、レイアウト用の元になるコンポーネントが element.usda
その次にペイロードの仕組みを入れるレイヤーが存在し、マテリアルとジオメトリが別レイヤー
（マテリアルのほうが強い状態で、同階層にリファレンス）

少し違うのが、geometry 部分がさらに model と分かれています。
geometry には、model(UsdGeomMesh)をペイロードで読み込む部分と
vdb を OpenVDBAsset スキーマを使用してロードしている部分が書かれています。

### USDA or USDC

IslandScene で注目したいところが、アセットのデータは **わざわざ usda と usdc を使い分けているところ**にあります。

USD には、usda (アスキー)と usdc (バイナリー)の 2 種類が存在しています。
それぞれの特徴は、 [USD は手書きするもの](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09) こちらの記事に書かれているので詳しくはこちらを見ていただきたいですが、
ざっくりいうと、テキストエディタで編集可能なデータが usda で、ファイルが小さく読み書きが早いのが usdc になります。

その特徴を生かした上で、コンポジションを構築していきたいわけです。

IslandScene では、多くの部分が usda によって構成されています。
（usdc を使用しているのは、 model.usd ＋ vdb）

頂点データやカーブのデータ、キャッシュデータなどのような巨大なデータは極力バイナリーで扱いたいです。
それこそ、1 フレーム単位で分離しつつバイナリーで扱うくらいでしょう。
ですが、それに対してのメタデータや ValueClip ( {{markdown_link('value_clip_01')}} )を使用するレイヤー
マテリアルデータ、レンダーセッティング等はシーンの頂点データなどをわざわざ読まずに
編集して書き換えたりしたいはずです。

このようなことをするためにも、USD のアセットは 1 ファイルにデータを固めるのではなく
役割ごとにファイルを分離し、容易に編集可能な形で設計しておきます。

拡張子は、 usda usdc usd とありますが
アスキーであってもバイナリーであっても usd にしておけばいい感じに取り計らってくれるので
あとでバイナリーとアスキーを切り替えたくなっても楽なように、すべてを usd としておくのが良いです。

### それ以外のデータの話

今回はモデル前提でしたが、エフェクトのデータだったりライティングデータが増えた場合も
fx.usd や light.usd といった形で分離して、ペイロードでロードします。

![](https://gyazo.com/5120e956aaec93250477e29824651599.png)

こんな感じ。
この例だと「赤」くしている usd は usdc がよさそうです。
Light や FX に対してアスキーでメタデータを付加したい場合は、 payload.usd と各要素の USD の間に
サブレイヤーを追加するなどの工夫をすると
さらに柔軟に構成できるかもしれません。

## ディレクトリ階層

シーンの構造を定義し、レイヤーの構成を設計できたら
最後にディレクトリ階層を用意します。

作成したアセットをどのように管理するかはケースバイケースですが、多くの場合
アセットをパブリッシュするタイミングでバージョン管理をしたいですし
場合によっては特定のショットだけバージョンを固定したりする必要がでてきます。
そうなると、Git や SVN、Perforce といったものではなくディレクトリによって管理したりしたくなります。

USD のアセットは、コンポジションで使用する場合 assetPath と呼ばれるアトリビュートで定義されます。
この assetPath は、AssetResolver と呼ばれれる仕組みを使用して
USD のプラグイン内でパス解決を行うことができます。

{{markdown_link('asset_resolution')}}

詳細はこのあたりの記事にまとめられていますので、こちらを参照してください。

この AssetResolver を使用してバージョン管理をするのを考慮すると
Asset のディレクトリは以下のようになります。

![](https://gyazo.com/c701186ec632f03656231a8c56217c7e.png)

assets 下にアセット名、そしてその下にバージョンごとのフォルダ、そしてそのバージョンフォルダ以下に
必要なリソースを保存します。

asset://projName/assets/assetName/assetName.usd

個のアセットにアクセスする場合は、何も指定しない場合は最新の AssetName.usd をロードし

asset://projName/assets/assetName/assetName.usd?version=2

URI でバージョンを指定させたり、USD のメタデータや外部の json、あるいは DB の情報として
固定のバージョンを用意して、その情報をもとにパス解決をするなどします。

重要なのは、通常の Windows のフルパスで直接解決するのではなく
解決部分を USD のプラグインとして持たせられるので、
実際のファイルがどこにあるかをレイヤーに直接書かなくて良くなります。

それがどういった効果になるかというと、
ある程度パイプラインを自動化前提で構成しようとすると
そのディレクトリ階層は人間がアクセスするには不便な形になりがちです。
（階層が深くなったり等）
Resolver をいれることによってそのあたりを解決するのをプラグイン側に任せて
扱う人はわかりやすいパスで扱うことが可能になります。

さらに、ディレクトリが足りなくなったり部分的に高速なストレージに移動したいとなっても
通常だとファイルに書き込まれたパスを個別に直さなければいけないですが、
そういったことも不要になります。

プラグインの実装は必須になりますが、
USD でアセットを構築する場合は、Resolver を考慮したうえで設計したほうが
いろいろと取り回しがよくなります。

## まとめ

これまで断片的な USD の機能として説明記事を書いてきましたが
今回はその集大成として、実際の USD アセットの構築にかかわる部分をまとめていきました。

パイプラインの設計をする場合、これらの機能に加えて実際にプロジェクトに応じた
調整や、ショット管理側の設計、キャッシュの取り扱い含めて考えなければいけないことは多いです。
ですが、この記事がそれらの USD パイプラインを設計をするときの 1 つの参考になれば良いなと思います。

また、今回の記事をまとめるうえで、 [AssetStructureGuidlines](https://github.com/usd-wg/assets/blob/main/docs/asset-structure-guidelines.md) の内容をかなり参考にしましたが、
今回私が書いた内容以外にも重要な内容や考慮すべき点など
USD を扱ううえで非常に参考になる内容が書かれていますので、合わせて見ていただければなと思います。

## 参考

-   https://github.com/usd-wg/assets/blob/main/docs/asset-structure-guidelines.md
-   https://www.disneyanimation.com/resources/moana-island-scene/

### 関連記事

-   {{markdown_link('comp_arc')}}
-   {{markdown_link('kind_modelhierarchy')}}
-   {{markdown_link('asset_resolution')}}
-   {{markdown_link('07_create_usd_assets')}}
-   {{markdown_link('16_component_builder')}}
-   {{markdown_link('assetinfo')}}
-   {{markdown_link('payload_asset_dependencies')}}
-   {{markdown_link('kitchen_set')}}
