---
title: SOLARISでUSDファイルを開く
tags:
    - SOLARIS
    - Houdini
    - USD
---

Houdini Apprentice Advent Calendar 11 日目は、  
Houdini18 にて新しく追加された Layout/Lookdev/Lighting を行う SOLARIS にて  
USD ファイルを開いてみよう  
です。

## USD/SOLARIS

と、始める前に軽くおさらいというか USD について。  
USD というのは Pixar が作成したシーングラフを扱うためのライブラリで、  
複数人が同時に作業を行うために作られたファイルフォーマットです。

いままでのファイルフォーマットと大きく違うのは  
「プロシージャルシーングラフ」と呼ばれる、複数の USD ファイルを「プロシージャル」に  
合成して、１つのシーングラフを構築できることです。

![](https://gyazo.com/c08ab343dda8859f5b408132e8ddf508.jpg)

ローンチセミナーのスライドより。

SOLARIS では、この USD をネイティブでサポートし  
その USD ファイルを SOP を扱うように、プロシージャルに合成し、  
１つのシーングラフを構築することができます。

![](https://gyazo.com/0b54cdb337ab5eaa35ab5ead0e7429bc.png)

もう１つの特徴が、この SOLARIS（Stage ネットワーク）上のノードというのは  
メモリ上であったり、ファイルだったりはある物の  
そのノード１つづつが USD ファイルであり、レイヤーとして扱われています。

ノードの処理＝ USD 処理＝プロシージャルシーングラフ構築

というのが、この SOLARIS の世界であり  
SOLARIS の世界は USD の世界そのものでもあります。

というのが、ざっくりとした SOLARIS と USD の概要です。

## USD ファイルをダウンロード

というわけで開く前の準備段階。  
今回のサンプルをUSDファイルを、Pixar公式から持ってきます。

http://graphics.pixar.com/usd/downloads.html

場所は公式のダウンロードサイトから、毎度おなじみ KITCHEN SET をダウンロードします。

## SOLARIS を開く

ダウンロードできたら Houdini18 を起動します。

![](https://gyazo.com/12c067a991b01b4c2f7ddb3398d1c0c9.png)

起動できたら画面のレイアウトを Solaris に変更します。

### 画面構成

SOLARIS の画面には、今までの Houdini にはなかったビューが２つほど追加されています。

![](https://gyazo.com/fbf024ed32a3bcb741cd10c7cdd239dc.png)

まずひとつめが、 Scene Graph Tree  
これは、現在選択中のノードの段階の「USD のシーングラフ（いわゆるステージ）」を表示します。  
このSOLARISは、「USDのプロシージャルシーングラフ」を表し  
ノード１つがUSDファイル＝レイヤー扱いです。  
ノードの接続をすると、プロシージャルにそのノードが合成されていきます。  
そして、現在選択している　または　ディスプレイフラグオンになっているノードの  
段階が「そこまでのノードがコンポジションされた結果」です。  
  
その結果できあがったシーングラフが表示されているのが  
この「Scene Grapth Path」です。  
  
もうひとつが「Scene Graph Detail」です。  

![](https://gyazo.com/77fcd27b285a8dbdb75b48de3ba3e258.png)

これは、選択中のプリミティブのアトリビュートやその他諸々情報を核に出来るパネルです。  
細かいところを説明し始めると、ここだけで１記事できるぐらいの物量があるので  
今回は割愛しますが、個々を見るとどうコンポジションされてるかとか  
現在のアトリビュートの値などを見ることが出来ます。  
  
この２つは、SOLARISの機能というよりUSDに付属するものになります。  
SOLARISでシーングラフを構築された結果がこの２つに表示されるので  
ノードを作ったりするのと併せてこの２つのパネルを確認すると  
色々とわかりやすいです。  
  
ので、下の解説でもあわせてこの２つを表示していきます。

## USD、開いてみよう

というわけでようやく本題に移動します。  
ダウンロードしたUSDファイルをHoudini/SOLARISで開いてみます。  

![](https://gyazo.com/d33dec1b340af443fcaae9bb7d9ce326.png)

まず、USD ファイルを開くには「LoadLayer」ノードを使用します。  
何故に LoadUSD ではないのかというと、  
USD では USD ファイルのことをレイヤーと呼ぶからです。

このあたりの詳細は、  
https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/04_layer_stage/  
以前の記事を参照をば。

![](https://gyazo.com/87d8b7fcbb7e911938c72c9112a23d0d.png)

ただし、キッチンセットは Zup なので  
そのままだとおかしくなるので 3D Viewports を開き、  

![](https://gyazo.com/06048f4a13b907278e50a6711a3f4e70.png)

Orientation を「Z UP」に変更します。

![](https://gyazo.com/3e4def8e6db9c4f78fc37b125bda50c9.png)

無事読み込みができました。  
あとはこれにいろんな処理をしていけば OK です、、、と言いたいところですが  
実は SOLARIS にはいろんな USD の読み込み方法があります。  
せっかくなので、他の読み込み方法もみていきましょう。

## LoadLayer
    
まず、上で使用した LoadLayer は「指定の USD をレイヤーとして読み込み」ます。

![](https://gyazo.com/db5e31904a121df2625dd543d1a0dfe2.png)

SceneGraphPathを見るとわかりやすいですが、このノードを使用すると  
ルートしたにたいして、指定のUSDをそのまま「ロード」します。  
他のことはなにもしていません。  

## コンポジションアーク系のノードで開く

では、LoadLayer以外ではどういう方法があるかというと  
SOLARISのノードとして用意されている各種コンポジションアーク系のノードで  
読み込んでみます。  
このノードで読み込むと、コンポジションアークの機能と併せて  
USDファイルをロードできます。
このように読んだ場合、ロード先のusdaファイル内のClassPrimは隠蔽され
オーバーライドしたりすることはできなくなります。
しかし、LoadLayerでロードしてから、そのノードをReferenceノードに接続する場合、  
リファレンスで読み込みたいレイヤーを一度サブレイヤー合成し  
その後に \</sdfPath...\>こんな感じでシーン内にあるPrimを
リファレンスとしてロードする形になります。

この場合、レイヤーはカプセル化されず、指定のレイヤー内の別Primもロードされるので
継承処理と同じように、リファレンス元のPrimをオーバーライドできるようになります。
詳しくは [こちら](03_comp_arc_inherits.md)にて検証をまとめているので
参考にしてください。

### SubLayerで開く

まずは、Sublayerノードで開いてみます。  
  
![](https://gyazo.com/65d86205563105def4a757da5fd482d9.png)

サブレイヤーで開いた場合は、基本はLoadLayerで読み込んだ場合と同様です。  
  
![](https://gyazo.com/7fe464cc59894c03a62fa89d912489e2.png)

Scene Graph Path も、LoadLayerしたときと同様になります。  
loadlayerしたときとの違いは、このノード１つでUSDファイルをサブレイヤーで合成できることです。  
  
![](https://gyazo.com/8579995b8c8d05ed79a24f27d2c7ead4.png)

たとえばこんな感じで３つのファイルをロードします。  

![](https://gyazo.com/9bff0fba0911963e70b5f414ffda6280.png)

base.usdaがこんな感じの緑の玉として。  
  
![](https://gyazo.com/8616c46e18c492f7360d3be25481107a.png)

add_color.usda で赤く色を変えて  
  
![](https://gyazo.com/663563ef426f159324fc653667463a7e.png)

final.usda で四角くするようにしてみます。  
  
そうすると上から順番に合成されていき、すべてが合成された結果がこのノードの結果として出力されます。  
  
![](https://gyazo.com/1517709aa704c16940649eed8e3ef207.png)

このサブレイヤーで複数USDを合成するメリットとしては  
Mute Layer や Enable を使用してUSDの効果をON/OFF出来ることです。  
たとえば、この３つのサンプルのうち「add_color.usda」をミュートにしてみるとします。  
  
![](https://gyazo.com/1f40bdf1ef7f38294768e6bb6b66b417.png)

するとどうなるかというと、「赤くする」という レイヤー（USDファイル）だけがミュートされて  
緑のキューブになります。  
このように、2DソフトのレイヤーをON/OFFするように  
USDのレイヤー効果を簡単に切り替えつつ確認出来るのがSublayerノードの効果になります。  
  
読み込みしつつ、PhotoShopのレイヤーのようにON・OFFしたりできるのが  
このノードを使用して読み込むメリットですね。
  
### Referenceで開く

![](https://gyazo.com/01bc89a88163c456fa10e185ba3085ad.png)

つぎに、Referenceノードを使用してロードしてみます。  
  
![](https://gyazo.com/8e657966e5a397e2e394f6dae0af7f4b.png)

リファレンスノードは、MultiInputの入力結果をReference化するという機能もありますが  

![](https://gyazo.com/00bddb25883ddc0c7803c433a9ae0830.png)
Reference TypeをReference Filesにすることで、  
このノードを使用して「ReferenceでUSDファイルを読み込み」することができます。  
  
![](https://gyazo.com/39cab059035ce2a16e068a57bc790e86.png)

SceneGraphPathを見ると、プリミティブ名が緑になっていることが分かります。  
また、LoadLayerの時と大きく違うのは「トップのノード名が違う」事です。  
LoadLayerで読み込んだ場合は、USDファイルに書かれているプリミティブの構造が  
そのままロードされます。  
しかし、リファレンスの場合は違い  

![](https://gyazo.com/db1f6e2700a342d292056e2c555ea4e9.png)

Destination Primitiveで指定したプリミティブ名の下に  
Referenceで読み込むUSDのPrimitiveを読み込みます。  
$OSとは、ノード名のことなので、ノード名である reference1 下に子のプリミティブが読み込まれています。  
  
![](https://gyazo.com/47e20b46bcea9c6562f67f7b98b05c4e.png)

試しに リファレンスノードを右クリックし、LOP Actions > Inspect Active Layer を開いてみます。

```usd
#sdf 1.4.32

def HoudiniLayerInfo "HoudiniLayerInfo" (
    customData = {
        string HoudiniCreatorNode = "/stage/reference1"
        string[] HoudiniEditorNodes = ["/stage/reference1"]
    }
)
{
}

def "reference1" (
    prepend references = @C:/pyEnv/JupyterUSD_py27/usd/Kitchen_set/Kitchen_set.usd@
)
{
}
```
このメニューを開くと、現在のノードの編集状況（＝ノードのUSDファイル）を  
アスキーファイルで確認できます。  
  
すべてのノードはレイヤーと説明しましたが、このActiveLayerというのが「このノードのUSD」  
なわけですね。  
なので、コレを見ることで、このノードが今なにをしているのか、USD的になにをしているか  
確認することが出来ます。  
  
で、見る限りリファレンスで読み込んでるのが分かります。  

### Referenceノードで読む事での違い ※ 2020/01/05 追記

後々ノードの細かい挙動を調べているときに判明したことですが  
リファレンスノードを使用してロードした場合と、LoadLayerを使用してロードしたあとに  
ノードを接続してリファレンス化する場合とで大きな差があることがわかりました。  
その「差」がなにかというと、**「カプセル化するか否か」**です。

リファレンスノードでロードした場合は、USDAでみた場合
prepend references = @C:/pyEnv/JupyterUSD_py27/usd/Kitchen_set/Kitchen_set.usd@
こんな感じにファイルパス指定で、指定PathのUSDAのDefaultPrimまたはSdfPathで指定したPrim  
をリファレンスでロードするようになります。


## StageManager で開く

![](https://gyazo.com/a3cbe3fa1431c43261fd9c6e2b227f6d.png)

最後に、コンポジションアーク以外での開き方。  
それがStageManagerノード。  
  
チュートリアル動画だとこのStageManagerを使用している例も多くありますが  
上の３つとこのStageManagerではなにが違うのでしょうか。  
  
大きな違いが「Stage」マネージャーとある通り、このノードは  
これ単体でステージの構築を行うことが出来ます。  
  
この場合のステージとは、複数のUSDファイルをコンポジションした結果の事を指します。  
  
![](https://gyazo.com/bc946750eba4166a0a9ac58e4b768464.png)

開くと、StageManagerの画面は上の画像のようなウィンドウになります。  
その中のフォルダアイコンをクリックします。  
  
![](https://i.gyazo.com/154b283e8603f72965cb9740531eb334.gif)

今までのノードは、１つのノードで１つのUSDファイルを読み込むものが中心でしたが  
このStageManagerはこれ単体でステージ（USDのコンポジションした結果のシーングラフ）を構築  
出来るノードのため、複数のUSDをリファレンスなどでロードして  
グループ化などをしつつステージを構築することができます。

![](https://gyazo.com/d2c5c7780351d44e75f13c514d036357.png)

なので、このStageManagerノード単体で、ScenerGraphPathはリファレンスを含めて  
完成されたステージが構築されます。（オレンジ色はコンポジションアークで読み込まれている物）  
  
## アスキーファイルをそのまま書いて開く

![](https://gyazo.com/c57bdcde55538e2b7bab3e01d50b719f.png)

こんなことをするひとはほぼいませんが、inlineusd を使用すると、  
USDファイルをファイルではなく手書きで書いて読み込むことができます。

![](https://gyazo.com/ddc9efcb3436aa6016fb37a1d36f2349.png)

こんな感じで USD Source に対してアスキーで記述することで、

![](https://gyazo.com/6e567590ef26de63133b389d93f99478.png)

こんな感じで実際にSceneGraphPathにステージを構築することが出来ます。  


## じゃあ実際の所、どうやって開いたら良いの！！？？

見ての通り、USDファイルを開くだけでもやり方はたくさんあります。  
こんなんじゃどうしたらいいかわからんよ！  
って言う方に自分的オススメをご紹介。  
  
### たくさんのオブジェクトを配置したい場合は「StageMnaager」

![](https://gyazo.com/602c4cd806705c1680efdef7b8891968.png)

ステージ内でレイアウトをしたい場合、下手をしたら何百というアセットを  
ロードして配置する必要がでてきます。  
そんなときに１つづつ読み込んだり、グループでまとめたりするのは非常に面倒くさいです。  
  
そういうときは、StageManagerを使用すると、リファレンスでまとめてロードだったり  
複数アセットをロードしたりがドラッグ＆ドロップで手軽にできて
グループ化したり、階層を変更したりと言ったオペレーションが手軽に行えます。  
  
つまりは、このノード１つでステージの構築が完結するわけです。  
なので、レイアウトなどはこのノードがオススメです。

![](https://gyazo.com/f680a2f9047f6d24c24673460f2f66cb.png)

もちろん、１つのStageMnagerでまとめるとごちゃごちゃしちゃう！！！  
という場合は、複数のStageMnaagerを接続することも出来ます。  
この場合、入力で受け取ったステージのシーングラフに対して＋αでアセットを足したりといった  
ことが可能になります。  

### レイヤーをカプセル化したい場合は「Reference」

リファレンスで読み込みたいレイヤーのDefaultPrimまたは指定のPrim以外を
「カプセル化」してロードしたい場合はReferenceノードを使用してロードします。
Referenceノードで読み込んだ場合は、指定Prim以外は隠蔽され
オーバーライドできなくなります。
なので、キャラクターを読み込みたい場合などは
リファレンスノードを使用してロードするのが良さそうです。
  
### それ以外は「LoadLayer」

それ以外は、LoadLayer＋コンポジションアークのノード or それ以外のべんりノード（Graftなど）  
を使用するのがオススメです。  

LoadLayerで読むパターンは、このあとSOLARISのノードベースで何かしらの構造を構築したい  
（バリアントでバリエーションを作りたい、シェーダーのアサインをしたいライトノードを組み合わせながら  
シーンを構築したい....等。  
  
![](https://gyazo.com/65827db5367f92eb61c4d309a4d860ac.png)

SubLayerやReferenceでも直接ファイルを読み事ができますが  
その場合入力順序を差し替えたり、一時的にOFFにしたりするのが非常にやりにくく  
ノードでの一覧性があまり良くなくて私は使いにくく感じました。  
  
LoadLayerでかならず読みこんでコンポジションしておくと、  
切り替えしやすかったり、「ファイルを読んでる」というのが明確化するので  
個人的にはUSDファイルの単発でのロードはLoadLayerを使うのが良いかなと思います。  
  
### もちろん併用もできます

もちろんStageMnaagerとLoadLayer＋コンポジションアーク系ノードの併用も可能です。  

![](https://gyazo.com/ea296ad1a04c0989d6fd3d60428d4fbc.png)

まとめてStageMnagerでシーンを構築しつつ、細かいバリエーションはノードで作って  
最終的に合成する、、、、という風に  
複数のUSDの開き方を、良い感じに使い分ける事で  
複雑なシーンを極力シンプルにノードを構築することも可能になります。  
  
## まとめ

こんな感じで、SOLARIS/LOP内でのUSDファイルの開き方の紹介でした。  
USDファイル１つ開くだけでこれだけいろんなアプローチがあるのが凄いところです。  
これに＋SOPのシーンをLOPで開いたりなんかもできるので  
SOLARISはUSDを扱う上では非常に柔軟かつ、考え方次第でいろいろなUSDオーサリングを可能にする  
ツールだなと思いました。  
  
  
SOLARIS記事一杯書こうといった第一弾がこんな記事でいいんだろうか？  
次は今回さらっと書いたコンポジションアーク系のノードについて  
もう少し詳しく書いて行こうと思います。  
  
