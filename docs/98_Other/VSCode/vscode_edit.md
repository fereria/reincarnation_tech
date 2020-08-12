---
title: VSCode 便利な機能
---

最近 VSCode を触っていると、
「あ、こんな便利な機能あったんかよ！」
ってことが多いので、メモついでにまとめ。

## Python

### pylanceでAutoComplete

![](https://gyazo.com/a6f1759050fcce6d8735c8849c8fd7a5.gif)

最近でてきたPylanceを導入済み。
これ以外にもJediだったりそれ以外にもいくつかあるけれど
必須機能。これがないとまともにコードが書けない。

### import文ソート

![](https://i.gyazo.com/6b16a95f015ab4166bc7dc90b252e6c0.gif)

![](https://gyazo.com/a05314f9def68403ae10e21d9a28e9e3.png)

pythonのImport文をアルファベット順にソート。

### 定義元を表示する

![](https://gyazo.com/ffa25dfc681dd00545a66f8f331fba8d.png)

Alt + F12 で、カーソル下にある関数の定義元を表示。

### 関数名などをまとめて変更

![](https://gyazo.com/f493aa8d311d8c2f3737d4fc94aed073.gif)

Ctrl + F2 で、Pythonファイル内の関数名と使用している箇所をまとめて編集。

### ドキュメントフォーマット

![](https://gyazo.com/c19cf45fdd131edc006fb75279b052ff.gif)

pep8でフォーマットを実行。
渡しの場合はCtrl+X Ctrl+8 にフォーマットショートカットを指定して、常にpep8になるようにしている。

![](https://gyazo.com/178224f8f60afa587b6bca62fcb20a42.png)

MaxLineと一部エラーはスキップするようにしていて
設定は↑

## 便利拡張

### Code Spell Checker

![](https://gyazo.com/2614632837ff955b5a18e2a9c5f07b42.png)

タイポしているワードがないかチェックをしてくれる。
これを入れるとコードレビューで恥ずかしい思いをしないで済む。

### codic

![](https://gyazo.com/cd70964e53f1cb43a644b437b46568fa.gif)

日本語→英語の辞書を呼び出す。
関数名考えるときに便利。
