---
title: AssetResolution(2) ResolveとContext
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 17日目は、
USDの Asset Resolution (アセットパスの解決) 第二回目。

前回の [AssetResolution(1) - usdResolverExample](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/24_asset_resolution/) に続いて、USDのツールセットの１つ usdresolve についてと Pythonを使用したパス解決方法です。

!!! note
    USDTool 下に記事を書くか迷いましたが、
    割合的に usdresolve要素はわずかなので、前回の続きとして記事は書きます
    

## usdresolve

まず、USDのツールセットには usdresolve というコマンドラインツールが存在します。

https://graphics.pixar.com/usd/release/toolset.html#usdresolve

これは、前回説明したAssetResolverをコマンドラインから実行するためのツールです。
このコマンドラインを使用すると、AssetResolverで行っているAssetResolutionを実行して
USDのAssetPathから最終的なリソースへのパスを得ることができます。

まず、DefaultResolverを使用して、相対パスを絶対パスに変換したい場合。

```bat
usdresolve ./assets/CeilingLight/CeilingLight.usd --anchorPath D:\Kitchen_set\Kitchen_set.usd
```
> D:/Kitchen_set/assets/CeilingLight/CeilingLight.usd

Kitchen_set.usd 内のあるAssetPathの解決済のパスを取得したい場合は anchorPath に、
解決対象のPathの基準になる（ロードしている）USDのAssetPathを指定します。
指定すると、指定のパス（ ./assets/CeilingLight/CeilingLight.usd ) のanchorPath基準の絶対パスにして取得することができます。

次に、前回作成したようなカスタムのAssetResolverを使用する場合。

```
usdresolve asset:/Buzz/{$VERSION}/Buzz.usd --createContextFromString D:\testUsdResolverExample\shots\shot_1\versions.json
```

> asset:/Buzz/latest/Buzz.usd

カスタムのResolverの場合、解決用のContextは都度変わりますが usdREsolverExampleの場合、 version.json を
createContextFromStringに渡すことで、パスの解決をすることができます。


このように、usdresolve ツールは、引数に 未解決のAssetPathと
解決に必要な情報 (anchorPathであったりcontextであったり)を与えることで、解決済のAssetPathをプリントしてくれます。

### DEBUGメッセージをみてみる

```
set TF_DEBUG=USD_RESOLVER_EXAMPLE
```

実際のところ、どうAssetResolutionが行われていて
結果どのようなパスになっているのかがわかりにくいので Debugメッセージをいれてみます。

