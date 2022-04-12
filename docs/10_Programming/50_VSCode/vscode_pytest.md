---
title: VSCodeでPyTest
tags:
description: VSCodeのテスト機能で pytestする方法
---

VSCode は、指定した名前になっている UnitTest 用のテストコードを実行できる
機能があるので
これを利用して、Python のテスト環境を作っていきます。

## 設定する

![](https://gyazo.com/e3633649c159d38085f6f80bf09e5f9d.png)

まず、プロジェクト下にフォルダを作り、その下にテストファイルを指定の名前で起きます。
ルールは「test\_」から始まること、なのでその名前で指定しつつ
その中にテストコードを書きます。

```python
def test_Add():
    a = 1
    b = 2
    assert a + b == 3
```

テスト用の関数は、 test\_### とすることで自動で認識してくれるので
このようにしておきます。

![](https://gyazo.com/4d829d58e2d3569dbfab98b7d0c97512.png)

VSCode の「テスト」アイコンをクリックし、

![](https://gyazo.com/dff9e86236ea217d984b1abb1efb0226.png)

Configure Python Tests をクリックします。

![](https://gyazo.com/2265cd1e3bfbef06bd65d43ce84c74ed.png)

そして、どのテストフレームワークを使うかを指定します。
今回は pytest を使用します。

![](https://gyazo.com/8914ffbaf9d4d2bcb9372691f65faa3f.png)

テストファイルを含むフォルダを指定する画面が出るので「tests」フォルダを指定します。

![](https://gyazo.com/45d3b8a40e58d365a38231ca671d2de0.png)

準備ができたら、このボタンでスタートします。

![](https://gyazo.com/384094d2b690275cb9fe58576ad7985f.png)

テストが無事通ると、このようにグリーンの ✅ になります。

```python
def test_AddErr():
    a = 1
    b = 2
    assert a + b == 4

```

例えば、わざとエラーになる関数を追加すると

![](https://gyazo.com/93242dfa4dca747a5f498255899f3fe7.png)

エラーがあるテストは ✖ 表示になり、

![](https://gyazo.com/0a9db3b223c14e50b0a040bfb9f78cd7.png)

エラー箇所がわかりやすく表示されます。

![](https://gyazo.com/a60cb53c678a5ad1cdc9624ed2383cba.png)

test\_###.py ファイルを開くと、関数の左側に実行ボタンがでているので
このボタンを押せば、単独でテストも可能です。

コマンドラインに比べるとわかりやすいので、
日常的にテストを実行したい場合は、指定しておくといろいろ楽になりそうです。

## 参考

-   https://qiita.com/everylittle/items/1a2748e443d8282c94b2
