---
slug: /usd/specialize
title: スペシャライズドについて
description: USDのコンポジションアークの『S』「スペシャライズド」について
sidebar_position: 5
tags:
    - コンポジションアーク
    - USD
    - USD基本
---

コンポジションの中でもかなり特殊すぎて、詳しく構造を調べていなかった
Specialize を紹介しようと思います。

コンポジションの強さ（LIVRPS）では最も弱いのが Specialize です。
その挙動は継承（Inherits）とよく似ていますが
重要な違いとして Specialize/Inherits と Reference 比べてオピニオンが
強いか弱いか...という違いがあります。
文字だけだとわかりにくいので、
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Specializes
USD Glossary の Specialize にかかれているサンプルを使用して
図で説明してみようと思います。

## Specialize

![](https://gyazo.com/0929bd6be687af78762b20911fbf22e9.png)

Robot.usd と RobotScene.usd の２つのレイヤー内のコンポジションは
このようになっています。

![](https://gyazo.com/6cbd36de900b63e8030620da6484f76e.png)

まず、サンプルを usdview で表示するとこのようになります。

```
            # specialize roughness...
            float inputs:specularRoughness = 0.2
```

Robot.usd の CorrdedMetal の specularRoughness に、 0.2 とある通り
最終的な結果を見ても 0.2 になっています。

![](https://gyazo.com/3e1854cc497c91cadf44f563ad6aab86.png)

Specialize は Reference よりも弱いオピニオンなので、
Composition を確認すると、Robot.usd でまず Specialize で合成され
その合成されたあとに Reference されていることがわかります。

![](https://gyazo.com/a1a62d7f8e46c2a629a4c4a1d46e4eb9.png)

コンポジションの順番を追記すると、このようになります。

![](https://gyazo.com/1a31e11a753fa0cfe381f4ef22a47752.png)

ここで注目なのが、Robot.usd の CorrodedMetal.specularRoughness です。

![](https://gyazo.com/e5a6133b3ebdf21ee9793f2beffa0392.png)

diffuseGain は、Specialize のおかげで Metal.diffuseGain の値が合成されていますが
specularRoughness は、CorrodedMetal にオピニオンがあるため、その値が優先され 0.2 になります。

## Inherits との比較

比較のために Inherits に変更するとどうなるか確認してみます。

![](https://gyazo.com/db15a41b4a4e67e53d46a858a966df36.png)

Inherits の場合は、最終的な合成結果が変わっているのがわかると思います。

![](https://gyazo.com/1992a9c4e6d3d2ba6e9ae9530b593b29.png)

Composition を比較してみると、一目瞭然で
Reference を基準にしてみると Inherits は Reference より強く
Specialize は Reference より弱いことがわかります。

![](https://gyazo.com/576c961311e8adc5a0aac3b59de59506.png)

Inherits の場合は、まず先に Reference が合成されます。
Robot が Rosie にリファレンスされ、その Local の 0.1 が Metal に合成されます。
Inherits はその Prim を合成するので、 Metal と CorrodedMetal の値が同じになります。

つまり、Specialize とは Inherits と基本同じだが、コンポジションの解決順序が異なるため
大量の Reference を Inherits でまとめて編集できる Inherits に対して、
Reference よりも弱いことから、
結果、「**Reference の空間内で Inherits する**」挙動になるということがわかりました。

最初に説明した通り「Reference より弱いか・強いか」というのが大きな差になることから、
RobotScene.usd にリファレンスする前の Robot.usd では、
Inherits であっても Specialize であってもその結果は変わりません。

## まとめ

以上が Specialize(特殊化)の挙動についてのまとめになります。
思っていたよりもかなり特殊な処理なので、ぱっと使い所が思いつかないですが

以前 Houdini での USD セットアップの継承で説明したように
Reference よりも強いオピニオンであることを利用して、
大量のリファレンスしたアセットをまとめて編集する...というのが Inherits(継承)であるのに対して
サンプルのように、リファレンス先のマテリアルの一部バリエーション違いを作る...といった使い方をすれば良いのかな？と思います。

これにて全 6 種類のコンポジションの動作説明は終了です。
あとは、このコンポジションの解決順序・挙動を踏まえて、シーンをどのように構築するか
考えることになります。
