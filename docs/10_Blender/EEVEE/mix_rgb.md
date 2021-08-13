# MixRGB ノードのメモ

<!-- SUMMARY:MixRGB ノードのメモ -->

![](https://gyazo.com/07e76472a7e10b5267f5fefbd6888fce.png)

MixRGB は、その名の通り複数の Color を指定の方法で Mix して出力することができる。

![](https://gyazo.com/fffa396d74bbc75d0840c887378d1f6a.png)

Blend 方法は、PhotoShop のレイヤーのかさね方などとほぼおなじようなことができる。

## パラメーター

### Fac

Color1 と Color2 の RGB のブレンド割合。  
かさね方によって計算が変わるが、基本は Fac0 = Color1 Fac1 = Color2 の色になり  
その間はかさね方によって計算される。

### かさね方

![](https://gyazo.com/ec5d91846322629cbea3836856319ce5.png)

#### Mix

Mix は、かさね方は通常にした状態で、(Color2_Alpha \* Fac) をして重ねる。

![](https://gyazo.com/6041a2154fa26a40b6c8feea76832ca4.png)

AE のコンポで作ると、このような状態。  
青が Color2、緑が Color1、Fac が透明度となる。

### Add

```
outValue = Color1 + (Color2 * Fac)
```

Color2 に Fac をかけた数値を Color1 に加算する。  
そのため、Fac を上げると必然的に明るくなる。
Color2 が黒の場合は、Fac を変えてもなにもおきない。

### Multiply

```
outValue = Color * (Color2 * Fac)
```

Color2 に Fac をかけた数値を、Color1 にかけ算する。  
そのため、Fac を上げると必然的に暗くなる。  
Color1 が黒の場合は、Fac を変えてもなにもおきない。
