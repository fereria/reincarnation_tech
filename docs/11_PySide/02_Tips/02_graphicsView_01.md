# GraphicsViewの基本(Sceneをスケールする)

<!-- SUMMARY:GraphicsViewの基本(Sceneをスケールする)-->

GraphicsViewを使用して、色々オブジェクトを配置したり移動したりする方法を  
わりとちゃんと調べることにしました。  
特にMatrix周りとか、View、Scene、Item周りは今まであやふやに使ってたので  
その当たり特に重点的にやっていきたいと思います。

## 基本的な構成

![](https://gyazo.com/6d6bee54ab9c8d0fa4243438b5fb4352.png)

まず、GraphicsViewを使用するときは  
大きく分けて「View」「Scene」「Item」の3つの構造になります。  
PhotoShopに例えると、Viewは新規　とかで作成できるウィンドウ。  
Sceneはレイヤー、 Itemはシェイプで、基本的にはSceneに対してItemを配置し  
それをViewに表示する...という形になります。  
とりあえず、その3つ＋Dialogクラスを作成したサンプルを元にざっくりまとめ。

<script src="https://embed.cacher.io/83503b805863a944faf845c50b2c4faf2a5ffc40.js?a=c96d660f9a5afd75389879576678bc39"></script>

実行すると、

![](https://gyazo.com/467b0327752953f929ebc3e0ebfd707d.gif)

ホイールで拡大・縮小、○をドラッグすることで動かせます。

## QTransformを使用して拡大縮小

今回のポイントは、「QTransform」を使用して変換を行うところ。  
今まではなんとなく移動したりするのにTransformを使う、、、程度の認識だったのですが  
ViewとSceneの役割考えて使わないと意図しないことになるな...という感じで調べ直しました。  
  
まず、今回の場合はマウスホイールでSceneに置いてあるオブジェクト全部をスケールしたいです。  
そのような処理をしたい場合は、個別のItemをそれぞれポジション弄って大きさ変えて...とか面倒くさいです。  
ので、transformのscaleに数値を入れることで変換を行います。  
  
ItemのPosition　→　TransformのMatrixで変換　→　表示  
  
こんな感じで、PySideのGraphicsItemやView、Sceneには transformを取得・設定できるようになっていて  
その中には「今描画する時の変換用Matrix」が保存されています。  
  
今回の「拡大・縮小」をしたい場合の行列は

![](https://gyazo.com/e6815d68f718d155c3b864041baa7205.png)

この行列で求められます。  
Sx、Syというのが、ベクトル（X,Y,1)を拡大縮小するためのスケール値。  
元のベクトル（X,Y,1）に対して行列をかけ算することで、スケールした結果を取得できます。  
  
## いろいろと勘違いしてたので...

Transform周りを調べつつもどうも腑に落ちてないというか理由がよくわからずうーん...  
になってたのですが  
いろいろと教えてもらって（たぶん）理解したので書き直し...orz  
  
GraphicsViewのデフォルトのTransformは3ｘ3の単位行列になっています。  
いわゆる「なにもしない」行列です。  
その行列に対して、 self.scale(x,y) を実行すると  
現在のTransformに対してかけ算された数値がセットされます。  
  
今回のように、単純なスケールのみならOKなのですが  
これに回転が入ってくると、

![](https://gyazo.com/50a8f3fe59c00c82d7cb725a035d9ec6.png)

10度まわした結果、数値が綺麗な数字ではなくなり、  


スケールの今のスケール値を

```
    transform = self.transform()
    cur_scale = (transform.m11(), transform.m22())
```
このように取得使用とすると

![](https://gyazo.com/6196a8bad55610bcf832b2ccf5a27b51.png)

意図しない数値が返ってきてしまうのであまり望ましくありません。  
  
ということで、  
修正版ではScaleの値はGraphicsViewに保持しておいて  
Zoom処理で一度Transformをリセットしてからscaleに数値を入れるようにしました。  
  
Viewにスケールを持つことで、最大・最小値でClampするところかも大分シンプルになりました。  
  
指摘してもらえるのが超貴い...orz  
  
コレを機に、GraphicsViewベースに行列の勉強します(´･ω･`)