---
title: Value Clips を使おう(レイヤー合成編)
tags:
    - USD_APISchema
    - USD
---

[前回](./12_ValueClip_01.md) に引き続きValue Clips周りについて。
今回は、USDのコンポジションが絡んだ場合、複数のClipが絡んだ場合など
レイヤーを合成する処理関連をまとめていきます。

## Value Clips の強さ

USDのコンポジションは、 LIVRPSの原則にあるとおり
決められたルールに従って解決されます。
では、Value Clipsを使用した場合はどうなるかというと、L（Local）の次が
Value Clipsになります。

前提として、Value Clips はメタデータとして扱われています。

![](https://gyazo.com/e5c71736b62359a3f097c9d9ea6b3c86.png)

複数のレイヤーにわたってValue Clips の定義がある場合、
そのレイヤーのうち「最も強いレイヤー」が、ValueClipsのメタデータ扱いになります。
そのレイヤーのことを「**アンカーポイント**」と呼びます。

例えば上のように、３つのレイヤーがサブレイヤーで合成されていた場合
Stageとして開いているのが rootLayer.usda だった場合
rootLayer.usda がもっとも強いレイヤーになるので、ここがアンカーポイントになります。
結果、Clips は clipA.#.usda のレイヤーが読み込まれる...ということになります。
このClipsの部分の解決に関しては、通常のコンポジションアークと変わらないということになります。

あとは、このValue Clipsによって解決された値は
そのClipsが指定されているレイヤーのローカルにオピニオン（定義）がなければ
Clipsの値が使用されます。

これだけだとわかりにくいのでシンプルな例で見てみます。

![](https://gyazo.com/fbed5687ad65f30efd4da1591f8a6b1b.png)

まずはこんなClipレイヤーとManifestを用意します。

```
#usda 1.0
def "ModelA"
{
    double a.timeSamples = {
        1: 1
    }
}
```

```
#usda 1.0
def "ModelB"
{
    double a.timeSamples = {
        1: 1000
    }
}
```

それぞれのレイヤーには、doubleのtimeSamplesをもつアトリビュートを定義します。
どちらが使われてるかわかるように値やPrimを変えておきます。

Clipを指定するレイヤーはこちら。
```
#usda 1.0
(
    endTimeCode = 4
    startTimeCode = 1
    subLayers = [@./result_subLayerB.usda@]
)

def "TestModel" (
    clips = {
        dictionary default = {
            asset manifestAssetPath = @D:/work/py37/USD/clip/A/manifest_sample.usda@
            string primPath = "/ModelA"
            string templateAssetPath = "d:/work/py37/USD/clip/A/clip.#.usda"
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

result_subLayerB.usdaは、
```
#usda 1.0
(
    endTimeCode = 4
    startTimeCode = 1
)

def "TestModel" (
    clips = {
        dictionary default = {
            asset manifestAssetPath = @D:/work/py37/USD/clip/B/manifest_sample.usda@
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
こんなかんじ。
大体同じですが、Clipの読み先だけ異なります。

![](https://gyazo.com/7d038d51bf6b1691146ba7e57e9386c1.png)

コンポジション結果。
この場合一番強いレイヤーは result_subLayer.usda となります。

![](https://gyazo.com/97ccceba86a82140ed25a60b6bfd050a.png)

結果。
サブレイヤーで合成したレイヤーのうち、一番強いレイヤーにある clips が
使われているのがわかります。

```
#usda 1.0
(
    endTimeCode = 4
    startTimeCode = 1
    subLayers = [@./result_subLayerB.usda@]
)

def "TestModel" (
    clips = {
        dictionary default = {
            asset manifestAssetPath = @D:/work/py37/USD/clip/A/manifest_sample.usda@
            string primPath = "/ModelA"
            string templateAssetPath = "d:/work/py37/USD/clip/A/clip.#.usda"
            double templateEndTime = 4
            double templateStartTime = 1
            double templateStride = 1
        }
    }
)
{
    double a = 9999 # <- 値を入れる
}
```

ではそのレイヤーの a のローカルで値をセットするようにしてみるとどうなるか。

![](https://gyazo.com/7a3d1d4d7cd7a667a122a0f9983eb613.png)

Clipが指定されていても、ローカルで定義されている値が最も強いので
Clipは無効になり、ローカルの値になります。

こんなかんじで、コンポジションが絡んできた場合も、基本は同じで
複数レイヤーがコンポジションアークのルールに則って合成
その合成結果で、最も強いレイヤーのClipsが使用されるが
ローカルの定義があればそちらが最優先で使用される...ということになります。

## 複数Clipの合成

最後にClipがあった場合の合成について。
Clipsの定義は上に書いてあるようコンポジションによって最も強い値が使われますが
どのClipを適応するかは複数持たせることができます。
それがClipSetです。

こちらもかんたんなサンプルでみてみます。

```
#usda 1.0
def "ModelB"
{
    double b.timeSamples = {
        1: 1000
    }
}
```
B/clip.#.usda のほうは、 double b の timeSamples をもつようにします。

```
#usda 1.0

over "ModelB"
{
    double b
}
```
Manifestも更新。

```
#usda 1.0
(
    endTimeCode = 4
    startTimeCode = 1
)

def "TestModel" (
    clips = {
        dictionary A = {
            asset manifestAssetPath = @d:/work/py37/USD/clip/A/manifest_sample.usda@
            string primPath = "/ModelA"
            string templateAssetPath = "d:/work/py37/USD/clip/A/clip.#.usda"
            double templateEndTime = 4
            double templateStartTime = 1
            double templateStride = 1
        }
        dictionary B = {
            asset manifestAssetPath = @d:/work/py37/USD/clip/B/manifest_sample.usda@
            string primPath = "/ModelB"
            string templateAssetPath = "d:/work/py37/USD/clip/B/clip.#.usda"
            double templateEndTime = 4
            double templateStartTime = 1
            double templateStride = 1
        }
    }
    prepend clipSets = ["A", "B"]
)
{
    double a
    double b
}
```

Clipsを追加するPrimには、複数のClipsを読むようにします。
そして clipSets = [] で、 clips にあるValueClipのうち
適応したいClipを clipSets に追加します。

![](https://gyazo.com/45639c034c7ffe711d63e231b8e3003e.png)

結果。
１つのPrimに対して複数のValueClipを指定することができました。
clipSets は List Editing なので、レイヤー合成でも追加・削除などができる（はず）です。

この clipSetを使えば、細かく出力しておいたClipレイヤーを
組み合わせて１つのステージに組み立てることができます。
Crowdなどのシーン構築などでは、この仕組を使うことでかなり柔軟な対応ができそうです。

## Pythonでの操作方法

このValueClip周りをPythonで扱いたい場合どうしたらいいのか？というと
UsdClipsAPIという、ValueClipsを扱うためのAPIが用意されています。

https://fereria.github.io/reincarnation_tech/60_JupyterNotebook/USD/CompArc/variantset01/
https://fereria.github.io/reincarnation_tech/60_JupyterNotebook/USD/CompArc/variantset02/

使用方法は、JupyterNotebookを使用してテストしたものがのこってるので
こちらを参考にしてください。

## まとめ

以上２回にわけてみてきたValueClipですが
今までのコンポジションの仕組み加えて、この機能を使うことで
アニメーションを使う場合などに、より柔軟なシーン構築ができそう...というのがわかりました。

ValueClipを使うと、アニメーションレイヤーの管理方法・コントロール方法の幅が広がりそうで、
どうやったらより効率的にシーンを扱えるか夢が広がります。

## おまけ

![](https://gyazo.com/93557c89717cb1bb2e09cc0504f764dc.png)

調べてて気がついたのが、HoudiniSOLARISにはちゃんとVlaue Clipノードが存在していて
この機能がすでに使えました（すごい）