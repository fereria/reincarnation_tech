# トゥーンのアウトラインを作成する(基本)

<!-- SUMMARY:トゥーンのアウトラインを作成する(基本) -->

![](https://gyazo.com/d8f86b79622a3289cabe482db26dda04.png)

BLender でアウトラインを使用する場合は、Render タブの **Freestyle** を ON にする。

![](https://gyazo.com/318cddfdf019a6f25c3e769c618ced9d.png)

基本は、この設定を ON にするだけで、Rendering すると LEVEE でもアウトラインを表示することができる。

![](https://gyazo.com/6796ef9b8790d49cf941fe8879de5b78.png)

細か胃設定を行いたい場合は、LayerView タブの FreeStyle で調整をする。

## アウトラインの太さの調整

太さを調整するのは Render 画面の LineThickness。  
Absolute の場合は、LineThickness のピクセルのアウトラインになり、  
Relative の場合は、画面のピクセル数に応じて太さが変化する。  
アウトラインサイズが 1.0pix になるのが 480pix で、以降解像度が増えるごとに
720->1.5 960->2.0 のように太くなる。

## アウトラインの出方を調整する

どの部分にアウトラインを出すか野調整は、ViewLayer 内の FreeStyle で行う。

![](https://gyazo.com/ae1aa88256379b9dd2246af6e6bd4684.png)

まずおおまかなくくりを「Selection By」で指定する。  
Vibility は、現在表示されているオブジェクトすべてにアウトラインを表示する。  
EdgeType にチェックがある場合は、より細かい指定をすることができる。

![](https://gyazo.com/d7917b6506a57a164101f861fc9520f8.png)

Edge Type の Inclusive Exclusive で、以下のチェックボックスが ON のものが有効（Inclusive）か  
チェックしたものが無効（Exclusive）かを指定する。

![](https://gyazo.com/de8625d61cd1753e57e26964f54cd2f0.png)

Logical OR AND は、EdgeType が複数選ばれている場合  
選択されているオプションに「1 つでも当てはまる場所」に表示する（OR）  
あるいは「すべてにあてはまる」（AND）  
いずれかを選ぶ。

![](https://gyazo.com/8e22db0d85bf47ded8e639fda24753fa.png)

### Silhouette

![](https://gyazo.com/faac2ad2e2bb7dd6a39241007761e184.png)

各オブジェクトの輪郭のみを表示する。

![](https://gyazo.com/e0afb92981e4476614372c792dbeee58.png)

シルエットの場合は、いわゆる Maya の輪郭と同じようにオブジェクトの立体にそった形で  
アウトラインが表示される。

### Contour

![](https://gyazo.com/c48405887a90face6a12a278de9a03ea.png)

輪郭は、シルエットとは違いオブジェクトの境界部分にアウトラインが表示される。  
同じオブジェクトの中の重なり部分にはアウトラインは表示しない。

### Border

![](https://gyazo.com/cc90419693a65a6d26faf6a06d022ea3.png)

オブジェクト内の重なり部分にアウトラインを表示する。

### External Contour

![](https://gyazo.com/923a600469312062a6581c999094def8.png)

全オブジェクトの輪郭のみを表示する

### Crease

![](https://gyazo.com/d7116434eb7a467b254928c28ebe9ecd.png)

Edge の角度が、Crease Angle より小さい Edge にアウトラインを表示する

### Material Boundary

![](https://gyazo.com/df1d7353061396fdedc1d2f953f9facc.png)

オブジェクト内のマテリアル境界部分にアウトラインを表示する。

## Vibility

画面に表示されている Edge 部分するかどうかを設定する。

![](https://gyazo.com/72289caf825265eac83bd5103db6b582.png)

Visible

![](https://gyazo.com/d7026c918757b9a48e30a74fd3603483.png)

デフォルトが Visible。
画面に見えている Edge にのみアウトラインを表示する。

Hidden

![](https://gyazo.com/8d128ec3a77801d774f80d73d6f9e65e.png)

画面に映らない場所にアウトラインを表示する。

QI Range

指定した数の Mesh の奥行に応じてアウトラインを表示する。

![](https://gyazo.com/7c8d3456356fab9b47ff5533cad566d9.png)

0~1 のようにすると

![](https://gyazo.com/3065e60fb18eb6aff54dd7668cf62620.png)

Mesh の重なりが 1 までの所にアウトラインが表示される。  
End が 0 の場合は、Visible と同じ内容が表示される。
