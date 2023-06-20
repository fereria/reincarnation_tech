---
title: USDをPythonから色々操作するための環境を作る
description: JupyterNotebookを活用する方法
sidebar_position: 2
---

# USD を Python から色々操作するための環境を作る

USD 周りの基本であったり、構造周りの説明を先にやろうと思いましたが  
なんとなく中途半端な理解で書くと~~~微妙に恥ずかしいことになりそうなきがするので~~~  
混乱をうみそうなので、そっちはもうちょっと自分の中で咀嚼しつつ.....

前回 usdview で USD を開くまではできたので、  
USD ファイルをそのまま直書きするのではなく、Python 側から操作して  
なにがどうなっているのか検証するための環境を作ってみようとおもいます。

## じゅんび

まず、準備。  
モデルをチェックできる usdview ですが、これはあくまでもビューワーなので  
AttributeEditor で数値をいれてコントール...のようなことはできません。

![](https://gyazo.com/c9db8ccab23266051d25085db95c77bd.png)

が、数値を弄りたければ PythonInterpreter がついているので  
そちらからコントロールすることはできます。

が、このインタープリターで頑張るのは無理があるので  
私は VSCode と Jupyter を使用して環境をつくってみることにしました。

まず、使用する Python は３系を使用します。  
しかしこちらには usdview は入っていないので  
別途 Python2 用の USD（nvidia ビルド）をダウンロードしておき  
そちらから usdview を開いておきます。

```
cd /d I:\jupyter_notebook_root
jupyter notebook
```

とりあえず、こんな感じで固定の場所で Jupyter を起動できる Batch を作り  
裏で notebook を起動しておきます。  
しかし、この notebook をブラウザから使用すると、

![](https://gyazo.com/b3a8bf3a0e527f61b217b5cab8d82e9d.png)

一応使えますが、この場合 AutoComplete がきかないのと  
ショートカットが使いにくいので、これを VSCode 側からたたくようにします。

![](https://gyazo.com/de2de82522cab139a46da49981bae9cc.png)

Python の Jupyter Server URI の設定を開き、  
裏で起動している Notebook の URL を入力します。

が、Token を入れたりするのが面倒だったので

```
jupyter notebook --generate-config
```

まず、Config を作り、

C:/Users/<ユーザー名>/.jupyter

下にある、 jupyter_notebook_config.py の中の

```python
c.NotebookApp.token = ''
```

Token を消しておいて、

```python
c.NotebookApp.password = "sha1:～～～～"
```

パスワードをいれておきます。

パスワードは

```
python -c "import IPython;print(IPython.lib.passwd())"
```

このコマンドで生成できます。

で。

ここまで準備ができたら、あとは VSCode 側でいろいろ検証していきます。

## VSCode でいろいろやる

![](https://gyazo.com/833bf64be619f449b049a72ce03c982b.png)

現在のバージョンの VSCode は、 .ipynb (JupyterNotebook のフォーマット)を開くと
VSCode 上で Notebook の編集をすることができます。
（ショートカットなども VSCode のものが使用できる）

## プリントする

まず、usdview で開く前に　 USD ファイルの中身をプリントで確認してみます。

```python
print(stage.GetRootLayer().ExportToString())
```

たびたび確認をしたくなるので、ここだけをセルで分けておいて  
必要に応じてプリントしてみます。

![](https://gyazo.com/67708aa3b9cd65a747f03ca9084c6a11.png)

こんな感じで、現在の USD ファイル（正確にはレイヤー）を  
プリントすることができます。

注意点として、プリントする場合は「 print(～～～)」のように  
ちゃんとプリントコマンドを使用する必要があること。  
なしでも表示はできますが、その場合改行ができません。

### 保存する

保存するときは Stage を Export します。  
ここも度々やるのでセルにしておくと便利です。

```python
stage.GetRootLayer().Export(USD_PATH_ROOT + "/refTest.usda")
```

こんな感じで出力します。

USD は、開くときに NewOpen して Save することもできるのですが  
すでにファイルがある場合エラーになってしまったりと微妙に面倒だったので

```python
# 一度メモリ上にファイルを作り
stage = Usd.Stage.CreateInMemory()
# Export
stage.GetRootLayer().Export("PATH")
```

こんな感じでメモリ上にシーンを作り、最後に Export する方が  
毎回新規シーンでテストできてお手軽かなと思います。（たぶん）

### usdview で開く

Export したら、usdview でファイルを開きます。

```
usdview I:\usd_test\refTest.usda
```

Windows で usdview を使う場合のトラップなのか  
引数で渡す usd ファイルはフルパスである必要がある上、引数に usd ファイルを必ず渡す必要があります。
また、このツール起動が尋常じゃなく遅いので  
初回のみ適当なファイルで開いておいて  
ツール上のメニューからファイルを NewOpen したり Reload したりするのがオススメです。

![](https://gyazo.com/052b4430de2622643f14ae59322af78d.png)

とりあえずファイルが開けました。

ここまで準備ができたら、あとは VSCode 側でコードを書きつつ  
保存したら usdview で Ctrl+R でシーンをリロードしてプロパティやら Prim やら見た目やらが  
望む形になっているのか確認します。

https://snippets.cacher.io/snippet/e4a461c3093c7ce7929f

あとは、テストした結果は Cacher にメモとして UP するようにしています。

## 小ネタ

![](https://gyazo.com/5878a971ba83dcf4312eb3e6d1afcaae.png)

VSCode の PythonInteractive の実行結果表示ですが  
どんどんたまっていきます。  
が、Interactive の右上にある × ボタンを押せばリセットできます。

また、フロッピアイコンを押すことで Jupyter の ipynb ファイルとしても出力できます。

https://snippets.cacher.io/snippet/90166b7fd86eb73d7d0e

出力はできるけど、そこまで使わなそう。

とりあえず、ここまでやったら Python で色々弄りたおすのに  
ストレスがないぐらいまでの環境ができました。

多分、Exporter とかでデータフォーマットとして使う分には  
ここまでやらなくても良いかと思うのですが  
やはり USD の合成を扱うには Python や C++での操作は必須になりますし  
データ構造を理解する意味でも Python 側から扱うのは重要なので

テスト環境をストレスなくできるようにするのは大切かなーと思います。
