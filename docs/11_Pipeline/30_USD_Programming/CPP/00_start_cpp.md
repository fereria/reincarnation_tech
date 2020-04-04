---
title: C++でUSDのコードを書こう(準備編)
---

C++はやらなきゃと思いながらもよくわからん！！と放置してきたところがあるのですが
そもそも始めることすら出来なくて放置してました。  
が、、、せっかくUSDをはじめたので、PythonだけではなくC++でもコードが書けるように
色々とビルドできるようにするまでの環境を、調べながらつくってみました。

## コードを書く

とりあえずこんなコードを動くようにしてみます。

```cpp
#define NOMINMAX

#include "pxr/usd/usd/stage.h"
#include "pxr/usd/sdf/path.h"
#include "pxr/usd/usdGeom/sphere.h"

void main()
{
  auto stage = pxr::UsdStage::CreateInMemory();
  auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/TestSphere"));
  stage->GetRootLayer()->Export("D:/test_sphere.usda");
}
```

同じコードをPythonで書くと、こうなります。

```python
from pxr import UsdGeom,Usd

stage = Usd.Stage.CreateInMemory()
sphere = UsdGeom.Sphere(stage,"/TestSphere")
stage.GetRootLayer().Export("D:/test_sphere.usda")
```

Pythonの場合は、書いたらそのまま実行すればOKなのですが
C++だとそう簡単ではなく、ビルドをする必要があります。
なので、このコードをビルドするためのcmakeを書いていきます。

## cmakeを書く

https://cmake.org/

まずは、cmakeをダウンロードしてインストールします。

```
cmake_minimum_required(VERSION 3.1)
project(testProj)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(USD_INSTALL_ROOT D:/python_lib/usd_py27)
set(PYTHON_ROOT_DIR C:/Python27)

set(USD_LIBRARY_DIRECTORY ${USD_INSTALL_ROOT}/lib)
set(USD_INCLUDE_DIRECTORY ${USD_INSTALL_ROOT}/include)
set(BOOST_INCLUDE_DIRECTORY ${USD_INSTALL_ROOT}/include/boost-1_65_1)

# ライブラリのPath取得
find_library(USD_SDF sdf HINTS ${USD_LIBRARY_DIRECTORY})
find_library(USD_TF tf HINTS ${USD_LIBRARY_DIRECTORY})
find_library(USD_USD usd HINTS ${USD_LIBRARY_DIRECTORY})
find_library(USD_GEOM usdGeom HINTS ${USD_LIBRARY_DIRECTORY})
find_library(TBB_LIB tbb HINTS ${USD_LIBRARY_DIRECTORY})
find_package(PythonLibs 2.7)

add_executable(main_app main.cpp)
target_compile_options(main_app PRIVATE /DWIN32_LEAN_AND_MEAN)
target_include_directories(
    main_app
    PUBLIC
    ${PYTHON_INCLUDE_PATH}
    ${USD_INCLUDE_DIRECTORY}
    ${BOOST_INCLUDE_DIRECTORY}
    ${PYTHON_ROOT_DIR}/include
)
target_link_libraries(
    main_app
    ${USD_LIBRARY_DIRECTORY}/boost_python-vc141-mt-1_65_1.lib
    ${PYTHON_LIBRARY}
    ${TBB_LIB}
    ${USD_SDF}
    ${USD_TF}
    ${USD_USD}
    ${USD_GEOM}
)
```
cppと同じフォルダに、 CMakeLists.txt を作り
中身を↑のようにします。

まずは、cppをビルドするためのプロジェクトを作ります。
いわゆるVisualStudioの slnファイル（ソリューション）がこれにあたります。

そしてその中に追加するプロジェクトを add_executable で追加します。
この第一引数が、プロジェクト名になり、

![](https://gyazo.com/56ebe3e8aa739a3943df57699105cc5b.png)

こんな感じで追加されます。
さらに、そのプロジェクトに対して、使用するライブラリとIncludeフォルダを指定します。
このlinkライブラリのパスは、find_libraryで検索することができますが
boost_pythonはみつけたサンプルのとおりにやるとエラーになったので
自分のビルドしたUSDフォルダにあるboost_pythonのlibを書いてあります。

もう1つトラップだったのが、
サンプルだとPythonLibも find_library で書かれていたのですが、
find_package(PythonLibs REQUIRED)
コレで書くと、python3.7のライブラリが引っかかってしまったので
とりあえずフルパスで追加するようにしました。

...とおもったら色々勘違いしていただけで、REQUIREDではなく指定のバージョンにすれば
そのバージョンのpythonlibをみつけてくれるので、2.7にしておきました。(※追記)

find_package自体は、.cmakeで検索コードを書いたりも出来るみたいなので
色々やってみたいです。

で。
サンプルに必要な Sdf UsdGeom Stage のlibを追加して準備完了。

おなじフォルダに build フォルダを作り、コマンドラインで buildフォルダに移動します。

```
cmake -G "Visual Studio 15 2017 Win64" -DCMAKE_BUILD_TYPE=Release --build ..
```
そしてコマンド実行。
今回はVisualStudio 2017 Win64でビルドしたいので、 -G でバージョンを指定します。
さらに、Debug版だと tbb で盛大にビルドエラーになるので今回はReleaseにします。

実行すると、buildフォルダ下にソリューションファイルができあがるので、
VisualStudioで開き、あとは ソリューションエクスプローラーから main_app を右クリック
そしてビルドすれば完了です。

## はまりポイント

C++初心者な自分が盛大にはまったポイントがいくつかあります。

### window.h マクロ定義問題

https://yohhoy.hatenadiary.jp/entry/20120115/p1

まず1つめが、window.hの定義マクロ問題。
window.hが「min/max」という超被りそうな名前のマクロを定義してしまうため
盛大にエラーを吐いてビルド出来ませんでした。
というわけで、回避策として #define NOMINMAX を定義。

### DWIN32_LEAN_AND_MEAN

もう1つ、window.h が「small」という名のマクロを定義してしまうことで発生する
ビルドエラーを回避するために、DWIN32_LEAN_AND_MEAN を追加。

### Debugモードでのエラー

最後にDebugモード時に、tbb周りのマクロ定義で盛大にエラーになってしまう問題。
なので、cmake コマンドでソリューションを作る時に -DCMAKE_BUILD_TYPE=Release
フラグを追加して回避しました。

### lib入れ忘れ

これも超基本ですが、途中でSphereを作るUsdGeomSphereを追加した場合、 sphere.h を
インクルードしたらエラーになってしまいはじめはかなり困りました。
が、よく考えてみると target_link_libraries で usdGeom.libをリンクしないと
だめじゃん！ってことに気がついて追加したらいけました。

## というわけで...

とりあえず色々と分からないことがあるものの、書き始められるだけの環境はできました。
なんだかんだで理解するだけで1ヶ月以上かかりました。。。C++難しい。

ビルドが通るようになって以降は、ドキュメント自体はC++で書かれていることもあって
（一応文法もわかるので）Pythonで書いたサンプルをC++に移植するとかは出来るようになりました。
一番難しいのはビルドだったのではないかと思います。

とにもかくにも動くようにはなったので、
しばらくはC++の基本を勉強しつつC++でUSDのデータを作って見るのを試してみようと思います。

## 参考
* https://qiita.com/janus_wel/items/a673793d448c72cbc95e
* https://qiita.com/shohirose/items/45fb49c6b429e8b204ac
* https://github.com/ColinKennedy/USD-Cookbook/tree/master/concepts/mesh_with_materials/cpp
* https://www.wagavulin.jp/entry/2017/02/20/082608