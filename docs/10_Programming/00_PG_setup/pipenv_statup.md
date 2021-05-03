---
title: pipenvを使用したPython開発環境の作り方
tags:
    - Python
    - 環境構築
---

## pipenvとは？

pipenvとは、AnacondaのようなPythonの環境構築ツールの１つで
pip + virtualenv を組み合わせたものです。
これを使用することで、Pythonの仮想環境を作りつつ、かんたんにpipを使用したモジュールのインストールを
行うことができます。

## py.exe

これを説明する前に、 py.exe について触れておきます。
py.exe とは、最近のPythonをインストールすると一緒にインストールされる
複数のPythonをインストールしている場合の使用バージョンスイッチを用意にしてくれるものです。
exeは C:/Windows/py.exe に入っているので、コマンドライン上では py というコマンドで使用することができます。

使い方は、
```bat
py -3.6 
```
このようにすると、指定のバージョンのPythonを使用できます。

これを活用することで、環境変数のPythonPathを毎度変えたりすることなく
Pythonを使用することができます。

で、一般的には pip.exe があるフォルダにPATHを通すことで

pip install hogehoge 

のようにしていますが、固定のバージョンのフォルダ下にPATHを通さずに
py を使用することでも pip install を使用することができるので
そちらを利用して説明していきます。

## インストール方法

というわけで、まずは pipenvを使えるようにインストールします。
```
py -3.6 -m pip install pipenv
```
今回は、python3.6を基準として扱うPythonとして使用するので -3.6 とします。

インストールが完了すると

```
py -3.6 -m pipenv ～～～
```
これで、pipenvを使用することができます。
  
## インストール先を変更する

準備ができたら、次にpipenvの設定をします。
pipenvは、仮想環境を .venv 下に作成するのですが、
デフォルトだとHOME下に仮想環境が作成されてしまうので、プロジェクト下になるように環境変数で指定します。

```batch
PIPENV_VENV_IN_PROJECT=true
```
この設定を入れておくと、現在のフォルダ下に .venv が作成されます。

## Versionを指定してPIPENVの環境を作成する

準備ができたら、実際の環境を作っていきます。

仮想環境を作りたいPythonのプロジェクトフォルダのルートに移動して、
以下のコマンドを実行します。

```bat
py -3.6 -m pipenv --python 3.6 install
```

pipenvでの環境構築は、 --python ### install の ### ここで
仮想環境のバージョンを指定することができます。
上の場合は 3.6用の仮想環境をつくります。

![](https://gyazo.com/ab722703e030286001e9ea35120b752e.png)

構築が完了したら、このように .venv フォルダができあがります。
これでもとりあえずOKなのですが、
これだと毎回 py -3.6 pipenv のように書かないといけないので
```
py -3.6 -m pipenv install pipenv
```
作成した仮想環境にも pipenv を入れておきます。

```
py -3.6 -m pipenv shell
```
pipenvが入れ終わったら、作った仮想環境をセットします。

## VSCodeの設定

まず、pipenvをインストールしたフォルダを開きます。

![](https://gyazo.com/f62d154d5af3a6b46289cddec578d078.png)

特に何もしていない場合は、こんな感じでインタープリタが指定されていませんので

![](https://gyazo.com/1f75099b6292794682074ad855f45b69.png)

インタープリタの選択の中から作成したpipenvの環境を選択します。

![](https://gyazo.com/fa506a203231cada557b92957c4ad90d.png)

この設定をすると、VSCodeのターミナルを開いたときに自動的に .venv にアクティベートした
状態でコンソールを開いてくれるので

```
pipenv install pyside2
```
こんなかんじで、pipを使用するのと同じ感覚で仮想環境にモジュールをインストールすることができます。

## pipenvの主要なコマンド

| cmd                    |                                                                        |
| ---------------------- | ---------------------------------------------------------------------- |
| install <package_name> | 指定のパッケージをpipenvにインストールすｒ。（バージョン指定も可）     |
| run <cmd>              | Pythonのコマンドを実行する。                                           |
| shell                  | 現在のフォルダの仮想環境でShellを起動する。                            |
| lock                   | Pipenv.lock ファイルを作成する。                                       |
| update                 | lockコマンドを実行後、その時同期する                                   |
| clean                  | Pipenv.lock に記載されていないすべてのパッケージをアンインストールする |

## 設定済みファイルから環境を構築する

pipenvは、設定ファイルをベースに仮想環境を再構築することができます。  
  
```Pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
jupyter = "*"
notebook = "*"
ipykernel = "*"
pyside = "*"
qt-py = "*"
pyopengl = "*"

[dev-packages]

[requires]
python_version = "2.7"
```

まずは、空のフォルダに Pipfile という名前の空のテキストを作成します。  
作成したファイルを開いて、↑のようにインストールしたいパッケージや、Pythonのバージョンを  
記載して保存します。  
このファイルは、 pipenv install hogehoge したときに作成されるファイルで  
すでに別の仮想環境を作っていた場合はファイルが作成されています。  
ので、すでにあるファイルをコピペしてくるのでもOKです。  
  
次に、コマンドプロンプトでフォルダに移動して

```
py -3.6 pipenv install
```
を実行します。  
  
実行すると、 Pipfile に記載されているパッケージのうちインストールされていない物があれば  
インストールされます。  
空の場合、指定のPythonバージョンの環境構築も行われます。  
  
なので、よく使うモジュールを設定しておいた Pipfile を用意しておけば
専用の仮想環境をコマンド１つでモジュールのインストールまで一括で
行うことができます。

VSCodeと組み合わせるとより快適になるので、とても便利です。

## 追記

```bat
@echo off
; path version
mkdir %1
cd /d %1
C:\Windows\py.exe -3.6 -m pip install pipenv
C:\Windows\py.exe -3.6 -m pipenv --python %2 install
C:\Windows\py.exe -3.6 -m pipenv install pipenv
```

毎度プロジェクト作るときにコマンド叩くの面倒だったので、Batを書いた。

これで 

create_pipenvproj.bat D:\hogehoge 3.6 とかやるとかんたんにプロジェクトがつくれる!
