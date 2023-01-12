---
title: SOLARISのPayloadの使い方
tags:
    - Houdini
    - USD
    - SOLARIS
description: SolarisでPayloadを使う方法
---

USD のペイロードは、ロードをしないことを選択できるリファレンスです。
巨大なシーンを構築する場合、すべてのデータをロードすると開くのに時間がかかってしまうので
編集したい部分をロードせずにシーンを開きたいということが発生します。
そのため、モデルデータをロードする場合はリファレンスではなくペイロードを使用した上で
アンロードにしておくほうが多いです。

そんなペイロードを SOLARIS 上で使用する方法などをまとめておきます。

![](https://gyazo.com/5471484816a8848d69f619a0afdf1246.png)

Payload でファイルを読む場合は、Payload ノードを使用します。

![](https://gyazo.com/ff84522e36b05a77f9afd286cf643307.png)

使用すると、Payload とあわせて LoftPaylaodInfo ノードが作成されます。

![](https://gyazo.com/8a0c4ef8c70040d94655de0dd12bf75d.png)

この LoftPayloadInfo は、アンロードしているモデルの BoundingBox を表示するための
パラメーターを追加するノードです。

![](https://gyazo.com/2817f9f1760931125496e999f1e57996.png)

ノードがある場合、こんな感じでアンロード状態でも BoundingBox が表示されます。

![](https://gyazo.com/5c4e9e5defa29910d44a09e3bb9f010d.png)

Payload ノードは Reference ノードのパラメーター違いです。
Reference Type が Payload File の場合、Payload 扱いになります。

PrimitivePath にペイロードする Prim を指定し、
FilePattern に USD ファイルパスを書きます。
これでロードは完了です。

## アンロードする

![](https://gyazo.com/8883082db52690de9c39b9df9510fbe6.png)

Payload のロード・アンロードは Scene Graph Three で制御します。
デフォルトだとロードされますが、

![](https://gyazo.com/b214ea0d90835a7fc3d6a45945b1c7c9.png)

Manage viewport load masks の Load all payloads in viewport を OFF にすることで
デフォルトをオフにできます。

![](https://gyazo.com/4cf7346227eddd29968bffd053fe5672.png)

「L」のチェックをオンにすると、チェックされたモデルのみロードできます。

### ロード状況を保存・呼び出す

![](https://gyazo.com/18b9553321e99d1958ee184a03d7117c.png)

設定した Payload は、 Save viewport load masks で保存できます。

![](https://gyazo.com/2ba3b5685902ea318f83e3a21e059599.png)

名前をつけると

![](https://gyazo.com/6ca779ef499d3def6b8c817e3a075df7.png)

プリセットを保存できます。

## Configure Stage で編集

SceneGraphTree 以外でも、ConfigureStage を使用すると
ノードで Payload のロード・アンロードを変更できます。

Load all payloads in viewport を ON にした上で、

![](https://gyazo.com/33045cb8768d1c0d3d144f58aa3fa755.png)

ConfigureStage ノードを追加します。
Configure ノードを使用すると、

-   {{markdown_link('population_mask')}}
-   {{markdown_link('usd_stage_load_rules')}}

を、SOLARIS 上で設定・使用できます。

![](https://gyazo.com/35380489c544140dfe178bb23b1c66cd.png)

今回は、 UsdStageLoadRules を使用します。
Load Primitives を Set primitives to load に変更します。
そして、Load Paths にロードしたい PrimitivePath を指定します。
複数ある場合はスペースをはさむことで複数指定できます。

Add and Remove Primitives to Load にすると、現在の設定に対して削除と追加が可能で
Set Primitives to Load だと、現在の指定はすべて廃棄して変更します。
Load all primitives だと、問答無用ですべてロードするようになります。

![](https://gyazo.com/986a0741d6c8a1bf2da9d7f46c546a45.png)

ConfigureStage を使用する場合は、
Switch を組み合わせることで、Payloads の ON/OFF をを切り替えるなどが可能になます。
