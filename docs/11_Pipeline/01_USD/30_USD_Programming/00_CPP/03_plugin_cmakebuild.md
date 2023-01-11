---
title: USDプラグインをcmakeでビルドする
tags:
    - USD
    - cmake
    - C++
description: myGpをcmakeを使ってビルドする
---

C++のビルド環境を作るのが難しくて、今までは USD の build_usd.py を使うようにしていたのですが
cmake を利用してプラグインをビルドを試してみます。

ただし、困ったことに USD のリポジトリ以下にあるサンプルや Cookbook にあるサンプルは
Linux であることを前提にしているためそのままだと素直にビルドできないことが多いです。

https://qiita.com/takahito-tejima/items/01ab2abe2f4c0d12eeed
ので、今回は去年の年末に行われた USD アドカレの技師長師匠が書いた記事の

https://github.com/takahito-tejima/UsdSandbox/tree/main/myGp

こちらのサンプルコードを cmake を使用してビルドしていきます。

> 必要な USD ライブラリ（tf, gf, plug, hd, arch, sdf など）をライブラリに指定して、DLL を作ります。
> ファイル名は myGp.dll としてみました。
> boost とか tbb とか python のリンクあたりは各自の環境ごとに違いますので、
> ここでは説明しませんが頑張ってください。

がんばっていきましょう。

## USD をビルドする

まずは下準備。
プラグインをビルドする前に USD 本体の準備をします。

https://qiita.com/takahito-tejima/items/01ab2abe2f4c0d12eeed#hdgp-%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E4%BD%9C%E6%88%90%E6%BA%96%E5%82%99

詳細はこちらの記事を参照ですが、書かれている通りそのままだと Windows 環境で正しく DLL を作成できません。
ので、記事を参考に該当箇所に HD_API を追加します。

＋ ビルドするときの VisualStudio のバージョンは 2022 だと boost のビルドでエラーになってしまったので
今回は VisualStudio2019 を使用します。

## CMakeLists.txt を用意する

ビルドできたら、サンプルコードを Github からクローンしてきます。
そして、 myGp フォルダ下に CMakeLists.txt を作成します。

https://github.com/ColinKennedy/USD-Cookbook/tree/master/plugins/custom_resolver/project

今回は、 USD-Cookbook の custom_resolver の Cmake を参考にして書いていきます。
ので、こちらの cmake/FindUSD.cmake を cmake フォルダにコピーします。

https://gist.github.com/fereria/83c5311170e09f8c84f577b4e4286151

完成した CMakeLists.txt はこちら。

### find_package(USD REQUIRED)

まず、 find_Package するときの挙動。
ここで使用している find_package は、モジュールモードと呼ばれるもので
CMAKE_MODULE_PATH で指定したフォルダ以下にある Find###.cmake を探しにいきます。

今回の場合、プロジェクト以下に cmake フォルダがあり、その中に Find###.cmake をいれるようにしたので

{{'790a8819beff51c46c8e841521bb5ba3'|gist}}

CMAKE_MODULE_PATH を追加してから find_package しています。

参考: https://theolizer.com/cpp-school3/cpp-school3-10/

サンプルの FindUSD では、USD_INSTALL_ROOT(ビルドした USD の成果物フォルダ) 以下にある
INCLUDE_DIR LIBRARY_DIR、USD のバージョン番号をセットしています。

ただしサンプルは Linux 用でそのままだとエラーになるので
USD_LIBRARY_DIR を usd_usd.dll に書き換えておきます。

## find_package(PythonLibs REQUIRED)

一見すると Python 使ってないじゃん　と思うのですが、Boost 用に Python の IncludeDir を入れる必要があるので
find_package を使用して PythonLibs を読んでおきます。
が、そのままだとライブラリが見つからなかったのですが

```
set(PYTHON_LIBRARY "C:/Users/remir/AppData/Local/Programs/Python/Python39/libs")
set(PYTHON_INCLUDE "C:/Users/remir/AppData/Local/Programs/Python/Python39/include")
```

PYTHON_LIBRARY と PYTHON_INCLUDE を指定しておくと見つけられるらしいので入れておきます。

参考: https://qiita.com/peisuke/items/179094c9d1387788256e#%E3%81%9D%E3%81%AE%E4%BB%96%E3%81%AE%E3%82%B1%E3%83%BC%E3%82%B9

## /Zc:inline-

