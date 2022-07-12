---
title: Houdini 写経 02
---

https://www.youtube.com/watch?time_continue=441&v=1ytZJy_a_H8

このチュートリアルの内容を参考に、いくつか分からないノードの効果があったので  
真似しながら調べてみました。  
細かい手順は動画参照。

## Block For-Loop

![](https://gyazo.com/4e0a0c5466c6173c164e2571e98252c9.png)

houdini のノードには、指定の回数繰り返す For-Loop ブロックがあります。  
その名の通り、Begin と End の間にあるノードを、指定の数分繰り返してくれます。

![](https://gyazo.com/97cc33b72b4817027dd2b048441b40f2.png)

このサンプルの場合、

1. 画像からカラーを取得
2. 指定の色に一致するプリミティブを Group に追加
3. Group に追加したプリミティブを SubDivide で分割

を繰り返ししてます。  
どうして徐々に分割されてるんだろ？と思ったのですが、  
際の部分が分割される → より細かい単位でプリミティブの色を取得できる → グループ追加  
のように、境界部分が徐々に増えているからなんですね。

![](https://gyazo.com/a16f7ea840c17442415c267691a61e83.gif)

ループ回数を変更すると、↑ のようになります。

## measure

![](https://gyazo.com/1eca2c3e05101e6d5228a7e76647b7b2.png)

メジャーツールは、指定のエレメントの体積や面積、周囲長を取得できます。

![](https://gyazo.com/e0548de27286c9befb26f991cb279b9a.png)

今回のサンプルの場合は、周囲長を取得しています。

![](https://gyazo.com/97bd92850714b39b30d3886e8a6a3d35.png)

メジャーツールの結果は、アトリビュートに追加されているので  
wrangle の中で @perimeter で取得できます。  
周囲長をかけ算しているので、大きな ■ ほど高くなるようになるわけですね（なるほど

## PolyExtrude

![](https://gyazo.com/a6e9f53d216ef0ac2557be9ca1c52542.png)

サンプルの操作をみていてわからなかったのが、この「Individual Elements」  
この設定になっていると、グループ単位ではなく  
個々の面やエッジ単位で Extrude してくれるというオプション。

![](https://gyazo.com/a130eb9eb645f60cf0630c7355badfc1.png)

ConnectedComponents になっている場合は、グループ単位になるので、  
For-Loop した単位で Extrude されている状態になります。

### Local Attribute

LocalAttribute は、指定のアトリビュートの値を、Extrude の値に掛け算してくれる。  
AttribWrangle で、zscale を指定しているので  
各プリミティブごとにこのアトリビュートを取得して Extrude の高さを変えている。

## 参考

-   http://nomoreretake.net/2018/06/06/houdini_omoshirokatayo_thistutorial/
