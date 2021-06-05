---
title: CompArc(5) 特殊化（Specialize）
tags:
    - コンポジションアーク
    - USD
    - USD基本
---

コンポジションの中でもかなり特殊すぎて、詳しく構造を調べていなかった
Specializeを紹介しようと思います。

コンポジションの強さ（LIVRPS）では最も弱いのがSpecializeです。
その挙動は継承（Inherits）とよく似ていますが
重要な違いとして Specialize/Inherits とReference 比べてオピニオンが
強いか弱いか...という違いがあります。
文字だけだとわかりにくいので、
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Specializes
USD GlossaryのSpecialize にかかれているサンプルを使用して
図で説明してみようと思います。

## Specialize

![](https://gyazo.com/0929bd6be687af78762b20911fbf22e9.png)

Robot.usd と RobotScene.usd の２つのレイヤー内のコンポジションは
このようになっています。

![](https://gyazo.com/6cbd36de900b63e8030620da6484f76e.png)

まず、サンプルをusdviewで表示するとこのようになります。
```
            # specialize roughness...
            float inputs:specularRoughness = 0.2
```
Robot.usd の CorrdedMetal の specularRoughness に、 0.2 とある通り
最終的な結果を見ても 0.2 になっています。

![](https://gyazo.com/3e1854cc497c91cadf44f563ad6aab86.png)

Specialize は Reference よりも弱いオピニオンなので、
Compositionを確認すると、Robot.usdでまずSpecializeで合成され
その合成されたあとに Reference されていることがわかります。

![](https://gyazo.com/a1a62d7f8e46c2a629a4c4a1d46e4eb9.png)

コンポジションの順番を追記すると、このようになります。

![](https://gyazo.com/1a31e11a753fa0cfe381f4ef22a47752.png)

ここで注目なのが、Robot.usdの CorrodedMetal.specularRoughness です。

![](https://gyazo.com/e5a6133b3ebdf21ee9793f2beffa0392.png)

diffuseGainは、Specializeのおかげで Metal.diffuseGainの値が合成されていますが
specularRoughness は、CorrodedMetalにオピニオンがあるため、その値が優先され 0.2になります。


## Inheritsとの比較

比較のためにInheritsに変更するとどうなるか確認してみます。

![](https://gyazo.com/db15a41b4a4e67e53d46a858a966df36.png)

Inheritsの場合は、最終的な合成結果が変わっているのがわかると思います。

![](https://gyazo.com/1992a9c4e6d3d2ba6e9ae9530b593b29.png)

Compositionを比較してみると、一目瞭然で
Referenceを基準にしてみると InheritsはReferenceより強く
SpecializeはReferenceより弱いことがわかります。

![](https://gyazo.com/576c961311e8adc5a0aac3b59de59506.png)

Inheritsの場合は、まず先にReferenceが合成されます。
RobotがRosieにリファレンスされ、そのLocalの 0.1 がMetalに合成されます。
InheritsはそのPrimを合成するので、 Metal と CorrodedMetalの値が同じになります。

つまり、SpecializeとはInheritsと基本同じだが、コンポジションの解決順序が異なるため
大量のReferenceをInheritsでまとめて編集できるInheritsに対して、
Referenceよりも弱いことから、
結果、「**Referenceの空間内でInheritsする**」挙動になるということがわかりました。

最初に説明した通り「Referenceより弱いか・強いか」というのが大きな差になることから、
RobotScene.usd にリファレンスする前のRobot.usd では、
 Inherits であっても Specialize であってもその結果は変わりません。

## まとめ

以上が Specialize(特殊化)の挙動についてのまとめになります。
思っていたよりもかなり特殊な処理なので、ぱっと使い所が思いつかないですが
https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/13_create_usdAssets_01/#_11
以前HoudiniでのUSDセットアップの継承で説明したように
Referenceよりも強いオピニオンであることを利用して、
大量のリファレンスしたアセットをまとめて編集する...というのがInherits(継承)であるのに対して
サンプルのように、リファレンス先のマテリアルの一部バリエーション違いを作る...といった使い方をすれば良いのかな？と思います。

これにて全6種類のコンポジションの動作説明は終了です。
あとは、このコンポジションの解決順序・挙動を踏まえて、シーンをどのように構築するか
考えることになります。
