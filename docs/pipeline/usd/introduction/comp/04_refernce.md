---
slug: /usd/reference
title: リファレンスについて
description: USDのコンポジションアークの『R』「リファレンス」について
sidebar_position: 4
tags:
    - コンポジションアーク
    - USD
    - USD基本
---

コンポジションアークの説明もこれでラスト。  
最後はリファレンスとペイロードについて。

## リファレンスとは

まず、コンポジションアークの「リファレンス」とはどういう機能かというと  
ざっくり言うと、別のレイヤー（usd ファイル）のルート直下にある指定プリム以下を  
指定のプリムに接続する機能のことを言います。

![](https://gyazo.com/013f4cb003fa0e6feaa142788f5e4a3a.png)

まず、このような usd ファイルを準備します。

```
#usda 1.0
(
    defaultPrim = "RootGrp"
)

def "RootGrp"
{
    def Sphere "Sphere"{}
}
```

中身はこんな感じ。  
defaultPrim が指定された Sphere1 つだけのファイルです。  
このファイルをリファレンスで読み込んでみます。

```
#usda 1.0

def "Grp"{
    def "RefA" ( prepend references = @ref_data.usda@){}
    def "RefB" ( prepend references = @ref_data.usda@){}
    def "RefC" ( prepend references = @ref_data.usda@){}
}
```

試しに同じファイルを複数読み込んでみます。

![](https://gyazo.com/990e77d5c23040ba88b97b64b82c7e32.png)

結果、3 つ Sphere ができあがってることが分かります。

![](https://gyazo.com/8accdae3dd2e3a8370cdca656e59b62a.png)

どういう状況になっているかというと、  
リファレンス先で定義している prepend referencd = ～～～ つきのプリムが  
リファレンスしたいファイルの defaultPrim に置き換わるようになります。

上の例でいうと、 RootGrp が RefA という名前になって  
RootGrp 以下のプリムがすべてマージされ、

![](https://gyazo.com/97e00b38e377338af778aed9e9fca250.png)

こうなります。（RefB,C も同様）

今まで説明したサブレイヤーや継承、バリアントと大きく違うのは  
指定がプリムではなくレイヤー（USD ファイル）指定であること。  
構造すべてを合成するのではなく、あるプリムに対して別のレイヤーを合成するというのが  
異なります。

## ペイロードとは

実質最後のコンポジションアークですが、これは実質リファレンスと動作は同じで、  
あるプリムに対して指定のレイヤーのデフォルトプリムを接続します。

では、リファレンスとはなにが違うかというと

![](https://gyazo.com/43db8e78a0f37b8f7fd1446280071e55.png)

usdview の Help を見るととてもわかりやすいのですが  
--unloaded フラグの Help にある「Do not load payloads」の通り  
ペイロードで読まれているものは、指定のフラグ付きでロードした場合「アンロード状態」  
でシーンが開きます。

![](https://gyazo.com/dac0a1b3f1d246ef268be5cbd99359cc.png)

試しに、キッチンセットを --unloaded フラグ付きで読み込んでみると  
なにも表示されません。

```
#usda 1.0
(
    defaultPrim = "Ball"
    upAxis = "Z"
)

def Xform "Ball" (
    assetInfo = {
        asset identifier = @./assets/Ball/Ball.usd@
        string name = "Ball"
    }
    kind = "component"
    payload = @./Ball_payload.usd@</Ball>
)
{
}
```

何故かというと、キッチンセットのアセットの途中にかならずペイロードでのロードが  
含まれているからです。

なぜこんな機能があるのかというと、  
複雑なステージになると、1 ステージで数百・数千の USD で構成されることもあるそうで  
「ステージ内のある 1 つのレイヤーのみ調整したい」  
という場合、全シーンをロードすると時間がかかってしまいます。

ので、ペイロードフラグを入れているものはロードしない状態にしておき  
開いてから、作業をしたいアセットのみ表示してから  
保存する...のようなワークフローを可能にしているらしいです。

## 指定のプリムをロードする

リファレンスは、指定のレイヤー内のルート以下プリムを指定する必要があります。  
特に指定されていない場合は「デフォルトプリム」をロードするようになります。

では、デフォルトプリムの指定がされていない場合はどうなるかというと、

![](https://gyazo.com/ed9c0857b1ac88c4ebc7aa6fbf3a933c.png)

エラーが表示され、

![](https://gyazo.com/3bc2968690f8c40fae7ea4412e040911.png)

正しくロードできなくなりました。  
これは、どのプリムをリファレンスすれば良いかが分からなくなってしまうからです。

その指定する方法の 1 つは、デフォルトプリムの指定でしたが

![](https://gyazo.com/c1617250c696477d8202344a3622bb25.png)

では、このような  
1 つのレイヤーにいろいろなプリムが入っていて  
それらを選択して読み込みたい場合はどうすれば良いか。

```
#usda 1.0

def "Grp"{
    def "RefA" ( prepend references = @ref_data.usda@</RootSphere>){}
    def "RefB" ( prepend references = @ref_data.usda@</RootCube>){}
    def "RefC" ( prepend references = @ref_data.usda@</RootCylinder>){}
}
```

その場合は、このように、

```
</PrimName>
```

読み込みたいレイヤー指定の後に SdfPath を指定することで  
指定の SdfPath のプリムをリファレンスできます。

## 他のコンポジションとの組み合わせ（バリアントとの組み合わせ）

コンポジションアークのプリムとアトリビュート合成の解決順序は  
Local Inherits Variants Reference の順なので  
リファレンスは 4 番目になります。（実質一番弱い）

では、今回のリファレンスも他と組み合わせたときにどうなるかを確認してみます。

```
#usda 1.0

def "testPrim" (
    variants = {
        string hogehoge = "Sphere"
    }
    prepend variantSets = "hogehoge"
)
{
    variantSet "hogehoge" = {
        "Sphere" {
            def "RootSphere"(prepend references = @ref_data.usda@</RootSphere>){}

        }
        "Cube" {
            def "RootCube"(prepend references = @ref_data.usda@</RootCube>){}

        }
        "Cylinder" {
            def "RootCylinder"(prepend references = @ref_data.usda@</RootCylinder>){}
        }
    }
}
```

前回のバリアントに対して、リファレンス構造をつけてみます。

![](https://i.gyazo.com/492bd725c5d17960038fc0de13d6373a.gif)

こうすると、どのようになるかというと  
リファレンスのロードの前に、まずバリアントによるスイッチが選択されるようになります。  
その後に、バリアント内にあるリファレンスがロードされます。

もしこの解決順序が逆の場合  
リファレンス 3 つが読み込まれるので、バリアントが効かなくなります。  
リファレンスをスイッチングできるようにするための解決順序が  
V→R なのかなぁと  
挙動を調べているときに気がつきました。

## リファレンス先のサブレイヤー

V→R の順序の確認はできましたが  
では、リファレンス先にコンポジションアークがあった場合はどうなるのか確認してみます。

```
#usda 1.0

(
    defaultPrim="SubA"
)

def "SubA"
{
    string name = "Hoge"
}
```

まず、こんな感じの SubA.usda を作成し

```
#usda 1.0
(
    subLayers = [
        @subA.usda@
    ]
)
```

サブレイヤーで合成。  
このファイルを ref_SubLayer.usda とします。

```
#usda 1.0

def "Grp"{
    def "SubLayer" ( prepend references = @ref_SubLayer.usda@</SubA>){}
}
```

そのファイルをリファレンスでロードしてみると、

![](https://gyazo.com/803949d35f17036055bf51e6c25991cc.png)

リファレンス先のサブレイヤーが合成され、その結果をリファレンスすることができました。  
このように、リファレンス先に対してコンポジションがあった場合は  
リファレンス内で LIVR...の順でプリムやアトリビュートの解決を行い  
その結果をリファレンスするようになります。  
リファレンス先は、1 つのローカルデータ扱いになる感じ。

このあたりは、Maya のリファレンス機能にちかいものがあって  
ある構造（Joint 構造・Mesh 構造、リギング済みアセットデータなど）をシーンにリファレンスでロードするように  
USD 内にアセットロードする時などに役に立ちます。
