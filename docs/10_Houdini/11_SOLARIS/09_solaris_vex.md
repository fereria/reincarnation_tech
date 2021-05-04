---
title: SOLARISのVEXで遊ぼう
tags:
    - USD
    - SOLARIS
    - Houdini
    - HoudiniAdventCalendar
---

[Houdini Apprentice Advent Calendar 2020](https://qiita.com/advent-calendar/2020/happrentice)
 5日目は
「SOLARISのVEXで遊んでみよう」
です。

## ゴール

まず今回の目的ですが、私自身Pythonでコードを書いたりすることはできますが
HoudiniのVEXは全く書けないため、その書き方の基本的な部分を理解することが
今回のゴールになります。

VEXで書いたら何ができる？
基本的な文法は？
どういうときに向いてる？

といった基本的なところを調べながら書いていこうと思います。

基本的な文法は
https://www.sidefx.com/docs/houdini/vex/lang
公式ドキュメントを参考にします。

## まずは使ってみる

まずは基本的なVEXを書くところまでやってみます。

![](https://gyazo.com/e4974283bf0a31bfa20d72d54ade21ce.png)

まず、SOLARISでVEXで色々処理するために attribwrangle ノードを作り
こんな感じのノードを作ります。

attribwrangleノードのVExpression に、

```vex
usd_addprim(0,"/hoge","Cube");
```

と入力してみます。

![](https://gyazo.com/292972c9472ef8224aa92f1455ae3672.png)

![](https://gyazo.com/2e62d880c94ce99ca07b60c5e3853e0a.png)

無事Cubeが出現しました。

こんな感じで、VEXにはUSD用の関数が複数追加されていて
これを利用してUSDのシーングラフを操作をすることができます。

## 処理の対象について

VEXで処理をする対象は Primitives で指定した入力Primが対象です。

```
`lopinputprims('.', 0)`
```
デフォルトがこちら。
Input 0 に入力されているPrimのうち
最後に編集されたPrimの数だけVEXの処理が実行されます。

![](https://gyazo.com/f4263e455687e7352d17b484bc4d5136.png)

なので、こんなかんじで複数PrimをマージしたあとにWrangleにつなぐと

![](https://gyazo.com/6e981b64dbf816deb1c924bb0d27a4c0.png)

CubeとSphereの２回分実行されます。
複数処理する場合は、その処理ごとに @primpath などの Built-in variable(後で説明)が
Primの処理ごとに置換されます。
なので、入力が複数であっても for で繰り返しなどを書く必要がありません。

## Build-in variables

Build-in variables とは、SOPでいうところの @Cd や @P といったアトリビュートと同じで
InputのPrimを受け取るための変数（？）です。

![](https://gyazo.com/45849f30920fe97750096a0b153e07af.png)

受け取るPrimitivesは、このPrimitivesで指定されたものになります。
つまり、これを利用するとInputで与えられるなにかしらのPrimitiveに対して
Forを使用して何かしらの処理をまとめて実行することができます。

たとえば、入力のPrimに対してAttributeを追加したい場合。
Pythonの場合は

```python
from pxr import UsdGeom,Sdf

node = hou.pwd()
stage = node.editableStage()

for i in node.inputPrims(0):
    prim = stage.GetPrimAtPath(i)
    prim.CreateAttribute('hoge',Sdf.ValueTypeNames.Bool).Set(True)
```

こうなります。
では、同様の処理をVEXで書いてみるとどうなるかというと

```vex
int handle = usd_addattrib(0,@primpath,"hoge","bool");
usd_setattrib(handle,@primpath,"hoge",true);
```

こうなります。

Build-in variables の @primpath は、入力のPrimitiveのPathに置換されます。

入力が多数ある場合、このVEXpressionに書かれた記述が
入力のPrimitive全てに対して実行され、その実行都度、 Build-in variables は
処理するPrimitivePathに置換されます。

つまり、↑だけで繰り返し処理を書いたのと同様の処理になるわけですね。
なるほど。

このBuild-in variables は、
@primpath @elemnum @numelem @primtype @primkind @primname @primpurpose
@primdrawmode @primactive @primvisible
の計10個あります。

これを利用すれば、
指定のスキーマのときだけ
Xformにだけ移動値を入れたい、Cubeのときだけ動かしたいなどといった
特定の処理を書いたりできます。

## 制御構文

### if 

まずは if 文。

```
if(usd_istype(0,@primpath,"Cube"))
{
    usd_setmetadata(0, @primpath,"documentation", "Cube!!");
}
```

指定のPrimTypeのときのみなにか処理を実行。
usd_is###系の関数を使えば、色々判定ができるので
その判定を利用して if 文で処理をわけたりできます。

### for 

次に、 for で複数のPrimを作ってみます。

```
for(int i = 0;i < 10;i++)
{
    usd_addprim(0,@primpath + "/test_" + itoa(i),"Cube");
}
```
Inputのノード以下に複数のPrimを作ります。
for文などは他の言語とほぼ同じ感じで使用できました。

```
for(int i = 0;i < `chs("./duplicateNum")`;i++)
{
    usd_addprim(0,@primpath + "/test_" + itoa(i),"Cube");
}
```
![](https://gyazo.com/da3ed8d36da457ae09c2857e256cd45e.png)

固定の数値というのもあれなので、Houdiniのアトリビュートを追加してみた例。
今までの関数も使用できます。


## USD固有の関数を使う

次は関数の使い方。

https://www.sidefx.com/docs/houdini/solaris/vex.html

USDのVEXの一覧はこちら。
ぱっと見た感じ、USDの操作は一通りのことができそうです。
使いそうなものからいくつかピックアップして試してみます。

### Prim名を取得

```
printf("%s",usd_name(0,@primpath));
```

現在処理をしているPrim名を取得します。
関数を使う場合の１つ目の引数はStageの読み先となる入力番号を指定します。

なので、Wrangleノードの１つ目の入力にノードが接続されている場合は 0 になります。
usd_nameの場合 primPathを指定するとPrim名が帰ってくるので
現在処理中の PrimPathに置換される @primpath を指定すればよさそうです。

### 移動

```
usd_addtranslate(0,@primpath,"test_move",{0,5,0});
```
移動などの処理はすべて関数が用意されていて、このようにすると
指定のPrimを移動することができます。

```
def Xform "sphere"
{
    double3 xformOp:translate:test_move = (0, 5, 0)
    uniform token[] xformOpOrder = ["xformOp:translate:test_move"]

    def Sphere "sphere1" (
        customData = {
            int HoudiniPrimEditorNodeId = 19
        }
    )
    {
        float3[] extent = [(-1, -1, -1), (1, 1, 1)]
        double radius = 1
        matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
        uniform token[] xformOpOrder = ["xformOp:transform"]
    }
}
```
その場合は、移動情報を追加することができます。

ただ、この場合は移動するPrimがXformである必要があるようで
（UsdGeom.XformCommonAPIを使用するときも同様なので、このCommonAPIの仕様っぽい）
注意が必要です。
そもそもSphereに対してxformできてしまうのが問題かもしれないです。

transform以外にも rotate scaleなどの関数があるので
Wrangleで移動などの操作がしたい場合は同じ方法でできます。

### メタデータの編集

```
usd_setmetadata(0, @primpath, "documentation", "docs!!");
usd_setmetadata(0, @primpath, "customData:strVal", "testText");
```
USDはレイヤー、Prim、アトリビュートそれぞれに対してメタデータを仕込むことができます。
スキーマで指定されたメタデータであれば documentation のように指定できるし
それ以外の任意の情報であれば、 customData:～～の形式でセットできます。

```
usd_metadata(0,@primpath,"customData:strVal");
```
メタデータの取得もできるので、
USD側になにか情報を入れておいて処理したい場合などは
この方法で対応できます。

### Primを作成

```
usd_addprim(0,@primpath + "/test","Cube");
```
指定のPathに対してPrimを生成します。
３つ目の引数がPrimのタイプで、この場合はステージに１つのCubeを作ります。

### まとめ

Build-in variables と、ステージハンドルの意味を抑えておけば
あとはほぼ関数名通りの昨日をVEXで使用できました。

関数の一覧を見る限り、PrimやAttributeの操作を実行するものは
ほぼVEXでなんとかなりそうです。
ただし、Namespaceを変更したりLayerに関わる操作はこちらではできなそうなので
あくまでも入力のステージのうち該当するPrim or Attributeに対して
何らかの処理をしたい場合に使うのが良さそうです。

### アトリビュートへのアクセス

次にアトリビュート周り。
関数を使用するとアトリビュートへのアクセスができましたが
VEX的な書き方でもっと簡略化ができるようです。

SOPでは、GeometrySpreadSheetなどで

![](https://gyazo.com/19678d56f14ae349eeb6897ee8a1961d.png)

各オブジェクトの頂点だったりフェースだったりノーマルに対して

```
@P = ～～～
```
このようにジオメトリのアトリビュートや情報にアクセスしていました。

SOPでは、まさにジオメトリごとのアトリビュート操作がキモになっていて
このアトリビュートに対して色々セットしたり取得したりして
処理を書くことができます。

ではLOPの場合はどうかというと、USDのアトリビュートに対して
編集したり取得したりすることが同様の記述方式できます。

### セットする

まずはかんたんなサンプルから。

![](https://gyazo.com/4e9b0ec684b7f97ffa25fe7460999605.png)

こんなかんじでSphere１を作り、attribwrangleノードにつなげます。

![](https://gyazo.com/cadb08a65f9aea0d25bda269b9be0225.png)

そしてアトリビュートを追加して、

```
f@radius =`chs("/stage/attribwrangle1/sphereSize")`;
```

VEXにこう書きます。

![](https://gyazo.com/89df4236993d4d48da446975e1506987.gif)

結果。

fは、アトリビュートの型で、@以降はUSDのAttribute名を指定することで
USDのアトリビュートに対して値を設定することができます。
この型は、いわゆるUSDのスキーマで定義されているものです。

![](https://gyazo.com/a7383362603807d7f2194eee75f88944.png)

スキーマが持つアトリビュートは、 Edit Parameter Interface のFromUSDに一覧があるので
スキーマのアトリビュートを編集できるようにするのならば、
このスキーマのアトリビュートをノードに追加して
VEXでこのアトリビュートの値をセットする ... のようにすれば
編集できるようになりそうです。

### アトリビュートを作成する

これはすでに定義済のものでしたが、

```
s@fuga="FUGA!!";
```
例えばこうすると、

```
def Sphere "sphere1" (
    customData = {
        int HoudiniPrimEditorNodeId = 19
    }
)
{
    float3[] extent = [(-1, -1, -1), (1, 1, 1)]
    custom string fuga = "FUGA!!"
    double radius = 1
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]
}
```

customのアトリビュートが追加されます。
つまりは、USDに対して自分の好きな値を埋め込むことができるわけです。

SOLARIS上でUSDのアトリビュートを操作する方法は、私が調べた限りだと
Python側から操作する以外見当たらず、アトリビュートの編集の方法がわかりませんでした。
しかし、このVEXからだと
Pythonから操作するよりも遥かに簡単に　かつHoudini的にアクセスできるので
こちらを使うのが正解のようです。

### xformOp

上のような単純なアトリビュート以外にも、移動などのパラメーターも設定できます。

```
v@xformOp:translate = {0,3,0};
s[]@xformOpOrder = {"xformOp:translate"};
```

VEXでPrimを移動する例。

```
def Sphere "sphere1" (
    customData = {
        int HoudiniPrimEditorNodeId = 19
    }
)
{
    float3[] extent = [(-1, -1, -1), (1, 1, 1)]
    double radius = 1
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    custom double3 xformOp:translate = (0, 3, 0)
    uniform token[] xformOpOrder = ["xformOp:translate"]
}
```
実行すると、指定のPrimに対して translate のアトリビュートが追加されました。
このxform:### というのは、USDの XformPrimなどでの移動値などを保持するアトリビュートです。

```python
from pxr import UsdGeom,Sdf

node = hou.pwd()
stage = node.editableStage()

for i in node.inputPrims(0):
    prim = stage.GetPrimAtPath(i)
    UsdGeom.XformCommonAPI(prim.GetParent()).SetTranslate((0,3,0))
```
Pythonの場合は、こんな感じで、指定のXformPrimに対して SetTranslateすると
xformOp:translate と xformOpOrder に対してVEXで書いた内容を追記します。

VEXだけだとものすごいわかりにくいですが、
USDの記述を手書きで書いているのと同じように、移動などの値も編集できるわけですね。
（超マニュアル操作！！）

このxformOpOrderというのは、アトリビュートとしてセットされた
**xformOp:#### の操作順をどの順で実行するか** という意味になります。

Translate１つならば問題ありませんが

```
v@xformOp:translate = {0,3,0};
v@xformOp:rotateXYZ = {30,0,0};
s[]@xformOpOrder = {"xformOp:rotateXYZ","xformOp:translate"};
```
例えば 移動して回転する例の場合、
X方向に回転してから移動するのと、移動してから回転するのでは結果がかわります。
その操作順を指定するのがこの xformOpOrder で、
これはUSD側の記述ルールです。

なので、USD側の挙動がわかっていればVEXの type@attrname = ～～～～ で
USD側のアトリビュートを編集したり加工したりできるわけですね。

https://graphics.pixar.com/usd/docs/Referencing-Layers.html

一応公式Docsのチュートリアルを見ると、アトリビュート名を確認できます。

SOPなどでのアトリビュートコントロールをLOPに当てはめると
LOPの中ではUSDのコントロールすることになります。
とはいえ、ほぼusdaのアトリビュートを手書きするようなものなので
VEXでなにかする場合はUSDのAPIやスキーマの把握が必須になりそうです。

そのかわり、USDの構造をほぼダイレクトに操作できるので
構造を理解できればかなりシンプルにUSDの構造を操作する事ができそうです。

## パフォーマンス

最後にパフォーマンスについて。
ほぼ同様の処理はPythonでも書けますが、Pythonと比較してどのぐらいの速度差があるか
確認してみます。

とりあえずCube１００個を作ってみます。

VEXの場合
```
for(int i = 0 ; i < 100;i++)
{
    usd_addprim(0,@primpath + '/cube_' + itoa(i),"Cube");
}
```

Pythonの場合
```python
from pxr import UsdGeom

node = hou.pwd()
stage = node.editableStage()

path = node.inputPrims(0)[0]
for i in range(0,100):
    UsdGeom.Cube.Define(stage,path.AppendChild(f"cube_{i}"))
```

まずはVex
![](https://gyazo.com/2a4795d362c95236f4d6fbd4fa93bd4c.png)

続いてPython
![](https://gyazo.com/25caf240a1198441ef44531e0340b644.png)

わかってはいたものの、驚愕の速度差です。

基本繰り返し処理に関してはPythonは避けてVEXかLOPのノードで実行するほうが
良さそうです。


## まとめ

とりあえず、基本的な書き方のみを調べるだけになってしまいましたが
おかげでいつかわかったことがあります。

まず使い方について。
VEXの場合は、

![](https://gyazo.com/636b86946a69003f3d7c86141db9c512.png)

Primitivesで指定されたPrimに対して何らかの処理を書くことができる。
基本的なものは関数でカバーされているのでそれを使用すれば
USDの操作はほぼカバーできるので、Primに対しての処理はVEXを使うのが良さそうです。

アトリビュートを操作する

SOLARIS上ではUSDのアトリビュートの操作を可能にするノードがあまりありません。
（ConfigurePrimを使えばMetaDataの編集は可能）
なので、基本Houdini上にUSDのアトリビュート編集をできる
Houdiniのアトリビュートを作った場合は、このVEX上で
値をセットさせるのが良さそうです。

ただし、配置したりに関しては
現状だとSOPでPointを作りつつ組み立てるほうがやりやすそうなきがしました。

{{ 'https://twitter.com/fereria/status/1333796376254136326'|twitter }}

少し前にこんなつぶやきをしたのですが、
SOLARIS自体にしても、SOLARISのVEXにしても USDの構造をほぼマニュアル操作で
いじくり回す必要がある（とくに構造を作ったりする場合）ので
このあたりをいい感じにカバーしつつ
USDの構造などを完全に把握しなくても
USDのワークフローが作れるようにしていくのが今後の課題かなと思いました。
