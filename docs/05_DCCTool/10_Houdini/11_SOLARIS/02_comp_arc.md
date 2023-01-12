---
title: SOLARISでコンポジションアーク
tags:
    - USD
    - SOLARIS
    - Houdini
---

# SOLARIS でコンポジションアーク

前回で、SOLARIS の中で USD ファイルを開いてみましたが  
今回からノードを使って具体的な USD オーサリングをやっていこうと思います。

## コンポジションアーク

まず、やり方に行く前に「コンポジションアーク」についておさらい。

コンポジションアークとは、レイヤーを「プロシージャルに合成」していく時の  
合成ルールのことです。

USD は、複数のファイルを合成して結果シーングラフを作りますが  
合成するときに「どうやって合成する？」というルールがなければ  
プロシージャルに合成するできません。

そのときのルールがこの「コンポジションアーク」であり、

-   サブレイヤー
-   バリアント
-   リファレンス
-   継承
-   ペイロード
-   特殊化

この 6 種類が存在します。

詳しくは、

{{markdown_link('comp_arc')}}

こちらで解説しています。

では、このコンポジションアークが SOLARIS 上でどう扱うかを見ていきたいと思います。

### サブレイヤー

まず、最初はサブレイヤー。  
SOLARIS ではすべてのノードは USD のレイヤーなのですが  
そのレイヤーをつなげた場合の多くはこのサブレイヤーで合成されます。

![](https://gyazo.com/0c7d1aa903918adb1356646f2d7ca9bd.png)

まずは単純なノードで見てみます。

![](https://gyazo.com/6cf48172d70f2f02679e6a26d5301802.png)

SubLayer ノードは、Input1 とそれ以外の MultiInput をつけつけています。

![](https://gyazo.com/383eb4237bdb8aba0021e0a16aa15c02.png)

今の Layer 状況を「Scene Graph Layers Panel」で確認すると、  
Input1 の入力の子として MultiInput の Layer がついているような構造になっています。

```usda
#usda 1.0
(
    subLayers = [
        @CUBE.usda@,
        @SPHERE.usda@
    ]
)

def Xform "BasePrim"
{
}
```

USD の SubLayer を USDA ファイルで記述するとこうなります。  
このファイルをノードで表すと、  
ファイル自身が Input1 で、subLayers でセットしている usda ファイルが MultiInput の入力になります。

![](https://gyazo.com/c04d6f005b208c3ce07aa3af4af9c710.png)

ただし、このレイヤーの解決順序は USD の公式の順序ではなく  
「Sublayer Position」で指定されたものを SubLayer の位置として認識します。  
デフォルトの場合は、「Strongest Layer」になっていて  
一番強いノード（この場合最後の入力である SPHERE）が出力されます。

通常の USD と同じにしようとした場合「Strongest File Layer's Position」で  
RootLayer の Local（RootLayer に記載されている Prim）が優先されるのがデフォルトの USD 解決順序な気がします。

![](https://gyazo.com/04d3363de97ef7c8cc8920e68f6eccfc.png)

この SubLayer 時の優先順序（どの順番で合成されているのか）は、Scene Graph Detail の「レイヤースタック」で  
確認することが出来ます。

レイヤースタックとは、すべてのサブレイヤーを集めたものです。
レイヤーの Primitive や各種プロパティ・アトリビュートの値はレイヤースタックに積まれた順  
（上のスクショの例だと、上のほうが強い）で上書きされていきます。  
シーングラフを構築するときに、どのようにそれぞれのレイヤーが「解決しているか」は  
このレイヤースタックを確認することでわかります。

#### サブレイヤーのアウトプット

この SubLayer のアウトプットでなにを返すかというと

![](https://gyazo.com/17741f4878320e971ccb48891e4157da.png)

確認するには lopinputprims 関数を使用すればわかります。

![](https://gyazo.com/80ecd2d49c9f26dcb6431a758f3642bb.png)

Collection ノードで確認してみると、「BasePrim」つまりは、Input1 に入力されている Primitive が  
編集された Primitive として取得されることが分かります。

あくまでも取得出来るのは「編集している RootLayer」であり、  
合成側のレイヤー（MultiInput に入力されている物）は含まないというのが注意する点です。  
入力の Primitive を使用して、次のノードで何かをしたい場合（ lopinputprims で取得する場合）  
合成した結果すべてを得られるわけではありません。

なお、この出力される Primitive は Sublayer Position を変更しても変わらず Input1 の Primitive が帰ってきます。

![](https://gyazo.com/de942a02f5065a37feb04f13a41d108b.png)

似た挙動をするノードとして「Merge」がありますが  
こちらは SubLayer とは違い、入力したノードを並列で扱い合成し  
結果できたレイヤーを返します。  
なので、 lopinputprims で次のノードで取得した場合  
すべての Primitive を取得することができます。

![](https://gyazo.com/13ced403b9f124cac98bbe72c14e8307.png)

### SubLayer と Merge の違い

SubLayer と Merge は挙動がほぼ同じで、結果のシーングラフも同じです。  
ですが、上に書いたとおり結果出力されるノードなどに違いがあります。  
それが確認できるのが「Scene Graph Layers Panel」です。

![](https://gyazo.com/a6a5cdb5f6bac4a6bb5d44523844c08d.png)

まずは、SubLayer のレイヤー構造。  
レイヤーの構造は、Input1 のレイヤーの子に MultiInput のノードが存在する状態です。

![](https://gyazo.com/c9370ffaacadc4ee2a6c66bfd9244449.png)

つぎに Merge を見てみると、  
レイヤー構造は親子ではなく「並列」に扱われています。

#### Layer Flatten

サブレイヤーで合成されている各種レイヤーは ～ Layers 　という形でノードの右下に表示されています。

![](https://gyazo.com/1c0c0fef51af49f048fa627789ebed82.png)

この Layers の数は、SceneGraphLayersPanel の「Implicit」になっているレイヤーの数です。  
この複数のレイヤーを「1 つに結合」するのが LayerFlatten です。

![](https://gyazo.com/f5122a6a03831d13500b2625f90f78aa.png)

ConfigureLayers ノードの「FlatetenInput」を

![](https://gyazo.com/551e1df32b0baac4205472acf0b3347a.png)

Flatten Input Layers に切り替えると、

![](https://gyazo.com/6e2cedd9ba4d53054a7058431d03c275.png)

レイヤーは 1 つに統合されます。  
 PhotoShop のレイヤー統合、あるいは AE のプリコンポーズのような処理で  
 各レイヤーをサブレイヤーで合成していった場合の結果を制御できるようにしてあります。

USD を SOLARIS ではなくそのまま使っていると問題になってくるのが、レイヤーのコンポジションの解決順序です。

{{markdown_link('comp_arc')}}

USD の解決順序は上のページの通りですが  
 SOLARIS では要所要所のノードで Flatten、あるいはノードの接続順によるプロシージャルな解決制御  
 をできるようにしているように感じました。
