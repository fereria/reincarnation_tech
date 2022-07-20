---
title: melをpythonに書き換えるテクニック
tags:
    - Mel
    - Python
    - Maya
description: melをみてpythonに翻訳するコツとか
---

Maya では mel と python という 2 つのスクリプトを利用することができます。
ですが、今となっては mel を使用することはなく python がメインになっています。

しかしながら、Maya は何か操作をした場合 ScriptEditor に mel でログが表示されるので
Maya のスクリプトを書く場合、それをヒントにコードを書くことが多々あります。
なので、始めたばかりで MayaPython を書く場合は
ある程度は mel を読み解けるようにするとスクリプトを書くヒントになります。

なので、今回は基本的な mel の書き方と
そこから python に置き換えるにはどのようにすればいいのかを解説していきます。

## mel コマンドを確認する

まずは Maya の操作をしたときの実行結果を確認するため
ScriptEditor を開きます。

![](https://gyazo.com/ef7353acddb38626a7f6ffbe8d3c50ca.png)

右下あたりにある アイコンをクリックして、スクリプトエディタを開きます。

![](https://gyazo.com/e6f30a024159b568f075e06d6e81056d.png)

開いたら、わかりやすいように Edit > Clear History で
ログをクリアしておきましょう。
クリアしたら、何かしら実行をします。

今回は、Sphere を作り、作成した Sphere の TranslateY を 5 にします。

![](https://gyazo.com/86f50302373eb43cb5075951890622dc.png)

```mel
CreatePolygonSphere;
polySphere -r 1 -sx 20 -sy 20 -ax 0 1 0 -cuv 2 -ch 1;
// Result: pSphere1 polySphere1
setAttr "pSphere1.translateY" 5;
```

実行結果はこのように表示されました。
作成した Sphere を一度削除して

![](https://gyazo.com/ea6a0e6189590848b75f81d43ca089a6.png)

![](https://gyazo.com/e625bcec81c70cb5b61f5c6f7814ed65.gif)
ScriptEditor の MEL タブにペーストして、全選択して Ctrl+Enter を押してみます。

実行すると、Sphere が２つできてしまいました。
これは、 CreatePolygonSphere と polySphere が同じようなコマンド
（CreatePolygonSphere が polySphere を呼んでる）なので、
CreatePolygonSphere を削除します。

> Mel を実行したとき、このようにコマンドがダブってログに表示されることがあります。
> この時は、引数を持たないものは Menu から呼ぶ場合などの関数なので
> 削除してみると良いです。

これで、必要なコマンドが判明しました。
:fa-external-link: [polySphere](https://help.autodesk.com/cloudhelp/2023/JPN/Maya-Tech-Docs/CommandsPython/polySphere.html) と :fa-external-link: [setAttr](https://help.autodesk.com/cloudhelp/2023/JPN/Maya-Tech-Docs/CommandsPython/setAttr.html)
こちらの２つ。
コマンドがわかったら、Maya のドキュメントを確認して必要な引数を確認します。

### import

python は mel と違ってモジュールを読み込む必要があります。
そして、mel のコマンドは共通ですが、このモジュール内に関数があるので
頭に cmds をつけます。

```python
import maya.cmds as cmds
cmds.polySphere()
```

### mel の引数のルール

コマンドはわかりましたが、このコマンドに対して指定された引数を書き換えます。

Mel の引数は、 -args value のように -引数名 セットする値 のように指定します。
これを、Python の場合 (args=value) のように書き換えます。

```mel
polySphere -r 1 -sx 20 -sy 20 -ax 0 1 0 -cuv 2 -ch 1;
```

これが

```python
cmds.polySphere(r=1,sx=20,ax=(0,1,0),ch=1)
```

このようになります。

基本は args=value になりますが、 ax のように -ax 0 1 0 のように複数の数字などが
指定されている場合は ()でタプル（あるいはリスト）にします。

## 引数の名前が指定されていない場合

mel の引数は 最後に引数のフラグを持たない値が入ります。

```mel
setAttr -type "string" pSphere1.strValue "aaa";
```

例えば、このように string のアトリビュートに値をセットした場合。
-type "string" AttributeName Value の順番になっています。

```python
cmds.setAttr("pSphere1.strValue","value",type="string")
```

これを Python に書き直すとこのようになります。
Python は引数名（キーワード引数）を指定するものは後に書くというルールがあります。
そのため、 setAttr のアトリビュート名とセットする値という必須のパラメーターを最初に書いて
それ以外のオプション（必須ではない引数）が後になります。

## まとめ

これらを踏まえたうえで、今回の Sphere を作って動かすスクリプトを
Python で書き換えた場合は

```python
# 必要なモジュールをimport
import maya.cmds as cmds
# melの引数を書き換えてpythonコマンドにす
cmds.polySphere(r=1,sx=20,ax=(0,1,0),ch=1)
# 値をセットする
cmds.setAttr("pSphere.translateY",5)
```

このようになりました。

## 別のパターンでも試してみる

上記の法則を念頭に入れて別のコマンドでも試してみます。

今度は、Maya の Sets を作る Sets にノードを追加する を試してみます。

```mel
// setsを作る
select -r pSphere1 ;
$createSetResult = `sets -name "set1"`;
// setsに入れる
sets -edit -forceElement  set1 pSphere2 ;
```

ログに表示される mel スクリプトはこのようになります。

どちらのコマンドも :fa-external-link: [sets](https://help.autodesk.com/cloudhelp/2023/JPN/Maya-Tech-Docs/CommandsPython/index.html) コマンドを使用しています。
それぞれの mel コマンドを詳しく見ていきます。

## return を受け取る場合

```mel
$createSetResult = `sets -name "set1"`;
```

sets を作成している行を確認してみると、 変数名に \`バッククォートでかこんだ 書き方をしているのがわかります。 mel の変数は $変数名 になりますが、個の変数に対して 関数の return を代入する場合 \`mel のコマンド\`; このようにします。

```mel
// これはエラー
$createSetResult = sets -name "set1";
```

今回書き換える場合は、変数にセットする必要はないので、
sets コマンド部分だけを抜き出せば OK です。

```python
# set1というsetsを作る
cmds.sets(name="set1")
```

## mel の特徴 なにかのノードに実行する場合のコマンドの書き方

sets コマンドの 作成する側を見てみると
選択する → sets コマンドを実行 このように選択してからコマンドを実行しています。
mel コマンドで、 sets や group のように何かしらのノードに対して処理をするような
コマンドは、

1. コマンドの引数に対象ノードが書かれている場合は、そのノードが対象
2. 何も書かれていない場合は、選択されているノードが対象

のようになります。
つまり、 sets コマンドに対して「sets に入れたいノード」が指定されていない場合
事前に select したノードが対象になります。

なので、
select -r pSphere1;
sets -name "set1";
を 1 行で書く場合は、

```mel
sets -name "set4" pSphere1;
```

このように書くことができます。
これを python に書き換えると、

```python
cmds.sets("pSphere1",name="set4")
```

mel コマンドでフラグを使わない引数がある場合は、先頭に書きます。
複数ノードがあれば列挙します。

## どこまでがフラグなしの引数？

もう１つの sets にノードを追加したい時のコマンドは、
パット見ると最後にノード名が複数ついているので

```
sets -edit -forceElement  set1 pSphere2 ;
```

```python
# エラーの場合
cmds.sets("set1","pSphere2",edit=True,forceElement=True)
```

このように書き換えるのか？
と思うかもしれません。
ですが、この場合エラーになってしまいます。

うまくいかない場合はドキュメントを確認します。

![](https://gyazo.com/3a7b49c2f6b849c4f45af51507d4235f.png)

forceElement の項目を見てみると、引数タイプが「name」になっています。
これはつまり、 -forceElement nodeName のように Bool ではなく何かしらの文字列が
来ることを表しています。

```python
cmds.sets("pSphere2",edit=True,forceElement="set1")
```

書き換えるとこのようになります。
「なにを」sets に入れるのかは sets の先頭にノード名を指定します。

## ログに表示されないケース

多くの場合はログを確認することで、どのようなコマンドで実行されているのか
探すことができます。
しかし、場合によってはログに何も表示されないケースがあります。

![](https://gyazo.com/11cb2bff895f0aa7ba7fc287ee435266.png)

その場合は、この History の「Echo All Commands」をオンにします。
このチェックをオンにすると、普段は OFF になっているすべてのログが表示されます。

不要な行もかなり表示されるので、必要な行を探す必要がでてきますが
コマンドが見つからない、ログにも表示されないという場合は
Echo All Commands をオンにして、mel スクリプトの実行方法を調べると
問題を解決することができます。

## まとめ

Maya でスクリプトを書きたいときに、
やりたいことがどうやったら Python 出かけるかわからない！！そんな時に
コマンドを探す方法のまとめでした。
