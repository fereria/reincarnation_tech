# Driver を作成する

<!-- SUMMARY:Driverを作成する -->

Driver は、Maya でいうところの DrivenKey+Expression のような機能。

## 作成する

![](https://gyazo.com/d5e27a765089d664d5b3dbd7463a952e.PNG)

まず、Driven 側（動かしたい側）のプロパティ上で右クリックして、 **Add Driver** を追加する。

![](https://gyazo.com/365ed6476c3188ac588ef801268db2d5.png)

Driven プロパティ上の「Object」に、Driver になるオブジェクトを指定する。  
つぎに、どのプロパティで動かすかを「Type」で指定する。

![](https://gyazo.com/99d99ddcd89c5aad20a9d8354837afea.gif)

作成すると、Driver を動かすと Driven 側のオブジェクトも一緒に動くようになる。

## Driver Settings

### Scripted Expression

![](https://gyazo.com/ce2c5d79b0ea3018a9be8458b7640fa6.png)

Driver には、計算式を挟んで値をセットする機能がある。

DrivenProperty 内の InputVariable の中の（ｘ）が、いわゆる変数名で  
InputVariable で指定した値が、（ｘ）で指定した文字列に代入される。

この画像の場合、 var に対して Cube.001 の TransformX がセットされている。

Input Variable で指定した変数は Expression 欄の計算で使用することが出来る。  
この Expression の計算結果が、DrivenProperty にセットされる。

![](https://gyazo.com/6cca69a69b3e2bf0758fb43d7228b197.png)

このように Expression に計算式を入れると

![](https://gyazo.com/503a802e55e4fdb0e39f2a1c53ff8dff.gif)

計算結果が反映される。

#### Expression 内で使用出来る変数名

|            |                            |
| ---------- | -------------------------- |
| **frame**  | 現在のフレーム番号を返す。 |
| **cos(x)** | コサインの数値を返す       |
| **sin(x)** | サインの数値を返す         |

## Input Variable

変数に代入するための数値の取得方法を決める

### Distance/RotationalDifference

![](https://gyazo.com/21974d9b4efa295928735d13e9e339c0.png)

2つのオブジェクトの距離を代入する

![](https://gyazo.com/0655b8c24639422bbfe7078768f0be8f.gif)

var / 2 のようにすると、2つのノードの間にオブジェクトが移動するようになる。

Differenceは距離、RotationalDifferenceは2つのオブジェクトのRotationの差を返す。

### TransformChannel

指定オブジェクトのTransformを変数に代入する。

### SingleProperty

![](https://gyazo.com/a9012bd9f3fcc960bd1a611eedfcb721.png)

指定のData-Blockのプロパティの値を変数に代入する。  
ここで指定する数値は **RNA ID name** を指定する。  
ここで指定したい名前の確認方法は

![](https://gyazo.com/b31e589c8e3cdc9e0a780f5c931ef7d2.png)

確認したいプロパティの「CopyDataPath」で取得することが出来る。  
  
