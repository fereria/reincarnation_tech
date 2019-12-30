---
title: SOLARISでInherits(継承)/Reference(継承)を扱う
---

# SOLARIS で Inherits(継承)を扱う

SOLARIS の中での USD コンポジションアークは、ほぼサブレイヤー・リファレンス・バリアント  
の 3 つで成り立っていて、なんか継承の影が薄いなーということで  
せっかくなので継承について調べてみました。

## 継承のノード

まず、SOLARIS 上で継承を使いたい場合は  
独自ノードではなく Reference ノード内の ReferenceType を使用します。

![](https://gyazo.com/3ed522a786d457a1acfdf98c96b8f36d.png)

ReferenceType の Inherits From First Input を選択すると  
Input1 のノードを継承して新しく Primitive を作成します。

## Class と Def の違い

継承の説明をする前に、USD の Primitive の定義をする場合、  
「def」という Specifier(指定子)を使用しますが  
def 意外にも「class」という指定子が存在します。
コレが一体どう違いが出るかというと、

![](https://gyazo.com/6d454b690b4b78c015d03b7e13c653f3.png)

このように、定義するとシーングラフ上に表示されるものの  
名前の左側にかがみもちみたいなアイコンが表示され、ビューポートにはなにも表示されません。  
class の場合は、あくまでも定義だけで実体を作らず  
Reference や Inherits を使用することで  
class で定義している Primitive を作成することが出来ます。

## 継承について

そもそも USD の継承はなにかというと、その名の通りある Primitive の構造を「継承」して  
あたらしい Primitive を作成します。  
挙動的にはほぼ Reference と同じですが、その挙動には若干の違いがあります。

まず、Reference。  
Reference は完全なカプセル化された別のレイヤーを、指定の Primitive に対してロードします。  
「カプセル化」がなにかというと、

![](https://gyazo.com/abe1f03c14eb9860d18acba61564c6a2.png)

まず、こんなサンプルを用意します。

```
#usda 1.0
(
    defaultPrim = "Obj"
)
class Cube "ObjBase"{}

def "Obj"(references=</ObjBase>){}
```

Reference ノードでは、↑ のようなファイルをロードしておきます。
そして、片側の inlineusd で

```
class Sphere "ObjBase"
{
}
```

こうします。
この 2 つをサブレイヤーで合成してみます。
「Reference」の場合、
![](https://gyazo.com/95b84ecd4714255fea7597bcc58666d0.png)
結果は Cube になります。
![](https://gyazo.com/a93988890062bf95905bff56ce47593d.png)
シーングラフをみても、Class 定義はなくロードされた Primitive のみが表示されます。

Reference で読み込まれてるレイヤー内の構造がカプセル化されているので
あとからサブレイヤーでファイルをロードしたとしても、
![](https://gyazo.com/b149ebd89d2c87713455b6c313035363.png)
合成はされるものの、リファレンス内の構造には影響を与えません。

これを

```
#usda 1.0
(
    defaultPrim = "Obj"
)
class Cube "ObjBase"{}

def "Obj"(inherits=</ObjBase>){}
```

このように「継承」にしてみます。

![](https://gyazo.com/ddffc80dc903d4d7bbd76db180e3fb28.png)

すると、サブレイヤーの結果は Sphere に変わりました。
つまりは、Merge ノードを使用して合成した class Sphere "BaseObj" {} が
Reference ノードを使用して読み込んだレイヤー内の class を上書きしている...ということがわかります。
この差が、Reference と Inherits の大きな違いになります。

## SOLARIS 内での扱い方

ここまでが USD 的な挙動でしたが
では実際に SOLARIS 上での挙動を調べてみます。

![](https://gyazo.com/e31a8ff3a7fe359848543aa128581d24.png)

まずはこんな感じで class 指定子で Class を定義します。

![](https://gyazo.com/a7b53ffc68a27085e9614eb449785bb3.png)

Primitive ノードを使用すると、指定の Type で def または class を作成できます。
ので、今回は Cube を Class で作成します。

![](https://gyazo.com/3b08a8faa09279b3acaa7e01d7e5c7ad.png)

Inherits は単独のノードではなく Reference ノードのオプションで切り替えできます。
切り替えたら、継承元の Primitive を指定します。

なお、Reference と Inherits の違いとして、Reference は別のレイヤー（別の usd）を指定して
ロードすることが出来ますが、Inherits は同じレイヤー内の Primitive を指定する
必要があります。
ので、別ファイルで定義している場合はサブレイヤーで合成してから inherits =<～～>で
Primitive を指定する必要があります。

で。

Inherits で継承した結果

```
class Cube "TestClassA"
{
}

def "Inherits" (
    prepend inherits = </TestClassA>
)
{
}
```

こんな感じの usda が作成されます。

![](https://gyazo.com/950e06b355b39a04cc3f51ad37023b0e.png)

結果のシーングラフ。
Inherits という名前の Cube が作成されました。

![](https://gyazo.com/5f3dbf0b535e9a4e164732c0169c368e.png)

この継承したレイヤーを USD ROP で出力します。

![](https://gyazo.com/fe31288229a60c9f434557f69eefe10b.png)

そのファイルをRefernceノードでロードすると、
このようにClass定義はなくなり、ファイル内の指定のPrimitive（通常はDefaultPrim）のみが  
表示されます。
しかし、表示はされていないものの、継承元の TestClassA クラスはオーバーライド可能で
```
class Sphere "TestClassA"
{
}
```
このようなファイルをサブレイヤー合成すると、

![](https://gyazo.com/40d836b0c63eb4969d1639f136f694ee.png)

こんな感じで合成され

![](https://gyazo.com/906b3fc84f75c9a91320c9cb1595ec9f.png)

結果はSphereに変わります。

![](https://gyazo.com/76cdcad45e0256c13183dc15ff170314.png)

しかし、これを Reference From First Input にしてから再度出力して、
同じノードを確認すると

![](https://gyazo.com/3883cd57f7e755a63e633749ef1434ba.png)

同じ構成であっても、オーバーライドされずにreference4はCubeのまま

![](https://gyazo.com/6bcc7060d30110560ba73c1c6c79fcef.png)

Reference内のClassは隠蔽された状態になります。

これが、ReferenceとInheritsの挙動の差のようです。

### loadLayerでの読み込み

![](https://gyazo.com/79ae7a0058c30649d105bb2e1dd7d63b.png)

レイヤーを読み込む場合、Referenceノードの場合は
Classは隠蔽され、シーングラフには表示されず、継承したクラスをオーバーライドする等は
出来ません。

loadLayer＋Referenceノードを使用してリファレンス化した場合

![](https://gyazo.com/b1618979ee926c0bd1c22258e355af88.png)

こうすると

![](https://gyazo.com/44f3c51dc5bf107a8b511d26861cdf88.png)

こうなります。
ファイルでReferenceを読み込むのではなく
LoadLayerでReferenceノードにつなぐと
あくまでも、同じレイヤー内にあるPrimitiveをリファレンスでロードした状態と同じになり
レイヤー内の隠蔽はされず
この場合は、

```
class Sphere "ObjBase"
{
}
```
こんな感じのレイヤーをサブレイヤー合成すると
合成されてオブジェクトがCubeからSphereになります。

LoadLayerで読み込んでReferenceノードでリファレンス化（複製）しても
挙動は同じなのかなと思っていましたが、挙動は違っていて

LoadLayer＋Referenceノードにノード接続の場合は
サブレイヤーで合成されたあと、同じレイヤー内にあるPrimitiveをReferenceしている状態で
Referenceノードの場合はPrimitiveで reference=@Path@\</SdfPath\>している状態ということか。

というわけで、レイヤーでカプセル化してロードしたい場合は
Referenceノードを使用してロードするのが正解でした。
ノードでの表現方法、まだまだ難しい....`