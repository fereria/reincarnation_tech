---
title: MonkeyTypeで自動アノテーション追加
tags:
    - Python
    - VSCode
---

Python3 から追加された機能で、関数の引数や戻り値の型指定をすることができるようになりました。
基本、コードを書きながら追加すれば OK ですが
Python2 のコードをコンバートした場合などにまとめてアノテーションを追加したいみたいな場合もおこります。

そういった場合に、アノテーションを自動でつけてくれる機能があるようなので
試してみます。

まず、モジュールを pip で追加します。

```
pip install MonkeyType
```

インストールをしたら、

1. アノテーションを追加したいモジュール
2. そのモジュールを使用した Python コード

の 2 つを用意します。
使用した Python コードを利用して、型を推定し自動で追加する...というのがこの MonkeyType です。

```python title="samplemod.py"
def Add(a, b):
    return a + b
```

まず、アノテーションを追加したいモジュール。
このファイルの中にはこのようなシンプルな関数（アノテーションなし）が書かれています。

```python title="execsample.py"
import samplemod

samplecod.Add(1,2)
```

そして、そのモジュールを使用したコードを用意します。

## データベースを作成する

準備ができたら、アノテーション用のデータベース（使用したコードを解析して、型情報のデータベースを作る）

```
monkeytype run execsample.py
```

データベースは、このようにコマンドラインで作成できます。

![](https://gyazo.com/12a71bac5ce45bc62b048ca78e4ef3ae.png)

無事に実行されると、同じフォルダに sqlite3 ファイルが作成されます。

## 適応する

データベースができたら、アノテーションを追加したいモジュールを指定して
実行します。

```
monkeytype apply samplemod
```

```python

def Add(a: int, b: int) -> int:
    return a + b
```

無事アノテーションが追加されました。

そのままだと手順が多いので使うのが大変ですが、VSCode のタスクを作ったりいろいろすれば
autopep 的な感覚で使えそうかも？しれません。

-   https://github.com/Instagram/MonkeyType
