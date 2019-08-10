# コンポジットを使用する(基本編)

<!-- SUMMARY:コンポジットを使用する(基本編) -->

![](https://gyazo.com/4cd80266f11db53c54d2ea586cba4a59.png)

レンダリングの計算結果に対してポスト処理をしたり  
素材分け（Maya でいうところの RnederLayer 的なもの）をしたいときには  
Compositing タブを使用する。

Compositing タブでは、ノードを利用して  
レンダリング計算結果と出力との間でポストプロセスを仕込むことが出来る。

## ノードを使用する

![](https://gyazo.com/2ad804aa86be487d7b9cc6bb9b46875d.png)

まず、「Use Nodes」のチェックを ON にする。  
このチェックを入れることで、ノードで処理を組めるようになる。

![](https://gyazo.com/ffc9bd6512e23e6d23e8c034811128d5.png)

チェックを入れると、ノードが作成される。

基本構造は、Input にあたる「RenderLayer」ノードで  
レンダリングをしたいレンダーレイヤーを取得できる。  
そして、なにかしらの出力ノードにつなぐことで、結果を出力できる。  
デフォルトでは、単純にレンダリングボタンを押しただけと同等になる。

## レンダリングを実行する

Node 表示にしただけだとなにも画面に表示されていないが  
「F12」を押して、レンダリングを行うと

![](https://gyazo.com/a637c8c18fa9929ba51250d3add632cd.png)

ノードにサムネイルが表示される。

### Backdrop

デフォルトの状態だと後ろは Grid が表示されているだけだが  
このバックグラウンドにレンダリング結果を表示できるようにするのが「Backdrop」。

![](https://gyazo.com/eaa722caab78e1ca933d9bcbc6ba6441.png)

チェックが ON になっている状態で

![](https://gyazo.com/7c06a6dfc92fad29b46dc2c0916f9b37.png)

Viewer ノードに確認したいノードの出力をさすと、

![](https://gyazo.com/026832ec04c14914cbd0c2d1ac10fb33.png)

ノードエディタの後ろ側にレンダリング結果が表示される。  
画面に対してどう表示するかは、Backdrop オプションの「Zoom」または「Fit」を押すことで  
Backgrround に表示することが出来る。

## 画像に出力する

![](https://gyazo.com/e990299fb700e6ed0f9a649d7d6b5f32.png)

レンダリング結果を画像として出力したい場合は  
「File Output」ノードを使用する。  
このノードは、1 回のレンダリングに対しても複数指定することができるので  
素材分けをしたい場合などは、この Output ノードを使用することで  
複数のレイヤーや違うレンダリングなどの素材を出力することができる。

![](https://gyazo.com/cac18eb4f0988a2340b63171d452655d.png)

レイヤーごとの設定は、ノードの「Properties」内で指定する。  
ここは、各ノードごとの各種パラメーターが表示されるところで  
File Output の場合、  
画像出力関係をオーバーライドできるパラメーターが表示される。

画像のファイル名の変更などもここにあり  
「FileSubPath」に、拡張子なしの名前を入れると  
FileOutput でつないだ画像を、指定のファイル名＋拡張子で出力する。  
連番の場合は、数字の桁数を#の数で指定すれば OK。