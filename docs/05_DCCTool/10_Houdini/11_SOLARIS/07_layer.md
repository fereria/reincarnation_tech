---
title: SOLARISでのLayerの扱い
tags:
    - USD
    - SOLARIS
    - Houdini
---

ぼんやりと SOLARIS の 1 ノードが 1 レイヤーだと思っていましたが
詳しく調べていくと色々新しいことがわかってきたのでメモをば。

## Layer とは

まず、Layer とはなにか。
詳しくは {{markdown_link('stage_layer_spec')}} にまとめてありますが、  
ざっくりいうと 1 つの usd ファイルのことを Layer と呼びます。

そして、この Layer をコンポジションアークと呼ばれる合成ルールにそって
複数の Layer を合成して、1 つのステージを構築する...というのが、USD の基本になります。

では、SOLARIS ではこの Layer 構造がどのように作られているのか
少し詳しく調べてみます。

## LayerStack を調べる

まずは、SOLARIS でのコンポジションの LayerStack を見てみます。
LayerStack とは、複数の Layer をサブレイヤーで合成するときの Layer を束ねたものです。
1Layer にはそれぞれいろんな定義（主張）が書かれていているわけですが
それがどういうふうな関係になっているのかを確認することができます。

```python
node = hou.pwd()
stage = node.editableStage()

# Add code to modify the stage.
# Use drop down menu to select examples.

for layer in stage.GetLayerStack():
    print(layer)
    print(layer.ExportToString())
```

確認用のコードはこちら。

