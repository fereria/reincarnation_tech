---
title: Stage/Layer/Spec
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description](https://qiita.com/advent-calendar/2021/usd) 8日目は、
USDのStageとLayer、そしてSpecとはなにか？というのを説明していこうと思います。


## Stageとは

USDに触れていると、この「Stage（ステージ）」という言葉はあらゆるところで見られます。
[アドカレ２日目の記事](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09#%E3%81%AF%E3%81%98%E3%82%81%E3%81%A6%E3%81%AE-usda)曰く

> しかしちょっと待ってください。USD では厳密に言うと、
> usda ファイルとは「私はこうしようと思うんだけどな」という 計画の記述 なのです。
> 従ってこの時点ではまだ誕生はしていません。そうなんです。実はあなたの他にも神がいるのです。
> 八百万の神々が集まり本当に世界を生み出すところは出雲（Stage）と呼ばれますが、
> その話はこのアドカレの別の記事 で @fereria さんが明らかにしてくれるでしょう。

ということで、今回はそのStageと現在開こうとしているUSDファイルとの違い
八百万の神々が集まり本当に世界を生み出すところは出雲（Stage）について詳しく説明したいとおもいます。

## USDと今までのフォーマットとの違い

多くのフォーマット（FBXだったり、OBJだったり、GLTFだったり）では、
１つのファイルに１つのシーングラフが保存されています。

![](https://gyazo.com/d7969029777a1af21f8b1baa2ae23c29.png)

なので、たとえば複数に分かれたFBXをレンダリングする場合などに
Mayaでインポートなどをした場合も、それはあくまで１つのMayaシーンになる（統合される）
だけで、Mayaシーンが複数のFBXを持っているわけではありません。
（追いかけようとした場合は、別途なにかしらの情報を持っておく必要がある）

ですが、USDの場合はコンポジションアークによって
複数のUSDファイルが合成されて、その結果１つのシーングラフになります。
そのため、 **開いたUSDファイルと実際に出来上がったシーングラフは一致しません。**

このあたりは具体的な例を見ていったほうがわかりやすいので、Kitchen_setをみていきます。

## Kitchen_setでみるStage そして Layer

Kitchen_setをダウンロードして解凍したフォルダ内には Kitchen_set.usd というファイルがあります。

```
usdview D:\Kitchen_set\Kitchen_set.usd
```

![](https://gyazo.com/62cfb961c797a4c7a27bc6db984bf3d1.png)

このファイルを、 usdviewで開くとこのようにKitchen_setが表示されます。
開くと、モデルが配置されていて１つの完成されたシーンになっています。

ですが、この Kitchen_set.usd を、[以前解説したusdcat](https://fereria.github.io/reincarnation_tech/11_Pipeline/20_USDTools/01_usdtools_usdcat/)を使用してアスキーファイルでどうなっているかを見てみます。

```
usdcat D:\Kitchen_set\Kitchen_set.usd
```

![](https://gyazo.com/adc274495504010c793b68eea80f263a.png)

実行すると、このようなusdaで表示されます。
見てわかる通り、ここにあるのはXform（MayaでいうところのGroupノード）と
リファレンスをしているPrim（Kitchen_1等)と、その配置情報（xformOp:translate)のみが
書かれているだけで、Meshの情報などは見当たりません。

つまりは、開いているファイルは Kitchen_set.usd ではあるものの
このファイルに書かれているのは「私はこうしようとおもうんだよな」という主張（オピニオンと呼ぶ）が書かれているだけで、
これが最終的なシーングラフの形ではありません。

この計画の記述が書かれているファイルのことを、USDではLayer(レイヤー)と呼び
このレイヤーがコンポジションによって組み合わされた結果出来上がったものを Stage と呼びます。

> 実際に配置されているオブジェクトは、 add references = @./assets/Kitchen/Kitchen.usd@ とか書かれている通り
> Kitchen_set/assets/Kitchenフォルダ以下にあります。
> 
> ![](https://gyazo.com/3c51138285d9c3af6f84fcea95aa9c4a.png)
> このアセットフォルダ以下も、１つのファイルではなく複数ファイルで構成されています。
> このあたりの詳しい事は別途記事にする予定です。


## LayerとSpec

Kitchen_setだと複雑なので、もっとシンプルなusdファイルで確認してみます。

{{'5c2f8cc7ad988bea665dfce639c2050c'|gist}}

{{'2f49e19ff084fe357e19a70660a75a4b'|gist}}

このような、samplePrimに sampleValue = false を設定したレイヤーと
そのレイヤーをサブレイヤーしているレイヤーを用意します。

![](https://gyazo.com/83762e2dc4f33947702cdfcee14d91d8.png)

この２つのPrimを usdcat を使用して Flatten（コンポジションした結果）を表示してみると
このようになります。

![](https://gyazo.com/ffe14d2a08cf7b39dae9d20450252d66.png)

書き表すとこのようになります。

Stageは、コンポジションアークによって（この場合[サブレイヤー](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/06_comp_arc_subLayer/)によって合成された結果出来上がったものです。
今回のサンプルならば、 subLayer.usda と root.usda が合成された結果出来上がったシーングラフが
Stageです。

LayerとStage、というのの何が違うのか？というのは、
たとえるならPhotoShopのレイヤーがわかりやすいです。

![](https://gyazo.com/400f7493d7c9c8ccf4f31491d858cd1f.png)

このような赤いレイヤーと青いレイヤーがあった場合、最終的に表示される色は何色になるでしょうか。
上にあるレイヤーが赤なのだから、赤！とも思えるかもしれませんが

![](https://gyazo.com/503e6b3707438a17965363f0f4dc8ac1.png)

合成方法が乗算なら

![](https://gyazo.com/ff04830977ca3212d1dc71f0a4bf2034.png)

黒になります。

今は２つのレイヤーだけでしたが、これがもっとレイヤーが増えて、フォルダでまとめられていたりしたら？
重ね方が複雑になっていたら？
**レイヤーにある絵がなんであろうと、最終的にすべてが合成されるまでどんな絵（どんな色）になるかはわかりません。**

これと同じ考え方がUSDにもあります。

PhotoShopのレイヤーが、すなわちUSDのLayer＝usdファイルにあたりますし、
キャンバス上に表示されている最終的な絵がStageです。

この合成前のUSDのLayer内にもPrimやPropertyの記述はあります。
ですが、これは最終的な形と同じとは限りません。
なぜならば、ほかのレイヤーによって上書きされている可能性があるからです。
**PhotoShopの別のレイヤーに別の何かが書かれていて絵が上書きされるように、
PrimやPrimに指定されているPropertyは別のレイヤーによって上書きされる可能性があります。**

そのため、USDでは合成前のレイヤーに書かれている記述を「Prim」とは別に **「PrimSpec」**

> A PrimSpec can be thought of as an “uncomposed prim in a layer”. 
> 引用: https://graphics.pixar.com/usd/release/glossary.html#usdglossary-primspec

レイヤー内にある **「合成されていないPrim」** として区別して呼びます。
Propertyに関しても同様に「PropertySpec」と呼ばれ、合成後とは区別されます。

![](https://gyazo.com/72cfe0edb913f6a8708a9521888f858f.png)

図に書き出すと、Layer内に記述されている内容はこのようになり、

![](https://gyazo.com/a010bb15b790395b74a246e08047eacf.png)

すべてのLayerが合成された結果、出来上がったものが StageでありPrimであり、Propertyです。

言い換えるならば、
各StageにあるPrimやPropertyとは多くのレイヤーに記述されているPrimSpecあるいはPropertySpec
の寄せ集められた（合成された）結果とも言えます。

### usdviewで確認したい場合

このLayerやPrimSpec、PropertySpecは
 usdview の Layer Stack と Composition で確認することができます。

![](https://gyazo.com/e8e8861c67ca34a7831bcc012c434e8b.png)

![](https://gyazo.com/dfb92904ea8916eae4fb9fbf14f68259.png)

samplePrimを選択すると、このPrimがどのレイヤーにどのように定義されていていたのか
結果どのようなSdfPathになったかがわかりますし、

Propertyの場合は、

![](https://gyazo.com/27e636ac5133dae571b9233f48a4b89b.png)

Compositionを見ると、sampleValue のComposition には２つのレイヤーに主張（オピニオンと呼ぶ）があり
レイヤー内に Spec (合成されていない「合成予定のもの」)があると示す Has Spec が yes になっています。

![](https://gyazo.com/cae776120021b3791210970da5395430.png)

さらには、 Layer Stack を見ると、それぞれのレイヤーにあるValue（PropertySpec）が書かれていて
どのような順番で合成されて、結果なにになったか（上のほうが強い）がわかります。

![](https://gyazo.com/7a8fae533c0e9b71a46b5ec938092f47.png)

これは、これよりも多くのレイヤーで、複数のコンポジションが絡んできても同様で、たとえばKitchen_setを見ると

![](https://gyazo.com/bcd2b57b6096bda7ba4e13be61681e01.png)

どのレイヤーで定義されているのか、
そのレイヤー内のどのPrimSpec（LayerStackに書かれているPathが、PrimSpecのPath）がもとになっていて

![](https://gyazo.com/e6d9d09332661d786322b2ee20641e06.png)

それらPrimSpecが、
どのようなコンポジション順序によって、結果このPrimが出来上がったのかがわかります。
（CompositionのArcPathがPrimSpecのPath）

## Pythonから取得する場合

これまでのStageとLayer、そしてSpecについてを頭に入れたうえでPythonから取得してみます。

### Layerで取得

```python
# レイヤーを取得
layer = Sdf.Layer.FindOrOpen('D:/root.usda')
# primSpecを取得
primSpec = layer.GetPrimAtPath('/samplePrim')
# AttributeSpecを取得
attrSpec = primSpec.attributes['sampleValue']
print(attrSpec.default)
print(layer.identifier)
```

まず、Layerから値を取得する場合。
この場合はStageではなくSdfLayerと各Specのオブジェクトとして扱います。

![](https://gyazo.com/0d34b101444068bbca4f1bc7825ceb2c.png)

Layerから値を取得する場合、Pythonからだと非常に大きな罠があって
C++のAPIドキュメントとは関数もなにもかも異なります。

Pythonの場合はどれも Sdf.Find という形で値が取得されますがこれはLayerまたは～～Specといった
合成される前の情報のいずれかです。
上のサンプルコードの場合は、LayerからPrimSpecを取得し、そこからさらにAttributeSpecを
取得しています。

これらはあくまで合成前の「今のレイヤーに書かれている記述」なので
コンポジション情報やほかのレイヤーへの情報は持ちません。

### Stageから取得

```python
stage = Usd.Stage.Open("D:/root.usda")

prim = stage.GetPrimAtPath('/samplePrim')

# PrimSpecを取得する
for primSpec in prim.GetPrimStack():
    print(primSpec)
    # primSpecからattribute取得
    attributeSpec = primSpec.attributes['sampleValue']
    print(attributeSpec.default)
    # primSpecから、そのprimSpecが記述されたレイヤーを取得
    layer = primSpec.layer
    print(layer.identifier)
```

次にStageから、Layer・各種Specを取得した例。

これは、指定のPrimの由来や成り立ちを知るための方法とも言えて
GetPrimStackは、このPrimが出来上がるまでに合成されたPrimSpecを強い順に取得します。

![](https://gyazo.com/555f420fdc669432643fbe8366b9b942.png)

実行するとこのようになります。
GetPrimStackで取得できるのはPrimSpecなので、そこからAttributeSpecや
それが記述されているレイヤーなどを知ることができます。

## まとめ

usdaファイルとStageとの違いが理解できたでしょうか。

LayerStackとCompositionの違いはなんだろうとかもろもろ出てくるかもしてませんが
さらに詳しいことが気になった方は、以前[PCPでコンポジションアークの構造を解析・編集対象を取得する](https://fereria.github.io/reincarnation_tech/11_Pipeline/30_USD_Programming/01_Python/04_pcp_compositionArc/)という
ここまでいけばUSD１級というディープな記事を以前書きましたので
もしさらに詳しい事を知りたい！！という方はぜひとも合わせて読んでください。
