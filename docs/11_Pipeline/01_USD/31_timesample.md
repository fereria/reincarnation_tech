---
title: USDのTimeSampling（Animation）
tags:
    - USD
description: USDのアニメーションの構造
---

[USD AdventCalendar2022](https://qiita.com/advent-calendar/2022/usd)13 日目は、USD の TimeSampling です。

USD は、キャラクターのアニメーションなどは、 {{markdown_link('18_valueclip')}} にもあるようにジオメトリキャッシュを使用しますが
それ以外にもちろんアトリビュートに対してのアニメーションも入れることができます。

このアニメーションは、TimeSampling という形で表現されています。

TimeSample の項目を公式ドキュメントの用語集で確認すると

> TimeSamples as source for Value Resolution
> Each PropertySpec for an Attribute can contain a collection called timeSamples
> that maps TimeCode ordinates to values of the Attribute’s type.
> 引用: https://graphics.pixar.com/usd/release/glossary.html#usdglossary-timesample

Value Resolution と呼ばれる、プロパティやメタデータなどのデータを含む PropertySpecs や PrimSpecs から最終的な値を「合成」すること
に使用されるソースデータであり、
「TimeCode」と呼ばれる時間軸に対応する Attribute の値をマップする形で扱われています。

TimeCode とは、ルートレイヤーに記載された TimeCodesPerSecond（24 フレームや 30 フレームといった情報）メタデータによってスケーリングされます。

が…それだけ言われてもわかりにくいので、シンプルな例をみてみます。

## timeSampling

まずはシンプルなアトリビュートに対して、アニメーションを追加してみます。

```python
stage = Usd.Stage.CreateInMemory()

stage.SetTimeCodesPerSecond(30)
stage.SetStartTimeCode(1)
stage.SetEndTimeCode(30)

prim = stage.DefinePrim("/samplePrim")
attr = prim.CreateAttribute('sampleValue',Sdf.ValueTypeNames.Float)
attr.Set(1,1)
attr.Set(10,10)
```

通常値をセットする場合は attr.Set(value) のようにしますが、TimeSampling を使用する場合
Set の 2 つ目の引数に [UsdTimeCode](https://graphics.pixar.com/usd/release/api/class_usd_time_code.html) を指定します。

```usda
#usda 1.0
(
    endTimeCode = 30
    startTimeCode = 1
    timeCodesPerSecond = 30
)

def "samplePrim"
{
    custom float sampleValue
    float sampleValue.timeSamples = {
        1: 1,
        10: 10,
    }
}
```

アニメーションを使用する場合は、ルートレイヤーに対して、startTimeCode endTimeCode を指定する必要があります。
（これがないと usdview 上でアニメーション再生ができない）
また、フレームレート指定として、 timeCodesPerSecond を設定します。
今回の例だとフレームレートを 30 に指定しています。

指定した場合、timeSamples に対して、 timecode:value という辞書型が指定されます。

![](https://gyazo.com/164f1909ab858bf5893a6087e3293686.gif)

結果をプレビューしてみると、 TimeCode と TimeCode の値ををリニアに補完する形で
アニメーションのキーが指定されているのがわかります。

### Interpolation(補完)

timeSamples にキーが指定された場合、TimeCode と TimeCode の間は指定された補完方式で補完されます。
デフォルトは Linear で補完されるので、上の例の場合だと 2 フレームなら 2、3 フレームなら 3 のほうに補完されていきます。

それ以外には Held が指定可能で、この場合は補完されず 1 ～ 9 が 1 10 ～ が 10 のように
キーの値が次の timeSampling まで値は補完されず維持される形になります。

```python
stage.SetInterpolationType(Usd.InterpolationTypeHeld)
```

補完方法は Stage に対して指定をします。

![](https://gyazo.com/1cd07bc16624091d3f625dcb72800489.gif)

試しに usdview で InterpolationType を Held に変更してみると
見ての通りスライダーを動かしても 1 のまま、途中から 10 に切り替わっているのがわかるかと思います。

!!! info

    MayaやBlender、HoudiniといったツールからアニメーションありのUSDを出力する場合は
    基本全フレームにアニメーションをベイクする形になります。

## アニメーションファイルを分離したい場合

USD のコンポジションの仕組みを考えるのならば、
アニメーションデータと頂点情報などは分離しておきたい気持です。

どうしておくといいか？というと、以前に書いた [Specifier](26_specifier)という記事の「over」で
アニメーションデータだけを Export し、そのレイヤーをサブレイヤーで合成することで
アニメーションデータと頂点データを分離できます。

しかしながら、Maya も Blender も別レイヤーで over でアニメーションを出力する機能がみつからないので
なにかしらの対策が必要そうです。

## まとめ

以上が USD のアニメーションの基本でした。
今回は Attribute に対してのアニメーションで、UsdSkel に関してはまた別の構造がありますが
それはまた別途まとめようかと思います。
