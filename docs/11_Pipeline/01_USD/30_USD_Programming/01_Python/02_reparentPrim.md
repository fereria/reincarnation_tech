---
title: PrimをReparentする
description: USDのPrimの階層をPythonで変更する方法
---

USD の親子構造をあとから編集したい...  
みたいなことは当然のことながらやりたくなります。  
しかしドキュメントを読み漁ってもみつからずうわーんになっていたので泣きついて  
やり方を教えてもらったのでメモをば。

## 準備

まずはかんたんな usda ファイルを用意します。

```usda
#usda 1.0

def "A"{
    def "B"{}
    def "C"{}
}
```

これを

```usda
#usda 1.0

def "A"{
    def "B"{
        def "C"{}
    }
}
```

こう。

![](https://gyazo.com/ba1c15de5821d0413a48f851acdfd0a4.png)

図にするとこんな感じにしたいとします。

## 基本的な移動方法

Maya などの場合は cmds.parent(子,親) などでノードの移動ができますが  
USD の場合は若干異なります。  
どう違うかというと、Prim や Layer オブジェクトで行うのではなく
[SdfBatchNamespaceEdit](https://graphics.pixar.com/usd/docs/api/class_sdf_batch_namespace_edit.html)と呼ばれる、Namespace（あとで説明）の操作をカプセル化したクラスを介して  
Prim の移動（Reparent）を行います。

```python
stage = Usd.Stage.Open(r"D:\work\usd_py36\usd\namespaceEdit.usda")
layer = stage.GetRootLayer()
edit = Sdf.BatchNamespaceEdit()
edit.Add("/A/C", "/A/B/C")
layer.Apply(edit)
```

BatchNamespaceEdit は、「Batch」と名のつくとおり移動処理を複数積み上げてから  
編集したいレイヤーに対して Apply することで、Prim の階層を編集することができます。

```python
edit.Add("/A/C", "/A/B/C")
edit.Add("/A/D", "/A/B/D")
```

Batch なので複数の操作を書くことができます。

```
[Sdf.NamespaceEdit(Sdf.Path('/A/C'),Sdf.Path('/A/B/C'),-1),
 Sdf.NamespaceEdit(Sdf.Path('/A/D'),Sdf.Path('/A/B/D'),-1)]
```

どんな操作が積まれているかは、Python の場合は edits で確認できます。（C++とは違う）

Prim 操作を探しているときに NamespaceEdit は見つけていたのですが  
うまく行かないしそもそもターゲット指定していないのにどうやってつかうんだ...  
と思っていたのですが、Batch に渡すための１つの操作が NamespaceEdit でした。  
ひどいトラップ...

### Namespace とは

USD の Namespace とは [Glossary](https://graphics.pixar.com/usd/docs/USD-Glossary.html)によると

> Namespace is simply the term USD uses to describe
> the set of prim paths that provide the identities for prims on a Stage, or PrimSpecs in a Layer.

木構造内のある Prim (レイヤーの場合は PrimSpec)を識別するのに使うものです。  
（A という Namespace にある B、等）  
つまりは、上の BatchNamespaceEdit というのは、  
Namespace つまりはステージまたはレイヤーの階層構造を編集するためのものだよーということです。  
なお、この Namespace の位置を表すのが SdfPath になります。

## 移動以外の操作

BatchNamespaceEdit では、Prim の移動以外にも Namespace 関係の操作を実行することができて

```python
edit.Add("/A/B/D", Sdf.Path.emptyPath) # 削除
edit.Add("/A/B/C","/A/B/C_rename")
```

こうすると、Prim の削除やリネームを行うことができます。
これ以外にも Variant の Reparent やプロパティのリネームなどもできるので
シーングラフやプロパティの構造を大きく変更したい場合は、この方法を使うと
できることが増えそうです。

## SubLayer 時の Namespace 操作

注意点ですが、この BatchNamespaceEdit を実行するのが SdfLayer だということ。  
なので、Prim の定義があるレイヤーをサブレイヤーでロードした

```usda
#usda 1.0
(
    subLayers = [
        @namespaceEdit.usda@
    ]
)
```

こんなファイルを作成して、このレイヤーに対して Apply(BatchNamespaceEdit) を実行したとしても  
False になってしまい正しく実行できません。

なので、サブレイヤーをしている場合は

```python
# Primの定義があるレイヤーを取得して、そのレイヤーに対してApply
stack = stage.GetLayerStack()[2]
stack.Apply(edit)
```

定義があるレイヤーを取得して、そのターゲットに対して Apply します。

### サブレイヤーで読み込んだ先に定義がある場合

```
#usda 1.0

(
    subLayers = [
        @namespaceEdit.usda@
    ]
)

over "A"{
    over "B"{}
    over "C"{}
    over "D"{}
}
```

定義がない場合はなにもおきないですが、  
例えばこんな感じでサブレイヤーに対して Prim が定義されている場合  
EditNamespace をするとどうなるかというと

```
def "A"
{
    def "B"
    {
        over "C_rename"
        {
        }
    }

    def "C"
    {
    }

    def "D"
    {
    }
}
```

こうなりました。  
あくまでも編集ターゲットにしたレイヤーの定義のみ変更されます。

なので、これだと具合が悪い（コンポジションした結果に対して Prim 移動をしたい）場合は

```python
flatten = stage.Flatten()
flatten.Apply(edit)
```

Flatten してから Edit するか

```python
for layer in stage.GetLayerStack():
    layer.Apply(edit)
```

LayerStack に対して edit するとかでもいけそうです。

しかし、Prim 移動を行うのが BatchNamespaceEdit というのはさすがにわかるかあぁぁぁ！！！！
になりましたよ...

## 参考

-   https://github.com/ColinKennedy/USD-Cookbook/tree/master/features/batch_namespace_edit
