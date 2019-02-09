# AmbientOcclusion を使用する

<!-- SUMMARY:AmbientOcclusion を使用する -->

![](https://gyazo.com/fe2bdaa144c004f29b75c7c58058ec36.png)

AO を使用したい場合は、まずは Scene の設定で AO を ON にする。  
しかしこれだけだと AO を使用することができない。  
使用したい場合はノードエディタを使用して AO のノードを接続する。

![](https://gyazo.com/7f70b62d9a1eefcd0cf3f63b6acdad0d.png)

MaterialOutput が、最終出力の情報尾セットするノード。  
Maya でいうところの
Mesh と Shader をつなぐ ShadingEngine の surfaceShader に Shader の output をさす  
ようにする。

![](https://gyazo.com/13886746ff49827dd3898a770520de39.png)

Shader の結果に対して AO を乗せる場合のノード。  
BSDF シェーダーの結果に対して、Multiply で乗算して、その結果を MaterialOutput にさす。

Shader to RGB は、EEVEE 専用のノード？  
シェーダーの結果を一度 RGB に変換している。

![](https://gyazo.com/db1811d0b68be111cdb1ef71101ebd6f.png)

RGB の計算は、Maya のように個別のノードになっているわけではなく  
MixRGB ノードにまとめられている。

![](https://gyazo.com/5ef76e73224116f1cd97e98ca5ec4fc4.png)

Fac は、 **Color1 \* (Color2 - Fac)** このような関係になる。  
Color が #000000 の場合は、Fac の値がどうであろうと真っ黒になる。

## 参考

- https://cycles.wiki.fc2.com/wiki/Mix%20Shader