![](https://gyazo.com/8b4bc57da574b657738e834f8561f79d.png)

たとえば、asset URI ではないファイルを実行してみたばあいも、UsdResolverExampleResolver が呼ばれているものの
Contextが見つからないため、DefaultResolverが呼ばれていることがわかりますし、

![](https://gyazo.com/24141e1099ccb3854bfd7630f2f39890.png)

Assetが見つかった場合は、このようにFileSystem上に見つかっていることがわかります。

## Pythonで実行する

コマンドラインを使用するのなら以上で終了なのですが、
今回はPythonから使用したい場合も併せて試してみます。

### anchorPathの場合

```python
resolver = Ar.GetResolver()

anchorPath = Ar.ResolvedPath("D:/Kitchen_set/Kitchen_set.usd")
assetPath = "./assets/Ball/Ball.usd"
fullPath = resolver.CreateIdentifier(assetPath,anchorPath)
```

anchorPathの場合は、ある解決済のPathをもとに、assetPathを解決することができる CreateIdentifierForNewAsset 関数を使用します。
ArResolvedPathは、その名の通り解決済のAssetPathです。
CreateIdentifierは、この解決済のArResolvedPathからのパスを取得することができます。

以前AssetInfoで解説したでも
このResolvedPathとResolverのCreateIdentifierを使用して、指定のレイヤーからの相対パスを解決していました。

### Resolveを使用する場合

上記の例の場合は、指定ファイルからのパスを取得することができました。
（./～～から指定される、現在のレイヤーからの相対パス)

これとは別に、AssetResolverのResolveを使用してAssetResolutionを実行する事ができます。

#### ArResolver ArResolverContextBinder ArResolverContext

AssetResolverは、大きく分けると ArResolver ArResolverContextBinder ArResolverContext の３つに分かれています。
**ArResolverContextとは、AssetResolutionを行うためにResolverに追加情報を与えるための機能** です。
そしてそのContextをResolver で使用できるようにするのに ArResolverContextBinderを使用します。

![](https://gyazo.com/284ef1cf10c3ff8b9592c3ed1a1c117b.png)

ArResolverContextとは、
usdResolverExample の場合でいうと、バージョンが書かれているjsonファイルのPathです。
usdResolverExample本体側で、このContextからjsonを受け取り、AssetResolutionを行います。

DefaultResolverの場合、このArResolverContextに、PXR_DEFAULT_SEARCH_PATHを渡して
パスの検索を行っています。

まずは、DefaultResolverを使用した場合。
DefaultResolverは、PXR_DEFAULT_SEARCH_PATHを、; で分割した文字列を、ArResolverで順番に検索し
見つかったPathをResolvedPathとして返します。

```python
from pxr import Ar

resolver = Ar.GetResolver()

context = resolver.CreateContextFromString("D:/sample;D:/Kitchen_set")
with Ar.ResolverContextBinder(context):
    print(resolver.Resolve("assets/Ball/Ball.usd"))
```

GetResolverで ArResolver オブジェクトを取得します。

Pythonで実行した場合、
ContextBinderに対して Contextを指定するのですが、その有効範囲は with で指定します。
with 内では、 Binderで指定したContextを使用してResolutionが行われるので
今回の場合なら、Resolve関数は
検索対象のPath（サンプルの場合 D:/sample D:/Kitchen_set ) を順番に検索し見つかったパスを返します。

#### URIを使用した場合

次はカスタムしたResolverを使用した場合。

```python
resolver = Ar.GetResolver()

ASSETS_DIR = "D:/testUsdResolverExample/assets/"

ctx = resolver.CreateContextFromString('asset',r"D:\testUsdResolverExample\shots\shot_1\versions.json")
# あるいは ctx  = UsdResolverExample.ResolverContext(r"D:\testUsdResolverExample\shots\shot_1\versions.json")
with Ar.ResolverContextBinder(ctx):
    resolved = resolver.Resolve("asset:Buzz/{$VERSION}/Buzz.usd")
    print(resolved.GetPathString().replace("asset:",ASSETS_DIR))
```

URIを使用している場合は、指定のContextを CreateContextFromString にURIを指定することで取得します。
あるいは、Pythonのモジュールを作成している場合はそれ経由でカスタムのContextを取得します。

ContextはResolverで使用する追加情報を指定します。
（今回の場合はversionを書いたjsonのパス）

Resoverは、Contextを経由して version.json を受け取ります。
そして、version.jsonをロードし、その中にあるAssetNameのバージョンを取得します。
そしてそのバージョンを使用することで、AssetName以下の未解決の $VERSION を置換し、最終的なAssetのFullPathを解決します。

usdResolverExampleの場合は、Resolveで取得できるPathは URIのPathなので
asset: を USD_RESOLVER_EXAMPLE_ASSET_DIR に置換していますが、(サンプルではAssetOpen時に _GetFilesystemPath(resolvedPath) でFullPath取得)
それ以外の「どのバージョンを使用するか」はResolveを使用することで最終的にどのPathが使用されているのかわかりました。

!!! info
    Resolverには（Resolverに限らずLayerなどでも） ResolveForNewAsset のように ほぼ同じような処理だけど NewAssetとつく
    関数が用意されています。
    これは、新規アセットの場合ファイルが存在しない可能性があるので
    それによって処理を分岐させているようでした。
    Resolveの場合は、既にファイルがあることを期待して見つからない場合はからのArResolvedPathを
    返す処理が入っていたり。
    
## まとめ

２回にわたってAssetResolutionを見てきました。
Resolverを使用すれば、FilePathの解決をいろいろカスタマイズできそうですし
データベースや、各種クラウドストレージの活用を
USDのパイプラインで実装することができます。

この機能は、コンポジションやスキーマといった強力な機能と同じぐらい魅力的なものであり
USDを使用したパイプラインを支える強力な武器でもあります。

AssetResolver2.0になり、わかりやすいサンプルも追加されたことで
より導入がしやすくなったと思いますので
USDを導入する際には活用していただければなと思います。

!!! info
    Pythonでの使用方法は
    
    > extras/usd/examples/usdResolverExample/testenv/testUsdResolveExample.py
    
    を参考にしています。
    C++の実装と合わせてテストコードをみると、より分かりやすいです
