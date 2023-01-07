---
title: Kind と Model と ModelHierarchy
description: USDでのシーンアッセンブリ時のルールについて
---

今回は、 {{markdown_link('13_create_usdAssets_01')}} 記事内でほんの少し触れた **「Kind」** についてを見ていきます。

## Kind とは

USD における Kind とは、

> Kind is a reserved, prim-level metadatum whose authored value is a simple string token
> 公式 Docs から引用

公式の用語集をみると、Prim 単位で指定することができるメタデータの一種とのことです。
Kind 自体はシンプルな文字列（Token）で表されています。

```
def Xform "SamplePrim" (
    kind = "component"
)
{
}
```

Kind を指定すると、このようになります。
Kind は他のメタデータと同じように Prim に対して指定することができます。
この Kind は、後述する **ModelHierarchy** という概念に応じて指定の役割を持っていて
その役割を Prim に対して指定することができます。

## Model Hierarchy

では、この Model Hierarchy とはなんでしょう。

USD は、多数のレイヤーを複雑に組み合わせることで１つの巨大なシーングラフを
構築することができます。
そうして出来上がったシーングラフはとても巨大で、PrimType や名前だけで
その巨大で複雑なシーングラフをコントロールするのは非常に大変です。
その巨大なシーングラフを、管理可能な単位に分割するために
この「Kind」と呼ばれるラベルを付けて、管理するための概念が
この ModelHierarchy となります。

シーングラフ内の Prim のうち、 **重要な目次に当たる重要な Prim**、
それは **シーン内に配置されたモデル部分** であったり、
**それらを分類ごとにまとめるグループ** であったり
**パブリッシュされるアセットの RootPrim であったり**
そういった階層を構築する上で重要となる箇所にインデックスとして
決められたルールに沿った Kind を指定し、階層構造を作成します。

この Model Hierarchy によって定義されている Kind が
**model group assembly component subcomponent**
の 5 つです。
この５つを指定のルールに則って使用することで、
巨大な構造をコントロールすることができます。

この Model Hierarchy で定義されている Kind とそのルールを
順番に見ていきます。

## Kind の種類

### Model

まず、すべての基本となるのがこの「 **Model** 」です。
モデルとは、 Assembly Group Component などの各種類の基本となるもので
これらの要素を抽象化したものが Model になります。

