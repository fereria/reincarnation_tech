# Bone を作成して Bind する

<!-- SUMMARY:Boneを作成してBindする -->

![](https://gyazo.com/343b5ffe252a3c3e077cd0a18e75c191.png)

まず、Bone を作成するための骨組み（Armarture）を作成する。  
Maya のように、Joint オブジェクトを配置するのではなく  
Blender では「Armarture」オブジェクトがまず存在していて  
その中の構造として Bone（Joint）がある。

Add 画面から Armarture を選択します。

![](https://gyazo.com/711183956f4d5f08830e3ccaac90f7f9.png)

選択するとカーソルに新しい Bone が作成されます。

![](https://gyazo.com/2ded92590fea3ad8885d6e43ae5005ae.png)

Outliner の構造はこのようになっている。  
オブジェクトの中に Armarture データが入っている。

## Bone を追加する

Bone を追加するには、「Edit モード」に変更する。

![](https://gyazo.com/809d964442fcd0cec47b6b5885334b92.gif)

Edit モードにした状態で増やしたい Bone の親を選択し「E」を押すと、Bone を追加することができる。

![](https://gyazo.com/92b416e0036f294851a3eab022cdf208.png)

Bone を追加すると、Armature 下に親子化された状態で表示される。

## Mesh に Bone を Bind する

![](https://gyazo.com/ba701a1b825cf1f074ef0ad8c4997eb0.png)

Bone を作成したら、Object モードにして Mesh→Armarture の順に選択し、 **「Ctrl+P」** を押す。

![](https://gyazo.com/2046ad0c401344b1b1c9090cfbb2e405.png)

Parent To が表示されるので、 **「With Automatic Weights」** をクリックする。

![](https://gyazo.com/068a823874c153f584dfd150a2ec1239.png)

AutomaticWeight を実行すると、  
Mesh オブジェクトに対して Armature モディファイアと VertexGroup が追加される。

### VertexGroup

![](https://gyazo.com/f685d28ec2642271d8eded214aed1ab2.png)

VertexGroup Influence を表している。

Vertex - VertexGroup(Influence/Weight を保持) - Bone - Armature <=== [Deformer]

![](https://gyazo.com/dc6223d49c30efb159308ec667cb1ea5.png)

SkinBind は、「Armature モディファイア」でコントロールしているが
構造的には、VertexGroup で どの Bone がどの Vertex の Influence になっているかと  
Weight 値を管理している。

## Weight を調整する。

![](https://gyazo.com/47f7ea7ae2633812e5f05f8c9d8f55ce.png)

Bone の Bind が終わったら、Weight を調整する。  
Weight を調整するには「WeightPaint」モードに切り替えする。

![](https://gyazo.com/e00a7a3e01b788b212145efed0ab6e79.png)

切り替えると、見慣れた Weight 塗り画面になるので  
ブラシを調整しつつペイントする。

![](https://gyazo.com/9e50e8e2c963d8216d872d5f7aa781ec.png)

ペイントする Bone の選択はアウトライナ上の VertexGroup または、  
ObjectData 内の VertexGroup を切り替えれば OK。

## Bone を動かす

![](https://gyazo.com/19204c4395d1d6c5d921af24dc6377bd.png)

作成した Bone を実際に動かすには、Armature を選択して  
モードを「PoseMode」に切り替える。

![](https://gyazo.com/4141aa90e6782b2253b6704a2360326e.gif)

あとは Bone を動かせば、Bind された Mesh が変形する。

## 参考

- http://nn-hokuson.hatenablog.com/entry/2017/10/03/205639
