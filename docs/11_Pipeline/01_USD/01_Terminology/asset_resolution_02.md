---
title: AssetResolution(2) ResolveとContext
tags:
    - USD
    - AdventCalendar2021
    - CEDEC2022
---

[Universal Scene Description AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 17 日目は、
USD の Asset Resolution (アセットパスの解決) 第二回目。

前回の {{markdown_link('asset_resolution')}} に続いて、USD のツールセットの１つ usdresolve についてと Python を使用したパス解決方法です。

!!! note
USDTool 下に記事を書くか迷いましたが、
割合的に usdresolve 要素はわずかなので、前回の続きとして記事は書きます

## usdresolve

まず、USD のツールセットには usdresolve というコマンドラインツールが存在します。

https://graphics.pixar.com/usd/release/toolset.html#usdresolve

これは、前回説明した AssetResolver をコマンドラインから実行するためのツールです。
このコマンドラインを使用すると、AssetResolver で行っている AssetResolution を実行して
USD の AssetPath から最終的なリソースへのパスを得ることができます。

まず、DefaultResolver を使用して、相対パスを絶対パスに変換したい場合。

```bat
usdresolve ./assets/CeilingLight/CeilingLight.usd --anchorPath D:\Kitchen_set\Kitchen_set.usd
```

> D:/Kitchen_set/assets/CeilingLight/CeilingLight.usd

Kitchen_set.usd 内のある AssetPath の解決済のパスを取得したい場合は anchorPath に、
解決対象の Path の基準になる（ロードしている）USD の AssetPath を指定します。
指定すると、指定のパス（ ./assets/CeilingLight/CeilingLight.usd ) の anchorPath 基準の絶対パスにして取得することができます。

次に、前回作成したようなカスタムの AssetResolver を使用する場合。

```
usdresolve asset:/Buzz/{$VERSION}/Buzz.usd --createContextFromString D:\testUsdResolverExample\shots\shot_1\versions.json
```

> asset:/Buzz/latest/Buzz.usd

カスタムの Resolver の場合、解決用の Context は都度変わりますが usdREsolverExample の場合、 version.json を
createContextFromString に渡すことで、パスの解決をすることができます。

このように、usdresolve ツールは、引数に 未解決の AssetPath と
解決に必要な情報 (anchorPath であったり context であったり)を与えることで、解決済の AssetPath をプリントしてくれます。

### DEBUG メッセージをみてみる

```
set TF_DEBUG=USD_RESOLVER_EXAMPLE
```

実際のところ、どう AssetResolution が行われていて
結果どのようなパスになっているのかがわかりにくいので Debug メッセージをいれてみます。