{{'08e9f095026c2f53452dea3c8a160a5c'|gist}}

:fa-external-link: [HdGp プラグイン作成～準備～](https://qiita.com/takahito-tejima/items/01ab2abe2f4c0d12eeed#hdgp-%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E4%BD%9C%E6%88%90%E6%BA%96%E5%82%99)にも言及されていますが、Windows の場合このままだとプラグインのロードができないので
/Zc:inline- をフラグに追加しておきます。

https://github.com/PixarAnimationStudios/USD/blob/faed18ce62c8736b02413635b584a2f637156bad/cmake/defaults/msvcdefaults.cmake#L37
https://github.com/PixarAnimationStudios/USD/blob/0c7b9a95f155c221ff7df9270a39a52e3b23af8b/CMakeLists.txt#L38

USD リポジトリにある cmake のコードはこのあたりに書かれていて
特定のバージョン以上の場合は、 /Zc:inline- を入れるようになっています。

このフラグを入れなかった場合、usdview を起動するときに

```
set TF_DEBUG=PLUG_*
```

デバッグフラグを入れて確認してみると、

![](https://gyazo.com/23c96a38d02fb0d0b9b44b525575a1e6.png)

このようなエラーになり、プラグインロードに失敗していることがわかります。

なお、今回は VisualStudio2019 でテストしましたが
2022 の場合は /Zc:inline- ではなく /OPT:NOREF を指定して回避するようです。
バージョンによって対応が異なるので注意が必要です。

## link_directories

次に地味にはまったのが link_directories
ライブラリの位置を指定して、 target_link_libraries で相対パスで記述できるようにするのですが
この記述は add_library の前に書いておかないとダメでした。
（lib が見つからないエラーではまる）

## add_library

add_library は、プラグインのコード(cpp) を入れておきます。
そして target_link_libraries で、使用する lib を指定します。

{{'629ee8538bb2f20eee808fc09f28f6a6'|gist}}

なお、hdGp に HD_API を足すのをやらないと
target_link_libraries に usd_hdGp.lib を入れていてもリンクエラーになるので要注意です。

## install

ビルドは以上ですが、ビルドが終わった後に特定のフォルダーに
成果物をコピーできるように install を書いておきます。

{{'cd1360bc56ed860c8a1cdfe159179f31'|gist}}

USD のプラグインは、特定のフォルダ以下に PluginName/resources/plugInfo.json を置くようなルールになっています。
ので、今回はインストール先直下に dll を、 myGp/resources 下に pluginInfo.json を配置できるようにします。

## 実行する

準備ができたら実際にビルドします。

![](https://gyazo.com/e7645b0f317a00bf2bd173cc6b0ae6cb.png)

myGp 以下に build フォルダを作り、コマンドプロンプトで build 以下に移動します。

```batch
cmake -G "Visual Studio 16 2019" ..
cmake --build . --config Release
cmake --install . --prefix C:/USD/plugin/usd
```

はまったところとしては、ビルドするときには Debug ではなく Release にしておかないと

{{'https://twitter.com/anamorphobia/status/1612099101147160576'|twitter}}

boost_python の lib が -gd つきのデバッグ用の lib になってしまうので
対象のライブラリが見つからずにエラーになります。

インストール先は、 DCMAKE_INSTALL_PREFIX で指定したフォルダー以下にインストールされるのですが
cmake のコマンドラインで変更したい場合は --prefix を指定すれば OK でした。

## 起動してみる

無事にビルドができたら、usdview で再生してみます。
再生前に、 22.11 の場合はあらかじめ環境変数をセットしておきます。

```
set HDGP_INCLUDE_DEFAULT_RESOLVER=1
set TF_DEBUG=PLUG_*
```

assets 以下にある gp2.usda を開いてみると

![](https://gyazo.com/e339e47526b5df5d93a82cb05192eb9d.png)

無事プラグインのビルドができていました。

## まとめ

というわけで、無事にビルドができました。
すでに存在しているコードをビルドするだけで年を越を超えてしまいました。
Windows でビルドするの難し過ぎます。
（これを専門にしているビルドエンジニアやばい）

まだまだ基本的なところのみでクリアできた程度ですが
今回 cmake でビルドするまでの流れをだいぶ調べたおかげで
手も足も出なかった部分に少し手が出せるようになった気がします。

試行錯誤できるスタートラインに立てたので、しばらくは C++のプラグイン作成を
勉強していこうと思います。
