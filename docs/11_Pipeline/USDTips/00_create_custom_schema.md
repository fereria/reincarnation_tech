# オリジナルの New Schema Classを作る

<!-- SUMMARY:オリジナルの New Schema Classを作る -->

USD のスキーマは自分で新しく定義することができます。  
今回は、1からスキーマを作成してPython上から呼び出しをできるようにしてみます。  

一応、公式のHPチュートリアルに  
https://graphics.pixar.com/usd/docs/Generating-New-Schema-Classes.html  
  
こちらがあります。  
日本語ページは、  
最近北口( [@kit2cuz](https://twitter.com/kit2cuz) )さんの翻訳があります（感謝！！！！）ので  
そちらも併せてご確認をば。

https://usd.prisms.xyz/tutorials/Generating-New-Schema-Classes.html  
  
## 環境を作る

まずは環境を作ります。  
プラグインスキーマを作りたい場合は、プラグインを単体で作ると言うより  
USDのGitHubリポジトリからクローンしたプロジェクトをベースに作成していきます。  
  
なぜならば、

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">スキーマプラグインのビルドとusdのビルドはほぼ同じ意味なので、そうですね。<br>そもそも全部プラグインです。</p>&mdash; 技師長 (@gishicho) <a href="https://twitter.com/gishicho/status/1178182489216409600?ref_src=twsrc%5Etfw">September 29, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

公式のスキーマもカスタムスキーマもも扱いは同じ「プラグイン」なので  
公式で用意されている各種ビルド環境を使う方が色々と容易にビルドすることができるからです。  
  
というわけで、まずはUSDのビルドから始めます。

### USDをビルドする

自分もなんとなく「USDのビルドってみんな面倒くさいって言ってるし・・・」と  
ビルド方法すら、調べることすら拒否してるところがありましたが  
実際は全然そんなことはなく、ものすごく簡単です。  
  
まずは、  
https://github.com/PixarAnimationStudios/USD  
公式のリポジトリからソースコードをクローンしてきます。  
  
そして、

* Visual Studio2017
* (おそらく) Windows 10 SDK
* Python2.7

をインストールします。  
  
次に、 Python2.7 の

* C:/Python27
* C:/Python27/Scripts

この2つのPATHを通します。  
  
次に、 pip を使用して
```
pip install pyside
pip install PyOpenGL
```
この2つをインストールします。  
  
そして最後に、

![](https://gyazo.com/a10b6ae596f249d65c96d1866c66f697.png)

開発者コマンドプロンプト for  VS 2017を開き、  
クローンしたフォルダに移動して

```
python build_scripts\build_usd.py "<Build先>"
```
コマンドを実行します。  
<Build先>部分は、自分の好みのパスにします（例 I:/USD 等）  
  
あとは1時間ほど待つと

![](https://gyazo.com/334872b5d37a7866c0e1c79a81119468.png)

ビルドが完了するので  
あとは、書かれている通りに  

PYTHONPATH を

* USD/lib/python

に通すのと

PATHを

* USD/bin
* USD/lib
* USD/plugin (これは後で説明)

この２つに通します。  
  
以上で準備は完了です。  
  
### NewSchemaClassを作る

#### 作業フォルダを作る

ここまで準備ができたら、NewSchemaClassを作成します。  
まずは、USDの公式のビルドシステム（上の build_usd.pyを使用したやり方）に乗っかって  
ビルドできるように、CMakeLists.txtを作成していきます。  
  
リポジトリのプロジェクト下の  

![](https://gyazo.com/c73bf027c3b9733d507a0381ae348bad.png)  

USD/extras/usd　下に、 custom というフォルダを作ります。  
名前は何でもOKです。  
  
次に、extras/usd 直下にある CMakeLists.txt に

```cmake
add_subdirectory(examples)
add_subdirectory(tutorials)
add_subdirectory(custom)
```

![](https://gyazo.com/2c4edeed7bd9153523b4b673828a1805.png)

add_subdirectory(####) #### は作成したフォルダ名　を追加します。  
そして、customフォルダしたに作成するスキーマの作業フォルダを作り、  
customフォルダ下に CMakeLists.txt を作成して

```
add_subdirectory(hogehoge)
```

add_subdirectory を追加します。  
  
#### schema.usda を作る

フォルダができたら、次にカスタムスキーマのためのcppを作成する元になる  
schema.usdaファイルを作成します。  
  
```schema.usda
#usda 1.0
(
    subLayers = [
        @usd/schema.usda@
    ]
)

over "GLOBAL" (
    customData = {
        string libraryName       = "hogehoge"
        string libraryPath       = "."
    }
) { 
} 

class "FugaPrim" (
    inherits = </Typed>
    customData = {
        string className = "Fuga"
    }
)  {
    int intAttr = 0
}
```
  
ここで定義した内容が、カスタムスキーマの構造になります。  
  
まず、必須なのが usbLayers = [～～～～]の部分と over "GLOBAL" 部分になります。  
GLOBAL部分は、作成するプラグイン情報の定義を行う所で  
libraryName が必須要素になります。  
これは、全プラグイン（デフォルトのスキーマも含めて）でユニークである必要があります。  
  
libraryPath は、ビルドした後の includeとlib 下のどこに Headerファイルを配置するか  
指定する場所になります。  

!!! info
    現状、 libraryPath を入れると .h が見つからないエラーが出てビルドできない  
    それは原因調査中。  
    . の場合は include 直下に、ライブラリ名の Headerが作成されます
  
準備ができたところで、この schema.usda を cpp と .h ファイルにコンバートします。

```
usdGenSchema S:\fav\import_data\github\USD\extras\usd\custom\hogehoge\schema.usda
```

コンバートをするときは usdGenSchema に、作成した schema.usda を渡せばOKです。  
Windowsのせいなのか、相対パスでは記述できないのだけ注意が必要です。  
  
![](https://gyazo.com/b806510f43362a68c1af4e499193c327.png)

実行すると、同じフォルダに cpp と .h が作成されます。  

#### 必要なファイルを準備する

実行した cpp .h 以外にもいくつか必要なファイルがあるので  
それらをサンプルからコピペしてきます。  
USD/extras/usd/examples/usdSchemaExamples  
場所はこのカスタムスキーマのサンプルから

* module.cpp
* moduleDeps.cpp
* pch.h
* __init__.py

この4つをコピペします。  
そして少し書き換えます。

```cpp
#include "Python.h"
#include "pxr/pxr.h"
#include "pxr/base/tf/pyModule.h"

PXR_NAMESPACE_USING_DIRECTIVE

TF_WRAP_MODULE
{
    TF_WRAP(HogehogeFuga);
}
```
まずは module.cpp の中の TF_WRAP_MODULEのなかに TF_WRAP( #### ) を作成したい  
プロジェクト名＋クラス名にします。  
今回は hogehoge ライブラリの Fuga クラスだったので HogehogeFuga になります。  
頭の文字は大文字に代わるので注意。  
  
```cpp
TF_REGISTRY_FUNCTION(TfScriptModuleLoader) {
    // List of direct dependencies for this library.
    const std::vector<TfToken> reqs = {
        TfToken("sdf"),
        TfToken("tf"),
        TfToken("usd"),
        TfToken("vt")
    };
    TfScriptModuleLoader::GetInstance().
        RegisterLibrary(TfToken("hogehoge"), TfToken("pxr.Hogehoge"), reqs);
}
```
次が moduleDeps.cpp   
このファイルは  
上の TF_REGISTRY_FUNCTION 内にある RegisterLibrary にある TfToken("プロジェクト名"),TfToken("pxr.プロジェクト名") の部分を書き換えます。  
pxr. のあとのプロジェクト名は頭を大文字にします。  

```python
import _hogehoge
from pxr import Tf
Tf.PrepareModule(_hogehoge, locals())
```
__init__.py は、ビルド後にPtyhon側でモジュールをロードしたときに呼び出すためのファイルです。  
これは一番上にある import _#### 部分と、 PrepareModule の１つめの引数を _プロジェクト名に書き換えます。  
  
pch.h は書き換えなくてもOKです。  

#### CMakeLists.txt を作る

次に、作成したcppをビルドをするためのCMakeLists.txt を作成します。  
hoge フォルダ下に CMakeLists.txt を作り、

```cmake
set(PXR_PACKAGE hogehoge)

pxr_plugin(${PXR_PACKAGE}
    LIBRARIES
        tf
        sdf
        usd
        vt

    INCLUDE_DIRS
        ${Boost_INCLUDE_DIRS}
        ${PYTHON_INCLUDE_DIRS}

    PUBLIC_HEADERS
        api.h

    PUBLIC_CLASSES
        fuga
        tokens

    PYTHON_CPPFILES
        moduleDeps.cpp    

    PYMODULE_FILES
        __init__.py

    PYMODULE_CPPFILES
        module.cpp
        wrapFuga.cpp
        wrapTokens.cpp

    RESOURCE_FILES
        generatedSchema.usda
        plugInfo.json
        schema.usda:schema.usda
)
```

中身をこうします。  
  
変更点は、1行目の  PXR_PACKAGE 部分（ビルドされた後のlib等の名前がこれになります）  
PUBLIC_CLASSES　と　PYMODULE_CPPFILES　部分で、ここに作成するクラス名（hoge）を入れます。  
(指定したクラス名の頭が大文字の場合小文字になります)  
Python用は、wrapが頭につきます。  
  
以上で準備が完了です。

![](https://gyazo.com/73abbebb98072118a03ba5a511195e3d.png)

できあがったフォルダがこちら。  
  
```bat
python build_scripts\build_usd.py "<Build先>"
```
準備ができたら、 build_usd.py を使用してビルドします。  
  
### ビルド結果を確認する

特にエラーがなく無事に完了すると、  
ビルドフォルダとして指定したフォルダ下に、作成したlibとdll等が作成されます。  
  
![](https://gyazo.com/cf61e13e4ed9a875fed59af4f9a7fab0.png)

まず、 lib と dll。  
この２つは USD/plugin/usd 下に作成されます。  
このフォルダにできた２つを lib にコピーしても良いですが  
カスタムプラグインは分けておいたほうが後々わかりやすいので  
とりあえずこの USD/plugin/usd にPATHを通しておきます。  
  
![](https://gyazo.com/5321c4646178c5eaddf4be4c078dd78e.png)

次が python/pxr/Hogehoge  
これが、Pythonから呼び出すときのモジュールになります。  
  
![](https://gyazo.com/a85eaf068fb94141d11ca07e0d806d51.png)

最後に include 下のHeaderファイル。  
ここは、libraryPath下にプロジェクト名のフォルダが作成され  
その下にHeaderファイルが作成されます。  
  
![](https://gyazo.com/ca466eede5ed9ac6586339a6445edc1e.png)

こんなかんじ。  
  
libraryPathが . 以外だとうまくいかないのが現状謎なので  
今は直下にフォルダができます。  
  
### テストしてみる

とりあえず出来上がったモジュールをPython側から使ってみます。

```usda
#usda 1.0

def FugaPrim "Fuga"
{
    int intAttr = 100
}
```

とりあえず、こんな感じでサンプルのUSDファイルを作ります。  
  
![](https://gyazo.com/cce0e2c321a11a1dead9824733c620bf.png)

UsdViewで開くとこうなります。  
ここの FugaPrimが schema.usda で指定したクラス名になります。  
  
できあがったusda ファイルをPythonでロードしてみます。  
  
```python
from pxr import Usd, UsdGeom, Sdf, Gf
from pxr import Hogehoge

stg = Usd.Stage.Open("I:/test.usda")
cp = stage.GetPrimAtPath("/Fuga")
hoge.GetIntAttrAttr().Get()
```
  
ビルドが上手くいっていて libにちゃんとPATHが通っていれば  
作成したモジュールが使えるようになっています。  
ので、あとはファイルを開き、FugaPrimのプリムを取得してから  
作成したカスタムスキーマ経由で値を取得します。  
  
カスタムスキーマで定義した  
int intAttr = 0  
この部分が、 Get + 名前 + Attr().Get() という形でアクセスできてることが  
わかるかと思います。  
  
とりあえず第一段階はこれにて終了。  
  
しかしながら、これだとPtyhon側から定義したスキーマのプリムの作り方がわからなかったので  
そのあとはまた次回。  
  
