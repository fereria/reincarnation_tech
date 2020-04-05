---
title: VSCodeでJupyter
---
# VSCodeでJupyter

数学関係の勉強をPythonで実行するために  
話題のJupyterをVSCodeにインストールしてみました。  

## 下準備

[pipenvのインストール](/10_Programming/00_PG_setup/pipenv_statup/)

Jupyterの環境を作成する前に、Pipenvを使用して環境を構築します。  

![](https://gyazo.com/bb59a891a8dea4b109982792059b6795.png)

VSCodeのワークスペースを作成し、その下に「.venv」を作成します。  

```Pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
numpy = "*"
pandas = "*"
jupyter = "*"
matplotlib = "*"
scipy = "*"
sympy = "*"

[dev-packages]
pytest = "*"
"flake8" = "*"

[requires]
python_version = "3.6"
```
今回の環境はこんな感じにしています。  
Pythonのバージョンは3.6です。  
  
Jupyterに関して調べたときにはAnacondaで構築している例のほうが圧倒的に多いですが、  
Pipenvを使用しても環境構築はできました。

## コードを作成する

まず、実行するコードを書きます。

```python
# %%

from sympy import Symbol, solve

a = Symbol('a')
b = Symbol('b')

ex1 = -1 * a + b - 2
ex2 = 2 * a + b - 4

solve((ex1, ex2))

# %%

print("hello world")
```


Jupyterは、「セル」と呼ばれる単位でスクリプトを実行していきます。  
ざっくりというと、1つのPythonファイルだけど複数のコードを区切って記述できる機能で  

```
# %%
```
コードの区切り部分にコレを記述しておくと、そこがセルの開始・終了地点扱いになります。  
そして、  

![](https://gyazo.com/6276c083c75014b2aa1ea3928f648198.png)

こんな感じで Run Cell が表示されるので、大文字のCのほうの「RunCell」（中央）を  
クリックします。  
  
!!! Note
    初回の起動のみ、若干時間がかかります。
    

![](https://gyazo.com/54cfda0226941ef1714d0eb51267d7bb.png)

実行すると、こんな感じで現在の変数と、セルの実行結果が表示されます。  
  
結果は、printをしていなくても表示される模様。  
  

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-10, 10, 0.1)

y = x**3 + 3 * x ** 2 + 3 * x + 1
plt.plot(x, y)
plt.show()
```

Jupyterの便利なところは、こんな感じでグラフを表示するコードを書いた場合  
  
![](https://gyazo.com/9ba6509c311dc4f640b8835d9234eb2a.png)

Python Interactive画面にグラフを描画してくれるところ。  
  
```
#%% [markdown]

# # HOGEHOGE
# * fugafuga
# * fugafuga
```
通常のJupyterの場合、セル内にMarkdownを書くと  
Markdown扱いにしてくれますが  
VSCodeの場合はコメントアウトが必要のようです。

![](https://gyazo.com/d0582992e0963f13529b0340b2a49973.png)

結果。  
  
## 実行結果を出力する

![](https://gyazo.com/5bdbc552c911631ed5424299dbab0b2a.png)

Jupyterで実行した結果は、ipynbファイルに出力ができます。  

## notebookを起動して、実行する

Anacondaでインストールした場合は、Windowsのスタートアップからノートブックを起動  
できるようですが、Pipenvの場合は特にないので  

```
.venv\Scripts\jupyter-notebook.exe
```

この実行ファイルを実行します。  

![](https://gyazo.com/cbb77f6f598aeaad37b95f69730570bd.png)

実行すると、サーバーが起動してブラウザからJupyterを開くことができます。  
このときの初期フォルダは、jupyter-notebook.exeを実行したフォルダがルート扱いになるので、  
（特に指定しなければ Scriptsフォルダがルート）  
Pythonプロジェクト下に「notebook-run」フォルダを作成し  
そこがルートになるように起動しました。  
  
このルートに表示されている「test_result.ipynb」をクリックすると  
  
![](https://gyazo.com/cb3960af19acd0cd2234c537cf18cf4a.png)

ブラウザ上でも同じ結果を確認することができます。  
  
自分のように、数学の勉強に使うだけなら保存機能はいらない気もしますが  
グラフの結果を共有したりとかするのには便利そうです。  
  
これ以外に、自宅のSynologyサーバーのDockerに  
Jupyterのコンテナをインストールしてみましたが、現状の使用範囲だと  
VSCode内で実行できたほうが便利でした。  
  
![](https://gyazo.com/eb56a1e0c72526debc06c3a989dfb468.png)

今のところうまくいってないのですが、  
SelectanExistingJupyterNotebookで、サーバー上のDockerを指定することで  
サーバー上で実行できる機能があるようですが、（Run cellで実行されるのはこっち？）  
VSCodeのエラーがでてしまい実行できませんでした。  
  
使い所はまだまだ未知数ですが、  
数学まわりの勉強の土台にしつつ色々と試してみようかなと思います。