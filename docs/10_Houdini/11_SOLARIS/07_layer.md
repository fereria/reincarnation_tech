---
title: SOLARISでのLayerの扱い
---

ぼんやりとSOLARISの1ノードが1レイヤーだと思っていましたが
詳しく調べていくと色々新しいことがわかってきたのでメモをば。

## Layerとは

まず、Layerとはなにか。
詳しくは [USDの基本構造](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/04_layer_stage/)にまとめてありますが、  
ざっくりいうと 1つのusdファイルのことをLayerと呼びます。

そして、このLayerをコンポジションアークと呼ばれる合成ルールにそって
複数のLayerを合成して、1つのステージを構築する...というのが、USDの基本になります。

では、SOLARISではこのLayer構造がどのように作られているのか
少し詳しく調べてみます。

## LayerStackを調べる

まずは、SOLARISでのコンポジションのLayerStackを見てみます。
LayerStackとは、複数のLayerをサブレイヤーで合成するときのLayerを束ねたものです。
1Layerにはそれぞれいろんな定義（主張）が書かれていているわけですが
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

これを、まずはこんな感じでPythonノードに入れて、結果をみていきます。

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
LayerStackを取得すると Sdf.Find という形でLayerオブジェクトを取得できます。
このLayerが、上のようなusdaの定義が記述されています。

で、上のコードをよく見ると HoudiniEditorNodes というアトリビュートがあるのがわかりますが
このLayerを作るのに使われているノードがここに書かれています。

## 複数レイヤーの場合

![](https://gyazo.com/be037461737f283efeff13a80b53711b.png)

1ノードのみだと、定義があるLayerは１つのみだったですが
こんな感じでMergeを使って複数のPrimを組み合わせた場合はどうなるかみてみます。
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
これのように、1Layerごとに1つのノード、そしてそれぞれが

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
つまりは、Houdiniのノードの右下に ～Layersが出ている場合、

![](https://gyazo.com/427a9abebd979a6def3c83e5a45f4561.png)

ノードの縁の色ごとに、1つのLayerとしてメモリー内でLayerが構築されている...ということになります。

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
試しに、Pythonノードのコマンドをこんなふうにして
PythonノードでもPrimを定義してみると

![](https://gyazo.com/fdc10a6c4bd2172e7c706803b5e5ff95.png)

Pythonノード部分が 3Layers目になり

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
LayerStackには、PythonscriptのHoudiniCreatorNode が追加され、
そこに PythonScriptで定義をしたPrimが追加されていることがわかります。

## どういうときにレイヤーが分かれるのか

ほぼ自分の興味というか疑問だったのが、このLayersがどういうタイミングでまとめられたり
分けられたりするのか　ということと、SOLARISのノードを接続することが
実際のところなにをしているのか非常に曖昧で構造を理解できていませんでした。
ですが、詳しく調べるとどういう処理なのかが見えてきます。

### Merge

まず、Merge。
![](https://gyazo.com/19abb3222d90fdb3752b8914feafbb0b.png)

Mergeには、MergeStyleというものがあり
デフォルトだと Separate Layers 、上の出力結果の通り
それぞれを個別のLayerとして扱ってサブレイヤーで合成する設定になっています。

![](https://gyazo.com/df7531ccc140ed5f5cc1bad410b99134.png)

それをFlatten Layersに変更すると、

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
入力のLayer２つが1つのLayerにまとまった状態になります。

![](https://gyazo.com/8ab27ef99d1fa46c6e6fc4b2e794c92e.png)

この差がどういうところに影響するかというと、
LOP Actionsの Inspect ActiveLayer (現在の編集ターゲットになっているLayerの中身を確認する)
が、Flattenした方で確認できるようになります。（Flattenしていない方は見れない）
これは、Flattenしていない場合は、選択しているノード段階では2つ含まれているから
ターゲットになるLayerが選択されていないからかと思われます。

### Graft

もう一つ、レイヤーが統合されるケースが　Prim階層が編集されている場合です。

![](https://gyazo.com/3b3716e91cfd791b5c5e9ac569dada5f.png)

Graftノードを使用すると、Input1のStageに対して指定の構造で「接ぎ木」するように
結合してくれます。

![](https://gyazo.com/708c2eac7dd10e90e8f7535d4882848f.png)

結果。
Mergeとは違い、Graftした場合は　Layersという記述が増えず

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
1つのLayerに、 Input1のノードもInput2のノードもまとまった状態になります。
これは [PrimのReparent](https://fereria.github.io/reincarnation_tech/11_Pipeline/30_USD_Programming/Python/02_reparentPrim/)のときにわかったことですが
Reparentの処理はUSDのコンポジションには存在しない（Referenceであるノードに対して構造を追加することはある）わけで、
Graftのような入力ノードの階層を変更するようなノードの場合、
サブレイヤーでの構築はできず、１Layerにまとめた上でBatchNamespaceEditしているから
Layerは１つにまとまっているのかなと思います。

という感じで、SOLARISではレイヤーが暗黙的に構築されてサブレイヤーされて出力されていました。

多くの場合はあんまりここまでLayerの構築単位を考える必要はないと思うのですが
これが影響するケースが１つあって

![](https://gyazo.com/0c366c7465cbf386aace7e741f52d1aa.png)

USD ROPでUSDをExportするときに、 SaveStyle を Separate Layers にした場合
出力されるusdの単位が変わります。

このオプションはその名の通り、出力されるUSDファイルを
どういう単位で出力するか..というものになります。

Separate Layers では、SOLARISの ～Layers（↑のLayerStackで確認した単位）で
ファイルが小分けされます。
（作成ファイルは、SdfPathのサブフォルダ下にExportされる？）

もしかしたら他にもこのLayer単位が影響するところがあるかもしれないですが

* SOLARISのノードはサブレイヤー合成
* 特定条件下だとFlatten（１つのLayerに統合）されたりする

というのを理解するだけで、ノードの構築がどのように行われて
結果どういうシーングラフが出てくるのか、理解できるのかなと思います。
（Flattenしてないとうまく行かなかった何かがあった気がしたけど思い出せない...）

## まとめ
こんな感じで、SOLARISでのノード操作のふわっとした理解をしていたところが
だいぶ整理できたおかげで、各種ノードの違いとか意図がつかめるようになってきました。

これをベースに、色々とシーンの構築やらUSD的なオーサリング方法を
色々ねっていきたいです。