# SSS を設定する

<!-- SUMMARY:SSS を設定する -->

![](https://gyazo.com/45b045fb3e32a619e40cdc0562f910e8.png)

後ろからライトを当てたときの、うっすらと透けてみる SubSurfaceScattering を  
eevee で設定する。

## 設定

![](https://gyazo.com/7a3007027b51a2cfd4410027caf9baaa.png)

まず、eevee の設定画面で、SUbSurfaceScattering を ON にする。

![](https://gyazo.com/a1e943e560af1ef6f05c6454c7f07f7a.png)

Subsurface が 0 の場合がこの状態。

![](https://gyazo.com/f6fe2c429a338c18683de5768ebbe65e.png)

次に、Material の設定で BaseColor と、SubsurfaceColor を指定し、
Subsurface の数値を 0 から 1 に変更する。

![](https://gyazo.com/103e6d7c8cc73c96de0ee8b64b82a54f.png)

変更した結果。  
全体が SUbsurfaceColor になったような見た目になるが、  
あまりスケ感はでない。

![](https://gyazo.com/1ef1e154cba4c8fe2cc289d6accd8bc3.png)

最後に、Settings 内の「Subsurface Translusency」のチェックをオンにする。

![](https://gyazo.com/4478a4bd7bd211948fb3a954d558bffe.png)

チェックを入れると、薄い部分は裏から光が入っているような見た目になる。

## 関係するパラメーター動作

### Subsurface

Diffuse と SSS の数値をミックスする。

ミックスする SSS の色は、Translusence のチェックが入っている場合は  
SSColor に SubSurfaceRadius によって計算された透過した色が乗ったものになる。

![](https://gyazo.com/4340112fda70097e238d46ebf34f2ec8.png)

そのため、このように、SSColor が白で SubsurfaceRadius に緑だけ透過する設定がされている場合  
で、Subsurface 値を変更すると

![](https://gyazo.com/ccd9afb6b00a1bc776c366c5eccb7e8a.gif)

BaseColor と、SSColor に透過がはいった色とがミックスされる。

![](https://gyazo.com/d3fc6b46f180fb20ba9f18c0bf274a6b.gif)

トランスルーセンスのチェックが OFF の場合は、単純な BaseColor <-> SSColor の  
MIX として動作する。  
また、SubsurfaceRadius のパラメーターも影響しない。

![](https://gyazo.com/64908d84e79a84394101624ead9b0bb4.gif)

SubSurface の数値で、透過具合の強度を調整したい場合は、  
SSColor と BaseColor を同じ色にし、Radius の数値を調整すればよい。

### SubsurfaceRadius

![](https://gyazo.com/6d7beface1fa92895cbbf1de6b495eec.png)

光がサーフェース下に散乱する距離。  
半径が多いほど、光が影の中や被写体を通り抜けて軟らかい外観になる。  
パラメーターが 3 つあるのは RGB それぞれの値に対応している。

![](https://gyazo.com/37688eb0513687200a2772119ba255a2.gif)

例えば、皮膚なら赤い光がより散乱するので R の数値を上げる。  
上のサンプルは、SSColor の値を白にして  
RGB の数値をそれぞれ数値変更している。
