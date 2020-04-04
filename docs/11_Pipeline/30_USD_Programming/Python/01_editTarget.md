---
title: EditTargetでLayerを操作する
---

[LayerStageについて](../../01_USD/04_layer_stage.md)の説明にもあるとおり
USDは１つのusdファイルだけではなく、複数のusdファイルが「コンポジションアーク」と呼ばれる
合成機能によって１つのファイルとして構築されている...と説明をしました。

![](https://gyazo.com/a3e2e76893dcdc9304cce43ed48ef32c.png)

つまりは、なにかのUSDファイルをOpenしてできあがったStageは
複数のUsdファイル（レイヤー）によって構成されていて
その個別のファイル単位でPrimの元になっている「Spec（主張）」をもった
大量のファイルの塊でもあるわけです。

通常のファイルの場合は、ファイルを開いたら
そのファイルを編集して保存すれば良いですが
上に書いたとおりUSDは大量のファイルの塊なので
「どのファイル（レイヤー）」を「どのように編集するか」というのも
作成することができます。

なので、今回はUSDの指定のレイヤーをPythonから操作する方法を
説明しつつ、USDのStageとLayerについて改めて調べてみようと思います。

## サンプル

サンプルUSDファイルとして、下の３つを作成します。

```usd
#usda 1.0

(
    subLayers = [
        @layerA.usda@
    ]
)

def "testPrim"
{
    string hoge = "Root"
}
```
Root.usda

```usd
#usda 1.0

(
    subLayers = [
        @layerB.usda@
    ]
)

def "testPrim"
{
    string hoge = "layerA"
    int val = 20
}
```
layerA.usda

```usd
#usda 1.0

def "testPrim"
{
    string hoge = "layerB"
    int val = 10
}

def "addTest"
{
}
```
layerB.usda

![](https://gyazo.com/a48c5f5153ea9df1022e7125f66b595c.png)

構造はこんなかんじのシンプルな構造を用意します。

## 開く

```python
from pxr import Usd, UsdGeom, Sdf
stage = Usd.Stage.Open(r"D:\work\usd_py36\usd\rootLayer.usda")
```
まずは、上のUSDファイルを開きます。

![](https://gyazo.com/5f66e9f4fe98f81081560b245eb45c1b.png)

構造はこんなかんじで、

testPrimのアトリビュートは、

hoge = "Root"
val  = 20

という値を取得することができます。

ここで取得できるのは、コンポジションアーク（合成）されて構築された結果になります。

## 編集する

というわけで、開くことができたので中のファイルを編集してみます。

### 開いているファイルを編集する

```python
UsdGeom.Xform.Define(stage, "/hoge")
stage.GetRootLayer().Save()
```
USDの編集はこのようにStageを経由して編集を行います。
これは今のステージに /hoge Prim を作る操作をしています。
そして保存時は「GetRootLayer」でレイヤーを取得して保存します。

この場合の「レイヤー」とは、usdaファイルのことになります。

![](https://gyazo.com/c3aca6dc695414b1be879752776705ca.png)

図に表すとこういう状態です。
GetRootLayerは現在のStage上のRootLayer(開いたusda)を取得することができます。

### 指定のレイヤーを編集する

![](https://gyazo.com/8609e16fec4bd6d6b8d4365afde9bf1c.png)

では、RootLayerではないレイヤーを編集したい場合はどうすればいいでしょうか。
このあたりを理解するには「EditTarget」を理解する必要があります。

EditTargetは、現在のStage内の「編集対象のレイヤー」へのアクセスをできるようにするための
クラスです。

```python
target = stage.GetEditTarget()
# 編集ターゲットのusdaPathを確認
print(target.GetLayer().identifier)
# 保存
target.GetLayer().Save()
```
現在の編集ターゲットはGetEditTargetで取得することができます。
この場合、GetEditTarget = RootLayer になっています。

```python
targetB = stage.GetEditTargetForLocalLayer(Sdf.Find('d:/work/usd_py36/usd/layerB.usda'))
stage.SetEditTarget(targetB)
# 試しに追加
stage.DefinePrim("/addTest")
# そして保存
targetB.GetLayer().Save()
```

では、RootLayer以外を編集したい場合はどうするかというと
SetEditTargetで編集したいLayerを指定してあげればOKです。

上はDefinePrimでPrimを定義していますが、

```python
print(targetBPrim.attributes['val'].default)
# 10
targetBPrim.attributes['val'].default = 20
print(targetBPrim.attributes['val'].default)
# 20
```

こうすると、指定のレイヤーのアトリビュートを書き換えることができます。

![](https://gyazo.com/a9bb18ca571cc7fd9a18769b4586c4a2.png)

ざっくりと書くとこんな感じで
stageのEditTargetを経由して、編集したいLayerを取得して
Layerオブジェクトを利用して編集を行います。

注意点は、ここで書き換えたり編集しているものは「最終的な結果ではない」ということです。
あくまでも、最終的なコンポジションされた結果ではなく
コンポジションされる前の「Spec（主張）」を書き換えているので、
自分よりも強い主張をもつレイヤーやプリム、アトリビュートがある場合は
いくら書き換えても最終的なPrimには反映されないので
注意が必要です。

### Specとは

```python
targetBPrim = targetB.GetLayer().GetPrimAtPath('/testPrim')
```
EditTargetの GetLayerを使用した場合、
通常の stage.GetRootLayer() とは違いGetPrimAtPathでPrimを取得すると

![](https://gyazo.com/2df47f719f8dda18e0a699556ed5c80d.png)

PrimSpecというオブジェクトになります。

```python
help(stage.GetPrimAtPath("/testPrim"))
```

![](https://gyazo.com/af3e54f1385994c4b0a992a40198ebfa.png)

stage経由の場合は、 Primオブジェクトになります。

ここでいうところのSpecというのがなにかというと、
各レイヤーに記述された「合成される前の主張」です。

PrimSpecの場合は「こういうPrimを作りたい！！」という主張で
この段階では他のPrimSpecとの兼ね合い（コンポジション優先順位）によって未解決
の状態になります。

### Sdf.Find のトラップ

ここで盛大にハマったのが「Sdf.Find」という関数です。
この関数、PixarのAPIドキュメント（C++）には存在しません。
print(dir(Sdf.Find(～～)))のようにしても、ものによって使える関数などが異なり
こいつはいったいなんなんだよ！！！と思っていました。

が、 help関数を使用してみるとなんとなく実態がわかります。

```python
help(Sdf.Find('d:/work/usd_py36/usd/layerB.usda'))
```
試しにHelp関数を使用してSdf.FindのHelpを見てみます。

![](https://gyazo.com/e3ca0b5d2a6e388f94590a2cb40abbb8.png)

Sdf.Find表示になっているものの実態はなにかというと、Layerだったり

```
print(targetB.GetLayer().GetPrimAtPath('/testPrim'))
```
こうしたときの
![](https://gyazo.com/5852f350fb8d60bc6d509d3a5f3b547a.png)
このばあいは
```
help(targetB.GetLayer().GetPrimAtPath('/testPrim'))
```
こうすると

![](https://gyazo.com/e64d952293197949e1bd3d0f03c9bcc0.png)

こうなったりと、オブジェクトの実体は別のものになっているようです。
~~わかりにくすぎるよPythonnnnnn!!!!!~~

なので、GetEditTargetForLocalLayer の引数として渡している
```python
Sdf.Find('d:/work/usd_py36/usd/layerB.usda')
```
は、Sdf.Layerオブジェクトを渡しているということになります。


### このアトリビュートはどこで「主張」されているのか？

各レイヤーが合成され、最終的なPrimが出来上がりますが
ではそのPrimが「どこのレイヤーで定義されているのか」というのを調べたくなることがあります。

サンプルの hoge は layerA と layerB で定義されていることがわかりますが
これをPythonで確認してみます。

```python
prim = stage.GetPrimAtPath("/testPrim")
# Primのアトリビュートを取得
attr = prim.GetAttribute("hoge")
print(attr.Get())
# アトリビュートのStack（主張をつんだもの）
stack = attr.GetPropertyStack(Usd.TimeCode())

# 一番強い主張
print(stack[0].default)
print(stack[0].layer)
```
指定のプロパティがどのような主張を持っていて結果どうなったかを
見たい場合はｐGetPropertyStackを確認します。

![](https://gyazo.com/c74967e595daa075bddcfef8e9b1bb2f.png)

stack は、こんなかんじにSdf.Findの配列になっていて
この場合のSdf.Findの中身は

![](https://gyazo.com/602aebc46d2cfd4313256e5c6a38f3df.png)

AttributeSpecになります。
Specなので、ここのアトリビュートは「主張」になります。

これを見ると、 rootLayer layerA layerB の３つに主張があり
rootLayerが最も強い主張をもっていて、最終的にコンポジションされた結果になっているのが
わかります。

GetPropertyStack で Usd.TimeCode() を渡しているのは、
アトリビュートはPrimと違いアニメーションのキーフレームのようにフレームごとに
あるかどうかが異なります。
なので、タイムコードをわたして、指定のタイムコードでのStackを取得しています。

### レイヤーに「主張」があるかどうか

PrimからSpecを探すのはできましたが、今度は指定レイヤーにSpecがあるかどうか
調べたいこともあります。

```python
target = stage.GetEditTargetForLocalLayer(Sdf.Find('d:/work/usd_py36/usd/layerB.usda'))
layer = target.GetLayer()
primSpec = layer.GetPrimAtPath("/testPrim")
# このPrimのAttribute
# 定義があるか
print('hoge' in primSpec.attributes)
attrSpec = primSpec.attributes['hoge']
print(attrSpec)
# 値を確認
print(attrSpec.default)
```

ここのあたりもC++とPythonとで全く挙動が違っていて
APIドキュメントが全く参考にならず苦戦しました。

まずは、EditTargetを経由して
編集したいレイヤーを取得します。

取得したら、定義の有無を確認するために primSpecからAttributeSpecを取得します。
AttributeSpecの取得方法がかなり特殊で
attributes はDict型になっているので、取得したいアトリビュートを引数とすることで
AttributeSpecを取得できます。

つまりは、指定のレイヤーで主張があるかを確認するためには
'name' in spec.attributes のようにして、Dictにアトリビュート名が含まれているか
確認すればOKです。

## まとめ

いままではEditTargetを知らずに、なんとなく開いているファイルを編集すればOKという
イメージを持っていましたが、
EditTargetを使用することで、開いている以外のレイヤーもPhotoShopのレイヤーを
編集するようにコントロールできることがわかりました。

いままでの GetRootLayer() での編集というのは、言ってしまえば
PhotoShopの一番上に新規でレイヤーを作成して、そこに絵を書き足しているような
操作だったわけですね。

これで、できることの幅などが大きく変わりそうです。
USDすごい。

このあたりの検証をしていたときのJupyterNotebookが
[EditTargetで指定レイヤーを操作](https://fereria.github.io/reincarnation_tech/60_JupyterNotebook/USD/USDEditTarget/)
でした。

やはり日々研究していかないとUSDを有効活用できないなーと思いました。
がんばろう。

あと、今回やったあたりはAPIドキュメントが全く参考になりません。
ひたすら pprint.pprint(dir(hogehoge)) したりしながら関数をさがしてまわってた週末でしたが
help(hogehoge)すればちょっとだけまともなHelpを見れるという知見を得たので
しばらくはこれを利用してPythonでの操作方法を全力で調べていこうと思います。