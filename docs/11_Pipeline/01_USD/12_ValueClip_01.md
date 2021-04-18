---
title: Value Clips を使おう(基本構造編)
---

USDは、コンポジションアークをりようして、複数のレイヤーから１つのシーングラフを作る
ことができますが、それだけだとあるアトリビュートのTimeSampleされる値は
もっとも強いレイヤーの値になるため、時間方向に複数のレイヤーを合成するといったことが
できません。
（サブレイヤーやリファレンスで、時間のオフセットやスケールはできる）

そういった場合に、より柔軟に対応できるようにする機能が「Value Clip」という機能です。

USDのValue Clipとは、様々なアトリビュートのTimeSampling、つまりはアニメーションを
使用するときに、レイヤーを複数のファイルに分割して
ビデオ編集ツールのように、結合することができます。

これがどういうときに使えるかと言うと、

* Crowd/BackGround 複数のキャラクターに対して適応するClipを作成してシーケンスやサイクルを組んで
  さまざまなパターンを作りたい場合
* １つのフレームが超巨大なデータの場合

などが、[公式のGrossary](https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-ValueClips)で例として挙げられています。

これだけだとよくわからないので、サンプルを確認しながら構造を確認してみます。

## ValueClipの基本構造

ValueClipは、大きく分けると３つの要素で構成されています。
１つがめStage、いわゆるアニメーションをさせたいPrimが存在するレイヤーです。
２つめがClip、これはStageのあるPrimのアトリビュートに対して指定する値を持つレイヤーです。
３つめがManifest、ManifestはあるClipのうち、実際にStageのPrimに対して反映させる
アトリビュートを指定するためのレイヤーです。