![](https://gyazo.com/8b4bc57da574b657738e834f8561f79d.png)

たとえば、asset URI ではないファイルを実行してみたばあいも、UsdResolverExampleResolver が呼ばれているものの
Context が見つからないため、DefaultResolver が呼ばれていることがわかりますし、

![](https://gyazo.com/24141e1099ccb3854bfd7630f2f39890.png)

Asset が見つかった場合は、このように FileSystem 上に見つかっていることがわかります。

## Python で実行する

コマンドラインを使用するのなら以上で終了なのですが、
今回は Python から使用したい場合も併せて試してみます。

### anchorPath の場合

```python
resolver = Ar.GetResolver()

anchorPath = Ar.ResolvedPath("D:/Kitchen_set/Kitchen_set.usd")
assetPath = "./assets/Ball/Ball.usd"
fullPath = resolver.CreateIdentifier(assetPath,anchorPath)
```

anchorPath の場合は、ある解決済の Path をもとに、assetPath を解決することができる CreateIdentifierForNewAsset 関数を使用します。
ArResolvedPath は、その名の通り解決済の AssetPath です。
CreateIdentifier は、この解決済の ArResolvedPath からのパスを取得することができます。

以前 AssetInfo で解説したでも
この ResolvedPath と Resolver の CreateIdentifier を使用して、指定のレイヤーからの相対パスを解決していました。

### Resolve を使用する場合

上記の例の場合は、指定ファイルからのパスを取得することができました。
（./～～から指定される、現在のレイヤーからの相対パス)

これとは別に、AssetResolver の Resolve を使用して AssetResolution を実行する事ができます。

#### ArResolver ArResolverContextBinder ArResolverContext

AssetResolver は、大きく分けると ArResolver ArResolverContextBinder ArResolverContext の３つに分かれています。
**ArResolverContext とは、AssetResolution を行うために Resolver に追加情報を与えるための機能** です。
そしてその Context を Resolver で使用できるようにするのに ArResolverContextBinder を使用します。

![](https://gyazo.com/284ef1cf10c3ff8b9592c3ed1a1c117b.png)

ArResolverContext とは、
usdResolverExample の場合でいうと、バージョンが書かれている json ファイルの Path です。
usdResolverExample 本体側で、この Context から json を受け取り、AssetResolution を行います。

DefaultResolver の場合、この ArResolverContext に、PXR_DEFAULT_SEARCH_PATH を渡して
パスの検索を行っています。

まずは、DefaultResolver を使用した場合。
DefaultResolver は、PXR_DEFAULT_SEARCH_PATH を、; で分割した文字列を、ArResolver で順番に検索し
見つかった Path を ResolvedPath として返します。

```python
from pxr import Ar

resolver = Ar.GetResolver()

context = resolver.CreateContextFromString("D:/sample;D:/Kitchen_set")
with Ar.ResolverContextBinder(context):
    print(resolver.Resolve("assets/Ball/Ball.usd"))
```

GetResolver で ArResolver オブジェクトを取得します。

Python で実行した場合、
ContextBinder に対して Context を指定するのですが、その有効範囲は with で指定します。
with 内では、 Binder で指定した Context を使用して Resolution が行われるので
今回の場合なら、Resolve 関数は
検索対象の Path（サンプルの場合 D:/sample D:/Kitchen_set ) を順番に検索し見つかったパスを返します。

#### URI を使用した場合

次はカスタムした Resolver を使用した場合。

```python
resolver = Ar.GetResolver()

ASSETS_DIR = "D:/testUsdResolverExample/assets/"

ctx = resolver.CreateContextFromString('asset',r"D:\testUsdResolverExample\shots\shot_1\versions.json")
# あるいは ctx  = UsdResolverExample.ResolverContext(r"D:\testUsdResolverExample\shots\shot_1\versions.json")
with Ar.ResolverContextBinder(ctx):
    resolved = resolver.Resolve("asset:Buzz/{$VERSION}/Buzz.usd")
    print(resolved.GetPathString().replace("asset:",ASSETS_DIR))
```

URI を使用している場合は、指定の Context を CreateContextFromString に URI を指定することで取得します。
あるいは、Python のモジュールを作成している場合はそれ経由でカスタムの Context を取得します。

Context は Resolver で使用する追加情報を指定します。
（今回の場合は version を書いた json のパス）

Resover は、Context を経由して version.json を受け取ります。
そして、version.json をロードし、その中にある AssetName のバージョンを取得します。
そしてそのバージョンを使用することで、AssetName 以下の未解決の $VERSION を置換し、最終的な Asset の FullPath を解決します。

usdResolverExample の場合は、Resolve で取得できる Path は URI の Path なので
asset: を USD_RESOLVER_EXAMPLE_ASSET_DIR に置換していますが、(サンプルでは AssetOpen 時に \_GetFilesystemPath(resolvedPath) で FullPath 取得)
それ以外の「どのバージョンを使用するか」は Resolve を使用することで最終的にどの Path が使用されているのかわかりました。

!!! info
Resolver には（Resolver に限らず Layer などでも） ResolveForNewAsset のように ほぼ同じような処理だけど NewAsset とつく
関数が用意されています。
これは、新規アセットの場合ファイルが存在しない可能性があるので
それによって処理を分岐させているようでした。
Resolve の場合は、既にファイルがあることを期待して見つからない場合はからの ArResolvedPath を
返す処理が入っていたり。

## まとめ

２回にわたって AssetResolution を見てきました。
Resolver を使用すれば、FilePath の解決をいろいろカスタマイズできそうですし
データベースや、各種クラウドストレージの活用を
USD のパイプラインで実装することができます。

この機能は、コンポジションやスキーマといった強力な機能と同じぐらい魅力的なものであり
USD を使用したパイプラインを支える強力な武器でもあります。

AssetResolver2.0 になり、わかりやすいサンプルも追加されたことで
より導入がしやすくなったと思いますので
USD を導入する際には活用していただければなと思います。

!!! info
Python での使用方法は

    > extras/usd/examples/usdResolverExample/testenv/testUsdResolveExample.py

    を参考にしています。
    C++の実装と合わせてテストコードをみると、より分かりやすいです
