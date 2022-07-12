---
title: SOLARISでInstancerを使う(2) 編集編
tags:
    - USD
    - SOLARIS
    - Houdini
---

[前回](05_point_instancer.md)PointInstancerを使用して、オブジェクトをばらまくことはできたので  
今回はそのばらまいたオブジェクトを編集していこうと思います。

## 入れ替える

前回のままだと、オブジェクトはランダムに配置されている状態で  
個別の編集はできません。

![](https://gyazo.com/7c8308a876405c1709ed42535be6b0bc.png)

そのオブジェクトを、個別に切り替えたい場合は、 editprototypeノードを使用します。  
  
![](https://gyazo.com/1e371724c17c7a796d86b959c443925f.png)

使い方はかんたんで、Instances に、モデルを入れ替えたいInstanceのパスを入れます。

![](https://gyazo.com/629d70cc383c5bca2e27ef00949026d3.png)

インスタンスのIDは、Instancesの右のこれでを押すことで  
インスタンスオブジェクトをビューポートで選択できるようになるので

![](https://gyazo.com/11b77c96e2e227afea88122ab41c31fa.png)

右クリックでCopy Pathsを押せばPathを取得することができます。

![](https://i.gyazo.com/db8a29dd8bb9759f9f641974f4b3ec60.gif)

あとはReplaceWithのPrototype Index を切り替えると、指定のオブジェクトに  
切り替えることができます。

## 移動・拡大縮小・回転をしたい

![](https://gyazo.com/c891d4af604a23d717655bbb47ea7452.png)

個別のInstanceの位置を調整したい場合は、 modifypointinstancesノードを使用します。

![](https://gyazo.com/f4740a2c801eb26015316e25564853e5.png)

このノードも edit prototypes と同様に、Point Instances で編集したいInstance
を選択します。
あとは、普通のオブジェクトと同様に移動などができるようになります。
なお、Pivotは原点になるようなので、回転や拡大縮小が謎なことになります。  
なので一工夫が必要そうです。

## Primとして切り出す

Instanceではなく、通常のPrimとしてPointInstancerのオブジェクトを使いたい場合は

![](https://gyazo.com/7677b28f91eceaf63d08e36be364d7ae.png)

extractinstancesノードを使用します。

![](https://gyazo.com/b8929697ea96e726835b58667509cdee.png)

Instancesで切り出したいInstanceを選択することで、 Primitive Path に
オブジェクトを切り出すことができます。

![](https://gyazo.com/daf73a0ef169a8cee2242e64f6340e0f.png)

結果、こんな感じになります。

Extractinstancesを使うと、実体のPrimになるので、
後は普通に色々変更を事ができます。

https://www.youtube.com/watch?v=Y3QEK6fV8W4&t=15577s

少し前に公開されていたHoudiniHive SOLARIS では、  
配置されているInstanceをこのノードで切り出して、

![](https://gyazo.com/e92509be9afbf1e0d84d8c59d48ddf96.png)

Pruneで自分以外のノードを消して、SOPModifyにわたすことで、
破壊やSIMをつけて、SOLARISに戻す...といったことを実現していました。

Instanceで大量にばらまきつつ  
Extract Instances でオブジェクトの種類を調整して
Modify Point Instances で、個別に位置調整をして
SOPでこねくり回したい部分は Extract Instances と Prune、SOPModifyのコンボで  
SOP側で編集してSOLARISに戻してレンダリング...

LOPでのレイアウトとSOPでの作り込み　そんな役割分担で  
大規模なシーンの構築などができるようになりそうです。

SOPでのPoints配置諸々も色々やりかたや方針を教えてもらったので
ぼちぼち触っていきたいです。


Instanceingメニュー内のノードの使い方がようやく理解できて満足！