![](https://gyazo.com/7928a27a9ce948c490ae450206d0c522.png)

これを、まずはこんな感じで Python ノードに入れて、結果をみていきます。

全部は長いので
https://snippets.cacher.io/snippet/b7130348f4ac41539759?t=U1ojSBLJ66yL6IovpVdLdABDfCtdx3
こちらに結果は貼っておきましたが、一部抜粋で重要なところをみていきます。

```
Sdf.Find('anon:000000007B132340')
#sdf 1.4.32

def HoudiniLayerInfo "HoudiniLayerInfo" (
    customData = {
        string HoudiniCreatorNode = "/stage/sphere1"
        string[] HoudiniEditorNodes = ["/stage/sphere1"]
    }
)
{
}

def Sphere "sphere1" (
    customData = {
        int HoudiniPrimEditorNodeId = 13
    }
)
{
    double radius = 1
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]
}
```

LayerStack を取得すると Sdf.Find という形で Layer オブジェクトを取得できます。
この Layer が、上のような usda の定義が記述されています。

で、上のコードをよく見ると HoudiniEditorNodes というアトリビュートがあるのがわかりますが
この Layer を作るのに使われているノードがここに書かれています。

## 複数レイヤーの場合

![](https://gyazo.com/be037461737f283efeff13a80b53711b.png)

1 ノードのみだと、定義がある Layer は１つのみだったですが
こんな感じで Merge を使って複数の Prim を組み合わせた場合はどうなるかみてみます。
この場合、ノードの右下に「2Layers」というのがでているのがわかるかと思いますが、これが意味
するところは

結果はこうなって
https://snippets.cacher.io/snippet/6141d563cd41b4502d3f
重要な部分だけ書き出すと

```
Sdf.Find('anon:000000007E0D2FC0')
#sdf 1.4.32

def HoudiniLayerInfo "HoudiniLayerInfo" (
    customData = {
        string HoudiniCreatorNode = "/stage/sphere1"
        string[] HoudiniEditorNodes = ["/stage/sphere1"]
    }
)
{
}

def Sphere "sphere1" (
    customData = {
        int HoudiniPrimEditorNodeId = 13
    }
)
{
    double radius = 1
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]
}
```

これと

```
Sdf.Find('anon:000000007E0D2E80')
#sdf 1.4.32

def HoudiniLayerInfo "HoudiniLayerInfo" (
    customData = {
        string HoudiniCreatorNode = "/stage/cube1"
        string[] HoudiniEditorNodes = ["/stage/cube1"]
    }
)
{
}

def Cube "cube1" (
    customData = {
        int HoudiniPrimEditorNodeId = 14
    }
)
{
    double size = 2
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]
}

```

これのように、1Layer ごとに 1 つのノード、そしてそれぞれが

```
Sdf.Find('anon:000000007E159800:root.usd')
#usda 1.0
(
    subLayers = [
        @anon:000000007E0D3B00@,
        @anon:000000007E0D2D40@,
        @anon:000000007E0D2FC0@,
        @anon:000000007E0D2E80@
    ]
)
```

こんな感じでサブレイヤーで合成されているのがわかります。
つまりは、Houdini のノードの右下に ～ Layers が出ている場合、

![](https://gyazo.com/427a9abebd979a6def3c83e5a45f4561.png)

ノードの縁の色ごとに、1 つの Layer としてメモリー内で Layer が構築されている...ということになります。

```python
node = hou.pwd()
stage = node.editableStage()

# Add code to modify the stage.
# Use drop down menu to select examples.

stage.DefinePrim('/hoge')

for layer in stage.GetLayerStack():
    print(layer)
    print(layer.ExportToString())
```

試しに、Python ノードのコマンドをこんなふうにして
Python ノードでも Prim を定義してみると

![](https://gyazo.com/fdc10a6c4bd2172e7c706803b5e5ff95.png)

Python ノード部分が 3Layers 目になり

```
Sdf.Find('anon:000000007E0D2D40')
#sdf 1.4.32

def HoudiniLayerInfo "HoudiniLayerInfo" (
    customData = {
        string HoudiniCreatorNode = "/stage/pythonscript1"
    }
)
{
}

def "hoge"
{
}
```

LayerStack には、Pythonscript の HoudiniCreatorNode が追加され、
そこに PythonScript で定義をした Prim が追加されていることがわかります。

## どういうときにレイヤーが分かれるのか

ほぼ自分の興味というか疑問だったのが、この Layers がどういうタイミングでまとめられたり
分けられたりするのか　ということと、SOLARIS のノードを接続することが
実際のところなにをしているのか非常に曖昧で構造を理解できていませんでした。
ですが、詳しく調べるとどういう処理なのかが見えてきます。

### Merge

まず、Merge。
![](https://gyazo.com/19abb3222d90fdb3752b8914feafbb0b.png)

Merge には、MergeStyle というものがあり
デフォルトだと Separate Layers 、上の出力結果の通り
それぞれを個別の Layer として扱ってサブレイヤーで合成する設定になっています。

![](https://gyazo.com/df7531ccc140ed5f5cc1bad410b99134.png)

それを Flatten Layers に変更すると、

```
Sdf.Find('anon:00000000BD376D40')
#sdf 1.4.32

def HoudiniLayerInfo "HoudiniLayerInfo" (
    customData = {
        string HoudiniCreatorNode = "/stage/sphere1"
        string[] HoudiniEditorNodes = ["/stage/sphere1", "/stage/merge1"]
    }
)
{
}

def Cube "cube1" (
    customData = {
        int HoudiniPrimEditorNodeId = 14
    }
)
{
    double size = 2
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]
}

def Sphere "sphere1" (
    customData = {
        int HoudiniPrimEditorNodeId = 13
    }
)
{
    double radius = 1
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]
}
```

入力の Layer ２つが 1 つの Layer にまとまった状態になります。

![](https://gyazo.com/8ab27ef99d1fa46c6e6fc4b2e794c92e.png)

この差がどういうところに影響するかというと、
LOP Actions の Inspect ActiveLayer (現在の編集ターゲットになっている Layer の中身を確認する)
が、Flatten した方で確認できるようになります。（Flatten していない方は見れない）
これは、Flatten していない場合は、選択しているノード段階では 2 つ含まれているから
ターゲットになる Layer が選択されていないからかと思われます。

### Graft

もう一つ、レイヤーが統合されるケースが　 Prim 階層が編集されている場合です。

![](https://gyazo.com/3b3716e91cfd791b5c5e9ac569dada5f.png)

Graft ノードを使用すると、Input1 の Stage に対して指定の構造で「接ぎ木」するように
結合してくれます。

![](https://gyazo.com/708c2eac7dd10e90e8f7535d4882848f.png)

結果。
Merge とは違い、Graft した場合は　 Layers という記述が増えず

```
Sdf.Find('anon:00000000701C5440')
#sdf 1.4.32

def HoudiniLayerInfo "HoudiniLayerInfo" (
    customData = {
        string HoudiniCreatorNode = "/stage/root"
        string[] HoudiniEditorNodes = ["/stage/root", "/stage/graft1"]
    }
)
{
}

def Xform "root" (
    customData = {
        int HoudiniPrimEditorNodeId = 25
    }
)
{
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]

    def Xform "hoge" (
        customData = {
            token HoudiniSourceNode = "/stage/cube1"
        }
    )
    {
        def Sphere "sphere1" (
            customData = {
                int HoudiniPrimEditorNodeId = 13
            }
        )
        {
            double radius = 1
            matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
            uniform token[] xformOpOrder = ["xformOp:transform"]
        }

        def Cube "cube1" (
            customData = {
                int HoudiniPrimEditorNodeId = 14
            }
        )
        {
            double size = 2
            matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
            uniform token[] xformOpOrder = ["xformOp:transform"]
        }
    }
}
```

1 つの Layer に、 Input1 のノードも Input2 のノードもまとまった状態になります。
これは {{markdown_link('02_reparentPrim')}} のときにわかったことですが
Reparent の処理は USD のコンポジションには存在しない（Reference であるノードに対して構造を追加することはある）わけで、
Graft のような入力ノードの階層を変更するようなノードの場合、
サブレイヤーでの構築はできず、１ Layer にまとめた上で BatchNamespaceEdit しているから
Layer は１つにまとまっているのかなと思います。

という感じで、SOLARIS ではレイヤーが暗黙的に構築されてサブレイヤーされて出力されていました。

多くの場合はあんまりここまで Layer の構築単位を考える必要はないと思うのですが
これが影響するケースが１つあって

![](https://gyazo.com/0c366c7465cbf386aace7e741f52d1aa.png)

USD ROP で USD を Export するときに、 SaveStyle を Separate Layers にした場合
出力される usd の単位が変わります。

このオプションはその名の通り、出力される USD ファイルを
どういう単位で出力するか..というものになります。

Separate Layers では、SOLARIS の ～ Layers（↑ の LayerStack で確認した単位）で
ファイルが小分けされます。
（作成ファイルは、SdfPath のサブフォルダ下に Export される？）

もしかしたら他にもこの Layer 単位が影響するところがあるかもしれないですが

-   SOLARIS のノードはサブレイヤー合成
-   特定条件下だと Flatten（１つの Layer に統合）されたりする

というのを理解するだけで、ノードの構築がどのように行われて
結果どういうシーングラフが出てくるのか、理解できるのかなと思います。
（Flatten してないとうまく行かなかった何かがあった気がしたけど思い出せない...）

## まとめ

こんな感じで、SOLARIS でのノード操作のふわっとした理解をしていたところが
だいぶ整理できたおかげで、各種ノードの違いとか意図がつかめるようになってきました。

これをベースに、色々とシーンの構築やら USD 的なオーサリング方法を
色々ねっていきたいです。
