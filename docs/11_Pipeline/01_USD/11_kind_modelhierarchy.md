---
title: Kind と Model と ModelHierarchy
---

今回は、[SOLARISでUSDアセットを作ろう](https://fereria.github.io/reincarnation_tech/10_Houdini/11_SOLARIS/13_create_usdAssets_01/)記事内でほんの少し触れた **「Kind」** についてを見ていきます。

## Kindとは

USDにおけるKindとは、

> Kind is a reserved, prim-level metadatum whose authored value is a simple string token
> 公式Docsから引用

公式の用語集をみると、Prim単位で指定することができるメタデータの一種とのことです。
Kind 自体はシンプルな文字列（Token）で表されています。

```
def Xform "SamplePrim" (
    kind = "component"
)
{
}
```

Kindを指定すると、このようになります。
Kind は他のメタデータと同じように Prim に対して指定することができます。
この Kind は、後述する **ModelHierarchy** という概念に応じて指定の役割を持っていて
その役割を Prim に対して指定することができます。

## Model Hierarchy

では、この Model Hierarchyとはなんでしょう。

USDは、多数のレイヤーを複雑に組み合わせることで１つの巨大なシーングラフを
構築することができます。
そうして出来上がったシーングラフはとても巨大で、PrimTypeや名前だけで
その巨大で複雑なシーングラフをコントロールするのは非常に大変です。
その巨大なシーングラフを、管理可能な単位に分割するために
この「Kind」と呼ばれるラベルを付けて、管理するための概念が
この ModelHierarchy となります。

シーングラフ内のPrimのうち、 **重要な目次に当たる重要なPrim**、
それは **シーン内に配置されたモデル部分** であったり、
**それらを分類ごとにまとめるグループ** であったり
**パブリッシュされるアセットのRootPrimであったり**
そういった階層を構築する上で重要となる箇所にインデックスとして
決められたルールに沿ったKindを指定し、階層構造を作成します。

この Model Hierarchy によって定義されているKindが
**model group assembly component subcomponent**
の5つです。
この５つを指定のルールに則って使用することで、
巨大な構造をコントロールすることができます。

この Model Hierarchy で定義されている Kind とそのルールを
順番に見ていきます。

## Kindの種類

### Model

まず、すべての基本となるのがこの「 **Model** 」です。
モデルとは、 Assembly Group Component などの各種類の基本となるもので
これらの要素を抽象化したものが Model になります。

![](https://gyazo.com/f733b4db896dffc799cda986c51d83b5.png)

関係図を表すとこのようになっています。
Modelとは、Hierarchyを構成する上での抽象化された概念
（すべてのKindはModelに属する）
なので、Kindでは model は指定しません。

そのかわり、このあと説明するKind（Assembly Group Component）は
すべてModelに属したものという意味になります。
そのため、Assembly Group Component が指定されたPrimに対して
IsModel() を実行すると、True になります。

では、それぞれのKindを見ていきます。

### Assembly

Assemblyは、Publishされたセット、またはPublishされたアセットへのリファレンスに
対してつけられます。
この「Publishされたアセット」というのが、
一般的に言われる「 **使用可能な状態になっている（リリース済）アセット** 」のことで
BGだったり、小物類だったりと、アーティストがShotワーク時に扱うモデルを
指すのかと思います。

![](https://gyazo.com/9728de9268c4e4a9a00962c0ab4c7b2a.png)

キッチンセットをみてみると、RootPrim以下にあるアセット名のPrim
（DefaultPrim）がこの assembly が指定されたPrimになります。

### Group

次にGroup。
これは名前の通り複数のPrimをまとめるためのものです。
上の Assembly も Groupの一種ですが、AssemblyはPublish用のアセットのルートを定義
するものなのに対して、こちらはシンプルに Model Hierarchy の階層化するために
存在するシンプルなものです。

![](https://gyazo.com/987075c47963fc1f3dbfb47cd39d848a.png)

キッチンセットの ####_grp となっているPrimが

![](https://gyazo.com/c86374d6a3bb5424cd928436d905299c.png)

この group にあたります。

### Component

次にComponent。
これは、このアセットを構成する最小要素のアセットにあたります。

![](https://gyazo.com/c7ff9afc7f22901a4fdcf3b8ad724657.png)

キッチンセット上にリファレンスでロードされている小物アセットが

![](https://gyazo.com/b0258f68034165b310ef0f4cab2757ad.png)

component になっています。
このcomponent は「leaf model」と呼ばれていて、
Model Hierarchyの概念では末端の構成要素になります。

このComponent以下には別のModelは存在しません。

![](https://gyazo.com/103a5fc6d8ee97eacfdfabcc91472994.png)

なので、Component以下（リファレンスでロードされている各アセット以下）のXformプリムは
Meshをまとめるためのグループの階層として利用されていても

![](https://gyazo.com/95c3f1c8a1a18adc70fccf235696d636.png)

子のプリムには Kind は指定されていません。

Componentの指定はどこで行うと良いのか？というと、
この /Kitchen_set 以下の Primに対して行うのではなく

![](https://gyazo.com/01772bcfc0d2ed26bb40bac180e4a214.png)
![](https://gyazo.com/636805213c366a1b7ed315f77fc44ba7.png)

リファレンス元のレイヤーのdefaultPrim に対して指定します。
このようにすると、リファレンスでロードするレイヤーが「leaf model」
あるModel Hierarchyを構成する末端の要素として機能するようになります。

### Model Hierarchyのまとめ

まとめると、 Model Hierarchy の概念で、アセット内のシーングラフを
書き表すとこうなります。

![](https://gyazo.com/a9f8631c65db94a9368d1be69e4e3e6b.png)

末端にあたる Component Primには、アセットを構成する細かいアセットが
リファレンスでロードされています。

USDで複数の細かなアセット（Component、リファレンスでロードされるレイヤー）を
配置して１つの大きな背景などとしてレイアウトしたい場合は、
TopNodeに Assembly(Publishされて、利用される１つの背景アセット)としてレイヤーを
用意します。
そして、区画や、タイプごとにGroupを作ってまとめ
実際に配置するモデル（Component）をロードする...
それが、シーンを構築する上での　基本構造になります。

### 活用方法

![](https://gyazo.com/f562caa3aaf7c2a43fbd6751f1bb771d.png)

この Kind を利用することでどのようなことが可能になるかというと、
例えば「USDView」のPickModelで「Models」に変更すると、

![](https://i.gyazo.com/2d2cb6209886ec9ebc67abf1ae70e75f.gif)

モデルをピックするときにShapeのPrimではなく、Kindが指定されたPrimを選択する...
といったことが可能になります。
この選択しているPrimは「Component」が指定されている つまりはレイアウトで配置する
階層をビューポート上でピックする...といったような
指定のPrimに対して追加機能を入れたりすることができます。

## 拡張する

ここまでで、kindの指定を利用したModelHierarchy構築を説明していきましたが
ここまででてきた assembly group component だけでは足りなかったり
もう少し詳細な分類をつけたいということも出てくるかと思います。

たとえば、背景の中でも建物と小物で別の分類を作りたいとか
Assemblyの中でも、背景とキャラとプロップとで別の種類を指定しておきたい
（そうすることでシーンをTraverseするときに効率化したい）
などなど。

その場合は、必要に応じて kind の指定を拡張することができます。
拡張するには、USDのPluginを作成します。

### Pluginを作る

作るには、Pluginを作成します。

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
内容はHelpの内容を持ってきたものです。
このjsonを plugInfo.json として保存して、
USD以下 **plugin/usd/####/resources/plugInfo.json** に保存します。

指定方法はかんたんで、ベースになるkindを指定して、新しいKind名をつけるだけです。
上の例だと、 assembly つまり、パブリッシュするアセットのルートにつける指定に
charであったりbgであったりpropであったりといった、より細かい分類を指定した
kindを追加しています。

同様に、 leaf model 実際に配置しているモデルに charprop というより詳細な指定を
した kind を追加しています。

プラグイン作成は以上で完了です。
実際に動いているか確認してみます。

```python
from pxr import Usd
api = Usd.ModelAPI(usdviewApi.prim)
api.SetKind('chargroup')
```
試しにusdviewで開いたモデルに、作成したKindをセットします。

![](https://gyazo.com/341b1b7995beea7768286c64b517cd12.png)

セットできました。
ただし、このセットはPluginで追加していなくても追加が可能です。

ですが、
```python
usdviewApi.prim.IsGroup()
```
セットしたPrimに対して IsGroup()を実行すると、 Trueが帰ってくるようになります。
これは、ベースとなる kind に assembly を指定しているので
group に属する assembly に属しているため、IsGroupでTrueになっています。

このように、kindを拡張することで
より細かく作成しているアセットの階層をコントロールできる
（検索して必要な Component に行きつける）
ようになることがわかりました。

## まとめ

はじめはどのように扱うかわかりにくかった Kind でしたが、
PrimTypeや名前ではなく別のタグで
シーン全体をトラバースし、コントロールできるようにすることで
複雑で巨大なシーングラフを構築するときに、大きな助けになる機能であるとわかりました。

また、このKindやModelHierarchyの概念（定義）を理解することは、
USDのシーングラフをどのように体系化させ、定義し、実際に構築するかを考える上で
重要な指標になると思いました。