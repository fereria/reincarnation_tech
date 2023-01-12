---
title: UsdCollectionを使おう
---

USDの「Collection」とは、MayaのSetsと似た機能で
USDシーン内のオブジェクトを識別するためのリレーションシップ機能を提供します。
つまりは、これをつかうとPrimをグループでまとめるだけではなく
Namespaceに関係なくオブジェクトをコントロールできるようになります。

## やってみる

まずはサンプルを用意します。

![](https://gyazo.com/3448d8a4f77c8f03839fbc65ba82abd6.png)

![](https://gyazo.com/14ee2d0a9604441a41f8292c981fb119.png)

このようなシンプルなレイヤーを用意します。

```python
# Collectionを作る
collection = stage.DefinePrim("/collectionSample")
collectionName = "sampleCollection"
api = Usd.CollectionAPI.Apply(collection,collectionName)
```
そして、Collectionを作成したいPrimに
UsdCollectionAPIを利用してCollectionを適応します。

```
#usda 1.0

def "collectionSample" (
    prepend apiSchemas = ["CollectionAPI:sampleCollection"]
)
{
}
```
適応できました。
ですが、これだけだとまだからのSetを用意したにすぎないので
Primを指定してみます。

```
api.IncludePath(Sdf.Path("/World/SamplePrims/Cube"))
```

```
#usda 1.0

def "collectionSample" (
    prepend apiSchemas = ["CollectionAPI:sampleCollection"]
)
{
    prepend rel collection:sampleCollection:includes = </World/SamplePrims/Cube>
}
```
追加されました。
指定したPrimへのリレーションに、IncludePathが追加されたのがわかります。

Collectionを追加すると、追加したPrimに対して「collection」のNamespace以下に
プロパティが作成されます。
そして、このプロパティ名にはCollection名（上の例なら sampleCollection ）が付き
そのコレクションごとのプロパティを追加するためのNamespaceが提供されます。
プロパティ以下にCollection名が入ることで、
１つのPrimに対して複数のCollectionが追加できるようになるわけですね。

## Primの取得

### Collectionに入れたPrimの取得方法

```python
print(api.GetIncludesRel().GetTargets())
```
IncludePathの指定は、リレーションで定義されているので、
CollectionAPIのGetIncludesRelでリレーションを取得すると
かんたんにCollectionに含まれているPrimを取得することができます。

### ExcludePathとExpansionRule

上の例だと、IncludePathを指定することでCollectionにPrimを入れることができました。
ですが、IncludePathとして指定したPrimだけではなく
その子Primも含めて取得したい場合もありますし、
その子Primのうち「除外したいPrim」も指定したいことがあるかとおもいます。

そうした時はExcludePath（除外指定）と、ExpansionRule（どのように展開するか）
を指定した上で、ComputeMembershipQueryを使うことで
Collectionに含まれるPrimを取得することができます。

```python
api.ExcludePath(Sdf.Path("/World/SamplePrims/Cube/ExcludeCube"))
```
まずは、サンプルのレイヤーのうち、Cube/ExcludeCube以下を除外するようにします。

```python
expansionRule = api.CreateExpansionRuleAttr()
expansionRule.Set("expandPrims")
```

そしてExpansionRuleを指定します。
これが、指定Prim以下の子すべてなのかだったり、そのPrimのみ指定だったりといった
選択をどのように展開するかを指定するアトリビュートになります。

| name                     |                                                 |
| ------------------------ | ----------------------------------------------- |
| explicitOnly             | IncludePathのみで子Primは含めない               |
| expandPrims              | IncludePath以下の子Primも含める                 |
| expandPrimsAndProperties | Includepath以下の子Primとアトリビュートも含める |

選択肢はこの３つです。

次に、このCollectionを利用してPrimを取得します。

```python
query = api.ComputeMembershipQuery()
# expandPrimsで指定されてるので、IncludePath以下にありExcludeに含まれないPrimがリストされる
print(Usd.CollectionAPI.ComputeIncludedObjects(query,stage))
```
apiからComputeMembershipQueryで、検査くるためのQueryを取得します。
そして、それを利用してComputeIncludeObjectsを実行すると
引数で指定したstage内のうち、Collectionに該当するPrimを取得できます。

```
[Usd.Prim(</World/SamplePrims/Cube>), Usd.Prim(</World/SamplePrims/Cube/pCube1>), Usd.Prim(</World/SamplePrims/Cube/pCube3>)]
```
![](https://gyazo.com/fe048cc982d07021c48b918b820adb89.png)

結果、ExcludePathで指定したExcludeCubeとpCube2のPrimは除外され
それ以外の結果が取得できました。

```python
expansionRule.Set("explicitOnly")
```
これを explicitOnlyに変えると、
```
[Usd.Prim(</World/SamplePrims/Cube>)]
```
子以下は含まれなくなりました。

```python
expansionRule.Set("expandPrimsAndProperties")
```
最後に、Propertiesまで展開するとどうなるかというと
![](https://gyazo.com/3fa9e7e8a4be40f01fd55ed5c0ef2b76.png)
Attributeまでふくめてすべて取得することができました。

このExpansionRuleは、MembershipQueryの
```python
print(query.GetAsPathExpansionRuleMap())
```
ExpansionRuleMapで確認することができて、このRuleMapに従って
ステージ内のPrimを「コレクション」することができます。

## PathがCollectionに含まれるかどうか調べる

以上のやりかたでCollectionに含むPrimを取得することができましたが
あるSdfPathがCollectionに含まれているかを知りたい...といったケースも
発生するかとおもいます。

その時は、ComputeMembershipQueryを利用して
```
# 引数で指定したSdfPathがCollectionに含まれるか
print(query.IsPathIncluded("/World/SamplePrims/Cube/pCube1"))
# 除外されたPrimの場合
print(query.IsPathIncluded("/World/SamplePrims/Cube/ExcludeCube/pCube2"))
```
このようにPathが含まれるかをチェックすることができます。

## Houdini

コードとusdaだけだとわかりにくいので、同様のことをHoudiniSOLARISで試してみます。

![](https://gyazo.com/ea449364d77085c342e3ae1b56705b17.png)

LOPにはCollectionノードが存在しているので、ノードを作成します。

![](https://gyazo.com/934b59f8405d7ed22e736fc8fe5a3fae.png)

DefaultPrimitivePathは、Collectionを追加したいPathを指定します。
そしてその下にCollectionに入れる条件を指定します。

![](https://gyazo.com/9c3eb94e8a0ba589601b3aa97f37b55e.png)

上の例だと、青枠をCollectionに入れて、そのうち赤枠部分は除外
ExpansionRuleは Cube以下の子Prim全てを入れるようにしました。

Collectionが作れているかをPruneノードを使用して確認してみます。
Pruneは、 PrimitivePattern で指定したPrimを非表示状態にします。

![](https://gyazo.com/8fb21f9fbae89638f9149ae92d170ee9.png)

PrimitivePatternにはCollectionを指定することもできるので、
カーソルボタンを押してCollectionを指定すると

![](https://gyazo.com/b7044d9587b5d23aee303157589f5062.png)

結果。
Collectionに含まれている pCube2 以外のPrimが非表示になりました。

最初に説明したとおり、IncludePathとExcludePath、そしてExpansionRuleによって
Collectionに含まれるPrimが計算され
その結果によってPruneノードが実行されました。
Pruneにも同じような TargetPrimitivesの指定がある（Collectionを作る機能もある）のですが
挙動・指定方法は、USDのCollectionと同様になります。

## まとめ

Collectionを使用すれば、IncludePath/ExcludePath/ExpansionRuleを組み合わせることで
単純なリレーションよりも、より手軽にステージ内のPrimにアクセスできるように
なることがわかりました。

これを使って、指定のPrimに自動で処理をさせたり
自分のやりたいシーングラフを表現できるようになるので、よりいっそうUSDで
できることの幅が広がりそうです。

https://fereria.github.io/reincarnation_tech/60_JupyterNotebook/USD/USDCollectoinSample2
Pythonでの操作方法は↑のNotebookで色々試してるので参考にしてください。
