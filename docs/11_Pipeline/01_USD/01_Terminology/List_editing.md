---
title: List Editingについて
description: 配列の要素を編集するための機能の解説
order: 7
---

USD のリファレンスを扱っていると、

```
#usda 1.0

def "sphereA" (
    prepend references = @sphere.usda@
)
{
}
```

こんなかんじで、 「prepend」という記述があることがあります。
prepend とは「付加する」という意味で、文字通り Prim に対して「Reference を付加」  
するという記述になります。
しかしながら、この prepend はなくても挙動としては正しく動きます。  
では、この prepend というのは一体何を意味するのか？  
というのが、今回のお題である **ListEditing** になります。

## List Editing とは

ListEditing とは、USD の Glossary によると

> USD が配列値のデータエレメントを読み込むことができる機能です
> この機能によって、 コンポジションアーク に対して配列タイプのエレメントを
> 非破壊的且つ疎らに編集することができます
> 日本語訳版より引用
> https://usd.prisms.xyz/intro/USD-Glossary.html#list-editing

とあるとおり、コンポジションアークによって複数のレイヤー（usd ファイル）を合成したときに  
配列タイプのアトリビュートなどを非破壊に編集するための機能を指します。

たとえば USD のリレーションの場合。

```
def "test"
{
    rel aaa = [<RelA>,<RelB>]

    def "RelA"{}
    def "RelB"{}

}
```

まずは、ベースでこんな感じの構造があったとします。
![](https://gyazo.com/5a27d415242ced5e193337774ff709c7.png)
Houdini の SOLARIS 上で要素を覗いてみると、  
aa の Value には、 test/RelA と test/RelB という２つの要素があるのがわかります。

これに対して test/RelC という Prim をサブレイヤーで rel aaa に「追加したい」とします。

USD の合成は非破壊で行われるので、ベースの USD ではなく  
サブレイヤーで合成するシーン側で「 aaa に加える」という処理を  
編集できてほしいわけです。
そういう場合、

```
def "test"
{
    prepend rel aaa = [<RelC>]
    def "RelC"{}
}
```

このように prepend とつけることで

![](https://gyazo.com/ebeacff897375086b571d05fa1d9755d.png)

サブレイヤーで合成した結果をみると、
prepend で追加した要素が、 aaa の先頭に追加されているのがわかります。

このように、配列の要素に対して、「追加」したり「削除」したりできるのが
この List Editing とよばれる「prepend add delete」の効果になります。

### prepend append delete の違い

この ListEditing の３つと、それがない場合どういう違いがおきるかというと、

```
def "test"
{
    rel aaa = [<RelC>]
}
```

まず、何もつかない場合。

![](https://gyazo.com/4f5bfb215111dfebfa4eda0357221152.png)
この場合、配列のアトリビュートをそのままあった要素を無視して「上書き」します。

```
def "test"
{
    append rel aaa = [<RelC>]

    def "RelC"{}

}
```

次に、append
この場合は、
![](https://gyazo.com/ac007e9309dd31d86353a1e49c73163e.png)

配列の最後に要素が追加されます。

```
def "test"
{
    delete rel aaa = [<RelB>]

}
```

最後に delete
![](https://gyazo.com/c68c399e804f723450f8a1dc45da2b3a.png)
delete の場合は、要素が配列から削除されます。

元のレイヤーを編集せず、サブレイヤー側に ListEditing を追加することで
非破壊で配列の編集をすることができました。

## コンポジションアークでの ListEditing の影響

リレーションの場合は、並び順に影響しましたが
では、コンポジションアークの場合はどうなるでしょうか。

```
def "test"
(
    prepend references = </RefA>
)
{
}

def "RefA"
{
    string name = "RefA"
}

def "RefB"
{
    string name = "RefB"
}
```

まずはこんな usda を用意してみます。
![](https://gyazo.com/505e6f8111835ce8a45afb1dc7a6df38.png)
この結果は、 RefA をリファレンスしているので「name」は「RefA」になります。

```
def "test"
(
    prepend references = </RefB>
)
{
}
```

このレイヤーに対して、 prepend で RefB を追加するレイヤーを作ってみます。

![](https://gyazo.com/60cfb84d259a216a712b61da54d1340a.png)

結果、リファレンスの評価の先頭に RefB がきたので、 name は「RefB」になりました。

```
def "test"
(
    append references = </RefB>
)
{
}
```

対して append した場合。  
この場合は、リファレンスの評価順序の末端に RefB が追加されているので

![](https://gyazo.com/054f6a0e4981e9c87543ec30057d747b.png)

結果は RefA になります。

```
def "test"
(
    delete references = </RefA>
)
{
}
```

最後に、 delete の場合。  
この場合は当然のように RefA のリファレンスが消えるので

![](https://gyazo.com/18c6758e2eae0e77da7bd4f11642c310.png)

アトリビュートがなくなりました。

## まとめ

こんな感じで、
単純にリファレンスで上書きしていくような場合は prepend があってもなくても  
挙動は同じ（ない場合は上書き＝最優先扱い）になりますが  
delete を使えばリファレンスは消えるし  
複数のリファレンスでコンポジションする場合は
この ListEditing の順番に影響されてくるので、注意が必要かもしれません。  
（基本サブレイヤーでの順番優先なら気にしなくて良いかもしれない）

あと、
余談ですが、カスタムメタデータの数字・文字列配列も List Editing 対応らしいのですが  
探しても記述方法がわかりませんでした。
どうやったらいいんだろう...？
