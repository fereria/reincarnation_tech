---
title: VSCodeで C++の環境を作るメモ
tags:
    - CPP
    - vcpkg
    - VSCode
description: vcpkgを使用してC++のプロジェクトを0から構築する方法
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

## imgui をビルドするために必要だったこと

基本は ↑ で良いのですが、指定の backends でサンプルを実行するにはいくつか必要だったので
メモがてらまとめておきます。

### imgui の指定の binding をインストールする

```
vcpkg install imgui[glfw-binding,opengl2-binding]:x64-windows --recurse
```

imgui のうち、 glfw-binding と opengl2-binding が必要だったので
両方をインストールするようにします。

```
vcpkg install glfw3:x64-windows
```

さらに glfw3 をインストールします。

```
cmake_minimum_required( VERSION 3.6 )

project(SampleProj CXX)

set( CMAKE_CXX_STANDARD 11 )
set( CMAKE_CXX_STANDARD_REQUIRED ON )
set( CMAKE_CXX_EXTENSIONS OFF )

find_package(imgui CONFIG REQUIRED)
find_package(glfw3 CONFIG REQUIRED)

add_executable(main main.cpp)

target_link_libraries(main PRIVATE glfw)
target_link_libraries(main PRIVATE imgui::imgui)
target_link_libraries(main PRIVATE opengl32.lib)
```

そのうえで CMakeLists.txt を書きます。
これで無事 imgui のサンプルを vcpkg でインストールした環境で実行できました。

難しい！
