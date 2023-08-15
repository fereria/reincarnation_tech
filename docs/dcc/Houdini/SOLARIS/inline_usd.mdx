---
title: InlineUSDを使おう
tags:
    - USD
    - SOLARIS
    - AdventCalendar2021
---

[Advent Calendar 2021 Houdini Apprentice](https://qiita.com/advent-calendar/2021/happrentice) ２日目は、InlineUSD を使おうです。

これとは別に開催中の[USD アドカレ](https://qiita.com/advent-calendar/2021/usd) 曰く、USD は手書きするものらしいので
今回は最強の USD 手書きエディタ Houdini の InlineUSD を紹介しよとうと思います。

## InlineUSD とは

![](https://gyazo.com/216927b3b3ca2d124f2c85675f386119.png)

InlineUSD とは、Houdini の LOP で使用できるノードの１つで
その名の通り USDAscii を直接書いて Stage を Output してくれるノードです。

## USDA

USD は usda というアスキー形式で手書きすることができます。

https://marketplace.visualstudio.com/items?itemName=AnimalLogic.vscode-usda-syntax

VSCode では Animal Logic 製のアドオンが公開されていて、
これを使用して VSCode で SyntaxHighlight された状態で書く＋ usdview でプレビューといったこともできますが、
やはり Typo したり、フォーマットを間違えたりすることが多くて
なかなか大変です。

そんな、USD を手書きする人におすすめなのが Houdini の Inline USD です。

## つかってみる

![](https://gyazo.com/2268047a36d7654489954827924cb303.png)

まず、Houdini を起動して LOP（Stage）を開きます。

![](https://gyazo.com/43e62af6228c58e3a5b7a29ca0b7c36c.png)

そして、 Inline USD ノードを作成します。

![](https://gyazo.com/bf34b70cf9bb62b5d1f5245fabe6786d.png)

作成したら、USD Source が出てくるのでこれで準備完了です。

![](https://gyazo.com/49fc0178e42fb497e9910be047e55e77.png)

この USD Source に USD Ascii を書くと

![](https://gyazo.com/390763ed3b54cabc01821ca492958c5d.png)

その USD Ascii のシーングラフを Scene Graph Tree に表示することができます。

![](https://gyazo.com/750bba168f59e5c3552d3cf9e613e953.png)

Ascii で書けることはなんでもできるので、このようにリファレンスをしたりアトリビュートを記述したりした場合も
Houdini 上ですぐにプレビューが可能で

![](https://gyazo.com/187245aaea2cb7399a8877118ccf227d.png)

リファレンス（コンポジション）した結果を確認することができます。

![](https://gyazo.com/c3637b2d112bd05921873ff2ca18fd18.png)

SyntaxError があった場合も、

![](https://gyazo.com/d50e7f70ded7ff93ae6d61c158fe03db.png)

エラー表示で、どこかまずいのかを表示してくれるので
心置きなく USD を手書きすることができます。

## Houdini のプロパティを埋め込む

USDAscii エディタとして使用するだけでもとても便利な InlineUSD ですが、
この USD Source のなかに、Houdini のエクスプレッション関数を埋め込む事が可能です。

![](https://gyazo.com/0f35e2ee0006f00513f5a1fe745f6ba7.png)

例えば InlineUSD ノードに Sample プロパティを追加します。

![](https://gyazo.com/8eacc2e8fb0880f76c6eab8c3d3fb4f4.png)

それを InlineUSD の USD Source に `chs(～～)` のように書くと、この部分は
Houdini のプロパティが展開された状態で USD に反映されます。

![](https://gyazo.com/243d57c0eeab71b034c2d19f5123f344.gif)

Houdini の sampleParam を変更すると、USD の Attribute も更新されるのがわかります。

```
def "sample"
{
    string path = "`opname(".")`"
}
```

ほかにも、現在のノード名をプロパティとして仕込んだりといったことが可能になります。
一応、このような操作は EditProperties でも可能なのですが、
例えば、各種 MetaData を出力できるようにしたい時などに、決まったフォーマットを準備するとかであれば、

![](https://gyazo.com/d7fde4280fcc30595a5454fae2df264d.png)

どこかに AssetInfo を指定するノードを用意しておいて

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

InlineUSD で、指定のノード以下のプロパティを埋め込みます。
USDSource 内のどの部分であっても置換可能なので
入力 Prim に対して AssetInfo を埋め込むといったことが簡単に書くことができますので
使いまわし用としては Python を使用したり専用ノードを使用するより楽でシンプルにできると思います。

## そのほか

![](https://gyazo.com/d1a5ec334f010426f24f66f50be5330e.png)

InlineUSD の Allow Following Nodes to Edit New Layer は、ON の場合新しいサブレイヤーとして作成され
最も強いアクティブなレイヤーとなります。
OFF の場合は、サブレイヤーは作成されず、入力のレイヤーを編集する形になりますので、アクティブレイヤーは作成されません。

![](https://gyazo.com/8d9978b2747fb811b032fc53109b4f43.png)

なので Inspect ActiveLayer した場合、OFF の場合

![](https://gyazo.com/261caeb9d300d7f1b96e27e17059f85e.png)

現在のノードにはレイヤーが作成されていないので、 Node has no active layer となり InspectActiveLayer は機能しません。
（おそらく、多くの場合はこのオプションを変更する必要はないはず）

## usda のフォーマットわからん！！

という方向けに
{{markdown_link('usd_format_cheatsheets')}}
よく使う記述のまとめ記事を過去書いたので参考にしてください。

## まとめ

そんなかんじで、自分以外喜ぶ人がいるんだろうか...？と思っていた InlineUSD ですが
USDAsciiEditor として使ったり、各種 Property を USD の入れるためのテンプレートとして使うなど
いろいろな使い方ができることがわかったかと思います。

慣れてくると、USDAscii はスラスラ書けて結構便利なので
VSCode 等を活用しつつぜひとも使ってみてください。
