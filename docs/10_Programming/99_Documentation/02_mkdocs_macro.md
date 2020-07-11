---
title: mkdocsのマクロプラグインを使う
---

mkdocs のマクロプラグインを使用することで、Python の関数を呼び出して  
その結果を表示できるようにできます。
というのを前からあるのは知ってましたが、mkdocs をバージョンアップするついでに  
使い方を色々調べてみました。

```
pip install mkdocs-macros-plugin
```

まずはプラグインを pip でインストールします。

```
plugins:
  - git-revision-date-localized:
      type: iso_datetime
      locale: ja
  - search:
      lang:
        - en
        - ja
  - awesome-pages
  - macros
```
そしてpluginsに macroを追加します。
これで準備は完了。

次に呼び出し用のpythonを作ります。
mkdocsのプロジェクト直下に main.py を準備して、そこに

```python
def define_env(env):
    # マクロはここに書く
```
define_env 関数を作ります。
マクロプラグインが呼び出すための関数で、
マクロに必要な値がこの関数の引数として渡されます。

## マクロを作る

マクロとは、
```
{{'hoge()'|macroprint}}
```
こんな感じで \{\{ \}\} で main.py の define_env に書かれた関数を呼び出して
そのreturnを表示できるようになります。

```python
    @env.macro
    def fontstyle(comment, size=1.0, color='#000000'):
        return f'<div style="font-size:{size * 100}%;color:{color}">{comment}</div>'
```

例えばこんな感じの定義を作り、@env.macro のデコレーターをつけます。

```python
    def testHoge():
        return 'return hogehoge
    # デコレーターを使わない場合
    env.macro(testHoge, 'hogevalue')

```
あるいは、デコレーターを使わない場合は、env.macroの第１引数で関数を渡し
第２引数で呼び出し用の {{hogevalue|macroprint}}に指定する文字列を指定しておきます。

出来上がったマクロは、

```
{{"fontstyle('ここに文字を書く',1.2,'#ff0000')"|macroprint}}
```

mkdocsにこのように書くと

{{ fontstyle('ここに文字を書く',1.2,'#ff0000') }}

このように文字サイズを変えることができます。  
フォントサイズや色はmarkdownだと難しいので、こうやってマクロをかけるのは  
とても便利です。


## フィルターを作る

フィルターとは、 Jinja2 の機能で  
```
{{'name|lower'|macroprint}}
```
こんなかんじで \{\{\}\} の1つ目の変数を2つ目の定義されたフィルターで変換して
結果を表示させることのできる機能です。

```python
    @env.filter
    def twitter(url):
        return f'<blockquote class="twitter-tweet"><a href="{url}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
```
フィルターの作り方はかんたんで、
デコレーターで @env.filterをつけた関数を作り、入力の値を引数として
その結果を return します。

```
{{"'https://twitter.com/fereria/status/1164544426967875584'|twitter"|macroprint}}
```

上のTwitterフィルターは、値でTwitterのURLを渡すと

{{ 'https://twitter.com/fereria/status/1164544426967875584'|twitter }}

Twitterを埋め込みにしてくれます。
引数を必要としない修飾はフィルターを使うと良さそうです。

ついでにマクロ前提だと {{'これ'|macroprint}} のカギカッコを表示するのも
面倒だったので、そういうマクロを書いてみました。

今は単純にタグを作るためのマクロがメインですが
return で文字列を返せば何でもできるので、mkdocsのかゆいところをPythonで書いたり  
他のAPIを叩いて結果をmkdocsに表示するみたいな使い方ができそうです。
