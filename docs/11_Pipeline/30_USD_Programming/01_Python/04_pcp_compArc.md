---
title: PCPでコンポジションアークの構造を解析・編集対象を取得する
---

このサイトのほかページでも何度か説明している通り、USDは複数のファイルを合成して
１つのシーングラフに構築することができます。

![](https://gyazo.com/e2d4b11418ae5af3a10c27a1e9531b1a.png)

たとえば、毎度おなじみキッチンセットでみてみます。

このキッチンセットは、 Kitchen_set.usd を開いた段階だとこのように１つのシーングラフに
なっていますが、

![](https://gyazo.com/8f504a6f53f8f40b0384fac654508624.png)

このusdは１つのusdではなく、複数のUSDをコンポジションアークを使用して１つのusdに合成して
上のようなキッチンセットになっているわけです。
(この１つのアセットを構成するusdファイルは 228ファイルありました)

では、この複雑なファイルの組み合わせでできあがったシーングラフが

1. どのようなファイルによって構成されているのか
2. どのファイルを編集すればどこに書き込まれるのか

を調べるにはどうしたらよいのだろう？？？というのが今回の記事の内容です。

### サブレイヤーの場合

コンポジションが「サブレイヤー」によって合成されている場合は、

```python
for spec in prim.GetPrimStack():
    print(spec.layer)
```

指定のPrimのPrimStackを取得して、そのPrimを構築するためのSpecを取得する方法つかったり、
編集対象を取得して切り替える場合は、以前に説明を書いた[EditTargetでLayerを操作する](01_editTarget.md)を利用して
編集レイヤーを取得してTargetを切り替えて編集する...という手を使うことができます。

しかし、サブレイヤー以外のコンポジションの場合はこの手段を使うことができません。

では、この場合はどうしたらよいかというと
今まで使っていたUsdネームスペースのAPIでは実行できませんが、 **PcpAPI** を使うことで実現することができます。

## PCPとは

PCPとは **「Prim Cache Population」** の略で、これが何をするものかというと、
**コンポジションアーク（シーン合成）を司る機構** になります。

あるPrimがシーンディスクリプション（usdファイルすべて）がこのPrimにどのような影響を与えているか
どのように構成されているのかを、PCPを使用することで知ることができます。

文章だけだとわかりにくいので具体的にみてみます。

![](https://gyazo.com/7e114528268de0918d4857c9fabcffed.png)

サンプルのキッチンセットから、冷蔵庫アセットを選択します。
このPrimがどのようなファイルによって構成されているのかPCPをつかって調べてみます。

調べるには、DumpToIndex を使って Index 情報を Dump してみます。

```
Node 0:
    Parent node:              NONE
    Type:                     root
    DependencyType:           root
    Source path:              </Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1>
    Source layer stack:       @d:/Kitchen_set/Kitchen_set.usd@,@anon:0000027614F5B360:Kitchen_set-session.usda@
    Target path:              <NONE>
    Target layer stack:       NONE
    Map to parent:
        / -> /
    Map to root:
        / -> /
    Namespace depth:          0
    Depth below introduction: 0
    Permission:               Public
    Is restricted:            FALSE
    Is inert:                 FALSE
    Contribute specs:         TRUE
    Has specs:                TRUE
    Has symmetry:             FALSE
Node 1:
    Parent node:              0
    Type:                     reference
    DependencyType:           non-virtual, purely-direct
    Source path:              </Refridgerator>
    Source layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator.usd@
    Target path:              </Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1>
    Target layer stack:       @d:/Kitchen_set/Kitchen_set.usd@,@anon:0000027614F5B360:Kitchen_set-session.usda@
    Map to parent:
        /Refridgerator -> /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
    Map to root:
        /Refridgerator -> /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
    Namespace depth:          5
    Depth below introduction: 0
    Permission:               Public
    Is restricted:            FALSE
    Is inert:                 FALSE
    Contribute specs:         TRUE
    Has specs:                TRUE
    Has symmetry:             FALSE
```
長いので全部は貼りませんが、
IndexをDumpするとこのような情報が表示されます。

このPrimIndexは、シーンディスクリプションのうち、ある特定のPrimに主張（Opinion）をしている
Indexで、「あるPrimに影響を与えているもの」を取得するために使用します。

これを見ると、このPrimがどのようにコンポジションされているのか。
コンポジションする要素（Opinion）がどうなっているのかを見ることができます。

例えば、 Typeを見ればどのコンポジションを使用しているのか
Source layer stack を見ればどのレイヤーかどうか、
Target Path は、そのレイヤーのどのPrimが対象か　など。

### Map To Parent / Map To Rot

または、 Map to Parent という情報もここから取得できます。

![](https://gyazo.com/512c736aa34652db07e5a174774ec081.png)

たとえば、Node1 のレイヤーを見てみると、冷蔵庫Primは /Refridgerator というPrimが
あります。
それがリファレンスされると、

![](https://gyazo.com/322781bde3a7663a33117e76a55dc07b.png)

Target Path のネームスペースにマップされている... というのがわかります。

このように、PCPを見ることで、
複数のレイヤーをコンポジションして最終的なPrimが出来上がるまで
どのようなコンポジションが行われているのか取得できているのがわかるわけです。

!!! info
    PcpPrimIndexはコンポジション機能だけを担うもので、シーングラフの親子関係（階層構造）
    は持ちません。
    Pcp自体は、あるPrimに誰が意見を持っているかを提供しているだけで
    **最終的な値はなにか とか、シーングラフのオブジェクトの型であったりスキーマ** は
    UsdPrimの役割として分離されています。

## PCPNodeRef

このDumpした情報をみると「Node」というキーワードが出てきます。

このNode (PcpNodeRef)は、コンポジションの木構造を表現するためのノードで、

たとえば、

1. どのレイヤーか
2. どのようにコンポジションしていくか
3. どのネームスペースにマップするか

という
**あるPrimを構成する「主張」** を持ちます。

この構造を視覚化してみます。

```python
from pxr import Usd,Pcp
stage = Usd.Stage.Open(r"D:\Kitchen_set\Kitchen_set.usd")
prim = stage.GetPrimAtPath("/Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1")
index = prim.GetPrimIndex()
index.DumpToDotGraph("D:/graph.dot")
```
まず、構成をしらべたいPrimを選択して、PrimIndexを取得します。

Indexの DumpToDotGraph を使用するとGraphVizのフォーマットで情報を出力できるので、
それを使用してグラフを表示してみると、

![](https://gyazo.com/5f2f50f295856a245262f85d87f65e9f.png)

このようになります。
rootNode から複数のコンポジションアークが木構造で表されてるのがわかります。

コンポジションの構造が木構造になっているので、再帰を使用することで

```python
def traverse(node):
    # コンポジションタイプ
    print(node.arcType) #CompositionArc
    print(node.path) #SdfPath
    print(node.site) #Layer + SdfPath
    print(node.GetRootNode()) # RootNode
    layer = node.layerStack.layers[0] # Layer取得
    print(layer)
    for child in node.children:
        traverse(child)
traverse(rootRef)
```

Primを構成する各レイヤーを検索することができます。

## 編集ターゲットを取得する

では、このPcpを使用してあるPrimを構成するレイヤーの１つを取得して
変更できるようにしてみます。
基本的には[EditTargetを使用する](01_editTarget.md)と同じように、UsdEditTargetを作れればよい
ので、PcpPrimIndexとPcpNodeRefを使用してEditTargetを取得します。

```python
et = Usd.EditTarget(rootRef.layerStack.layers[0],rootRef)
stage.SetEditTarget(et)
stage.DefinePrim(～～～)
```

取得方法はこのとおり。
PcpNodeRefからlayerStackを取得し、構成するレイヤーを取得します。
このlayerStackは、サブレイヤーの場合はこのStackにレイヤーが積まれた状態になっています。
そこからSdfLayerオブジェクトを取得することができます。

そして、レイヤーのネームスペースを取得するためPcpNodeRefをEditTargetに渡します。
あとは、SetEditTarget で、編集ターゲットをステージに渡せばOKです。

## まとめ

UsdのAPIを使用すれば、コンポジションアークを構築したり
シーングラフを管理したりできましたが
このUsdAPIからコンポジションを実際にどのように管理しているのかというのが
Pcpを見ることで理解できました。

![](https://gyazo.com/129e378b6ad3eb75beaf300a264aa135.png)

usdviewでPrimを選択しているときに表示される この Compositionや Layer Stackなどの情報も
今までの自分の理解だと Primから頑張って取得する。。。ぐらいしか思いつかなかったですが
PrimIndexからPcpNodeRefを使用することで
コンポジションの木構造を取得して表示してるんだなー　というのがよく分かるようになりました。
(むしろここに表示されてるTreeはPcpPrimIndexから取得できるNodeRefのツリーだった)

これを利用すれば、より複雑なコンポジションであっても
ターゲットレイヤーを選択して編集対象にして、usdを更新する...みたいなツールも
簡単に作ることができそうです。