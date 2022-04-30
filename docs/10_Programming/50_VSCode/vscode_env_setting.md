---
title: VSCodeのターミナルを設定する
tags:
description:
---

VSCode のターミナルは、最近のバージョンではいろいろ機能が追加されて
便利になっているので、使い方と設定を試してみます。

## ターミナルを開く

```
Ctrl+Shift+`
```

ターミナルは Ctrl+Shift+`で開けます。

![](https://gyazo.com/dcbdf70d4c70a16b184ef519e851e016.png)

デフォルトだとコマンドプロンプトが開きます。

![](https://gyazo.com/7a7e95cbd19299c63b39c3ddbdf4712e.png)

![](https://gyazo.com/29924ccf1f08465df2f620f593840416.png)

さらに、＋を押せば複数のプロンプトを切り替えながら使用することができます。

![](https://gyazo.com/0a1930b8fc124d82e7db9d72aa20746b.png)

さらに、広い画面で実行したければエディタ領域にも移動できるので、
これを利用することで、VSCode内で完結してターミナルの作業が可能になります。

## プロファイルの作成

VSCode には、ターミナルのプロファイルを自分で定義して追加する機能があります。
これに環境変数の指定を追加することで、
Windows 側に指定を入れずに環境を構築したり、自分好みの指定のターミナルを作成することができます。

![](https://gyazo.com/8f54af8cde44f9c20cdae4452e48fb02.png)

```
	"terminal.integrated.profiles.windows": {
		"terminal": {
			"path": ["cmd.exe"],
			"icon": "terminal-powershell",
			"env": {
				"PATH": "C:/USD/bin;C:/USD/lib;${env:PATH}",
				"PYTHONPATH": "C:/USD/lib/python;${env:PYTHONPATH}"
			}
		}
	},
	"terminal.integrated.defaultProfile.windows": "terminal"
```

デフォルトで起動するプロンプトの環境に、指定の環境変数を追加したい場合は
settings.json にこのように追加します。
プロファイルに対して環境変数を追加し、
デフォルトプロファイルを追加したものにします。

```json
		"python37": {
			"path": ["py"],
			"args": ["-3.7"],
			"icon": "star-full"
		}
```

このプロファイルは、コマンドプロンプト以外を指定することもできて、
たとえば、Path を Python、引数を指定することで

![](https://gyazo.com/f42e5662101d5dca994e9615914c8878.png)

Python のコマンドラインを簡単に起動できます。


## 参考

* https://code.visualstudio.com/docs/editor/integrated-terminal