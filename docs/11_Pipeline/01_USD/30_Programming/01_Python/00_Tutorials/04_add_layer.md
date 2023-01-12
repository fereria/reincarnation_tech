---
title: 0から始めるUSDPython(4) サブレイヤー
tags:
    - USD
    - USDPythonTutorial
    - AdventCalendar2022
description: Pythonでサブレイヤーの編集レイヤーを作る
---

これまでに、{{markdown_link('01_start_usdpython')}} では、
すでにあるファイルを開き、編集して保存するというのをやりました。
この時、変更は「上書き」しているので
当然のことながら変更によって以前の状態は破壊されてしまいます。

そうではなく、たとえば「元のデータは残しつつ、変更を上書きしたい」といったことがやりたくなるはずです。
USD ではコンポジションと呼ばれるファイルを合成する仕組みが用意されているので
このコンポジションの合成方法の１つ「サブレイヤー」を利用することで
編集を別のファイルに対して行うということが可能です。

ので、1 回目でやった編集を、別ファイルに対して行うようにしてみます。

## サブレイヤーとは

サブレイヤーとは、USD のコンポジション（複数のファイルを合成するしくみ）の１つで
複数のファイルを階層を維持した状態で 1 つにマージするような合成方法です。
{{markdown_link('comp_arc_sublayer')}}

