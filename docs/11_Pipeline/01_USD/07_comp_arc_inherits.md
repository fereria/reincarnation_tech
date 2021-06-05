---
title: CompArc(2) 継承
tags:
    - コンポジションアーク
    - USD
    - USD基本
---

# CompArc(2) 継承

## 継承とは

コンポジションアーク2つめは「継承（Inherits）」  
これは、プログラミングにおける継承と同じで、あるプリムのプロパティやその値を引き継ぎつつ  
別のプリムを作ります。  
特徴として、ある継承をしたいプリムに対して、 **継承の指定は SdfPathで行うこと** があげられます。  
  
以下詳しく。
  
## サンプル

### シンプルな構造の場合
  
```usda
#usda 1.0

class "BaseClass"
{
    int hoge = 100
}

def "Fuga"
(
    prepend inherits = </BaseClass>
)
{
}
```

継承を使った場合のレイヤーの最もシンプルな例がこちら。  
  
![](https://gyazo.com/362174863f643af0a00d1c42ac4b5c35.png)

これをusdviewで読み込むと、このようなシーングラフが表示され  
  
![](https://gyazo.com/dbbbd578393e0dc964c1b9a66414dcfd.png)

アトリビュートはこのようになります。  
Fugaプリムにはアトリビュートがありませんが、BaseClassを継承することによって  
BaseClassのアトリビュートがFugaのアトリビュートを引き継いでいることが分かります。  

### 複数でつかってみる

```usda
#usda 1.0

class "BaseClass"
{
    int hoge = 100
}

def "FugaA"
(
    prepend inherits = </BaseClass>
)
{
    
}

def "FugaB"
(
    prepend inherits = </BaseClass>
)
{
    int hoge = 200
}
```
クラスを使用すると、1つのデフォルトプリムを複数のプリムで共有することができます。  
ので、このようにベースのプリムを複数のプリムで使用すると

![](https://gyazo.com/6d00dba212071b67a1a57f4c761e703d.png)

このように2つのプリムができ、両方とも hoge アトリビュートを持ちますが  

![](https://gyazo.com/a0e91a42b08f028147d404474dccd45a.png)

片方のhogeアトリビュートはこのようにLocalの値（ hoge = 200 ）で上書きされているので  
200になっていることが分かります。  
  
### def と classの違い  
  
上のサンプルを見ると、継承元のプリム定義は「class」になっているのがわかるかとおもいます。  
ですが、継承を使用するときはclassを使用しなければいけないかといえばそういうわけでもなく  
  
```
def "BaseClass"
{
    int hoge = 100
}

def "FugaA"
(
    prepend inherits = </BaseClass>
)
{
}
```
このように def で定義したとしても  
  
![](https://gyazo.com/4902f904a0c033033f2446a3bc640031.png)

このように継承の機能を使用することが出来ます。  
（あるプリムを指定して値を継承させる）  
  
しかし、defを使用するとそれ自体もプリム扱いされるので  
シーングラフ上に「BaseClass」が表示されるようになります。  
  
## 継承元に子プリムがある場合

上の例だと継承元プリムと継承先プリムの関係は＝になりました。  
では、継承元側に子プリムがあった場合はどうなるか？というと

```usda
#usda 1.0

class "BaseClass"
{
    int hoge = 100
    
    def "Foo"
    {}
}

def "Fuga"
(
    prepend inherits = </BaseClass>
)
{
}
```

![](https://gyazo.com/a9a1baa2118247d788f696f3afb0d9fa.png)

このように、継承先にも子プリムが作成されます。  

### 継承先にも子プリムがある場合

```
#usda 1.0

class "BaseClass"
{
    int hoge = 100
    
    def "Foo"
    {}
}

def "Fuga"
(
    prepend inherits = </BaseClass>
)
{
    def "Bar"{
    }
}
```

上の例だと継承先にはプリムがありませんでしたが、では継承先にプリムがあった場合は  
どのように合成されるのか？  
というと、

![](https://gyazo.com/ef54451a6ff8676370f9e67b26b2134e.png)

このように、継承元の子プリムに継承先のプリムが追加されるようになります。  
このあたりの処理は、考え方的にはクラスと関数の関係に近いようで  
親クラス側の関数が継承先で使用できる、さらに継承先のクラスに関数を追加することで  
拡張する...それと同じなのかなと思います。  
  
```
#usda 1.0

class "BaseClass"
{
    int hoge = 100
    
    def "Foo"
    {
        string fooVal = "foo!!!"
    }
}

def "Fuga"
(
    prepend inherits = </BaseClass>
)
{
    def "Foo"{
        string fooVal = "FOOOO!!!!!"
    }
    def "Bar"{
    }
}
```
実際に確認してみると、継承先のほうに同じプリムがあると  

![](https://gyazo.com/e96b167fa51689650155443075223029.png)

こんな感じでオーバーライドされます。  
  
## 別のusdに定義されたプリムを継承したい場合

ここまでで、継承の挙動がなんとなく分かってきたかとおもいますが  
見直してみると、継承を指定している部分の  
 
``` 
prepend inherits = </ClassName>
```
この部分を見ると、SdfPathで継承元のプリムをしているのが分かります。  
同じレイヤー内（usdaファイル内）ではなく別のレイヤーに記述されているプリムを  
継承で扱いたい場合はどうすれば良いか？というと  
継承したいクラスの書かれたusdファイルをサブレイヤーで合成し  
その合成のあとに継承をします。  
  
```usd
#usda 1.0

class "BaseClass"
{
    int hoge = 100
}
```
例えばこのクラスが class.usda に書かれていたとします。  
  
コレを別のレイヤーで使いたい場合は  
  
```usd
#usda 1.0

(
    subLayers = [@class.usda@]
)

def "Fuga"
(
    prepend inherits = </BaseClass>
)
{
}
```
こうすると、  
先述の合成の原則から L(サブレイヤーによる合成)後、I（継承）が行われるので  

![](https://gyazo.com/947bcc20c8eef28464df5450ee722232.png)

同じレイヤーに書かれているのと同じように、プリムの継承をすることが出来ます。  
  
