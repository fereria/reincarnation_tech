---
title: VSCodeで C++の環境を作るメモ
tags:
    - CPP
    - vcpkg
    - VSCode
description:
---

C++で必要なライブラリを取得して、 CMakeLists.txt を使用して
VS Code でビルドするまでの流れをメモがてらまとめ。

## vcpkg のインストール

https://github.com/microsoft/vcpkg

C++のライブラリを取得してくるコマンドラインツール。

```bat
git clone https://github.com/microsoft/vcpkg
.\vcpkg\bootstrap-vcpkg.bat
```

Github からクローンして、上記のコマンドでビルドする。
無事に完了すると vcpkg に vcpkg.exe ができるので、このフォルダを PATH に入れたりして vpckg コマンドが
使えるようにする。

## VS Code のワークスペース設定

vcpkg がインストールできたら、VS Code でワークスペースを作成します。

```json
{
	"folders": [
		{
			"path": "."
		}
	],
	"settings": {
		"cmake.configureArgs": [
			"-DCMAKE_TOOLCHAIN_FILE=D:/work/repos/vcpkg/scripts/buildsystems/vcpkg.cmake"
		]
	}
}
```

code-workspace ファイルに、 cmake.configureArgs を追加します。
パスは vcpkg のインストールフォルダ以下の scripts/buildsystems/vcpkg.cmake を指定。

## vcpkg でライブラリを取得する

登録されているライブラリは vcpkg install #### でインストール可能なので、 imgui を入れてみる。

```
vcpkg install imgui:x64-windows
```

ライブラリ名の後に、 x64-windows を入れることで、64 ビット版を取得できます。

![](https://gyazo.com/7b46c9c51480bb26cdc71519074c4103.png)

無事インストールできました。
CMakeLists.txt への書き方が書いてあるので、CMakeLists.txt にコピペします。
