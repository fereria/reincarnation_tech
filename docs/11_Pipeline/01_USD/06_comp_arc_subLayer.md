---
title: CompArc(1) サブレイヤー
tags:
    - コンポジションアーク
    - USD
    - USD基本
---

# CompArc(1) サブレイヤー

前回ざっくりと個々のコンポジションアークの概要をしたので  
これからは個々のコンポジションについての動作を説明していきたいと思います。  
  
まず第一回は「サブレイヤー」について。  
  
## サブレイヤーとは  
  
サブレイヤーとは、プログラム言語的に言えば「Import」や「Include」  
DCCツール的に言えばシーンのインポートに近い処理です。  
  
![](https://gyazo.com/76645304065930109d3b22a64b46ac43.png)
  
図で表すとこのような処理になります。  
各レイヤーごとのノードツリーの階層構造を維持しつつ  
同階層がある場合はいいかんじに階層を維持しつつ  
レイヤーをまるごとマージしていきます。
  
### ルートレイヤーとは

まず個々で新しく「RootLayer」と呼ばれる概念が出てきました。  
これは、ざっくり言うと「現在開いているUSDファイル」がRootLayerとなります。  
  
サブレイヤーの評価は、RootLayer　つまりは現在開いたレイヤーから見て  
一番遠いレイヤーから上書きして行きます。  
  
![](https://gyazo.com/a3e2e76893dcdc9304cce43ed48ef32c.png)

散々参考にだしているこの図で言うと  
  
![](https://gyazo.com/23e95829508d5bd23d4703627324f838.png)


[サンプルのUSDはこちら](https://1drv.ms/u/s!AlUBmJYsMwMhhNRt4KxBpMYIPL8SdQ?e=mA179E)

![](https://gyazo.com/910f45d935ff0960a1e072d7c67608ec.png)

まず base.usda を usdview で開いてみると緑の玉が出てきます。  
  
```
#usda 1.0
def "Model"
{
    def Sphere "Sphere"
    {
        rel material:binding = </Material/MyMat>
    }
}
def "Material"
{
    def Material "MyMat"
    {
        token outputs:surface.connect = </Material/MyMat/testShader.outputs:surface>

        def Shader "testShader"
        {
            uniform token info:id = "UsdPreviewSurface"
            color3f inputs:diffuseColor = (0, 1, 0)
            float inputs:metalic = 0.9
            float inputs:roughness = 0.2
            token outputs:surface
        }
    }
}
```
usda の中身はこんな感じ。  
  
次に add_color.usda を開いてみると

![](https://gyazo.com/463b153a50480a4f59c534e7233e3e98.png)

見た目はこのように「赤いSphere」が出ています。  
usdaを開いてみると

```
#usda 1.0
(
    subLayers = [
        @base.usda@
    ]
)

over "Material"
{
    over "MyMat"
    {
        over "testShader"
        {
            color3f inputs:diffuseColor = (1, 0, 0)
        }
    }
}
```
こうなっています。  
このフォーマットを見てみると、  
上の base.usda に対して testShader にある inputs:diffuseColor = (1,0,0) だけが書かれ  
かつレイヤーのメタデータ内に subLayers がある事が分かります。  

!!! info
    プリムの定義部分は、他では def ～～～ になっていましたが  
    このファイルの場合 over になっています。  
    これは、サブレイヤー時に「もし定義がなければプリムを作らず、あったら上書き」  
    という定義になります。  
    なのでこの例の場合、「マテリアルの定義がすでにあったら、diffuseColorを赤にする」  
    という意味になります。
  
繰り返しになりますが、USDの特徴はコンポジションをしてシーンを構築していくことにあります。  
それはどういうことかというと  
各USDは「他のレイヤーとの差分を、それぞれ保持」しているという事です。  
  
サブレイヤーに限らず、コンポジションアークでレイヤーを合成するときには  
この差分情報を評価し、最終的なステージのシーングラフを構築します。  

![](https://gyazo.com/130909b25755df7bd5a9dfd471985a83.png)

なので、最後の final.usda を開いたときにこのようなCubeが出てきますが

```
#usda 1.0
(
    subLayers = [
        @add_color.usda@
    ]
)

over "Model"
{
    def Cube "Sphere"
    {
    }
}
```

マテリアルの色情報や構造は base.usda + add_color.usda の情報が来ていますが  
最後の final.usda で、形状の Sphereプリムを Cubeにオーバーライドしているので  
形状がCubeに変化しつつも  
差分情報以外はサブレイヤーの情報が引き継がれていることが分かります。  
  
## 評価順序とレイヤースタック

それぞれのレイヤーが差分情報を持ち、オーバーライドされていくのはわかりましたが  
では、このレイヤー結合はどのような優先順位で評価されるのでしょうか。  
サンプルシーンで試してみます。  
  
```
#usda 1.0
(
    subLayers = [
        @subA.usda@,
        @subB.usda@
    ]
)

def "testPrim"
{
}
```

まずこんなファイルを作り、

```
#usda 1.0

def "testPrim"
{
    string hoge = "subA"
}
```

サブレイヤーで読んでいるusda中身は、こんな感じのファイル名のはいった  
アトリビュートを入れておきます。  
  
![](https://gyazo.com/78b8685417417a112dbe35c79a5720c2.png)

usdviewでみてみると、 hoge = subA なので  
1つのレイヤーで subLayers をいれた場合は、配列の0番側が優先的に評価されるようです。  
  
では、コレがどうなっているのかを usdview を使用して確認してみます。  
  
![](https://gyazo.com/6af09a7330f3897d94fccd4cd7d0e0a7.png)

確認したいプリムをクリックし、右下の「Layer Stack」タブをみてみます。  
すると、現在選択中のプリムを合成するのに評価されたレイヤーが表示されます。  
  
この「レイヤースタック」とはなにかというと  
今回のように複数のレイヤーを結合していった際に使用したすべてのレイヤーをまとめた物  
の事を指します。  
  
それを踏まえてもうすこし複雑にしてみます。  
  
```
#usda 1.0

(
    subLayers = [
        @subC.usda@,
        @subD.usda@
    ]
)

def "testPrim"
{
    
}
```

subA.usdaをこのように書き換えて 同じような構造のCとDを作ります。  
  
![](https://gyazo.com/dcaa4e96d204e633af6e02bdbc686bdc.png)

関係図を書くとこうなります。  
  
この結果を確認するとどうなるかというと  
  
![](https://gyazo.com/5876c5be5779659131fa58553c86a9cf.png)

Cが読み込まれました。  
  
![](https://gyazo.com/2dfae0667c59f20000c5e1c1ee474626.png)

レイヤースタックを確認すると、こうなっています。  
なんとなくわかってきましたが、ちょっと不確定な部分があるので  
  
![](https://gyazo.com/bc2905753b760c9de9f5a076fdf6cf1c.png)  

もうちょっとサブレイヤーの階層を増やしてみます。  
  
![](https://gyazo.com/c31db70e3f2fa861ea44bd7e31342b64.png)

その結果のレイヤースタック。  

![](https://gyazo.com/66cc031572a1113e6bd08c64bf4b2b86.png)

見て分かるとおり、末端部分から深さ優先(DFS PostOrder？)で帰的に呼ばれているのが分かります。  
  
まとめると、サブレイヤーはルートレイヤーからサブレイヤーで指定された各レイヤーを  
再帰的に上書き結合して、1つのレイヤーにする処理のことで、  
その各サブレイヤーをまとめたものを「レイヤースタック」  
と呼びます。  
  
## LIVRPS原則の「Local」

[前回のコンポジションアークの説明](05_comp_arc.md)の説明でふれた各レイヤーの合成原則の時に、  
この中に「サブレイヤー」が含まれていないことに気づくかと思います。  
  
実は、この中の「L」とはレイヤースタックに積まれたレイヤーの結合結果  
を「Local」と言います。  
つまり、サブレイヤーで重ねた状態というのは  
他のコンポジションアークの要素と比較して、最も強い主張を持っていて  
構造のベース部分になるものと言えます。  
このサブレイヤー自体もツリー構造を持ちますが  
上に書いたように再帰的に（一定のルールで）合成され、  
最終的に1つのレイヤーに結合される形になります。  
  
というわけでサブレイヤーはこのくらい。  
次は原則順にそって Inherits(継承) について説明していきたいと思います。