---
title: HDA の作り方
---

## HDA とは？

HDA とは「Houdini Digital Asset」の略で、作成したノードを使い回しするために  
Export して、Tab キーのショートカットから呼び出せるようにできる機能の事。

Maya でいうなら Export したものを Reference で読み込めるようにする機能に近いが、  
どちらかというとプログラミングの関数化に近い気がします。

## Subset の作成

HDA を作成するには、まず Subnet を作成します。

![](https://gyazo.com/5753221616601561c2c52449453f47dd.png)

Subnet は、ノードネットワークを再利用することができるようにするための機能。

![](https://gyazo.com/1f93ef3703bafc71a7e4f521edfd0d03.png)

たとえば、こんな感じのノードがあった場合、Subnet 化すると

![](https://gyazo.com/149be445878e79771fe510a9a6230fa1.png)

１つのノードにまとめることができる。

イメージとしては、これはローカル関数に近い。  
Houdini のシーン内のみで使いまわしができるのがこの Subnet なのかな？

## パラメーターを外に出す

subnet 化は、いわゆるカプセル化というやつで  
１つの機能を１つのノードとしてまとめることで、中の処理を見えなくすることができる。  
ただ、それだとパラメーターの調整がいちいち Subnet 内に入らないとできないので  
Subnet 側にパラメーターを表示するようにする。

![](https://gyazo.com/92c2b911a6e90e5206887c7b82ff3797.png)

Subnet のノードを選択して、歯車マーク →Edit Parameter Interface...  
をクリックする。

そのあと表に出したいパラメーターのノードを Subnet 内で選択し、

![](https://gyazo.com/9e9e468408ff0054364482da007c1934.png)

外に出したいアトリビュートを、EditParameterInterface の Existing Parameters の枠の中に D&D する。

![](https://gyazo.com/5ef9b5a0b30cb40381f74a1bbc4b40ea.png)

D&D すると、Subnet にパラメーターが追加される。

![](https://gyazo.com/aa9b222fd8822ac7c69c952a45fac03c.png)

すると、グリーンマークになり、

![](https://gyazo.com/44cfda4cc29af3dc0b11810efcdde025.png)

Subnet にパラメーターが表示される。

## Export

![](https://gyazo.com/b5cb78864b0c7ca9743f7d731420510a.png)

準備ができたら、HDA を出力をする。  
HDA にしたい Subnet を選択 → 右クリックで　 Create Digital Asset...を選択する。

![](https://gyazo.com/28deb0aea86fa82661673741b76e98c5.png)

Operator Name を指定して、HDA ファイルの出力パスを指定する。  
とりあえずはデフォルトで。

最後に、出力する HDA の詳細情報を指定する。  
今回はスキップ。  
いわゆる配布物である HDA の使い方の Docs やら、アイコンなどの情報をここで指定する。

![](https://gyazo.com/5de8d72f17805901513406c53af1a89a.png)

いろいろありますが、とりあえずはデフォルトにしておきます。

![](https://gyazo.com/6ce359ffa4c444bc55dd523f182db946.png)

出力が完了すると、Tab→Labem 名を入れると、作成した HDA のノードを作成することができます。

## HDA の管理

HDA のノードを右クリック →Show in Asset Manager...を選択すると、

![](https://gyazo.com/cb703f64ddb254d03829ca009ef096b9.png)

作成した HAD を確認することができる。

### 設定の編集

![](https://gyazo.com/c9b9584384017dd3160c75155faecab4.png)

HDA 出力時の設定は、Asset Manager の　 Type Properties から編集することができる。

### HDA の中のノードを隠蔽する

![](https://gyazo.com/eee83b4505a322df55fca2ad35e0cff4.png)

ノードの中身を開かせたくない場合は「Create Black box assets...」を作成する。

![](https://gyazo.com/532c38fbc9a73227e211a1df29302edb.png)

ブラックボックス化されたノードの場合、ノードの中を見ようとすると PermissionDenied が表示され、  
中をみることができない。

## 参考

- https://www.kickbase.net/entry/houdini-create-hda#HDA%E4%BD%9C%E6%88%90%E6%89%8B%E9%A0%86
