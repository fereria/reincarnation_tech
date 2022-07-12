---
title: PyInstallerでexeを作る
tags:
    - Python
description: 単独で実行できるファイルにコンバートする方法
---

PyInstaller を利用すると、Python のコードを exe 化して
Python をインストールしなくても単独のツールとして利用できるようになります。

## 基本的な使い方

まず、使うときには pip で pyinstaller をインストールします。

```
pip install pyinstaller
```

インストールしたら、

```
pyinstaller <exeにしたいpythonPath.py> --name <toolName>
```

このように実行すると、

![](https://gyazo.com/f2ec06b080287cd660ae504132e091f1.png)

コマンドプロンプトのカレントディレクトリ以下に、 \<toolName\>.spec ファイル、 build dist フォルダが作成され

![](https://gyazo.com/b087ce5d0a62f7e57545aab9f606465b.png)

dist フォルダ以下に、exe が作成されます。

```
pyinstaller <exeにしたいpythonPath.py> --name <toolName> --onefile
```

デフォルトだと toolName.exe 以外にも各種 dll などが同じフォルダに作成されますが
--onefile を追加することで

![](https://gyazo.com/c74ad46e25b97b6ad16f58a4009d59f6.png)

１つの exe に固めることができます。

## spec ファイルを編集する

基本はこれで OK ですが、
例えば python ファイル以外に、追加でファイルが必用な場合（画像、ui ファイル等）は
別途 exe と同じフォルダにファイルをコピーしないといけないので
そのような場合は spec ファイルを編集します。

```txt title="sample.txt"
hogehoge
```

```python title="samplecode.py"
with open(resource_path('sample.txt'), 'r') as f:
    print(f.read())
```

例えば、同じフォルダ以下にある sample.txt をプリントするようなコードを exe にする場合

```python

a = Analysis(
    ['samplecode.py'],
    pathex=[],
    binaries=[],
    datas=[('sample.txt','.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
```

追加するのは、 datas の配列で
この配列に (ファイル名,コピー先) のタプルを入れることで、ファイルをコピーすることができます。

### onefile の場合

注意が必要なのが、 onefile の場合。
この場合、１つにまとめたファイルをいったん　\_MEIPASS 　に展開する都合、
相対パスで指定してしまうとエラーになります。

https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile

その場合は、ファイルパスの取得をするための関数を用意して
pyinstaller で固められている場合は、MEIPASS を指定するようにする必要があります。
