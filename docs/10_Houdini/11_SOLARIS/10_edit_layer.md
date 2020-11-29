---
title: editLayerを使おう
---

SOLARISでUSDの構造を作るときに、「どこをどのように分けて構築するか」
というのはとても重要なことです。
なのですが、ぱっと見てどのように制御するのかがとてもわかりにくかったので
手順とかをまとめてみようと思います。

## SOLARISでのレイヤー表示

![](https://gyazo.com/dc651ee92c221b0a7f21e61f6be7f477.png)

SOLARIS上でのレイヤーがどのように切り分けられているかというと、
ノードの縁の色単位で表示がわかるようになっています。
上の画像の場合は、 assetName と payload1 が同じレイヤー
cube2 が別のレイヤーとして作成されます。

## レイヤーを編集する

ここでいうところの「レイヤー」というのは、いわゆる USD のファイルのことです。
つまり現状だと assetName Prim と cube2 Primそれぞれが存在する USD ファイルが
あることになります。

ただし、とくに何もしていない場合このレイヤーは「Anonymousレイヤー」という
オンメモリー上にのみ存在するレイヤー扱いになり、

![](https://gyazo.com/a00b2a9ce07abe64073f06dbcaf05a83.png)

途中コンポジションされているCube2のPrimレイヤーがオンメモリー上にしか存在しない
レイヤーになってしまうので、 USDROP ノードでExportすると
エラーアイコンが表示されてしまいます。

!!! info
    このあたりの問題は、
    http://ikatnek.blogspot.com/2020/06/usd-rop.html
    こちらに詳細が書かれています
    

なので、各レイヤーの構造を維持したまま（Flattenしないで）
レイヤーワケした状態でExportしたい場合は、 **ConfigureLayer** ノードを
利用して、レイヤー設定を追加します。

![](https://gyazo.com/133158975ece65dce7009829abe258e8.png)

結果がこちら。
Cubeは cube.usda メイン部分は payload.usda という形で出力され、

```usda
#usda 1.0
(
    endTimeCode = 1
    framesPerSecond = 24
    metersPerUnit = 1
    startTimeCode = 1
    timeCodesPerSecond = 24
    upAxis = "Y"
)

def Xform "assetName"
{
    def Xform "model" (
        prepend payload = @./cube.usda@
    )
    {
    }
}
```
cubeをペイロードしたusdaが出力されます。

つまり、 ConfigureLayerノードは
接続されたレイヤーに対して設定を変更する事ができるノードというわけですね。

![](https://gyazo.com/59f4bdadd3fdbb13b60a357b18f50bc5.png)

例えばCube側のConfigureLayerをみてみます。
SavePathはそのレイヤーをどこに保存するのか、DefaultPrimitiveはレイヤーの
デフォルトPrimをなににするかの設定です。

```usda
#usda 1.0
(
    defaultPrim = "cube2"
    framesPerSecond = 24
    metersPerUnit = 1
    timeCodesPerSecond = 24
    upAxis = "Y"
)

def Cube "cube2"
{
    float3[] extent = [(-1, -1, -1), (1, 1, 1)]
    double size = 2
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]
}
```
その結果出力されるレイヤー。
defaultPrimとして cube2 が指定されていることがわかります。

![](https://gyazo.com/f4b53179ff274c7c575b990cb93df9f5.png)

Configure LayerでDefaultPrimが指定されているので、
Payloadノードの Reference Primitive で「 Reference Dfault Primitive 」を指定して
ペイロードすることができます。

![](https://gyazo.com/a5f58dcd2c544a14b22d99622acd630e.png)

他の設定も色々いれてみると

```
#usda 1.0
(
    "Hello World"
    customLayerData = {
        string testCustomData = "Test Test!!"
    }
    defaultPrim = "cube2"
    endTimeCode = 240
    framesPerSecond = 24
    metersPerUnit = 1
    startTimeCode = 1
    timeCodesPerSecond = 24
    upAxis = "Y"
)
```
色々仕込むことができました。

## 編集部分だけ別レイヤー出力

ConfigureLayerを使用すると、指定の部分のレイヤーの出力パスを編集し
レイヤーに対してメタデータを仕込んだりできることができました。
次は、編集した部分のみを別ファイルとして切り出してコンポジションしてみます。

![](https://gyazo.com/fb9e94f346414d2a26fe4e145c0b8229.png)

全体図がこんな感じになります。
Cubeを動かして、動かした部分だけを別レイヤー化して
そのファイルをペイロードでロードします。

なので、
1. モデル部分（cube1）
2. Edit部分
それぞれをレイヤーとして保存するために、ConfigureLayerノードで
出力先などのレイヤー設定を追加します。

そしてそのレイヤーをペイロードに入れて USD_ROPでExportします。

ここでの注目ポイントは「layerBreak」ノードです。

このlayerBreakノードは、Inputから入力されたStageをUSDROPなどでExportするときのみ
Exportしないようにするノードです。

なので

![](https://gyazo.com/c1faa54fab8f2701ed25d451b368a0ae.png)

こんなかんじにモデルをInputして編集するときに、layerBreakを使用すると
InputのMesh情報はレイヤーには保存されず、編集情報のみが

```usda
over "cube1"
{
    matrix4d xformOp:transform:edit1 = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 5, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform", "xformOp:transform:edit1"]
}
```

over でレイヤーに保存されます。

![](https://gyazo.com/8960a7f8948b3c80d762391fd891c28f.png)

このlayerBreakがないと、編集対象がEditノードにないためすべてエラーになってしまいます。

### Variant Blockの場合

更に別のコンポジションを追加してみます。
HoudiniのVariantにはVariantBlockという、すでにあるPrimに対して over で
Varinatを作れる機能があります。

詳細は [こちら](08_solaris_variant.md) に書いてあります。

これをSOLARIS上でコンポジションしつつ、サブレイヤーでも合成してみます。

![](https://gyazo.com/76fd012882c2808c6467975319770fc0.png)

といっても、基本的な方針は同じです。
BaseModel（モデルの実体部分）のレイヤー、Variant部分のレイヤー、その後に最後に
別途編集したい場合。
Variant側はVariant Block自体が layerBreakを使用したのと同じ状態になっています。
なので、そちらはlayerBreakなしでレイヤーを構築してConfigureします。
それだけだと、BaseModelにVariantが合成されないので、Merge（サブレイヤー）で
合成します。

そのあとに別レイヤーで指定のマテリアルを編集したい場合は、layerBreakして編集して
configureLayerしてレイヤーを出力
その結果をサブレイヤー合成して出力します。

上２つのみで基本モデル、別途バージョン違いだったりカットごとの微調整なんかの
パターンの場合は EditMaterial部分のような構造にしておくと
1レイヤーあたりのファイルサイズが少なく（差分のみ保持）されます。

サンプルは :fa-download:[こちら](https://1drv.ms/u/s!AlUBmJYsMwMhhOZo1uxWpX05TZZQsA?e=thiZbi)

## まとめ

HoudiniのノードとUSDのシーングラフ構築がいまいち結びつかなくて
なかなか意図した構造を作ることができませんでしたが、レイヤーの構造と
Configure系ノードの使い方を理解したおかげで
狙った構造が組めるようになりました。

ので、組み方ははわかったので実際のところどうやると良さそうなのかを
次は考えてみようと思います（2020年アドカレネタ）