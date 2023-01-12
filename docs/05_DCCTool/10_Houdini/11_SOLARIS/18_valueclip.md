---
title: CacheとValueClip
tags:
    - USD
    - SOLARIS
    - Houdini
description: HoudiniでCacheを使用したレンダリング用シーンの作り方
---

USD でレンダリングシーンを構築したい場合、ジオメトリキャッシュなどは 1 フレームごと別ファイルに分離したうえで、USD 単体で再生できるような構造を
構築したいはずです。
このあたりのレイヤーをフレーム単位で分割したりする方法をまだきちんと試したことが
なかったのでやり方を確認していこうと思います。

## キャッシュを作る

Houdini19.5 からは、USD のキャッシュを作るためのノード [File Cache](https://www.sidefx.com/docs/houdini19.5/nodes/lop/filecache.html) が新規で追加されました。
このノードは USD ROP と SublayerLOP の機能を組み合わせたもので
これを利用することで、各フレームごとのキャッシュを USD で出力できます。

![](https://gyazo.com/64eebd06fe760cc4099b8069bd17e9f5.png)

基本的な使用方法は、キャッシュしたいノードを Input に入力して、
BaseFolder や BaseName などを指定します。
Cache Range の Evaluate As を SingleFrame から Frame Range に変更し
指定のフレーム分だけキャッシュを出力します。

Frame Range に指定した場合は、そのままだと全フレームが同じファイル名で出力
されてしまうので、 Advanced タブの Path Construction の Cache Name に

![](https://gyazo.com/3bb1a21190034c6ed7ea84ae788495b2.png)

```
`chs("basename")`.`$F``chs("filetype")`
```

こんな感じで、 $F を足します。

USD の出力関係では
USD タブにある Save Style は

![](https://gyazo.com/d5bedee845d003945a90b80e8025fc5e.png)

デフォルトの Flatten Implicit Layers（アノニマスレイヤー部分を統合）で基本 OK だと思いますが
完全にキャッシュと割り切って切り離すなら Flatten Stage（それまでのレイヤーを 1 レイヤーにすべて統合）とかでもアリかと思います。

![](https://gyazo.com/da7d6fc7bd23c697455443c522835e77.png)

準備ができたら Save to Disk in Background で出力します。

![](https://gyazo.com/5776c4aff6d3a787677bc91873c4d302.png)

指定フォルダー以下に連番 USD が出力されました。
Load from Disk にチェックが入っていれば、これ以降はキャッシュが使用されるようになります。

## USD Stitch Clips

これで無事キャッシュが作成されましたが、多くの場合は Houdini を起動せず
husk などを使用して実行したいケースのが多いでしょう。
その場合、ブラーが正しくレンダリングできない（時間方向の情報を持たないため）
などの問題が発生します。

これらの、個別に出力したキャッシュを 1 つのレイヤーに統合して
バッチファイルや USDView などからも再生できるようにします。

USD には LOP に ValueClip ノードというノードが存在していて、
以前書いた {{markdown_link('value_clip_01')}} で説明している時間方向（TimeSampling）の
レイヤー分割をする機能を使用できます。
しかし、このノードの場合は、
指定の PrimitivePath に対して個別に ValueClip を指定する必要があるので
![](https://gyazo.com/5687a47d5ed4d8c7d920a98df771a8ad.png)
PrimitivePath は Clip PrimitivePath と同一のスキーマでないといけなかったり
Manifest なども自前で作らなければいけないなど、かなり USD を直接触る感じで
あまり使い勝手がよくありません。

{{'https://twitter.com/suamaGod/status/1567403383568633857'|twitter}}

これをもう少し使いやすくしたものが、すあまのかみさんに教えてもらった ROP Network の USD Stitch Clips ノードです。

![](https://gyazo.com/2c87cfb56bf0ec3c4e3f12db2e4f9add.png)

USD Stitch Clips は、Value Clip の Manifest と Template ファイル、
Input をベースにした Topology ファイルを生成します。

![[houdini_valueclip.svg]]

Topology ファイルとは、対象の Clip 以外の構造を出力したもので
ValueClip を指定するレイヤーからサブレイヤーで使用します。

Manifest は、ValueClip の Clip 対象の Prim にある対象の Attribute を記述したものです。
自動生成されたものは Clip Primitive Path（Clip 対象レイヤーにある Clip 対象 Prim）
にある Attribute が列挙されますが、このうちすべてを Clip する必要がなければ
必要なもの以外は削除しておくと、不要な部分はロードしないようになります。

今回は 1Prim だけ Clip しましたが、 Stitch Files を追加することで
複数の ValueClip を作成できます。

設定ができたら、 Render ボタンを押すと、

![](https://gyazo.com/afb2a3e6fa76d01d73f0fd407228c4da.png)

必要なファイルが出力されました。
このファイルのうち template.usda が、レンダリング用の連番データが統合されたファイルになります。

![](https://gyazo.com/18a46cd914f30fbdc73ca11d96a3615c.png)

開くと無事ロードができました。

実際に使用するときには、この Template.usda をキャラクターごとに作成し
背景などと合わせて Payloads などでロードし、
それに対してライティングなどを追加したうえでレンダリングするのかなと思います。

作成した template.usda は、フレームごとのキャッシュ更新では
PrimName や Namespace に変化がなければ更新する必要はありませんので、
最初に Cache 作成と合わせて USD Stitch するように、TOPs などで自動化するのがよいのかなーと思います。
