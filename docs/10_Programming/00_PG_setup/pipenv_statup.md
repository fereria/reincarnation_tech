---
title: PipEnv の使い方
---
# PipEnv の使い方

## インストール方法

まず、通常のpipを使用してpython3にpipenvをインストールする。  
```
pip install pipenv
```
```
C:\Users\<UserName>\AppData\Local\Programs\Python\Python36\Scripts
```
次に、pipのあるフォルダにPATHを通す。  
  
  
## インストール先を変更する

デフォルトだとHOME下に仮想環境が作成されてしまうので、
プロジェクト下になるように環境変数で指定する

```batch
PIPENV_VENV_IN_PROJECT=true
```

## Versionを指定してPIPENVの環境を作成する

```bat
pipenv --python 3.6
```

このようにバージョン指定すると、その指定されたバージョンで仮想環境を作成できる（2系3系どちらも可能） 

![](https://gyazo.com/ad0977ba38ddb16cd3aa8cc9556d177c.png)

実行すると、プロジェクト下に.venvが作成され  
その下に仮想環境が作成される。  
  
## Debugの構成を追加

![](https://gyazo.com/58d9a1d4ded9b6048fd526213ee48923.png)

Debugの構成を追加して、launch.jsonを作成する。

```json
{
   "version": "0.2.0",
   "configurations": [
     {
       "name": "Python: Current File used Pipenv",
       "type": "python",
       "request": "launch",
       "program": "${file}",
       "pythonPath": "${workspaceFolder}/.venv/Scripts/python",
       "console": "integratedTerminal"
     }
   ]
}
```

作成されたlaunch.jsonの中身を↑に書き換える。  
  
さらに、.vscode下にあるsetting.jsonの中身を

```json
{
   "python.pythonPath": "${workspaceFolder}/.venv/Scripts/python"
}
```

これに書き換える。  
この設定をすると、VSCodeでPythonを実行したときに、.venv内のpythonを  
使用するようになる。  
  
![](https://gyazo.com/47cd29cfc0bc4b6eab229f466179b845.png)

作成した仮想環境にモジュールをインストールしたい場合は、  
コンソールで pipenv install #### を実行することで  
インストールすることができる。  
  

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
pipenv install
```
を実行します。  
  
実行すると、 Pipfile に記載されているパッケージのうちインストールされていない物があれば  
インストールされます。  
空の場合、指定のPythonバージョンの環境構築も行われます。  
  



