---
title: PrimをReparentする
---

USDの親子構造をあとから編集したい...  
みたいなことは当然のことながらやりたくなります。  
しかしドキュメントを読み漁ってもみつからずうわーんになっていたので泣きついて  
やり方を教えてもらったのでメモをば。

## 準備

まずはかんたんなusdaファイルを用意します。

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

Mayaなどの場合は cmds.parent(子,親) などでノードの移動ができますが  
USDの場合は若干異なります。  
どう違うかというと、PrimやLayerオブジェクトで行うのではなく
[SdfBatchNamespaceEdit](https://graphics.pixar.com/usd/docs/api/class_sdf_batch_namespace_edit.html)と呼ばれる、Namespace（あとで説明）の操作をカプセル化したクラスを介して  
Primの移動（Reparent）を行います。

```python
stage = Usd.Stage.Open(r"D:\work\usd_py36\usd\namespaceEdit.usda")
layer = stage.GetRootLayer()
edit = Sdf.BatchNamespaceEdit()
edit.Add("/A/C", "/A/B/C")
layer.Apply(edit)
```
BatchNamespaceEditは、「Batch」と名のつくとおり移動処理を複数積み上げてから  
編集したいレイヤーに対してApplyすることで、Primの階層を編集することができます。  

```python
edit.Add("/A/C", "/A/B/C")
edit.Add("/A/D", "/A/B/D")
```
Batchなので複数の操作を書くことができます。
```
[Sdf.NamespaceEdit(Sdf.Path('/A/C'),Sdf.Path('/A/B/C'),-1),
 Sdf.NamespaceEdit(Sdf.Path('/A/D'),Sdf.Path('/A/B/D'),-1)]
```
どんな操作が積まれているかは、Pythonの場合は edits で確認できます。（C++とは違う）  
  
Prim操作を探しているときに NamespaceEdit は見つけていたのですが  
うまく行かないしそもそもターゲット指定していないのにどうやってつかうんだ...  
と思っていたのですが、Batchに渡すための１つの操作が NamespaceEditでした。  
ひどいトラップ...
  
### Namespaceとは

USDのNamespaceとは [Glossary](https://graphics.pixar.com/usd/docs/USD-Glossary.html)によると

> Namespace is simply the term USD uses to describe 
> the set of prim paths that provide the identities for prims on a Stage, or PrimSpecs in a Layer.

木構造内のあるPrim (レイヤーの場合はPrimSpec)を識別するのに使うものです。  
（AというNamespaceにあるB、等）  
つまりは、上のBatchNamespaceEditというのは、  
Namespaceつまりはステージまたはレイヤーの階層構造を編集するためのものだよーということです。  
なお、このNamespaceの位置を表すのがSdfPathになります。

## 移動以外の操作

BatchNamespaceEditでは、Primの移動以外にもNamespace関係の操作を実行することができて
```python
edit.Add("/A/B/D", Sdf.Path.emptyPath) # 削除
edit.Add("/A/B/C","/A/B/C_rename")
```
こうすると、Primの削除やリネームを行うことができます。
これ以外にもVariantのReparentやプロパティのリネームなどもできるので
シーングラフやプロパティの構造を大きく変更したい場合は、この方法を使うと
できることが増えそうです。

## SubLayer時のNamespace操作

注意点ですが、このBatchNamespaceEditを実行するのがSdfLayerだということ。  
なので、Primの定義があるレイヤーをサブレイヤーでロードした
```usda
#usda 1.0
(
    subLayers = [
        @namespaceEdit.usda@
    ]
)
```
こんなファイルを作成して、このレイヤーに対して Apply(BatchNamespaceEdit) を実行したとしても  
Falseになってしまい正しく実行できません。

なので、サブレイヤーをしている場合は  
```python
# Primの定義があるレイヤーを取得して、そのレイヤーに対してApply
stack = stage.GetLayerStack()[2]
stack.Apply(edit)
```
定義があるレイヤーを取得して、そのターゲットに対してApplyします。  

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
例えばこんな感じでサブレイヤーに対してPrimが定義されている場合  
EditNamespaceをするとどうなるかというと

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

なので、これだと具合が悪い（コンポジションした結果に対してPrim移動をしたい）場合は

```python
flatten = stage.Flatten()
flatten.Apply(edit)
```

FlattenしてからEditするか

```python
for layer in stage.GetLayerStack():
    layer.Apply(edit)
```
LayerStackに対してeditするとかでもいけそうです。

しかし、Prim移動を行うのが BatchNamespaceEditというのはさすがにわかるかあぁぁぁ！！！！
になりましたよ...

## 参考
* https://github.com/ColinKennedy/USD-Cookbook/tree/master/features/batch_namespace_edit