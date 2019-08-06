# USDを使ってみる

<!-- SUMMARY:USDを使ってみる -->

SIGGRAPH2019でUSDまわりが大変熱いことがわかったので  
色々検証しつつ、まとめた記事をアップしていこうと思います。  
  
まずは、USDをダウンロードしてセットアップするあたりをやっていきます。  
  
## ビルド済みデータをダウンロードする

USDはビルドするのがめんどくさいというので有名ですが  
nVidiaがビルド済みのデータをアップしているので  
今回はそれを使用します。  
  
https://developer.nvidia.com/usd  
  
ダウンロードはこちら。  
  
Pythonのバージョンが2と3がありますが、3のほうにはUSDViewが含まれていない  
（後で説明）ので、今回は2のほうを使用します。  
  
![](https://gyazo.com/e8b0f432726a6d442d45c38bcae9a2a1.png)

ダウンロードしたzipを解凍して、解凍したフォルダをリネームして  
お好みの場所にコピーします。  

## Pathを通す

ダウンロードが終わったら、必要なPATHを通します。  
必要なのは2つ

|変数名|PATH|
|--|--|
|PYTHONPATH|<downloadしたフォルダルート>/lib/path|
|PATH|<downloadしたフォルダルート>/bin <br> <downloadしたフォルダルート>/lib|

!!! info 
    lib下にPATHが通っていない場合は、
    pydファイルをインポート使用とするときにErrorになるので注意。

この2つを通したら準備は完了です

## サンプルデータを開いてみる

準備ができたら、サンプルUSDをダウンロードして、ビューワで開いてみます。  
  
http://graphics.pixar.com/usd/downloads.html  
  
サンプルデータはPIXARの公式サイトにあるので、そのKitchenSetをダウンロードします。  
  
ダウンロードしたら、解凍したあとコマンドプロンプトを開き  
```batch
usdview Kitchen_set.usd
```
usdviewでKitchen_set.usdをひらいてみます。  
  
![](https://gyazo.com/85f886a67bcafe10082f3e1e178848eb.png)

USDViewを使用すると、usdファイルのシーングラフやLayer、プロパティなどを確認  
することができます。  
また、Pythonコンソールも付属しているので  
色々テストするにはこのusdviewを使用するのがわかりやすい（らしい）です。  
  
## pythonからusdファイルを作ってみる

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
中身はシンプルな（空の）USDファイル。  

![](https://gyazo.com/56dcb8770dbbd7053dd164a261f19fbe.png)

usdeviewで開くと、シンプルなSphereが表示されました。  
  
とりあえずこれでUSDを触れる環境ができました。  
プチはまりポイントとしては、libフォルダにPATHを入れていなかったせいで  
DLL見つからないエラーがでたのと  
SynologyのNAS上のフォルダを保存先に指定するとパーミッションエラーで  
書き込めなかった所。  
  
準備は出来たので、USDの基本的な構造を調べながら  
使い方をまとめていこうと思います。