---
title: AssetInfoについて
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 13日目は、
AssetInfoについてとその使い方です。

## AssetInfoとは

[AssetInfo](https://graphics.pixar.com/usd/release/glossary.html#usdglossary-assetinfo)とは、USDで作成されたアセットを管理・識別するために、
**PrimやPropertyに対して指定することができる辞書型のメタデータ** です。

USDは、[Stage/Layer/Spec](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/21_stage_layer_spec/)の回で説明した通り、１つのファイルから構成されているわけではなく
１つのステージに対して複数のファイルによって構成されています。
その大量のファイルの依存関係がどのようになっているのかをAPIを使用して把握することはできますが
かなり深いところを触る必要があり（たとえば、データをサブミットしたりビルドしたりするときに
あるステージの構造を検索しようとすると、かなり大変なことになります。
（いわゆる「できないわけではない」）

AssetInfoをアセットに対して指定しておくと、
レイアウトしているシーン等から
「今のステージがどのようなアセットで構成されているのか」
「今のステージがどういう意図になっているのか」
を、特定すことができるようになります。

## Kitchen_setみてみる

説明を見てもピンとこないので、具体的な例をまず見てみます。

Kitchen_setにある Ball.usd を usdviewで開いてみます。

![](https://gyazo.com/1d050ae2719eeeba4d00f5e46976a4d8.png)

MetaDataタブを確認するとassetInfoに identifier と name が指定されていることがわかります。

![](https://gyazo.com/599388099f37306efc11461c98119b78.png)

Kitchen_set.usd を開き、Ball.usdをペイロードしているPrimをみると
Meta Dataに、 Ball.usd に指定されたAssetInfoが確認できます。

## 指定できる情報

AssetInfoには、そのアセットを管理するための情報がDict型で入っています。

```python
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim('/sample')
prim.SetAssetInfoByKey('hoge','fuga')
print(stage.ExportToString())
```

{{'5611248ba747a0ddc29e649b42b8bd66'|gist}}

Dict型なので、こんな感じでどんな情報でも入れることができますが、
デフォルトでは以下の４つを推奨していて
API側でもその４つがデフォルトで用意されています。

|                          | 型     |                                                                                                                                                                                                |
| ------------------------ | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| identifier               | asset  | コンポジションアークでターゲットにする時のファイルパス<br>いわゆるこのAssetInfoが指定されている（自分自身の）ファイルパス                                                                      |
| name                     | string | アセット名。<br>データベースへのクエリなどに使用                                                                                                                                               |
| payloadAssetDependencies | asset  | 動的に依存関係を検索するときに使用するアセットがペイロードしているアセットを指定する。、<br>事前にペイロードの依存を計算しておくことで、全部をロードしなくてもアセットの依存関係を把握できる。 |
| version                  | string | アセットのバージョンを設定する。<br>ShotGridなどでアセットを管理している場合などに、追跡するのに使える                                                                                         |

以上４つです。
アセットのバージョン管理などは、ShotGridなどといったデータベースを使用することが多いとおもいます。
ですが、そういったデータベースとは別に、アセット自体にも管理用の情報（name や version)は持たせたいはずです。
デフォルトで推奨されているAssetInfoは、まさにそういった用途で使用するものになっています。

> asset型は、アセット（USDファイル、テクスチャを含む）を指すためのパスを表す
> 参考：[USD は手書きするもののアトリビュート](https://qiita.com/takahito-tejima/items/ee0332bfb5c9baed3b09#%E3%82%A2%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%83%88)

## AssetInfoを活用する

どのような情報が保存されているかはわかりました。
これを実際にどう活用していけばいいのか、

「今のステージがどのようなアセットで構成されているのか」

を、AssetInfoを使用して調べてみます。


### Flattenした場合のAssetInfo

USDには、現在のStageを「Flatten」することで、すべてのコンポジションアークを実行した結果の
シーングラフを出力する機能があります。
Flattenしてしまうと、コンポジションの情報もすべて解決された状態になるため、

![](https://gyazo.com/82d53c910005559e69c338d092d3b0b4.png)

Compositionをみても、Layerは存在しません。
つまり、Flattenする前、どのようなLayerによって構成されていたのかは
Compositionから追うことはできません。

![](https://gyazo.com/8a37db52b438ecc1f7bd00e780f63249.png)
Flatten前

![](https://gyazo.com/5c2847686be38266b7376602140ff26b.png)
Flatten後

ですが、AssetInfoをみてみると
どのAssetがどこに置いてあるなんのアセットなのか、Flattenした後でもわかります。

> Kitchen_setにはversionははいっていないが、
> 入っていればFlattenした段階でどのバージョンのアセットかもわかる...ということになる

### 依存解決のためのAssetInfo

もう１つが、アセットの依存解決です。
最初に説明した通り、現在のStageがどのようなコンポジションによって構成されているかは
PCP等を使用すれば検索することは可能ですが、
複雑なStageをPCPを使用して依存を調べるとすると、かなり大変です。
さらに、「あるレイアウト済のシーンに配置しているアセットを収集したい」ということがあった時
使用するアセットを調べるためだけに巨大なシーンを開くのは効率的ではありません。

そういったときに、PayloadをアンロードにしてStageを開いて（アセットをロードしていないので、配置情報だけのロードで済む）
使用しているアセット情報だけを取得したい、、、ということはよくあると思います。
そういう場合に、AssetInfoは使用することができます。

```python
from pxr import Usd,Sdf,Ar

loadFile = "D:/Kitchen_set/Kitchen_set.usd"
stage = Usd.Stage.Open(loadFile,Usd.Stage.LoadNone)

# DefaultResolverを取得
resolver = Ar.GetResolver()

def traverse(prim):
    if prim.HasAssetInfo():
        # Kitchen_set.usdのPathから、アセットのフルパスを取得
        info = prim.GetAssetInfo()
        path = info['identifier'].path
        resolvedPath = Ar.ResolvedPath(loadFile)
        print(resolver.CreateIdentifierForNewAsset(path,resolvedPath))

    for child in prim.GetFilteredChildren(Usd.PrimIsActive & Usd.PrimIsDefined & ~Usd.PrimIsAbstract):
        # LoadNoneの時は、Traverse関数を使用するとPayloadsのPrimは取得できないので
        # 再帰で子Primを探す
        traverse(child)
        
traverse(stage.GetDefaultPrim())
```

例としてKitchen_setで使用しているアセットの一覧を取得した場合。
StageはLodNone（アンロード状態）で開きます。
この状態だと、アセットの依存を取得できません。
ですがPrimのAssetInfoを見てidentifierやnameが指定されていれば、そこからデータを収集することができます。

上の例だと、アセットの中に別のアセットへのコンポジションがあると検索できませんが、
あらかじめ使用しているアセットをpayloadAssetDependenciesにセットしておけば
すべてのレイヤーをアンロードにした状態でも、そのStageを構成するアセットの一覧を取得することができます。

> 備考
> Resolverは別の記事にてまとめ予定です。

## TF_DEBUGでのAssetInfoの確認

[USD・Hydra の環境変数と仲良くなる](https://qiita.com/takahito-tejima/items/c065c7cd5c3a7abe14f1#tf_debugsdf_asset) の記事にて、アセットの解決時に
どのように変化していくかを確認するためのDebug設定が紹介されていましたので
合わせて確認してみると、USDコンポジションの解決がどようにされているか確認できるので
試してみると面白そうです。

## まとめ

以上AssetInfoについてとその使い方でした。
アセットを管理するのにAssetInfoはとても有効です。
Houdini19に新しく追加されたComponentBuilderでは、このAssetInfoを自動で追加してくれますので
レンダリングを実行する前に依存を解決してデータチェックをしたい時、
ShotGridでアセットを管理するときにアセット側にも情報を持たせたい時など
ぜひとも活用してください。