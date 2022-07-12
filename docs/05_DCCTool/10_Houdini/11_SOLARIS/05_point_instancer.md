---
title: SOLARISでInstancerを使う(1) 配置編
tags:
    - USD
    - SOLARIS
    - Houdini
---

SOLARISのメニューには、
![](https://gyazo.com/bec22aba78ff3f49b3a60ac54e3cefbc.png)
Insatncingというカテゴリが存在している通り、SOLARISでのレイアウトでの  
Instanceというのはかなり重要な要素になってきます。

というわけで、今回はInstancer周りの構造の使い方とかが  
だいぶわかってきたのでまとめをば。

## Instanceとは

SOLARISでのInstanceとは、
> たくさんの"同じ"オブジェクトのインスタンスが
> UsdStage上で同じ表現(合成したPrim)を共有することができる機能のことです
> ([USD docs 日本語訳版より](https://usd.prisms.xyz/intro/USD-Glossary.html#id74))

とあるように、ある共通のPrimを参照・共有化して表示する機能のことです。

SOLARISではこのInstanceの機能で、HoudiniのPointsに対してInstance Objectsを作成
することができます。

## 基本構造

まずは基本的な構造から。

![](https://gyazo.com/39ad6d46f48153389f27e61b690955ad.png)

まずはPointsに配置したいPrimを用意します。  
そして、AddPointInstancerノードを作ります。  

今回のサンプルの場合だと Sphere と Cubeの２つを用意します。
そしてそれをMergeして
AddPointInstancerのInput2に接続します。

次にSOPネットワークで、オブジェクトを配置したいPointsを作成します。

![](https://gyazo.com/07089c4b932168789b4e8441be87f04b.png)

今回は、 Primitive TypeをPointsにしたGridを用意しておきます。

![](https://gyazo.com/f094c4fea202579377382e54b9938cd6.png)

最後に、AddPointInstancerノードの Target Points の SOP Path に  
先程作った配置用Pointsを指定して、

![](https://gyazo.com/60526128426e37509c88ad943b9a3b55.png)

配置したいPrim(Prototypesと呼ぶ）を指定するために
Prototype Source を Second Input にして、 Use Entire Stageをはずします。

![](https://gyazo.com/5480a55f656634d47d29b47fbfd36bf4.png)

そうすると、GridのPointsに対してオブジェクトがランダムに配置されます。

![](https://gyazo.com/78a480da0eed77f3cff738b5fd868e0b.png)

できあがったシーングラフがこちら。
Second Inputsに入力したオブジェクトは Prototypes スコープ下に配置され  
PointInstancerPrimが作成されます。

PointInstancerの特徴は

```
#sdf 1.4.32

def HoudiniLayerInfo "HoudiniLayerInfo" (
    customData = {
        string HoudiniCreatorNode = "/stage/addpointinstancer1"
        string[] HoudiniEditorNodes = ["/stage/addpointinstancer1"]
    }
)
{
}

def PointInstancer "addpointinstancer1"
{
    int64[] invisibleIds = []
    quath[] orientations = [(1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0)]
    point3f[] positions = [(-15, 0, -15), (0, 0, -15), (15, 0, -15), (-15, 0, 0), (0, 0, 0), (15, 0, 0), (-15, 0, 15), (0, 0, 15), (15, 0, 15)]
    int[] protoIndices = [0, 1, 0, 1, 1, 1, 1, 0, 1]
    rel prototypes = [
        </addpointinstancer1/Prototypes/cube1>,
        </addpointinstancer1/Prototypes/sphere1>,
    ]

    def Scope "Prototypes" (
        customData = {
            token HoudiniSourceNode = "/stage/merge1"
        }
    )
    {
        def Sphere "sphere1" (
            customData = {
                int HoudiniPrimEditorNodeId = 194
            }
        )
        {
            double radius = 1
            matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
            uniform token[] xformOpOrder = ["xformOp:transform"]
        }

        def Cube "cube1" (
            customData = {
                int HoudiniPrimEditorNodeId = 195
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

出来上がったUSDファイルを見るとわかりやすいですが、  
Prototypeとなる（生成元になっている）Primがあるけれども
実際に配置されているオブジェクトは生成されず、PointInstancerノードのPositionとOrientation、そして
PrototypesへのIndexが保持されたじょうたいになっています。

で、これの何が良いかというと尋常じゃないぐらい軽く、数万どころか数百万の
オブジェクトにすら耐えられたり（Houdiniだとさすがにきつかった）
ビューポート上での表示も非常に軽く、大量のオブジェクトをばらまいてシーンを構成するときには
非常に効果を発揮します。

追記メモ
https://graphics.pixar.com/usd/docs/api/class_usd_geom_point_instancer.html#details
> The PointInstancer schema is designed to scale to billions of instances

らしいので、数百万インスタンスどころではなかった。

## PointInstancerとCopyToPoint

このPointInstancerと似た機能というかほぼ同じような結果になるノードが「CopyToPoint」ノードです。
CopyToPointノードの指定方法やノードネットワークのつなぎ方はAddPointInstancerとほぼ共通
になりますが、結果できあがるシーングラフは大きく異なります。

![](https://gyazo.com/b70214e134e5e01b28b555d107a692cb.png)

上の例だと、PointInstancerノードが出来上がっただけでしたが
CopyToPointの場合は、実際のPrimが生成されます。

![](https://gyazo.com/dc1a73a154dd20229f5d6dfa5b512ee6.png)

Use Entire Stageがオンの場合は PrototypesのPrimがInstanceとして各Pointに生成され

![](https://gyazo.com/543562d3a787551b21092371b9e0d4d1.png)

こんな感じですべてのPrimが配置されるし、

Use Entire Stage がオフの場合は

![](https://gyazo.com/e47e2bcce78f42e193a63914bb022838.png)

PointInstancerと同じように、ランダムでPrimが配置されますが  
Prototypes以下にあるPrimをリファレンスで配置した状態になります。

PointInstancerと違い、実際にPrimが作られるので表示は遅いものの  
各Primに対しての編集・加工はやりやすいというメリットがあります。  

使い分けとしては、草とか石ころとかのようなランダムに大量にばらまきたいものは  
AddPointInstancerで配置して、街灯とか信号とかのような  
配置系アセットはCopyToPointを使う...というような使い方をするのが良さそうです。

## Prototypesオブジェクトのコントロール

基本的な例の場合は、MergeしたオブジェクトをInput2で渡す...といった方法で  
セットしていました。

これでもまぁ良さそうですが、他のやり方も確認してみます。

### Input1でわたすかInput2で渡すか

そもそも、上で「Input2につないでわたす」と書いたのですが  
![](https://gyazo.com/c4e43ab58672abf2bfed55e747326286.png)
何故に2つ方法があるのでしょうか。  

![](https://gyazo.com/d9a7935e87bf8ac857325f87e2f1ce62.png)

単純にInput1にしてみても「No prototype primitives found.」になってしまい  
エラーになってしまいます。

と、エラーを見ればそのとおりですが  
Input1につないだ場合は、Prototypesへのノードの移動は行われず  

![](https://gyazo.com/2ec0f29d8499b34e029cd992374663b8.png)

Prototype Primitives での指定が lopinputprims ではNGになってしまう模様。

つまりは、Input1で渡す場合は、入力で与えられたPrimではなく  
別の手段で明示的に（Stageの「どれか」）を指定する必要がありました。

これに限らずですが、SOLARISのノードのInput1はそれまでの段階で編集された  
Stageをつなぐことが多く、このAddPointInstancerも  
Input1はStageを受け取るものとして動作しているからっぽいです。  
対してInput2はPrototypesを渡すための口として働くので、InputのPrimをScopeに移動して  
すべてPrototypesとして動作させる...という意図なのかなと思います。

つーわけで、明示的に指定してみます。
書き方は公式のHelp内の [プリミティブマッチングパターン](http://www.sidefx.com/ja/docs/houdini/solaris/pattern.html)に記載されています。

### 名前で入れる

![](https://gyazo.com/df8f854c39980b234a5bf0d09f01ee12.png)

まずは単純な例として。  
こんな感じで特定の名前でPrimを作り、graftノードでまとめておきます。
![](https://gyazo.com/8c71b57ee13f27220886ad2c4b909c08.png)
こんな感じ。

![](https://gyazo.com/053e791472343579fe4b984bb1d5486f.png)

そして、名前でマッチするように Prototype Primitivesを指定します。
インスタンスはこれで作ることができますが

![](https://gyazo.com/f89f9ae44198be49be0a343b5945988a.png)

こんな感じで指定したPrimは移動されずその場にのこり、  
AddPointInstancerの下のPrimは、元になったPrimをリファレンスで読み込む構造になります。

なので、元のPrimを編集すればInstanceしたオブジェクトも自動で更新されるようになります。

### Collectionで指定する

名前ではなく、特定のCollectionに含まれるPrimを指定する事もできます。  
複雑なネットワークなどで、特定のPrimを入れたい場合や  
他のLayerから読み込んできた（SdfPathが不定な）Primを追加したい場合などでは  
このやり方が良さそうです。

![](https://gyazo.com/07d2bf62d3f10793f6f2d7ce40cc648f.png)

Collectionを使う場合は、 collectionノードを使用して、CollectionにPrimを追加します。

![](https://gyazo.com/aa0566d6f16e545fc927537b1686f6be.png)

そして、作成したCollectionノードで Collection Nameを指定して

![](https://gyazo.com/801d8a4ce60f343e960efafcacd6c176.png)

こんな感じでCollectionNameを指定します。
書き方は、

/PrimitivePath.collection:CollectionName

で、「collection」はお約束でかならず入れます。
公式Docsでは collections となってるのですが、こちらだと正しく動かないので注意が必要です。  
あるいは、
![](https://gyazo.com/3e37de1efd89daa022098136225eea11.png)
％/PrimitivePath/CollectionName でもOKのようです。

こんな感じで、  
1. 元Primを残す or 残さない でInput 1 or 2 を選び
2. Prototype Primitives で配置するPrimを制御して
3. Primを PointInstancerで作るか ReferenceのInstance（実際にPrimを作る）でCopyToPoint AddPointInstancerを使う

ことで、自分のやりたい作業のための大量のオブジェクト配置ができるようになります。

![](https://gyazo.com/be27c5211ca850e4983a14aa4340973c.png)

配置するPrim側メインで書いてますが、
配置するPoint側もコントロールできて、Point GroupをSOP側で指定すると  
配置に使用するPointをコントロールすることができます。

配置PointはSOP内で作成するわけですが  
SOP側での配置オブジェクトのコントロールをPoint Groupで行い  
LOP側はそのGroupでInstancerの制御をする（PointInstancerかReferenceかなど）
...そんな棲み分けになるのかなと思います。

編集周りもやろうと思いましたが長くなったので続きは次回。