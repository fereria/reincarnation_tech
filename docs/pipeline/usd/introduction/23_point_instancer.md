---
title: USDのPointInstancer
tags:
    - USD
    - AdventCalendar2022
description: USDのPointInstancerの構造について
slug: /usd/point_instancer
sidebar_position: 23
---

USD には、Reference で読み込む Prim に対して instanceable をつけることで
インスタンス化できる <AutoLinkTitle url="/usd/instance" /> 機能がありますが、
それ以外にも、数十億個のインスタンスを配置することを想定して設計されている「PointInstancer」スキーマが存在しています。

通常のインスタンスとの違いは、通常のインスタンスは 4x4 の行列で変換されているのに対し
PointInstancer の場合は、 **位置 方向 スケール** に分割された値で保持されています。
さらに、より小さい容量で、なおかつ位置・方向・スケールをそれぞれアニメーションするときのパラメータを管理できるため、
通常のインスタンスに比べて、データ量を大きく削減することができます。

もう 1 つの特徴として、PointInstancer は GPrim ではありません。
GPrim とは、Primitive の基底クラスで「DoubleSide」や「Orientation（法線を右手・左手系どちらで計算するか）」などのグラフィックの特性を扱い、「DisplayColor」などと合わせて
シェーダーで使用される primvar を提供するものです。

![](https://gyazo.com/1d6a7d5e2b3e00d757a07c038fe646a5.png)

そのため、Cube や Sphere のような基本的なプリミティブにしても、Mesh にしても、この UsdGeomGPrim を継承しています。
しかし、PointInstancer は Gprim ではありません。
Grpim ではありませんが、Boundable になります。
PointInstancer のアトリビュートには extent があり、これが PointInstancer の BoundingBox になっています。

### アニメーション

それ以外に PointInstancer に必要な仕様はアニメーションです。
PointInstancer のアニメーションは、上記に挙げた 位置・方向・スケール・範囲（BoundingBox）、そして各インスタンスの可視性（Visibility）などが
挙げられますが、これらのパラメーターは TimeSampled アニメーションを持っていれば、
個のアニメーションを再生できるようになっています。

### ID

もう１つ PointInstancer に必要なのが ID です。
これは、剛体シミュレーションの結果や、粒子状の物質のようなものを表現するのに仕様するのですが
これは時間経過とともに消滅したりします。
これらを管理するためには、各 Point に対して識別可能な ID を割り振る必要があります。

PointInstancer は、これらの仕様を含めた上で、大量のオブジェクトを票 j するための機能を提供しています。

## 基本構造

![](https://gyazo.com/14adbc0f2fb651eaa6a61c6712498288.png)

PointInstancer は、Point に対して表示するモデルを Prototypes として持ちます。
上の例だと、Cube と Sphere モデルが PointInstancer として表示されます。
この Prototypes オブジェクトには、それぞれ Index がつけられており
protoIndices アトリビュートによって、どの Point にたいしてどのモデルを
表示するかをコントロールしています。

![](https://gyazo.com/acd7f0a22d0d98b2898304df7e14d206.png)

最初に開設した通り、PointInstancer の配置対象の Point には ID が割り振られています。
各アトリビュート（protoIndices や orientations 等）は、Point の数だけの配列になっていて、Point の ID に対応します。

![](https://gyazo.com/8171342682e7cc3cfdced655de87cbdf.png)

最初に説明した通り、Point の位置情報もマトリクスではなく point3f で表されています。

## データを確認する

まずは実際に PointInstancer を使用したシーンを作成して、中身を確認してみます。
作り方は <AutoLinkTitle url="/houdini/solaris/instance_01" /> にまとめてありますのでざっくりとですが、SOP 上で Grid > Scatter で Point を作り、

![](https://gyazo.com/78b39b1c8650d8216eebf2c450dee9af.png)

Instancer ノードに Cube をつなぎ、

![](https://gyazo.com/e2ab04fe39ec1094800d17f23e34f98c.png)

こんな感じの 3 つだけ表示された状態にします。

![](https://gyazo.com/9808a42d62bb9e4b6f92535e6e22384d.png)

PointInstancer ノードは、Instancer ノードと、UsdGeomPoints(位置情報)と、Prototypes（Point に対して表示させるオブジェクト）
で構成されています。

![](https://gyazo.com/2d1cab55bad06cdf53dc7b1209bee1a4.png)

アスキーファイルを確認するとこのようになっています。
最初の概要に書かれている通り、位置情報などは行列ではなく 位置・方向・スケール・バウンディングボックス
それぞれが別のパラメーターとして扱われています。

このような構造にすることで、行列計算のコスト等を無くして
大量のオブジェクトを高速にインスタンスで扱えるようになっています。

## アニメーション

サンプルの例だと静止オブジェクトで、アニメーションはしていませんが
PointInstancer のオブジェクトもアニメーションをすることができます。

```vex
@orient = quaternion(@Time * rand(@P), {0,1,0});
@P.y = @Time * rand(@P);
```

まずはシンプルな VEX を SOP 側の Point に対して指定します。

![](https://gyazo.com/30c9f29fa893be6d0d1ac82c77fd2fee.gif)

このように、PointInstancer のオブジェクトを動かすことができました。

![](https://gyazo.com/717929511494b4a087356406d9b7fafe.png)

アニメーションデータは、各アトリビュートに対して timeSamples という形で指定されます。
USD のアニメーションは、基本リニア補完のみで全フレームにベイクされた状態で保持されています。

## まとめ

[SOLARIS で Instancer を使う(1) 配置編](/houdini/solaris/instance_01) や [SOLARIS で Instancer を使う(2) 編集編](/houdini/solaris/instance_02) で
Houdini での PointInstancer の作成方法はまとめていましたが
PointInstancer 自体はこれまできちんと調べられていませんでした。

通常のインスタンス ( [ USD の Instance について](/usd/instance) ) で USD の Instance について触れましたが
こちらの PointInstancer はより大量のオブジェクト（植生、岩や破片、森林、シミュレーション結果など）数億にもなるような巨大なデータを扱うことができるものというのがわかりました。

この PointInstancer は、Houdini とも非常に相性が良くて
SOP 上の Point を利用して LOP 側でのレイアウトを効率的に行うことなどが可能です。
もちろん制限もある（衝突などはできないので、その部分は実体化する必要があるなど）
大量の配置をする場合などには、この PointInstancer を使用すると
快適に大量の物量を扱えるようになるのでは？と思います。

## 参考

-   https://github.com/PixarAnimationStudios/USD/wiki/PointInstancer-Object-Model
