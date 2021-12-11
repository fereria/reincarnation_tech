---
title: InlineUSDを使おう
tags:
    - USD
    - SOLARIS
    - AdventCalendar2021
---

[Advent Calendar 2021 Houdini Apprentice](https://qiita.com/advent-calendar/2021/happrentice) ２日目は、InlineUSDを使おうです。

これとは別に開催中の[USDアドカレ](https://qiita.com/advent-calendar/2021/usd) 曰く、USDは手書きするものらしいので
今回は最強のUSD手書きエディタHoudini の InlineUSDを紹介しよとうと思います。

## InlineUSDとは

![](https://gyazo.com/216927b3b3ca2d124f2c85675f386119.png)

InlineUSDとは、HoudiniのLOPで使用できるノードの１つで
その名の通りUSDAsciiを直接書いてStageをOutputしてくれるノードです。

## USDA

USDは usda というアスキー形式で手書きすることができます。

https://marketplace.visualstudio.com/items?itemName=AnimalLogic.vscode-usda-syntax

VSCodeでは Animal Logic製のアドオンが公開されていて、
これを使用してVSCodeで SyntaxHighlightされた状態で書く＋usdviewでプレビューといったこともできますが、
やはりTypoしたり、フォーマットを間違えたりすることが多くて
なかなか大変です。

そんな、USDを手書きする人におすすめなのがHoudiniの Inline USDです。

## つかってみる

![](https://gyazo.com/2268047a36d7654489954827924cb303.png)    

まず、Houdiniを起動してLOP（Stage）を開きます。

![](https://gyazo.com/43e62af6228c58e3a5b7a29ca0b7c36c.png)

そして、 Inline USDノードを作成します。

![](https://gyazo.com/bf34b70cf9bb62b5d1f5245fabe6786d.png)

作成したら、USD Source が出てくるのでこれで準備完了です。

![](https://gyazo.com/49fc0178e42fb497e9910be047e55e77.png)

このUSD Sourceに USD Asciiを書くと

![](https://gyazo.com/390763ed3b54cabc01821ca492958c5d.png)

その USD Ascii のシーングラフを Scene Graph Tree に表示することができます。

![](https://gyazo.com/750bba168f59e5c3552d3cf9e613e953.png)

Asciiで書けることはなんでもできるので、このようにリファレンスをしたりアトリビュートを記述したりした場合も
Houdini上ですぐにプレビューが可能で

![](https://gyazo.com/187245aaea2cb7399a8877118ccf227d.png)

リファレンス（コンポジション）した結果を確認することができます。

![](https://gyazo.com/c3637b2d112bd05921873ff2ca18fd18.png)

SyntaxErrorがあった場合も、

![](https://gyazo.com/d50e7f70ded7ff93ae6d61c158fe03db.png)

エラー表示で、どこかまずいのかを表示してくれるので
心置きなくUSDを手書きすることができます。

## Houdiniのプロパティを埋め込む

USDAsciiエディタとして使用するだけでもとても便利なInlineUSDですが、
この USD Source のなかに、Houdiniのエクスプレッション関数を埋め込む事が可能です。

![](https://gyazo.com/0f35e2ee0006f00513f5a1fe745f6ba7.png)

例えば InlineUSDノードに Sample プロパティを追加します。

![](https://gyazo.com/8eacc2e8fb0880f76c6eab8c3d3fb4f4.png)

それをInlineUSDのUSD Sourceに `chs(～～)` のように書くと、この部分は
Houdiniのプロパティが展開された状態でUSDに反映されます。

![](https://gyazo.com/243d57c0eeab71b034c2d19f5123f344.gif)

HoudiniのsampleParamを変更すると、USDのAttributeも更新されるのがわかります。

```
def "sample"
{
    string path = "`opname(".")`"
}
```

ほかにも、現在のノード名をプロパティとして仕込んだりといったことが可能になります。
一応、このような操作はEditProperties でも可能なのですが、
例えば、各種MetaDataを出力できるようにしたい時などに、決まったフォーマットを準備するとかであれば、

![](https://gyazo.com/d7fde4280fcc30595a5454fae2df264d.png)

どこかにAssetInfoを指定するノードを用意しておいて

```
over "`opinput(".",0)`" (
    assetInfo = {
        asset identifier = @@
        string name = "`chs("/obj/geo1/SETUP/assetName")`"
        string version = "`chs("/obj/geo1/SETUP/version")`"
    }
){
}
```

InlineUSDで、指定のノード以下のプロパティを埋め込みます。
USDSource内のどの部分であっても置換可能なので
入力Primに対してAssetInfoを埋め込むといったことが簡単に書くことができますので
使いまわし用としてはPythonを使用したり専用ノードを使用するより楽でシンプルにできると思います。

## そのほか

![](https://gyazo.com/d1a5ec334f010426f24f66f50be5330e.png)

InlineUSDの Allow Following Nodes to Edit New Layer は、ONの場合新しいサブレイヤーとして作成され
最も強いアクティブなレイヤーとなります。
OFFの場合は、サブレイヤーは作成されず、入力のレイヤーを編集する形になりますので、アクティブレイヤーは作成されません。

![](https://gyazo.com/8d9978b2747fb811b032fc53109b4f43.png)

なので Inspect ActiveLayerした場合、OFFの場合

![](https://gyazo.com/261caeb9d300d7f1b96e27e17059f85e.png)

現在のノードにはレイヤーが作成されていないので、 Node has no active layer となり InspectActiveLayerは機能しません。
（おそらく、多くの場合はこのオプションを変更する必要はないはず）

## usdaのフォーマットわからん！！

という方向けに
https://fereria.github.io/reincarnation_tech/11_Pipeline/10_USDTips/03_usd_format_cheatsheets/
よく使う記述のまとめ記事を過去書いたので参考にしてください。

## まとめ

そんなかんじで、自分以外喜ぶ人がいるんだろうか...？と思っていたInlineUSDですが
USDAsciiEditorとして使ったり、各種PropertyをUSDの入れるためのテンプレートとして使うなど
いろいろな使い方ができることがわかったかと思います。

慣れてくると、USDAsciiはスラスラ書けて結構便利なので
VSCode等を活用しつつぜひとも使ってみてください。