![](https://gyazo.com/f733b4db896dffc799cda986c51d83b5.png)

関係図を表すとこのようになっています。
Model とは、Hierarchy を構成する上での抽象化された概念
（すべての Kind は Model に属する）
なので、Kind では model は指定しません。

そのかわり、このあと説明する Kind（Assembly Group Component）は
すべて Model に属したものという意味になります。
そのため、Assembly Group Component が指定された Prim に対して
IsModel() を実行すると、True になります。

では、それぞれの Kind を見ていきます。

### Assembly

Assembly は、Publish されたセット、または Publish されたアセットへのリファレンスに
対してつけられます。
この「Publish されたアセット」というのが、
一般的に言われる「 **使用可能な状態になっている（リリース済）アセット** 」のことで
BG だったり、小物類だったりと、アーティストが Shot ワーク時に扱うモデルを
指すのかと思います。

![](https://gyazo.com/9728de9268c4e4a9a00962c0ab4c7b2a.png)

キッチンセットをみてみると、RootPrim 以下にあるアセット名の Prim
（DefaultPrim）がこの assembly が指定された Prim になります。

### Group

次に Group。
これは名前の通り複数の Prim をまとめるためのものです。
上の Assembly も Group の一種ですが、Assembly は Publish 用のアセットのルートを定義
するものなのに対して、こちらはシンプルに Model Hierarchy の階層化するために
存在するシンプルなものです。

![](https://gyazo.com/987075c47963fc1f3dbfb47cd39d848a.png)

キッチンセットの ####\_grp となっている Prim が

![](https://gyazo.com/c86374d6a3bb5424cd928436d905299c.png)

この group にあたります。

### Component

次に Component。
これは、このアセットを構成する最小要素のアセットにあたります。

![](https://gyazo.com/c7ff9afc7f22901a4fdcf3b8ad724657.png)

キッチンセット上にリファレンスでロードされている小物アセットが

![](https://gyazo.com/b0258f68034165b310ef0f4cab2757ad.png)

component になっています。
この component は「leaf model」と呼ばれていて、
Model Hierarchy の概念では末端の構成要素になります。

この Component 以下には別の Model は存在しません。

![](https://gyazo.com/103a5fc6d8ee97eacfdfabcc91472994.png)

なので、Component 以下（リファレンスでロードされている各アセット以下）の Xform プリムは
Mesh をまとめるためのグループの階層として利用されていても

![](https://gyazo.com/95c3f1c8a1a18adc70fccf235696d636.png)

子のプリムには Kind は指定されていません。

Component の指定はどこで行うと良いのか？というと、
この /Kitchen_set 以下の Prim に対して行うのではなく

![](https://gyazo.com/01772bcfc0d2ed26bb40bac180e4a214.png)
![](https://gyazo.com/636805213c366a1b7ed315f77fc44ba7.png)

リファレンス元のレイヤーの defaultPrim に対して指定します。
このようにすると、リファレンスでロードするレイヤーが「leaf model」
ある Model Hierarchy を構成する末端の要素として機能するようになります。

### Model Hierarchy のまとめ

まとめると、 Model Hierarchy の概念で、アセット内のシーングラフを
書き表すとこうなります。

![](https://gyazo.com/a9f8631c65db94a9368d1be69e4e3e6b.png)

末端にあたる Component Prim には、アセットを構成する細かいアセットが
リファレンスでロードされています。

USD で複数の細かなアセット（Component、リファレンスでロードされるレイヤー）を
配置して１つの大きな背景などとしてレイアウトしたい場合は、
TopNode に Assembly(Publish されて、利用される１つの背景アセット)としてレイヤーを
用意します。
そして、区画や、タイプごとに Group を作ってまとめ
実際に配置するモデル（Component）をロードする...
それが、シーンを構築する上での　基本構造になります。

### 活用方法

![](https://gyazo.com/f562caa3aaf7c2a43fbd6751f1bb771d.png)

この Kind を利用することでどのようなことが可能になるかというと、
例えば「USDView」の PickModel で「Models」に変更すると、

![](https://i.gyazo.com/2d2cb6209886ec9ebc67abf1ae70e75f.gif)

モデルをピックするときに Shape の Prim ではなく、Kind が指定された Prim を選択する...
といったことが可能になります。
この選択している Prim は「Component」が指定されている つまりはレイアウトで配置する
階層をビューポート上でピックする...といったような
指定の Prim に対して追加機能を入れたりすることができます。

## 拡張する

ここまでで、kind の指定を利用した ModelHierarchy 構築を説明していきましたが
ここまででてきた assembly group component だけでは足りなかったり
もう少し詳細な分類をつけたいということも出てくるかと思います。

たとえば、背景の中でも建物と小物で別の分類を作りたいとか
Assembly の中でも、背景とキャラとプロップとで別の種類を指定しておきたい
（そうすることでシーンを Traverse するときに効率化したい）
などなど。

その場合は、必要に応じて kind の指定を拡張することができます。
拡張するには、USD の Plugin を作成します。

### Plugin を作る

作るには、Plugin を作成します。

```
{
  "Plugins": [
    {
      "Info": {
        "Kinds": {
          "chargroup": {
            "baseKind": "assembly",
            "description": ""
          },
          "charprop": {
            "baseKind": "component"
          },
          "newRootKind": {}
        }
      },
      "Name":"CustomKind",
      "Type": "resource"
    }
  ]
}
```

内容は Help の内容を持ってきたものです。
この json を plugInfo.json として保存して、
USD 以下 **plugin/usd/####/resources/plugInfo.json** に保存します。

指定方法はかんたんで、ベースになる kind を指定して、新しい Kind 名をつけるだけです。
上の例だと、 assembly つまり、パブリッシュするアセットのルートにつける指定に
char であったり bg であったり prop であったりといった、より細かい分類を指定した
kind を追加しています。

同様に、 leaf model 実際に配置しているモデルに charprop というより詳細な指定を
した kind を追加しています。

プラグイン作成は以上で完了です。
実際に動いているか確認してみます。

```python
from pxr import Usd
api = Usd.ModelAPI(usdviewApi.prim)
api.SetKind('chargroup')
```

試しに usdview で開いたモデルに、作成した Kind をセットします。

![](https://gyazo.com/341b1b7995beea7768286c64b517cd12.png)

セットできました。
ただし、このセットは Plugin で追加していなくても追加が可能です。

ですが、

```python
usdviewApi.prim.IsGroup()
```

セットした Prim に対して IsGroup()を実行すると、 True が帰ってくるようになります。
これは、ベースとなる kind に assembly を指定しているので
group に属する assembly に属しているため、IsGroup で True になっています。

このように、kind を拡張することで
より細かく作成しているアセットの階層をコントロールできる
（検索して必要な Component に行きつける）
ようになることがわかりました。

## まとめ

はじめはどのように扱うかわかりにくかった Kind でしたが、
PrimType や名前ではなく別のタグで
シーン全体をトラバースし、コントロールできるようにすることで
複雑で巨大なシーングラフを構築するときに、大きな助けになる機能であるとわかりました。

また、この Kind や ModelHierarchy の概念（定義）を理解することは、
USD のシーングラフをどのように体系化させ、定義し、実際に構築するかを考える上で
重要な指標になると思いました。
