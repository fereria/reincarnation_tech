# NodeだけでDotテクスチャを作る

<!-- SUMMARY:NodeだけでDotテクスチャを作る -->

ネット上に公開されているノードネットワークをみながら  
ノードの機能とかどこがどうなっているのかを確認しながら  
真似しつついろいろとこねくり回してみようとおもいます。

## 参考元

<blockquote class="twitter-tweet" data-lang="ja"><p lang="en" dir="ltr">Highspeed tutorial time!! :D I want to share the new way i found to make an even better dots pattern. Enjoy! <a href="https://twitter.com/hashtag/b3d?src=hash&amp;ref_src=twsrc%5Etfw">#b3d</a> <a href="https://twitter.com/hashtag/blender3d?src=hash&amp;ref_src=twsrc%5Etfw">#blender3d</a> <a href="https://twitter.com/hashtag/Eevee?src=hash&amp;ref_src=twsrc%5Etfw">#Eevee</a> <a href="https://twitter.com/hashtag/npr?src=hash&amp;ref_src=twsrc%5Etfw">#npr</a> <a href="https://t.co/fCksGaKxSN">pic.twitter.com/fCksGaKxSN</a></p>&mdash; 100drips (@100drips) <a href="https://twitter.com/100drips/status/1093947059349192711?ref_src=twsrc%5Etfw">2019年2月8日</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

まずは参考。  
カメラ座標系でオブジェクトに対してToon調のドットテクスチャを張り付けます。  

## 座標系の指定  
  
