---
title: SOLARISでコンポジションアーク
---

# SOLARISでコンポジションアーク

前回で、SOLARISの中でUSDファイルを開いてみましたが  
今回からノードを使って具体的なUSDオーサリングをやっていこうと思います。  
  
## コンポジションアーク

まず、やり方に行く前に「コンポジションアーク」についておさらい。  
  
コンポジションアークとは、レイヤーを「プロシージャルに合成」していく時の  
合成ルールのことです。  
  
USDは、複数のファイルを合成して結果シーングラフを作りますが  
合成するときに「どうやって合成する？」というルールがなければ  
プロシージャルに合成するできません。  
  
そのときのルールがこの「コンポジションアーク」であり、

* サブレイヤー
* バリアント
* リファレンス
* 継承
* ペイロード
* 特殊化

この6種類が存在します。  
  
詳しくは、  
  
https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/05_comp_arc  
  
こちらで解説しています。  
  
では、このコンポジションアークがSOLARIS上でどう扱うかを見ていきたいと思います。  
  
### サブレイヤー

まず、最初はサブレイヤー。  
SOLARISではすべてのノードはUSDのレイヤーなのですが  
そのレイヤーをつなげた場合の多くはこのサブレイヤーで合成されます。  
  
![](https://gyazo.com/0c7d1aa903918adb1356646f2d7ca9bd.png)

まずは単純なノードで見てみます。  

![](https://gyazo.com/6cf48172d70f2f02679e6a26d5301802.png)

SubLayerノードは、Input1とそれ以外のMultiInputをつけつけています。  

![](https://gyazo.com/383eb4237bdb8aba0021e0a16aa15c02.png)

今のLayer状況を「Scene Graph Layers Panel」で確認すると、  
Input1の入力の子としてMultiInputのLayerがついているような構造になっています。

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

USDのSubLayerをUSDAファイルで記述するとこうなります。  
このファイルをノードで表すと、  
ファイル自身がInput1で、subLayersでセットしているusdaファイルがMultiInputの入力になります。
  
![](https://gyazo.com/c04d6f005b208c3ce07aa3af4af9c710.png)

ただし、このレイヤーの解決順序はUSDの公式の順序ではなく  
「Sublayer Position」で指定されたものを SubLayerの位置として認識します。  
デフォルトの場合は、「Strongest Layer」になっていて  
一番強いノード（この場合最後の入力である SPHERE）が出力されます。  
  
通常のUSDと同じにしようとした場合「Strongest File Layer's Position」で  
RootLayerのLocal（RootLayerに記載されているPrim）が優先されるのがデフォルトのUSD解決順序な気がします。  
  

![](https://gyazo.com/04d3363de97ef7c8cc8920e68f6eccfc.png)

このSubLayer時の優先順序（どの順番で合成されているのか）は、Scene Graph Detailの「レイヤースタック」で  
確認することが出来ます。  
  
レイヤースタックとは、すべてのサブレイヤーを集めたものです。
レイヤーのPrimitiveや各種プロパティ・アトリビュートの値はレイヤースタックに積まれた順  
（上のスクショの例だと、上のほうが強い）で上書きされていきます。  
シーングラフを構築するときに、どのようにそれぞれのレイヤーが「解決しているか」は  
このレイヤースタックを確認することでわかります。
  
#### サブレイヤーのアウトプット  
  
このSubLayerのアウトプットでなにを返すかというと
  
![](https://gyazo.com/17741f4878320e971ccb48891e4157da.png)

確認するには lopinputprims 関数を使用すればわかります。  
  
![](https://gyazo.com/80ecd2d49c9f26dcb6431a758f3642bb.png)

Collectionノードで確認してみると、「BasePrim」つまりは、Input1に入力されているPrimitiveが  
編集されたPrimitiveとして取得されることが分かります。  
  
あくまでも取得出来るのは「編集しているRootLayer」であり、  
合成側のレイヤー（MultiInputに入力されている物）は含まないというのが注意する点です。  
入力のPrimitiveを使用して、次のノードで何かをしたい場合（ lopinputprimsで取得する場合）  
合成した結果すべてを得られるわけではありません。  
  
なお、この出力されるPrimitiveは Sublayer Position を変更しても変わらずInput1のPrimitiveが帰ってきます。
  
![](https://gyazo.com/de942a02f5065a37feb04f13a41d108b.png)

似た挙動をするノードとして「Merge」がありますが  
こちらはSubLayerとは違い、入力したノードを並列で扱い合成し  
結果できたレイヤーを返します。  
なので、 lopinputprims で次のノードで取得した場合  
すべてのPrimitiveを取得することができます。  

![](https://gyazo.com/13ced403b9f124cac98bbe72c14e8307.png)

### SubLayerとMergeの違い

SubLayerとMergeは挙動がほぼ同じで、結果のシーングラフも同じです。  
ですが、上に書いたとおり結果出力されるノードなどに違いがあります。  
それが確認できるのが「Scene Graph Layers Panel」です。  

![](https://gyazo.com/a6a5cdb5f6bac4a6bb5d44523844c08d.png)

まずは、SubLayerのレイヤー構造。  
レイヤーの構造は、Input1 のレイヤーの子にMultiInputのノードが存在する状態です。

![](https://gyazo.com/c9370ffaacadc4ee2a6c66bfd9244449.png)

つぎにMergeを見てみると、  
レイヤー構造は親子ではなく「並列」に扱われています。  
  
#### Layer Flatten

サブレイヤーで合成されている各種レイヤーは ～ Layers　という形でノードの右下に表示されています。  
  
![](https://gyazo.com/1c0c0fef51af49f048fa627789ebed82.png)

このLayersの数は、SceneGraphLayersPanelの「Implicit」になっているレイヤーの数です。  
この複数のレイヤーを「1つに結合」するのが LayerFlatten です。  
  
![](https://gyazo.com/f5122a6a03831d13500b2625f90f78aa.png)

ConfigureLayersノードの「FlatetenInput」を

![](https://gyazo.com/551e1df32b0baac4205472acf0b3347a.png)

 Flatten Input Layers に切り替えると、
 
 ![](https://gyazo.com/6e2cedd9ba4d53054a7058431d03c275.png)
 
 レイヤーは1つに統合されます。  
 PhotoShopのレイヤー統合、あるいはAEのプリコンポーズのような処理で  
 各レイヤーをサブレイヤーで合成していった場合の結果を制御できるようにしてあります。  
   
USDをSOLARISではなくそのまま使っていると問題になってくるのが、レイヤーのコンポジションの解決順序です。  
   
 https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/05_comp_arc/  
   
 USDの解決順序は上のページの通りですが  
 SOLARISでは要所要所のノードでFlatten、あるいはノードの接続順によるプロシージャルな解決制御  
 をできるようにしているように感じました。  
  
