---
title: USDを使ってみる
tags:
    - USD
description: USDをビルドする方法
---

# USD を使ってみる

SIGGRAPH2019 で USD まわりが大変熱いことがわかったので  
色々検証しつつ、まとめた記事をアップしていこうと思います。

まずは、USD をダウンロードしてセットアップするあたりをやっていきます。

## ビルドする

まずは USD をビルドします。
以前は USD をビルドして使用をするには非常に手間がありましたが、現在はビルドスクリプトも
用意されていて、比較的簡単にビルドをすることができます。

### 必用なものをインストールする

-   https://git-scm.com/
-   https://visualstudio.microsoft.com/ja/downloads/
-   https://www.python.org/downloads/release/python-3712/

まず、ビルドに必要な VisualStudio とソースコードを取得するための Git、Python をダウンロードしてインストールします。

Python は、インストールしたら
![](https://gyazo.com/b9e01b33a2198d006d082dbe6c43320e.png)

Python37 直下と Scripts を環境変数の PATH に追加します。
さらに USDView を使用する場合必要になる　 PySide2 と PyOpenGL をインストールしておきます。

```
pip install PyOpenGL PyOpenGL_accelerate PySide2
```

下準備はこれで完了です。

### リポジトリをクローンする

インストールが終わったら、USD の Github からリポジトリをクローンします。

コマンドプロンプトで、ダウンロード先のディレクトリに移動し

```
git clone https://github.com/PixarAnimationStudios/USD.git
```

クローンします。

クローンしたら、VisualStudio の Developer Command Prompt を開きます。

![](https://gyazo.com/ecddefa1fda425ead85330b083d05044.png)

開いたら、リポジトリをクローンしたフォルダに移動して、ビルドを実行します。

```
python build_scripts\build_usd.py <ビルド成果物の出力先>
```

## Path を通す

ダウンロードが終わったら、必要な PATH を通します。  
必要なのは 2 つ

| 変数名     | PATH                                                                     |
| ---------- | ------------------------------------------------------------------------ |
| PYTHONPATH | <download したフォルダルート>/lib/python                                 |
| PATH       | <download したフォルダルート>/bin <br> <download したフォルダルート>/lib |

!!! info

    lib 下に PATH が通っていない場合は、
    pyd ファイルをインポート使用とするときに Error になるので注意。

この 2 つを通したら準備は完了です

## サンプルデータを開いてみる

準備ができたら、サンプル USD をダウンロードして、ビューワで開いてみます。

http://graphics.pixar.com/usd/downloads.html

サンプルデータは PIXAR の公式サイトにあるので、その KitchenSet をダウンロードします。

ダウンロードしたら、解凍したあとコマンドプロンプトを開き

```batch
usdview Kitchen_set.usd
```

usdview で Kitchen_set.usd をひらいてみます。

![](https://gyazo.com/85f886a67bcafe10082f3e1e178848eb.png)

USDView を使用すると、usd ファイルのシーングラフや Layer、プロパティなどを確認  
することができます。  
また、Python コンソールも付属しているので  
色々テストするにはこの usdview を使用するのがわかりやすい（らしい）です。

## python から usd ファイルを作ってみる

準備ができたら、公式のチュートリアルを実行してみます。  
https://graphics.pixar.com/usd/docs/Hello-World---Creating-Your-First-USD-Stage.html

```python
from pxr import Usd, UsdGeom
stage = Usd.Stage.CreateNew('HelloWorld.usda')
xformPrim = UsdGeom.Xform.Define(stage, '/hello')
spherePrim = UsdGeom.Sphere.Define(stage, '/hello/world')
stage.GetRootLayer().Save()
```

実行すると、指定のフォルダに HelloWorld.usda ファイルが出力されます。

```usd
#usda 1.0

def Xform "hello"
{
    def Sphere "world"
    {
    }
}
```

中身はシンプルな（空の）USD ファイル。

![](https://gyazo.com/56dcb8770dbbd7053dd164a261f19fbe.png)

usdeview で開くと、シンプルな Sphere が表示されました。

とりあえずこれで USD を触れる環境ができました。  
プチはまりポイントとしては、lib フォルダに PATH を入れていなかったせいで  
DLL 見つからないエラーがでたのと  
Synology の NAS 上のフォルダを保存先に指定するとパーミッションエラーで  
書き込めなかった所。

準備は出来たので、USD の基本的な構造を調べながら  
使い方をまとめていこうと思います。
