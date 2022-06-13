---
title: Pythonで引数をパースする
---

基本的な argparse の使い方をメモ。

```python
# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser()

# 引数をセット
parser.add_argument('name',help="hello world!!")
parser.add_argument('-v', '--value')
# 必須パラメーターにしたい場合は、 required = Trueにする
parser.add_argument('-t', required=True)
# 引数複数にしたい場合
parser.add_argument('-f', '--foo', nargs=3)
# 可変にする
parser.add_argument('--hogehoge', nargs="*")
# 必須じゃなくする場合
parser.add_argument('-o', '--options', nargs="?", default=0)
# 指定のなかから選択する
parser.add_argument('--type', type=int, choices=[1, 2, 3])

# 引数の格納指定 オプション指定があればTrueを入れる
parser.add_argument('-y', action="store_true")
# 複数オプションがあったときにいろいろする
parser.add_argument('--add', action='append')

# 解析結果をGET。
# 引数空の時は、sys.args を入れてるのと同じ意味。
args = parser.parse_args()

# 表示するには、 .hogehoge のように、add_argumentで指定した名前にする
print args.name
print args.type
print args.y
print args.add
```

このスクリプトを hogehoge.py –h のようにすると

```
positional arguments:
  name                  hello world!!

optional arguments:
  -h, --help            show this help message and exit
  -v VALUE, --value VALUE
  -t T
  -f FOO FOO FOO, --foo FOO FOO FOO
  --hogehoge [HOGEHOGE [HOGEHOGE ...]]
  -o [OPTIONS], --options [OPTIONS]
  --type {1,2,3}
  -y
  --add ADD
```

こんな感じで Help を出すことが出来ます。
引数で help=””設定をすると、この help にコメントが表示されます。

パース結果は、 Namespace() クラスのオブジェクトとして帰ってきます。
使う時は、 args.xxx のように、 . + add_argument で指定した名前　で
値を取得することができます。

## 参考

- https://docs.python.jp/3/library/argparse.html#action
- http://python.civic-apps.com/argparse/
