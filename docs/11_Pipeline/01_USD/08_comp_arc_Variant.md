---
title: CompArc(3) バリアントセット
tags:
    - コンポジションアーク
    - USD
    - USD基本
---

# CompArc(3) バリアントセット

バリアントセットとは、プリムに対していわゆる「複数の選択肢から1つを選んで切り替える」  
スイッチをつけることができるコンポジションアークです。  
  
具体的にどういうものかを、お約束の公式サンプルキッチンセットのアセット下から  
assets/Book/Book.geom.usd  
を開きます。  

![](https://gyazo.com/4b983eea849342f559b4675859f81d2f.png)

開いたら、Bookプリムを選択して、MetaDataタブを確認します。

![](https://gyazo.com/f3c2a37c85edeb37599ec93a2a3d971d.png)

その中に「shadingVariant variant」という項目があります。  
  
![](https://i.gyazo.com/63f0b370573d22f9621d220b580b64d9.gif)

この項目を切り替えると、色を変えることができます。  
  
このように、いくつかの選択肢から1つを選ぶとプリムの中身をスイッチできるのが「バリアントセット」  
です。  
  
## 基本構造

```usda
#usda 1.0

def "testPrim" (
    prepend variantSets = "hogehoge"
)
{
}
```

バリアントセットは、切り替えを追加したいプリムに対して追加します。  
このサンプルを usdview で表示すると  
  
![](https://gyazo.com/512be3e912a4d1616b48b4ac92e2982c.png)

このような testPrim に  
  
![](https://gyazo.com/5f19a3c61c650ee6a9929b642f31a3bd.png)

空のvariant が追加されました。  
  
### 切り替え設定を追加する

```usda
#usda 1.0

def "testPrim" (
    variants = {
        string hogehoge = "green"
    }
    prepend variantSets = "hogehoge"
)
{
    variantSet "hogehoge" = {
        "blue" {
            string testAttr = "blue"
        }
        "green" {
            string testAttr = "green"
        }
        "red" {
            string testAttr = "red"
        }
    }
}
```

なんの選択肢もない場合はただの空の入れ物だけがある状態なので  
これに対して選択肢を作成します。  
  
![](https://i.gyazo.com/44efb9290644d3b8c73f5bdd934f6d07.gif)

これで、アトリビュートの切り替えができるようになりました。  
  
### LとVの関係について

前回の LocalとInheritsのように、このバリアントもコンポジションアークなので  
原則によってアトリビュートやプリムが決定するわけですが  
  
```
#usda 1.0

def "testPrim" (
    variants = {
        string hogehoge = "green"
    }
    prepend variantSets = "hogehoge"
)
{
    string testAttr = "????"
    
    variantSet "hogehoge" = {
        "blue" {
            string testAttr = "blue"
        }
        "green" {
            string testAttr = "green"

        }
        "red" {
            string testAttr = "red"

        }
    }
}
```

このようにしてみるとどうなるかというと

![](https://gyazo.com/7e0c5b3ab1e00e0c818dbe6c6135a3c0.png)

アトリビュートの値は、 ???? になっているのがわかります。  
この状態でvariantを切り替えても値は変わりません。  
つまりは、この ???? の行の部分がLocalの指定で  
Vよりも強いため値が上書きされていることが分かります。  
  
### 子プリムの切り替え

上の例だと、プリムにあるアトリビュートをセットする機能にも見えますが  
そういうわけではなく、

```usda
#usda 1.0

def "testPrim" (
    variants = {
        string hogehoge = "green"
    }
    prepend variantSets = "hogehoge"
)
{
    variantSet "hogehoge" = {
        "blue" {
            def "Blue"{}
        }
        "green" {
            def "Green"{}
        }
        "red" {
            def "Red"{}
        }
    }
}
```

このように、各バリアントセットの設定部分に対してプリムを定義することで

![](https://gyazo.com/88cbff2746d0f7b197f27d9a793169ab.png)

プリムの構造そのものを複数のパターン持つことが出来ます。  
このサンプルでは1階層ですが、もちろん子・孫、そのプリムに対してのアトリビュートもつけられますし  
このバリアントセットのスイッチ内に別のコンポジションアークを追加することができます。  
（このあたりは次回のリファレンスにて紹介）  
切り替えできるものがアトリビュートに限らず、構造そのものをまるごと切り替えできるのが  
バリアントセットの強力な機能になります。  
  
