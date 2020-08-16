---
title: Custom AssetResolver を作ろう
---

夏休みのまとまった時間を使ってなにか新しいことでもやってみるかー　ってことで
C++のみで作れる USD の AssetResolver プラグインを作ってみました。

## AssetResolver とは？

AssetResolver とは、USD 内のファイルパスの参照先の解決部分を拡張することができる機能です。

![](https://gyazo.com/d306a707c3d9aab0752ce0372c869012.png)

たとえば、ある usd ファイルが Char.usda というファイルをリファレンスで参照している場合。

```
def "char"{
    def "Char_A"(prepend references = @Char.usda@){}
}
```

こんな感じで @@ で囲んだ中に参照先の usda のファイルパスを記述します。
上の場合、デフォルトの場合相対パスとして扱われ
test.usda と同じフォルダにある Char.usda をリファレンスでロードしに行くようになります。

あるいは、 **PXR_AR_DEFAULT_SEARCH_PATH** と呼ばれる環境変数に PATH が指定されている場合は
相対パス以下にファイルがない場合、DEFAULT_SEARCH_PATH に指定された順序で usda を検索しにいき、
見つかった PATH を usda のロード先としてファイルの PATH 解決を行います。

### AssetResolver での拡張例

では、これを利用してどういうことができるかというと、

https://github.com/LumaPictures/usd-uri-resolver
LumaPictures が GitHub 上で公開している USD-URI-resolver のように、

@sql://<server_name><asset_path>@
このようにリファレンスのパス（アセットパス）をカスタマイズして、
SQL に usd ファイルの Path を問い合わせして、その DB の結果を元に USD のパスを返す...といったことや

https://github.com/westerndigitalcorporation/usd-s3-resolver

westerndigitalcorporation が公開している S3-Resolver のように
Amazon AWS に usda のファイルを問い合わせをして、PATH を解決するといったように

![](https://gyazo.com/576300414f58de8c16a559e41494b033.png)

単純に USD ファイルに記載された Windows などのファイルパスで USD の PATH を解決するのではなく
PATH解決に対して何かしらの処理をプラグイン内で行って
その結果でPATHを解決させられるのが AssetResolver という機能になります。

## 作ってみよう

というわけで、URI-ResolverとS3-Resolverをベースにして
もう少しかんたんなAssetResolverを作ってみます。

AssetResolverを作りたい場合は、PythonではなくC++で実装する必要があったので
今回はC++の勉強を兼ねてやってみました。

### ビルド環境を作る

今回は独自環境をつくるのではなUSDのリポジトリ以下にある ビルドスクリプトを利用して
本体と一緒にビルドする形で作ってみます。

![](https://gyazo.com/672302d498c96f38989c32ff8461c90e.png)

extras 下に plugins を作り、その下に testResolver を作ります。
そしてその下に CMakerLists.txt と plugInfo.json あとはResolverのcppとヘッダーを作ります。

```cmake
set(PXR_PACKAGE sampleResolver)

pxr_plugin(${PXR_PACKAGE}
    LIBRARIES
        tf
        sdf
        usd
        vt
        ar

    INCLUDE_DIRS
        ${Boost_INCLUDE_DIRS}
        ${PYTHON_INCLUDE_DIRS}

    PUBLIC_HEADERS
        sampleResolver.h

    PUBLIC_CLASSES
        SampleResolver
    
    RESOURCE_FILES
        plugInfo.json
)
```
cmakeは、他のプラグインサンプルを参考に必要最低限のものを用意します。

```json
{
  "Plugins": [
    {
      "Info": {
        "Types": {
          "SampleResolver": {
            "bases": ["ArResolver"]
          }
        }
      },
        "LibraryPath": "../sampleResolver.dll",
        "Name": "SampleResolver",
        "Root": "..",
        "Type": "library"
    }
  ]
}
```
plugInfo.jsonは、USDの環境に作成したAssetResolverプラグインをロードさせるためのファイルです。
Types の部分が、AssetResolverを使用するときのお約束部分で SampleResolver となっているところが
作成したResolverClassの名前です。

LibraryPath は、 plugins 以下での resource フォルダと plugInfo.json のPATH
そしてプラグインの本体になる dll のPATHの指定になります。
このPATHは、plugInfo.jsonから見た場合のパスになっていて、

![](https://gyazo.com/75817ea61347a8cb29de9fcd3fa041a2.png)

USD/plugin/usd フォルダに dll がリリースされ、
plugInfo.jsonは \<pluginName\>/resources/plugInfo.json にリリースされます。
ので、 このRootは、 resources フォルダを指し、そのRootから見ての LibraryPathは ../sampleResolver.dll
となっているので、Root の１つ上の階層の usd フォルダ直下にあるものをロードする
という意味になります。

### C++のコードを書く

次にC++のヘッダー。

```cpp
#pragma once

#include <pxr/usd/ar/defaultResolver.h>

#include <iostream>
#include <memory>
#include <string>
#include <vector>

PXR_NAMESPACE_OPEN_SCOPE

class SampleResolver : public ArDefaultResolver
{
public:
    SampleResolver();
    ~SampleResolver() override;

    std::string Resolve(const std::string &path) override;
    virtual std::string ResolveWithAssetInfo(
        const std::string &path,
        ArAssetInfo *assetInfo) override;
};

PXR_NAMESPACE_CLOSE_SCOPE
```
カスタムのAssetResolverを作る場合は、ArDefaultResolverを継承したクラスを作成します。
そして、PATH解決をするための関数 Resolve と ResolveWithAssetInfo ２つを実装します。
(今回の場合はResolveはなくても良かった)

```cpp
#include "sampleResolver.h"

#include <pxr/usd/ar/assetInfo.h>
#include <pxr/usd/ar/resolverContext.h>
#include "pxr/base/tf/fileUtils.h"

#include <pxr/usd/ar/defaultResolver.h>
#include <pxr/usd/ar/defineResolver.h>

using namespace std;

PXR_NAMESPACE_OPEN_SCOPE

AR_DEFINE_RESOLVER(SampleResolver, ArResolver)

// コンストラクタ
SampleResolver::SampleResolver() : ArDefaultResolver()
{
}
// デストラクタ
SampleResolver::~SampleResolver()
{
}

std::string SampleResolver::Resolve(const std::string &path)
{
    cout << "PATH: " << path << endl;
    return path;
}

std::string SampleResolver::ResolveWithAssetInfo(const std::string &path, ArAssetInfo *assetInfo)
{
    if (!TfPathExists(path))
    {
        cout << "AssetInfo PATH: " << path << endl;
        return "D:/USDsample/cube.usda";
    }
    return path;
}

PXR_NAMESPACE_CLOSE_SCOPE
```

そして本体。
今回のサンプルでは、Referenceで参照しているUSDファイルが見つからない場合
指定のUSDAを無理やり表示させてみる...というサンプルです。

このPATH解決をするには、 Resolve と ResolveWithAssetInfo という2つの関数があります。
当初は Resolve で return したPATHがReferenceのPATHとして使われるのかなと思っていたのですが
そういうわけではなく
Resolveは、現在の開いているレイヤーのPATH解決で
ReferenceのPATH解決は ResolveWithAssetInfo の return で返されるPATHでした。

なので、 URI-Resolverなどは、 Resolve 内で ResolveWithAssetInfoを呼び
同じ処理を実行するようにしている？ようです。

ResolveWithAssetInfoは、引数として処理しようとしているPATHと、そのPATHのAssetInfoが
渡されます。
C++初心者の理解として PATH の 方は const で編集不可
assetInfoはポインタ渡しで現在のAssetInfoが渡されているので
AssetResolverでPATH解決をするときに、AssetInfoを使用 or 書き換えを
この関数内で行うのかなと思います。

### ビルドする

ここまで準備ができたら USDビルドを実行します。
VisualStudioのコマンドプロンプトで
```bat
python build_scripts\build_usd.py D:/USD
```
ビルドスクリプトを実行すれば、本体のビルドと一緒に作成したプラグインもビルドしてくれます。

![](https://gyazo.com/4be4b274fe480b2bb53e3bc31c48a555.png)

dllは、plugin/usd 直下に作成され
plugInfo.json は sampleResolver/resources 下にコピーされます。

### PathUtils

C++のPathまわりってどうするんだろう？？というのが
AssetResolverを使用していたときの疑問だったのですが、
USDはこのあたりのユーティリティが色々用意されているようなので、今回はそれを利用しました。

https://graphics.pixar.com/usd/docs/api/file_utils_8h.html
https://graphics.pixar.com/usd/docs/api/path_utils_8h.html
os.pathにあるようなものは、FileUtilsか、PathUtilsを使用すれば概ね望んだ結果が得られて

```cpp
void USD_StringUtil()
{
    // StringUtil/PathUtilテスト

    vector<string> paths = TfGlob("D:/USDSample/*.usda");
    for (const auto &path : paths)
    {
        cout << path << endl;
    }
    // pathUtil
    cout << TfNormPath(paths[0]) << endl;
    cout << TfAbsPath(paths[0]) << endl;
    cout << TfIsRelativePath(paths[0]) << endl;
    cout << TfGetExtension(paths[0]) << endl;
    // StingUtil
    cout << TfStringJoin(paths) << endl;
    cout << TfStringToUpper(paths[0]) << endl;
    cout << TfStringContains(paths[0], "usda") << endl;
    cout << TfGetPathName(paths[0]) << endl;
    cout << TfStringReplace("hogehoge", "hoge", "fuga") << endl;

    //env
    cout << TfGetenv("PATH") << endl;
}
```
別途色々試してみましたが、GlobだったりBasenameだったり、Replace、Join、Upperなどが使えました。

今回のAssetResolverの場合、使ったのはTfPathExists だけでしたが
指定の名前をReplaceして、そのPathを返すなど
PATH関係の処理は概ねこのユーティリティを使えば作れそうなのがわかりました。

### 結果

ビルドができたら挙動を確認してみます。

```usda
#usda 1.0

def "reference1" (
    prepend references = @./sphere.usda@</sphere1>
)
{
}
```
まずはこんな感じのusdaを作り、

```
#usda 1.0

def Cube "sphere1"
{
    double radius = 1
    matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    uniform token[] xformOpOrder = ["xformOp:transform"]
}
```

あえて sphere.usda は作らず cube.usda を作っておきます。

普通の場合は、ファイルが見つからずにエラーになってしまいますが、
![](https://gyazo.com/d2cdbe142faa269510125c58ae2a32d5.png)
AssetResolverを作ったおかげで、ファイルは参照された状態になりますが
![](https://gyazo.com/fc981d77fe0e5c4cfeaff1b73e0cf13a.png)
Copy Layer Path などで、実際にロードされているファイルを確認すると
sphere.usda ではなく cube.usda がロードされていることがわかります。

あとは、自分の実際にやりたい処理に応じて Resolve または ResolveWithAssetInfo を
拡張していけばいろいろな処理を追加することができそうです。


## 参考
- https://github.com/ColinKennedy/USD-Cookbook/tree/master/plugins/custom_resolver