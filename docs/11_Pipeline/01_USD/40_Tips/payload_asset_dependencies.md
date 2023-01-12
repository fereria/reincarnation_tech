---
title: USDファイルの依存関係図を作る
tags:
    - USD
    - AdventCalendar2022
description: AssetInfoを使用してUSDのファイルの依存関係図を作る話
---

USD は、大量の usd ファイルをコンポジションすることによって、１つの巨大なシーングラフを構築します。
つまりは、開くファイルは 1 つでも、そのファイルを構築するのに必要なシーンの依存関係は巨大になり
全体像を俯瞰してみるのは難しいです。

ので、今回はこの巨大な USD の依存関係を、Graphviz を使用してビジュアライズしてみようと思います。

## 準備

まずは準備から。
依存関係図を検索する場合、USD のシーンを 1 つずつ開いては Reference や Payload を探し
そしてそのファイルをまた開いて...と繰り返していく必要があります。
それでも可能ですが、依存関係を確認したいだけなのに頂点データなどはいちいち開きたくありません。
それに、シーンのトラバースも毎回やりたくありません。

ので、この辺りは事前にアセットを作成する段階で
「個のアセットが使用している USD ファイルは～～～である」
という定義を事前に定義しておくことで、シーンを開かずに依存関係を記したメタデータを
参照していくようにします。

この時に使えるのが {{markdown_link('assetinfo')}} です。

### AssetInfo とは

AssetInfo とは、詳細は上記のページに詳しく書いているのですが
簡単にまとめると
「Prim や Property に対して指定することができる辞書型のメタデータ」
です。
今回のような、シーンに含まれているシーンデータであったり
LayerFlatten したときに元シーンをたどるための identifier であったりアセット名であったり、
シーン全体を開かずに取得しておきたいデータを
この AssetInfo に記載することで、Payload をアンロード状態でも必要な情報に
アクセスできるようになります。

### Houdini で AssetInfo を指定する

というわけで、サンプルデータを作っていきます。

![](https://gyazo.com/c2b55ff5d0dc1899cb204277dc67d189.png)

まずは Payload で読むための USD ファイルを用意します。

![](https://gyazo.com/0e2cb5079f2a5313ca6d4e347738dfce.png)

そして、DefaultPrim にするための RootPrim を作り、その子供に Cube と Sphere を
Payload で読み込みます。

USD は、特に事情がない場合（Reference 時に Prim を指定してロードするためなど）は
RootPrim は 1 つにしたうえで、その Prim を DefaultPrim に指定します。
これは、このサンプルファイルも、どこかでリファレンスされるアセットなので
リファレンスで読み込むルートになる Prim は DefaultPrim として
定義する必要があるからです。

![](https://gyazo.com/628f9aa61aee3e1b3f0c2182c63c06ab.png)

ので、ConfigureLayer ノードで Default Primitive を指定しておきます。

その次に Cofigure Primitive ノードを使用して、Prim に対して依存関係を定義するメタデータを
追加します。

この ConfigurePrimitive ノードは、その名の通り USD の Prim の編集をするノードです。
今回の AssetInfo は Prim に対して指定するメタデータですので、
その設定場所も ConfigurePrimitive になるわけです。

![](https://gyazo.com/18065665c44b8eb4db91540e1629fdc3.png)

Asset Dependencies に、 sphere と cube の USD パスを入れておきます。

ここまで出来たら、 USD ROP でファイルを出力しておきます。

![](https://gyazo.com/dfea67269ec509961d26b8593cde3186.png)

あとは同じ要領で、先ほど作成した cube と sphere が入っているアセットを
Payload するようなシーンを作成します。

![](https://gyazo.com/cc598d59f0b2a7e5f147cf134982e813.png)

現状の関係図を手動で作図してみるとこのようになります。
ので、これを Python を使用して作図してみます。

## 図を作る

```python
from pxr import Usd
import graphviz
```

まずは必要なモジュールをインポートします。
依存関係の表示には、今回は graphviz を使用します。

```python
def getPayloadLayers(path):

    retVal = set()

    stage = Usd.Stage.Open(path,Usd.Stage.LoadNone)
    for prim in stage.TraverseAll():
        info = prim.GetAssetInfo()
        if 'payloadAssetDependencies' in info:
            for i in info['payloadAssetDependencies']:
                retVal.add(i.resolvedPath)

    return list(retVal)
```

引数の USD ファイルを LoadNone(Payload を読まない状態で)で開きます。
こうすると、モデルはロードされないので AssetInfo だけを高速に読み取ることができます。

```python
def createGraph(path):

    nodes = []
    edges = []

    def Traverse(path):
        nodes.append(path.replace("\\","/"))
        payloads = getPayloadLayers(path)
        for i in payloads:
            edges.append((path.replace("\\","/"),i.replace("\\","/")))
            Traverse(i)

    Traverse(path)

    g = graphviz.Digraph(format='svg',filename='test.svg')

    for node in nodes:
        g.node(node.replace("/","_").replace(":","_"),node)

    for edge in edges:
        g.edge(edge[0].replace("/","_").replace(":","_"),edge[1].replace("/","_").replace(":","_"))

    g.view()
```

あとは、現在のシーンの Prim を Traverse して、 payloadAssetDependencies を探し
そこに指定されたパスを再帰で探します。

Graphviz で表示するための Node は、USD のファイル名で
Payload しているレイヤーと payloadAssetDependencies で指定されているレイヤを
edge でつなぎます。

あとはそれを表示して終了です。

ノード名は、ファイルのフルパスにしてしまうと意図しない形で解釈されてしまうので
ユニークな名前を : / を \_ に置換した文字列、ラベルにファイル名を指定しておきます。

![](https://gyazo.com/a3ccce6a1a9979a756fea615d0784dbb.png)

実行結果。

## まとめ

今回は、かなりシンプルなシーンで構築しましたが
AssetInfo と再帰と Graphviz を使用することで、シーンを全部探さなくても依存関係を
ビジュアライズできました。

ここから何が言えるかというと、
USD でアセット製作をする場合、形状やマテリアルだけではなく
依存関係やファイル名などのメタデータを、セットアップ時にきちんと指定しておくことで
できる幅が広がるということがわかったかと思います。

USD でパイプラインを設計する場合は、どんなデータを事前に入れておくかは
しっかり設計しておくのがとても大切です。
