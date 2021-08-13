# ScreenSpaceReflections を使用した反射

<!-- SUMMARY:ScreenSpaceReflections を使用した反射 -->

![](https://gyazo.com/76c559d39113537862e84a1d0fa03fe6.png)

ReflectoinProbe を使用した場合、メタル質感のものは反射できなかったり  
解像度の問題だったりでそれなりに制約がある。

![](https://gyazo.com/b8a10037df10b32210402848fe761ece.png)

ので、ReflectionProbe 以外で反射をつけたい場合は ScrenSpaceReflections を使用する。

![](https://gyazo.com/696c430d930694e0a9cf5fdd61d6538a.png)

Material 設定の Matalic を 1 にして、Roughness はマット感に応じて調整する。  
（サンプルは Roughness0）

この SSR は、IrradinaceVolume と併用することができるので、  
反射と合わせて間接光を入れる。

## 注意点

ScreenSpace という名前がある通り、  
スクリーン内にうつっているものしか反射されない。

## 反射の質の調整

### トレース精度（Trace Precision）

デフォルトでは、0.25 だが、この数値を上げることで、反射具合のジャギーを  
減らすことができる。

![](https://gyazo.com/02b148730187a97c8a24335cfdbc695d.png)

デフォルトだと、反射がボケた感じになるが、

![](https://gyazo.com/1c0abae78c4efe0f5c16afecb2509f3b.png)

Trace Precision を 1 にすることで、ジャギジャギしたかんじを減らすことができる。

### Half Res Trace

ScreenSpaceReflection に使用するバッファ画像の解像度をハーフにする。  
チェックが入るとボケた感じになるので、クリアにしたい場合はチェックを外す。

### Edge Fading

![](https://gyazo.com/4f0855c34a11f38838dbfdef8a643156.gif)

Reflection のエッジ部分がパツッとなるのをフェードをいれて緩和する。

## 参考

- https://shikihuiku.wordpress.com/2012/07/06/brdfirradianceradiance%E3%81%AE%E5%AE%9A%E7%BE%A9/
