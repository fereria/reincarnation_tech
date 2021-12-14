---
title: AssetResolution(1) - usdResolverExample
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 15日目は、
USDの Asset Resolution (アセットパスの解決)についてです。

## AssetResolutionとは

AssetResolutionとは、その名の通りアセットの実際のリソースまでのパスを
解決するためのプロセスのことを指します。

[Stage/Layout/Spec](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/21_stage_layer_spec/)の記事に書いた通り、USDは１つのファイルではなくて複数の（それは多くの）レイヤーによって
１つのステージが構成されています。
つまり、あるレイヤーの中には別のレイヤーへのパスが記述されているはずです。

![](https://gyazo.com/adc274495504010c793b68eea80f263a.png)

例えば、Kitchen_set.usd を見ると、中でReferenceされているモデルは ./assets/～ といった
現在開いているファイルからの相対パスで記述されていて、
子の相対パスで記述されたアセットのパスを「現在のファイルから見た相対パス」として
探し出し、その結果をロードしています。
あるいは、 **PXR_AR_DEFAULT_SEARCH_PATH** という環境変数が指定されている場合は
WindowsのPATHと同じように、DEFAULT_SEARCH_PATHで指定されたパス以下を検索して
見つかった場合は、そのフォルダ以下にあるファイルを使用するようになっています。

![](https://gyazo.com/6d69fa63bd8dff7b570ac14d3d196cdf.png)

図に表すと、このようになります。

デフォルトの場合はその名の通り「ArDefaultResolver」と呼ばれるアセットのパス解決のための
機能が実装されています。
このArDefaultResolverは、相対パスで記述されたアセットのパスを検索し
実際のリソースまでのフルパスを返します。
これによって、相対パスで記述されていてもフルパスで表示ができるようになっています。

このように、ある入力のパス（相対パス）からリソースまでのフルパスを検索して
その結果を返す機構のことを「Asset Resolution」と呼び、
そのためのインターフェースを AssetResolver と呼びます。
デフォルトの ArDefaultResolverも ArAssetResolverから継承され
実装されたプラグインです。

このパスを解決するためのプロセスは、独自にカスタマイズすることが可能です。

## 具体的な使い方を見る

といっても、これだけでは使用イメージがつかみにくいと思いますので
今回は、USDリポジトリ以下にあるサンプルプラグイン usdResolverExampleをみながら
どのようなものか、そしてどう使うのかを説明していこうとおもいます。

### ビルドする

まずはUSDをビルドします。

```
git clone https://github.com/PixarAnimationStudios/USD.git
```

どこか適当なフォルダにクローンしておきます。
そして、

![](https://gyazo.com/5aa98a788f70b6364b384a9e252c1d72.png)

環境変数のPATHに、PythonのPathを通しておきます。
[Pythonのバージョンは、3.7.9](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09#%E7%92%B0%E5%A2%83%E3%81%AE%E6%BA%96%E5%82%99)あたりを入れておきます。
なお私は、3.7.7 ですが多分それでも大丈夫でしょう。

![](https://gyazo.com/fe39fb957b103f73bf6ba96d601e53aa.png)

VisualStudio2017を事前にインストールしておいて、開発者コマンドプロンプト for VS 2017 をクリックします。

```
pip install PyOpenGL PySide2
```

忘れずに pip でPyOpenGLとPySide2を入れておきましょう。

```
python build_scripts/build_usd.py <インストールするフォルダ>
```

あとは、これを実行して３０分ほど待ちます。
Pythonは、環境変数で指定されているPATHのPythonでビルドされるので
今回なら 3.7.7 で使用できるUSDができあがります。

![](https://gyazo.com/84b5d587edf9cc07bf312956e8a1b464.png)

はじまって

![](https://gyazo.com/06c06cf00fefccb657ecc935ff5f922a.png)

無事終わると、このような表示になります。

ビルドが完了したら、インストール先のパスを環境変数に指定します。
しかし困ったことに、この環境変数を指定してしまうとHoudiniがいろいろおかしなことになってしまうので

```
set PATH=C:\USD\lib;C:\USD\bin;%PATH%
SET PYTHONPATH=C:\USD\lib\python;%PYTHONPATH%
cmd /k
```
私はこのようなBatを用意してそこから起動するようにしています。
(あるいはVSCodeの環境変数で指定)

## サンプルプラグインをコピーする

ビルドができたら、usdResolverExampleをpluginにコピーします。
ビルドで指定したフォルダ（サンプルの場合C:/USD）以下 share/usd/examples/plugin
にある

![](https://gyazo.com/782f7f65ac64a3007910a620fda88769.png)

この３つのファイルを、 plugin/usd 以下にコピーします。

コピーができたら準備完了です。

## サンプルを開く

サンプルのResolverが使えるようになったので、
Resolverのサンプルusdファイルを見ながらどのようなものかを見ていきましょう。

extras/usd/examples/usdResolverExample/testenv/testUsdResolverExample

サンプルは、以下のフォルダにあるので
このフォルダをどこかわかりやすいところにコピーします。
自分の場合は Dドライブ直下に置いておきます。

まずは何も考えず、サンプルの
shot_1/shot_1.usda
を開いて見ます。

![](https://gyazo.com/c4d872b57cf2cbe8aec3d9e573f330c1.png)

すると、盛大にエラーが出ていて表示できません。

shot_1.usda をエディタで開いてみると

```
references = @asset:Buzz/Buzz.usd@
```
リファレンスで読み込むファイルが asset: から始まるパスになっていて、相対パスではありません。
この「asset」は、URI(Uniform Resource Identifiers) と呼ばれる
通常の相対パスなどではなく特定の処理をするための「識別子」になっています。

### asset: と uriSchemes

この識別子は、pluginfo.json によって指定されています。

```json
{
    "Plugins": [
        {
            "Info": {
                "Types": {
                    "UsdResolverExampleResolver": {
                        "bases": ["ArResolver"],
                        "uriSchemes": ["asset"],
                        "implementsContexts" : true
                    }
                }
            },
            "LibraryPath": "../usdResolverExample.dll",
            "Name": "usdResolverExample",
            "ResourcePath": "resources",
            "Root": "..",
            "Type": "library"
        }
    ]
}
```

usdResolverExample の pluginfo.json を見ると、
Types の uriSchemes に asset が指定されているのがわかります。
これは、
**アセットパスに asset:～～ になってい場合は、UsdResolverExampleResolver プラグインを呼び出すようにしてくれ**
という、AssetResolverプラグインを使用するための設定になっています。



> usdのpluginsは、plugin/usd/pluginfo.json にある内容をロードします。
> そして、 plugin/usd/plugin/pluginfo.json は subdir/resources/pluginfo.json を
> Includeします。
> なので、今回のResolverプラグインの pluginfo.jsonは plugin/usd/usdResolverExample/resources下にあります。
> このあたりの話はまたいずれ。

```
set USD_RESOLVER_EXAMPLE_ASSET_DIR=D:\testUsdResolverExample\assets
```
サンプルのResolverは、アセット置き場を別途指定してあげる必要があるので
上のように USD_RESOLVER_EXAMPLE_ASSET_DIR を指定して
もう一度 shot_1/shot_1.usdaを開いてみます。

![](https://gyazo.com/00a841c3b6bcd43bed7ce9c837bdbfe3.png)

今度は開くことができました。

![](https://gyazo.com/2e95bf543fe44fb5b0ff4e14fa25400f.png)

usdviewでBuzz Primのコンポジションをみると、 assets以下のBuzzがリファレンスされているのがわかります。
usdResolverExampleプラグインは、
asset:Buzz の Buzz部分がAssetNameとして解釈して、USD_RESOLVER_EXAMPLE_ASSET_DIR 以下のAssetNameの AssetName.usd
にアセットパスが解決されました。

### Assetのフォルダ構成

ではこの呼び出されているBuzzアセットフォルダ以下はどのような構成になっているでしょうか。

![](https://gyazo.com/73011b50e7d064f71e363ad8d51f911b.png)

Buzz以下に Buzz.usd があり、
サブフォルダでバージョンごとのフォルダがあるのがわかります。

Buzz以下にある Buzz.usd を usdcat してみると

{{'86a90963fe7a3daa5912d7b06b59389b'|gist}}

Buzz/Buzz.usd は、
Buzz 以下 のバージョンフォルダをペイロードしています。

アセットは、このようにバージョン管理をすることがよくあると思いますが、

asset:Buzz/Buzz.usd

asset:\<AssetName\>  のように解釈するのに加えて、

```
{
    "Buzz" : "1",
    "Woody" : "1"
}
```

shot_1 以下にある versions.json というファイルの中身を参照し、
このファイルに書かれているバージョンのアセットを使用するようになっています。

![](https://gyazo.com/b5c1cf3c26219bf2e28328bb3fd45607.png)

つまりまとめると、アセットのパスが asset:\<AssetName\>/\<AssetName\>.usd のように指定されていた場合、

1. shot以下の versions.json を見て、環境変数 VESION に AssetNameのバージョンを指定
2. USD_RESOLVER_EXAMPLE_ASSET_DIR で指定したアセットフォルダ以下から
3. \<AssetName\> 以下の AssetName.usd をリファレンスして
4. その本体は、\<AssetName\> : version で指定されているバージョン以下のものをペイロードする

ということが、 usdResolverExample で行われています。

試しに、 versions.json を

```
{
    "Buzz" : "latest",
    "Woody" : "1"
}
```

このようにかきかえてみます。

![](https://gyazo.com/75b8060c6081d22490339b31cca7a1bf.png)

すると、AssetInfoは latest ではなく 2 になっています。

![](https://gyazo.com/e6f6b88674f88c5707d33b03ef534a6d.png)

次は バージョンフォルダを増やしてみます。

latestをコピーして2 にします。
latest以下の Buff_sublayer.usd のAssetInfoを書き換えて version:3 にしておきます。

![](https://gyazo.com/c8f4950c1c833752b9833ddd63f92ceb.png)

すると、latest 以下のBuzz.usdが読まれているのがわかります。

```
{
    "Buzz" : "2",
    "Woody" : "1"
}
```

2 にすれば、 latest ではなく 2 のフォルダを参照しに行きます。

## Resolverの効果について

以上の検証から、AssetResolverを使用することで以下のような効果が得られることがわかります。

1. 相対パスではなく、アセット名などを使用して実際のリソースへのパス解決を作れる
2. バージョン管理をUSDのプラグイン側でコントロールできる
3. アセットのバージョンを別ファイルに記述して固定化できる

これらができることによってなにが変わるかというと、
アセットの管理側（ShotGridのようなデータベース）とデータ側（USD）とのプラグインレベルでの連携が可能になり、
OSのファイルシステムのパスに依存しないアセットのパス管理ができるようになります。

* https://github.com/LumaPictures/usd-uri-resolver
* https://github.com/westerndigitalcorporation/usd-s3-resolver

たとえば、SQLやS3を使用したAssetResolverのサンプルなどもすでに存在しています。（Resolver2.0だと動かない）
このサンプルの場合、 sql://～～ のようにアセットパスを指定することで、
アセットのパスをデータベースを使用して解決しています。

usdResolverExample は、versionをjsonで保存していましたが
例えばこの部分を ShotGridと連携させて、ShotGridのバージョン管理と連動させることで
Shotでどのバージョンのモデルを使うかを管理したり
ファイルの置き場所をShotGridあるいはデータベースにて管理したりといったことが
可能になります。

USDに書かれているアセットパスは asset:Name/Name.usd （もちろん変えられる）なので、
よくありがちな、ファイルの置き場所が変わったらリファレンスやテクスチャのパスが切れて
どうにもならなくなる...だったり、
フォルダ階層で管理しようとしてものすごく階層が深くなり、人間にはどうにもならない感じになったり
同じファイルが複数の場所に散らばってカオスになったり。
環境が変わったら（以下略
といった無数の悲劇を回避することができます。

## まとめ

AssetResolution そして、AssetResolverがどんなものでどういうことができるかつかめたでしょうか。

> USD/extras/usd/examples/usdResolverExample

今回見てきた usdResolverExampleのソースコードは上記のフォルダにあるので
実際にどのように実装すればよいかはサンプルを見るとよくわかります。

多数のUSDファイル（レイヤー）によって構成されているUSDだからこそ、
リソースへのパス解決は重要になりますので
パイプラインを設計するときに、アセットのパスをどのように管理するかによって
カスタムのAssetResolverを実装すると、よりUSDを便利に扱えるようになると思います。

次回は、このAssetResolutionを踏まえて
USDツールのうちのひとつ usdresolve と、Pythonでのパス解決について
書く予定です。