![](https://gyazo.com/c2c6abc2935d152d221b15691bca6275.png)

まずはシンプルなCube1つがあるレイヤーを作成します。

```
#usda 1.0
(
    endTimeCode = 30
    startTimeCode = 1
)

def Cube "TestModel" ()
{
    float3 xformOp:rotateXYZ
    uniform token[] xformOpOrder = ["xformOp:rotateXYZ"]
}
```

ValueClipは、TimeSampling いわゆるアニメーションのための機能なので
startTimeCode endTimeCode を指定する必要があります。

今の段階ではなんのアニメーションもありません。
これに対してValueClipを指定します。

まずはClipを作ります。

```
#usda 1.0

def "RotateAnimation"
{
    float3 xformOp:rotateXYZ.timeSamples = {
        0: (0, 0, 0),
        30: (0, 359, 0)
    }
}
```

Primに対して、Rotateするアニメーションが指定されています。

次に、Manifestを作ります。

```
#usda 1.0
def "RotateAnimation"
{
    float3 xformOp:rotateXYZ
}
```

Manifestは、構造的にはClipのレイヤーと構造は同様ですが、
こちらには実際の値は持たず、「TimeSampleしたいアトリビュートのみ」が
記載されています。

Manifestとはなんのために存在しているかというと、
複数のClipを使用して合成したい場合、どのアトリビュートをサンプリングするか
を決めるためには、すべてのClipを参照しなければなりません。
そうではなく、どのアトリビュートをサプリングがどうかを判断するための材料として
使用されます。
ClipにTimeSamplingがあるアトリビュートがあったとしても、
このManifestにアトリビュートがなければ、ValueClipは動きません。
つまりはこのManifestがPrimのうち「どれを実際に使うか」選ぶためのレイヤーとして
機能します。

準備はできたので、
このClipとManifestを使うようにします。

```
#usda 1.0
(
    endTimeCode = 30
    startTimeCode = 1
)

def Cube "TestModel" (
    clips = {
        dictionary default = {
            double2[] active = [(1, 0)]
            asset[] assetPaths = [@d:/work/py37/USD/clip/rotate.usda@]
            asset manifestAssetPath = @d:/work/py37/USD/clip/manifest.usda@
            string primPath = "/RotateAnimation"
        }
    }
){
    float3 xformOp:rotateXYZ
    uniform token[] xformOpOrder = ["xformOp:rotateXYZ"]
}
```

assetPaths というのが、Clipレイヤーのことで、
primPath とは、Clip内のどのPrimをClipの対象にするか？という情報になります。
active は、今のステージのフレーム のときに どのClipを使うのか？という情報です。
この場合は、１フレームから rotate.usda を使う...というふうに書かれています。

ValueClipは、他のコンポジションと違い、メタデータとして書かれているというのも
特徴です。

![](https://gyazo.com/55e35f1bf4f6ceb152d2baf0e04dffdd.gif)

その結果。
Clipのレイヤーにあるアニメーションが、TestModelに適応されたのがわかります。
ですが、これだけだと１つのClipが読み込まれただけなので
普通にコンポジションしたのとあまり違いがありません。

次に、複数のClipを使用してみます。

```
#usda 1.0

def "RotateAnimation"
{
    float3 xformOp:rotateXYZ.timeSamples = {
        0: (0, 0, 0),
        30: (0, 0, 359)
    }
}
```
さっきとは違い、Z軸で回転します。

```
#usda 1.0
(
    endTimeCode = 30
    startTimeCode = 1
)

def Cube "TestModel" (
    clips = {
        dictionary default = {
            double2[] active = [(1, 0),(2, 0),(3, 0),(4, 0),(5, 0),(6, 1),(7,1),(8, 1),(9, 1),(10, 1)]
            asset[] assetPaths = [@d:/work/py37/USD/clip/rotate.usda@,
                                  @d:/work/py37/USD/clip/rotate_2.usda@]
            asset manifestAssetPath = @d:/work/py37/USD/clip/manifest.usda@
            string primPath = "/RotateAnimation"
        }
    }
){
    float3 xformOp:rotateXYZ
    uniform token[] xformOpOrder = ["xformOp:rotateXYZ"]
}
```

Clips を書き換えます。
Z軸回転するレイヤーを assetPaths に追加して、
active で、今のCurrentTimeのときにどのレイヤーを使うかを指定します。
今回は１～5まではY軸回転、6～10がZ軸回転をするレイヤーを読むようにしました。

![](https://gyazo.com/92c305e69fa7fdb7c09c6ff81468a935.gif)

結果。
時間方向に、参照するレイヤー（Clip）が変わっているのがわかるかと思います。

![](https://gyazo.com/6ccb38785e6d5454cc7f1707bc94125f.png)

usdviewをみると、Clipを使用しているアトリビュートのLayer Stackを見ると
Clipのレイヤーが表示されているのがわかります。

![](https://gyazo.com/9db2f01037beae86ba9a0054035c8205.png)

CurrentTimeを移動して再度確認すると、LayerStackのレイヤーも変わっています。

## Template

上の例だと、参照先のClipは、CurrentTimeとassetPathsのIndexによって紐付けされていました。
そうではなく、 clip.#.usda のように、CurrentTimeの(あるいはマッピングされた)数字の
Clipのレイヤーを参照しにいくようにするのがTemplateです。

```usda
#usda 1.0
(
    endTimeCode = 4
    startTimeCode = 1
)

def "TestModel" (
    clips = {
        dictionary B = {
            asset manifestAssetPath = @d:/work/py37/USD/manifest.usda@
            string primPath = "/ModelB"
            string templateAssetPath = "d:/work/py37/USD/clip/B/clip.#.usda"
            double templateEndTime = 4
            double templateStartTime = 1
            double templateStride = 1
        }
    }
)
{
    double a
}

```

Templateの場合でも、ManifestとClipは共通ですが、Clipを読み込むPrimの
構造が変わります。
assetPaths で、配列で指定していたところが templateAssetPath に対して
name.#.usda のように、数字部分を # で書き表したPathで指定し、
そのTemplateのどの範囲をClipとして読み込むかをを startTime,endTimeで
指定します。

このようにすると、CurrentTimeが１なら clip.1.usda のClipを参照...といったような
使い方ができます。
これは、最初にあげられた使用例のうち
巨大なデータを扱う場合などに、全フレームを別レイヤーとして作成したい場合などに
使いやすいのではないかと思います。
## まとめ

というわけで、まずは基本的な構造からみてきましたが
これを使えば、アニメーションのデータをアトリビュート・フレーム単位で
別レイヤーとして作成できるというのがわかりました。

これを使えば、レイヤーの構造の自由度があがる（＝複雑化する）気がしますが
じゃあ他のコンポジションと組み合わさった時にどうなるか
複数のClipを使った場合はどうなるかなど、
より詳しいことはまた次回。