![](https://gyazo.com/76645304065930109d3b22a64b46ac43.png)

階層を維持した状態で合成するので
今回のように、もともとあるファイルに対してなにか変更を加えるような場合に使用できます。

## Stage と Layer

コンポジションを理解する場合には、「Stage」と「Layer」というキーワードを
理解する必要があります。

<img src="https://gyazo.com/98c664089ff5e4257f21cae0a15dd7b2.png" width=200>

USD では、USD ファイルのことを「Layer（レイヤー）」と呼びます。
そして、その Layer を合成（組み合わせた）結果出来上がるシーングラフを「Stage（ステージ）」と呼びます。
この Stage と Layer の関係は、
PhotoShop におけるレイヤーとその結果キャンバスに表示される絵の関係と同じです。
PhotoShop のレイヤー 1 つだけでは最終的な絵が決まらないように、
USD のレイヤーも「最終的にできあがるものの材料の１つ」であって最終的な値とは限りません。

![](https://gyazo.com/12a713ed7a2c86b99314d2fd14ae47b6.png)

今回のように、元ファイル（Kitchen_set.usd）は残しつつ編集をしたい場合なら
edit.usd を追加して、変更は edit.usd 側にすれば
やりたいことは達成できます。

## 編集用レイヤーを作る

まず、編集用レイヤーを作成します。

```python
from pxr import Usd,Sdf

layer = Sdf.Layer.FindOrOpen("./edit.usd")
if not layer:
    layer = Sdf.Layer.CreateNew("./edit.usd")

layer.subLayerPaths = ["D:/Kitchen_set/Kitchen_set.usd"]
layer.Save()
```

USD のレイヤーは、「SdfLayer クラス」を使用して作成します。

![](https://gyazo.com/4a6260c682972e895d487cf5adc8700e.png)

これは「Layer」なので、＝ USD ファイルです。

FindOrOpen すると、すでにファイルがある場合はロードし、なければ None を返します。
ので、見つからない場合は CreateNew をして新規作成をします。

そして、このレイヤーに対して subLayerPaths で
上書きしたいファイルのレイヤーを指定して、保存します。

これでベースになる USD ファイルができました。

ですが、これだけだとレイヤーを作っただけ（＝素材ができただけ）で、合成して
最終的に欲しいシーングラフができたわけではありません。
ので、最終的な結果のシーングラフを開くために、Usd.Stage.Open でステージを開きます。

```python
stage = Usd.Stage.Open(layer)
```

![](https://gyazo.com/a6c4ab6c55953f9c9f6c82dd44911a6d.png)

開くと、このようになります。
Usd.Stage.Open で開くと、引数で渡したレイヤーが「EditTarget（編集対象のレイヤー）」となり
ステージを開くことができます。
これで、シーンを開きつつ別のレイヤー（USD ファイル）に編集できるようになりました。

```python
prim = stage.GetPrimAtPath("/Kitchen_set/Props_grp/North_grp/SinkArea_grp/CupCBlue_2/Geom/Cup")
# Attributeを変更する: 例の場合 Cupを非表示にする
prim.GetAttribute("visibility").Set("invisible")
layer.Save()
```

これで、初回と同じコードを実行してみます。
実行して Save しても、 Kitchen_set.usd のファイルは変更されません。
かわりに、 edit.usd ファイルは保存されました。

```python
print(layer.ExportToString())
```

試しに、 layer.ExportToString() で、中の記述を確認すると、

```
#usda 1.0
(
    subLayers = [
        @D:/Kitchen_set/Kitchen_set.usd@
    ]
)

over "Kitchen_set"
{
    over "Props_grp"
    {
        over "North_grp"
        {
            over "SinkArea_grp"
            {
                over "CupCBlue_2"
                {
                    over "Geom"
                    {
                        over "Cup"
                        {
                            token visibility = "invisible"
                        }
                    }
                }
            }
        }
    }
}
```

このように表示されます。
この edit.usd は、見ての通り Cup の visibility を invisible にする
という情報のみが入っています。
そして、ベースになるレイヤーは subLayers にファイルパスが入っているのがわかります。

つまり、 Usd.Stage を介して、
**EditTarget になっているレイヤーに対して編集している**
というのがわかったかと思います。

## GetRootLayer とは

{{markdown_link('01_start_usdpython')}} で、上書き保存するときに

```python
stage.GetRootLayer().Save()
```

をしていたのは、

![](https://gyazo.com/320c80e840ecc2ac56d5fcf778865dd5.png)

Stage は「複数のレイヤーを組み合わせた結果出来上がったシーングラフ」であり
ファイルではありません。
ので、上書き保存するには開いたレイヤーを取得する必要があります。

UsdStage で開いたレイヤーは「RootLayer」と呼ばれています。
ので、開いたファイルをそのまま保存したい場合は RootLayer を取得し
Save する必要がありましたので GetRootLayer().Save()
のようになっていました。

## EditTarget の変更

UsdStage の編集対象である「レイヤー」は、UsdStage で開いたレイヤーになっていることが
わかりましたが、当然ながら開いているレイヤーとは別のレイヤーを編集したくなる子もあるでしょう。
そういった場合は、UsdStage の EditTarget を変更することで
編集ターゲットを変えることができます。

```python
layer = Sdf.Find('d:/Kitchen_set/Kitchen_set.usd')
target = stage.GetEditTargetForLocalLayer(layer)
stage.SetEditTarget(target)
```

たとえば、Kitchen_set.usd を編集したい場合。

Stage の GetEditTargetForLocalLayer を使用して、ターゲットを取得し、
SetEditTarget で UsdStage のターゲットを変更します。

![](https://gyazo.com/158a8ac7714f657ef1d7eb5d45c3e5a5.png)

すると、RootLayer とは別のレイヤーを編集対象にできます。

この状態で、

```python
prim = stage.GetPrimAtPath("/Kitchen_set/Props_grp/North_grp/SinkArea_grp/CupCBlue_2/Geom/Cup")
# Attributeを変更する: 例の場合 Cupを非表示にする
prim.GetAttribute("visibility").Set("invisible")
```

このように編集すると、Kitchen_set.usd を編集することになります。

## まとめ

今回は、サブレイヤーを使用して別のレイヤーに対して編集をする方法をやっていきました。
サブレイヤーを使用することで
元のファイルを変更することなく、非破壊でパラメーターを変更できました。
アーティストが作業したデータに対して何か決められた処理をしたい場合も
（編集したり Prim を足したり）
サブレイヤーを使用すれば、アーティストの作業と Python を使用してなにかしたい場合も
今回の方法でできるようになります。
