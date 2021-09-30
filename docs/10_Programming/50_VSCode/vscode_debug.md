---
title: VSCodeでPythonデバッグ
tags:
    - VSCode
    - Python
---

![](https://gyazo.com/e0d44ec678d31e063aa16f86afd65302.png)

VSCodeでデバッグするときは、Debugアイコンを押して

![](https://gyazo.com/68829a27d4102e77d9ad868d9ad1f679.png)

launch.json ファイルを作成します　を押します。

![](https://gyazo.com/5246ef7ab53132a9b496ecd3ecef9d39.png)

押して、 Python File を選びます。

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

選ぶと、Python用のlaunch.json が出来がります。
この launch.json には、実行時の引数や、環境変数等を指定することができます。

```json
      "args": ["test"],
      "env":{
        "HOGE":"FUGAFUGA",
        "PATH":"D:/test;${env:PATH}"
      }
```

## 実行する

準備ができたら実行します。
デバッガを実行する場合は「F5」を押します。

### ブレークポイント

ブレークポイントとは、デバッガで実行したときに、一時的に停止する箇所のことです。

![](https://gyazo.com/05856587c0ecfb2fa1bdd20966d64985.png)

VSCodeの場合、行の左側あたりをクリックすることで追加できます。

![](https://gyazo.com/16015d395bb50efa12d9cb450bc118e7.png)

ブレークポイントを追加した後にデバッガを実行すると、
その地点で停止して、

![](https://gyazo.com/a85861dd54eb804310e14627271bf1c7.png)

その段階の変数の状態を確認したりできます。

![](https://gyazo.com/d030cabc38a9f08cf73fc4f329fdc7ed.png)

作成したブレークポイントは、「ブレークポイント」で確認することができて
ここでON / OFF することができます。

#### ブレークポイントの条件式

ブレークポイントは、指定の条件のときのみ止める...といったことができます。

![](https://gyazo.com/d144ed212737cf83d114646c58b56a91.png)

作成方法は、ブレークポイントの一覧から条件を付けたいもののペンアイコンを選択します。

![](https://gyazo.com/0d373f4c8ce4d7a62374a007ef35d9c8.png)

すると、ブレークポイント上に式の入力ができるようになります。

![](https://gyazo.com/fe3130cfae20682838ccf17769b8b52a.png)

例として、3の時のみブレークポイントで止めたいとします。
その時は、こんな感じで評価式を入れておきます。

#### ウォッチ式

ウォッチ式とは、ブレークポイントで停止中の評価式を書くことができます。

![](https://gyazo.com/3e38e0206df90107a41cb15df2ba4957.png)

たとえば、評価式にこのような値を入れておきます。

![](https://gyazo.com/7c5d26a0091e1174cc4070e8fbda3464.png)

すると、 __file__ の中身を評価した結果を表示してくれます。

```python
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('message')

args = parser.parse_args()
```
評価式には関数を書くこともできるので、例えばこのようなコードがあったとして
実行時に引数を受け取るようなコードがあるときに

![](https://gyazo.com/90058a6fbb23b71758697e3040c2a6c9.png)

ウォッチ式をこのように書いておきます。

![](https://gyazo.com/40157ed2b1b41fdabe5d115bb791172d.png)

結果。
コードで import をしていれば、import したモジュールの関数なども書くことができます。

### コールスタック

コールスタックとは、関数の呼び出しの改装状態を表示する機能です。

```python
def test(message):
    print(message)


test("hoge")

```

たとえばこのようなコードを実行して、ブレークポイントは printの行にしておきます。

![](https://gyazo.com/73bb69d1b2fe7cdc54b5ea9c183d3890.png)

その時のコールスタックはこんな感じです。

```python

def printMessage(message):
    print(message)


def test(message):
    printMessage(message)

test("hoge")
```

もう１つ関数を追加した場合、printにブレークポイントを追加して実行すると、

![](https://gyazo.com/63678dcabc8f01e9f67ead8306b338bf.png)

このようになります。

![](https://gyazo.com/e730bfc0eddeff8152075bf88363f47c.png)

コールスタックをクリックすると、それがコードのうちどの行になるのかを
ハイライトすることもできます。

### デバッグコンソール

![](https://gyazo.com/85500cc9a1b0d4cef193f1d2a644dfb9.png)

最後にデバッグコンソール。
デバッグコンソールは、ターミナルを表示するウィンドウと同じ場所にあります。

これはなにかというと、ブレークポイントで止めたタイミングの状態で
スクリプトを実行することができます。

![](https://gyazo.com/852a3a636f568303674e0580b151f665.png)

例えば、このようにしたとします。

![](https://gyazo.com/498129e4c9c9d8319f424ba8b8aebcb8.png)

デバッグコンソールで、このように式に値を代入してみます。

![](https://gyazo.com/7bdb5f6575d5448ed3755d2063d539c1.png)

すると、変数の値が書き換わりました。

![](https://gyazo.com/8262a9ecb820f0878935e52f6cc24f09.png)

その状態で実行をすすめると、書き換えた値で実行されていることがわかります。

デバッグコンソールを使用することで、あえて違う値を入れたり
今の値の状態を確認したりといったことが可能になります。


