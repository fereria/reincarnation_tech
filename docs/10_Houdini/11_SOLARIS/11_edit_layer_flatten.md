---
title: Flattenでレイヤーをコントロールしよう
tags:
    - USD
    - SOLARIS
    - Houdini
---

[前回](10_edit_layer.md) のConfigureノードを利用することで、自分の意図したところで
usdaファイルをコントールできることがわかりました。
ですが、それだけだとUSDファイルに名前をつけて保存はできますが
レイヤーの数だけUSDファイルが作成されてしまい、コントロールができなくなってしまいます。

また、場合によっては結果が意図しない形になったりすることもあるので
前回の補足としてFlattenについてまとめてみます。

Flattenとは、複数別れているレイヤーを１つのレイヤーに統合することです。
Flatttnをすると、コンポジションアークで別のレイヤーを読み込んでいたりする場所も
１つのレイヤーにまとめることができます。

このFlattenがSOLARIS上でどう扱われているかというと、

![](https://gyazo.com/190b91f4d6dc0aba8b3126ff2731b82d.png)

たとえばマージノードには Merge Styleという項目があり

![](https://gyazo.com/3135b473882799e361a90aadaf3ba68c.png)

このように、２つのレイヤーをマージした場合、
デフォルトの Separate Layers であれば、マージ結果は 2Layersになります。
つまり、2つのレイヤーが合成されている状態（レイヤーの状態は保持されたまま）
というわけです。

![](https://gyazo.com/eaa21c4482354aa0acd64ef2c323c366.png)

これを Flatten Layers にすると、 2 Layers という表示がなくなりました。
どうなったかというと、
今までは 2つのレイヤーがそれぞれ保持されていて、それをコンポジションしていたのが
それぞれのレイヤーにあった情報が1つのレイヤーに統合されたという状態になっています。

つまり、Flattenしていない場合は、 USD ROPなどでExportするときに
SavePathをしていない場合は、１つの USDファイルではなく
複数の USDに分かれて出力されることになります。
一方でFlattenしている場合は、出力されるUSDは1つだけになります。

なので、USDの出力する単位をどうするかをコントロールしたい場合は
このFlattenの設定（色んな所にある）をコントロールしていけばいいことになります。

## トラップ その１ - Pruneしたら...

出力する単位を管理する以外に、これを正しく指定しないと
結果が意図しないことになる場合があります。
それがPruneノードを使用して１つのUSDを複数に切り分けるような処理をした場合です。

実際にやってみます。

![](https://gyazo.com/cdd0fdf1ec2415a0c937ab1e3b59afe5.png)

こういうサンプルを用意します。

![](https://gyazo.com/aa9e2ee1be6c29447e84f738a6e11702.png)

Pruneで切り出す前のシーングラフはこんな感じ。
CubeとSphereがそれぞれあるような状態。
これを、 Cubeだけ Sphere だけで切り出してそれぞれ別レイヤーとして
出力する。
そして最後に１つにコンポジションをしたいとします。
なので、最終的にはCubeとSphereは両方見えていてほしいです。

が、この結果がどうなるかというと

![](https://gyazo.com/45df41da5e10d7c6bd942de46b5ce438.png)

こうなります。
両方消えてしまいました。

これは、USDのレイヤーそれぞれは非破壊でオーサリングした情報を持っています。
で、この Prune3 側のレイヤーがどうなってるかというと

```
#sdf 1.4.32
(
    framesPerSecond = 24
    metersPerUnit = 1
    timeCodesPerSecond = 24
)

def HoudiniLayerInfo "HoudiniLayerInfo" (
    customData = {
        string HoudiniCreatorNode = "/stage/prune3"
        string[] HoudiniEditorNodes = ["/stage/prune3"]
    }
)
{
}

over "sphere1"
{
    token visibility = "invisible"
}
```

Pruneで消したPrimには「visibility」が invisible （非表示）が指定されています。
で、この invisible したものがつぎのマージノードで
サブレイヤーされてしまうので
結果両方のノードがきえてしまうというわけです。

じゃあこれはどうすりゃいいんだ？っていうときに使用するのが
前回も使用したConfigureLayerノードです。

![](https://gyazo.com/40d1819f4f64d1a1f1841bd530dfe992.png)

まず、Pruneノードの Methodを Deactive にします。

![](https://gyazo.com/0a84665d50bc25c45487e6d305e723be.png)

Pruneノードの次にConfigureLayerを追加します。

![](https://gyazo.com/43bca3b477249a0b330452c81c4a94fc.png)

そして Configure Layer の Flatten Input を Flatten Input Stage します。

結果のシーングラフを見ると

![](https://gyazo.com/538ee55ce1390d42b4633db63c0f1291.png)

先ほどとは違い、PrimがHideではなく削除されて
切り出されたモデルのみになっています。

何が起きたかというと、 Pruneノードで切り出されてモデル以外は
Activeが False 状態になります。
これだけだとあくまでも「無効化」された状態なだけで、
レイヤーには情報が存在します。
いわゆる、PhotoShopのレイヤーの表示をOFFにしたのと同じ状態です。

これを、Flatten Input Stageすると、Photoshopのレイヤー統合を実行したのと
同じ状態になり、いままで非表示にしていただけのPrimは
なくなってしまいます。

![](https://gyazo.com/741ba4c8f78a0ee948daa0a91b409714.png)

結果。
それぞれ切り出されてFlattenした状態のレイヤーを合成したら
そもそも visibility や active の情報はすでになく
単純に切り出されたモデル同士を合成したことになるので
両方消える...みたいなことにはなりません。

SOLARIS上の合成処理はコンポジションアークのルールで行われているので
このあたりの構造を理解していないと、意図しない結果になるので
注意が必要です。

## トラップ２ 消えるバリアント

というわけで、場合によってはFlattenしてレイヤーをまとめたりする必要が
あることはわかりましたが
このFlattenを入れたせいで意図しないことが起きる場合があります。

![](https://gyazo.com/312dd0513e4ff777254f81a3bf392bf5.png)

例として、こういうシンプルなバリアントセットを用意します。
これで複数のモデルをきりかえできるようになります。

![](https://gyazo.com/7b3cb0db1b641858278d86b06a924c98.png)

これに、ConfigureLayerを追加して

![](https://gyazo.com/d3b9fee15401b10c8be0b84eb0fae24a.png)

Flatten Input Stage してみます。

![](https://gyazo.com/4b960d9d5a1f3544d1cfbc6f86724ca4.png)

結果、追加したはずのバリアントセットが消滅しました。

なぜかというと、Flatten（Flatten Input Stage) は
USDのコンポジションなどを１つのレイヤーにまとめる処理だからです。
なので、バリアントセットもなくなって
現在選択されているバリアントセットのみが残る...ということになります。

こういうシンプルな場合は問題なのですが、
ノードが複雑になって、複数のレイヤーを合成するようなことをすると
Flatten Input Stage してコンポジション（とくにバリアントが）がきえて
混乱する...ということにもなりかねないので
注意が必要です。（やらかした）

なお、 Configure Layerの Flatten Input にはもう１つ
Flatten Input Layers というのがありますが
こちらは複数に分かれたレイヤーを１つにまとめるもので
MergeノードのFlatten Layersと同じ挙動になります。

![](https://gyazo.com/c2fb6189095b543429237968e8ff070d.png)

この場合は、「2 Layers」という表記がなくなり、１つのレイヤーに統合されただけで
コンポジションの合成などの情報は非破壊で保持されます。

## まとめ

というわけで、ConfigureLayerとFlattenを利用することで
どこまでをどのレイヤーに入れるかをコントロールできることがわかりました。

これがどういうときに役立つかと言うと
例えばSOP内で作ったモデルをUSDアセットとして出力する場合に
どのようにモデルを分割して、どのように出力するかをコントロールしないと
すべてのレイヤーに重複したデータが保存されるので
ファイルサイズが増えたり、いらないPrimが含まれたUSDファイルが出来上がります。

ので、SOLARIS上で色々加工してアセットを作りたい場合などは
FlattenとConfigureLayerのExportPath指定などを活用して
最終的にUSD ROPなどで出力される USD ファイルの構造を
コントロールすると良さそうかなと思います。