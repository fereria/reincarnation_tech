# ShapeKey(BlendShape) を作成する

<!-- SUMMARY:ShapeKey(BlendShape) を作成する -->

![](https://gyazo.com/1f091cdab18cafdbe944db6f857ca5bb.png)

まず、BlendShape を作成するオブジェクトを選択し、  
「ObjectData」タブの「ShapeKeys」を開く。  
そして ShapeKeys の右がわにある＋を 2 回押す。

![](https://gyazo.com/74178c74a2de0764295295696fa27c8f.png)

追加すると、１つめが必ず「Basis」になる。  
これがベースとなるデフォルトの形状を表す。  
次に、「Key 1」を選択して  
Edit モードに変更して、形状を変形させる。  
変形モデルが出来上がったら、Object モードに切り替える。  
切り替えると、デフォルトの形状に戻る。

ObjectMode に戻した段階だと、KeyValue が 0 になっているので  
その値を動かす事で、デフォルト形状から編集した形状へ変形する。

![](https://gyazo.com/0f82bc6215cd8cb821fbcaeee4520336.gif)

このように、Value の値を変更することで  
形状を変更することができる。

## 別の Shape で形状を作成してから ShapeKey を作成

ShapeKey を作成してから形状を編集するのではなく  
BlendShape のように、あらかじめ形状を作成しておいてから  
その形状の Shape キーを作成することができる。

![](https://gyazo.com/cf772c18fec5284bb89498373ba242a8.png)

まず、2 つの Mesh を作成する。  
次に、モーフターゲット →Shape をセットしたい Mesh を選択し

![](https://gyazo.com/4ee90e8cb948e5c889fe56090608edce.png)

下向きの　＞　アイコンをクリック → Join as Shapes を選択する。

![](https://gyazo.com/c740d9eb7d8e19acfa9b7a9ac83a2343.png)

実行すると、Object の名前の ShapeKey が作成される。  
このターゲットは、Maya の BlendShape とは違い  
ShapeKey を作成した後にもーふターゲットを編集しても  
ShapeKey は更新されない。

## ShapeKey のポリゴンを増やす

Maya の BlendShape とは違い、トポロジが同一でなくても ShapeKey を指定することができる。

![](https://gyazo.com/66825318f9f8afb393c75b91a330a08e.gif)

ShapeKey を追加後、Mesh を分割したりエクストルードしたりしたあと  
Object に戻す →ShapeKey の Value を変更  
というようにしても、Value の編集をすることで  
形状を変更することができる。