![](https://gyazo.com/341dbdd5a7852df0512372b2f6f5d523.png)

まず、テクスチャを張り付けるための座標をしています。  
持ってくるには「TextureCoordinate」ノードを使用します。  
  
今回はカメラ座標を使用して張り付けるので「Camera」を選択します。  

!!! note
    Cameraと似たようなパラメーターに「Window」がある。  
    何が違うというと、Cameraの場合はCameraのズームに応じてテクスチャが拡大・縮小するのに対して  
    Windowの場合は、カメラの移動に関係なく同じ見た目のテクスチャを表示する。
    
## テクスチャのオフセット

テクスチャをオフセットしたり回転したり拡大縮小したりしたい場合があるので  
次にMappingノードをつなぎます。  
  
![](https://gyazo.com/4c3ff010ac2c296c3eb49f727ace5531.png)

Maya使い的に言うと「Place2DTexture」にあたるのがこれ。  
入力した座標系に対してTransform変換を行います。  
テクスチャのオフセットもこれでできます。  
  
## 分離と結合

NodeEditorでつなげられる値のうち「Vector」になっているものは  
「X Y Z」がワンセットになっている。  
もしこのそれぞれの要素を別々に取り出して処理をしたい場合は  
Separate XYZ　や　Combine　XYZを使用してX Y Zそれぞれの数字に分解したり  
分解された値を結合したりする。  
  
![](https://gyazo.com/70a8c698d0e6b3b69cc1bb4adb4c48b3.png)

MappingからのアウトプットをWaveにつなぐ。  
FloatからVectorにつないだ場合は、全部が同じ値がセットされる？  
  
![](https://gyazo.com/e31660c2ff9de0e3c3ed6cb382e57948.png)

WaveTexutreは、[「のこぎり波」](https://ja.wikipedia.org/wiki/%E3%81%AE%E3%81%93%E3%81%8E%E3%82%8A%E6%B3%A2)を出力してくれる。  

Vectorはこのテクスチャの座標系を入力。  
（なにもなければGenerated）  
今回はカメラ座標系で貼り付けるので、カメラ座標系をはりつけるのですが  
このときにXとYをそれぞれ分離して2つにわけてから入力する。  
  
![](https://gyazo.com/fc4838b770ab37eb63b108d566baf515.png)

こちらがX

![](https://gyazo.com/ece787a1aa2ef283d4558099a83ced79.png)  
  
こちらがY

このように、それぞれの座標系を分離してから入力すると  
縦横の向きになる。  
  
![](https://gyazo.com/83c40a025a2b57fe49c4e674ada0fe50.png)

分離してWaveにはりつけて、結合するとこうなる。  
これは、WaveTextureの波の数だけなかに小さな0-1の座標系グリッドをつくっている状態。  
  
![](https://gyazo.com/d187fec5b17e72885fa6eeaab3508a5c.png)

ので、GradientTextureにこの座標系グリッドをつなげると

![](https://gyazo.com/106ec35a9c67f484c2e6ba27bc316311.png)

Sphereのグラデーションが大量に並べられた状態になる。  
  
![](https://gyazo.com/c7d3739e42d92eb9cddb7a0f4899cefe.png)

GradientTextureのおかげで、円型のグラデーションができたので  
これを使用してドットにしていきます。  
現状、中央が１、外側が０の円状のグラデーションになっているので  
ここにクランプをかけて指定値のところで色が切り分けられるようにします。  
  
そのためにはMathノードの「Graeather Than」を使用します。  
これは、指定のValueの値よりも大きい場合は１、そうでない場合は０を返す  
ようになります。  

![](https://gyazo.com/53a54bfc021e67682534fc8b5116f769.png)

ある指定の数値で0か1に置き換わるので、このような●が並んだテクスチャになります。  
  
![](https://gyazo.com/5ad36a57dcfdeb0db0c3d9962e418703.gif)  
  
Valueを動かすと閾値がかわるので、ドットの大きさが変化します。  
  
![](https://gyazo.com/a314b91ee949619af031d4143d4a84c6.png)  
  
このモノクロドットをColorRampに閾値としてセットすると、色付きのドットになります。  
  
![](https://gyazo.com/808a0ea9a256dfbb4a1ae9f360c9be4d.png)

Greather Thanノードを指さない場合、ColorRampのグラデーションのPosが  
ドットの大きさに対応することになる。  
  
## オフセット用のノードを入れる

Waveを使用してつくったグリッド内でオフセットをしたい場合、Math内のSubtractとMultiplyノードを使用する。  
  
![](https://gyazo.com/5d31ad4d812a2b00326c7b8fa7124c8a.png)

### Subtract

Subtractは引き算。

![](https://gyazo.com/b5728841040164905d7ba9afbe7bff7c.gif)

引き算をすると、ドットの位置をグリッド内でオフセットしてくれる。  
  
![](https://gyazo.com/9af7232e3da9cd834e5298107c612f69.gif)

Xの値を動かしてみると、赤成分がオフセットされているのがわかる。  
数値が0-1でそれ以外はクランプされているので、グリッド内でしかグラデーションが移動  
しないようになる。  
  
### Multiply

![](https://gyazo.com/a4a5bfc139f40be23665dfd175eed2b8.gif)

Multiplyを入れると、スケールになる。  
グラデーションの値にかけ算が入る->閾値が変わる→大きくなる  
という理屈？  
  
## まとめ

Texture Coordinateでなにかしらの座標系を取得してきて  
間に計算を挟んで、それをカラーのグラーデーションにマッピングすることで  
Dotが出来ることが理解できた。  
  
Vectorに刺すのは、Mayaでトゥーンを作る時に  
UVCoordをRampにさしてマッピングするのとやってることは同じなので  
わかってしまえばなんとかなったけど、  
はじめVectorの意味するところが分からずかなり調べるのに苦労してしまった。  
  
![](https://gyazo.com/6eced0f8cd0a810fec10a25f6e1bc1ff.png)  

全体図はこちら。  
  
実際は、さらにこの塊を組み合わせていくので  
これ以上にノードが膨大になっていくんだろうなぁ...

## 参考

* https://cycles.wiki.fc2.com/wiki/Gradient%20Texture
* https://twitter.com/blug_jp/status/1094232402551926785
* https://wiki3.jp/blugjp/page/123