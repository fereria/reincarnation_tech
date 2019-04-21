# Attribute を追加して VOP で使用する

<!-- SUMMARY:Attributeを追加してVOPで使用する -->

## チャンネルとアトリビュート

まず最初に、Houdini の場合「チャンネル」と「アトリビュート」というのは  
別の用語として扱われます。

### アトリビュート

アトリビュートとは、各ジオメトリのエレメント（point,vtx,prim,detail）の  
固有値をさしています。

![](https://gyazo.com/720dda5258305e57fba89604a41e04fa.png)

GeometrySpreadSheet で各エレメントごとに表示されるもの  
Wrangle や Expression で「@HOGEHOGE」のように表されている物が「アトリビュート」です。

### チャンネル

対して、チャンネルとは各ノードのパラメータービューに表示されているものをさします。

![](https://gyazo.com/a4d96c6b327a39d0439b0cae4ca21330.png)

このように、スライダや数値入力が作成されている物がチャンネルになります。  
VEX や Expression で ch('channel_name') でアクセスします。

## VOP で使用する

### アトリビュートの作成

VOP 内でチャンネルを追加する場合は、

![](https://gyazo.com/bd9caba89a7447786bee4dcda5ae51ea.png)

ノードの入力口で中ボタン →Promote Parameter することで、  
チャンネルを追加することができました。
[VEX を VOP に置き換える 01 ノイズ](01_vex_to_vop_noise.md) では  
この方法を使用してチャンネルを追加しました。

それに対して、アトリビュートを使用した場合はどうやったらいいのかが  
わからなかったので調べてみました。

<blockquote class="twitter-tweet" data-lang="ja"><p lang="ja" dir="ltr">プロパティがアトリビュートのことを指しているのでしたらBind Exportがありますよ</p>&mdash; UnlimitedEffectWorks (@ijiVFX) <a href="https://twitter.com/ijiVFX/status/1109796139643985921?ref_src=twsrc%5Etfw">2019年3月24日</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Twitter で教えて頂きました。  
毎度の事ながらありがとうございます。

![](https://gyazo.com/eefa3c4dffa08229bdf416065893977f.png)

まず、VOP ノードの前に Attribute Create を追加します。

![](https://gyazo.com/969d2cdd9b51e15ab3a474134c2a8854.png)

AttributeCreate ノード内で、アトリビュートの追加を記載します。  
注意が必要なのが「Class」

アトリビュートは、ジオメトリのエレメントに対して追加します。  
エレメントは、point,vtx,prim,detail と 4 つ種類があるので「どれに追加するか」を  
指定する必要があります。

![](https://gyazo.com/fd17d1d03f63f1980ad77f80b9ce88c5.png)

例のように Detail にしている場合は、GeometrySpreadSheet 内の「Detail」タブに  
param アトリビュートが追加されています。

![](https://gyazo.com/39c9c01f427f38caa5e0b64ab6115e5d.png)

Point に対して追加すると、全ポイントに対して param が追加されます。

### VOP 内で使用する

![](https://gyazo.com/e034bcc385dc77680d3c9f81c7e36ccb.png)

VOP 内で追加したパラメーターを使用するには、Bind ノードを使用します。

![](https://gyazo.com/72f57b0766b1d85540a148bec9e0a88c.png)

Bind の設定で、どのアトリビュートと紐付けするかを指定します。  
今回は param アトリビュートを VOP 内で使用できるようにするので  
Name に「param」を指定します。

さきほどの「Class」指定が、この VOP 内での値の持ってきかたが変わります。  
Point に対してアトリビュートを追加した場合、  
この Bind の param は Point ごとに別の値をもつようになります。

![](https://gyazo.com/1c8fe01444a2a9e7943c941a466b4955.png)

たとえば、GeometrySpreadSheet で Point4.y に 1 をセットすると

![](https://gyazo.com/5f9d2ab15c426088e8c45ec278cc99b3.png)

頂点単位で数値を入れることができますが、

![](https://gyazo.com/35ebac5f98b3831435fe7344a2beff79.png)

Detail に入れると、Geometry 単位での入力になるので  
オブジェクト全体をオフセットする形になります。

この Bind は、入力以外にも値を出力したい場合にも使用できるので、

```
@param = hogehoge;
```

のようになにかしらの数値をセットしたい場合は

![](https://gyazo.com/2500714d0f37eb001e8ec1c855d3014f.png)

Bind ではなく BindExport ノードを作成し、input に値を入力すれば OK です。
