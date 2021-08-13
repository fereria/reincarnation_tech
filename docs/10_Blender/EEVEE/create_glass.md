# 透明なガラス質感マテリアルを作成する

<!-- SUMMARY:透明なガラス質感マテリアルを作成する -->

## 透明なマテリアルを作成

eevee では、Maya のような「透明」を扱うパラメーターは存在しない。
ので、

![](https://gyazo.com/722bbd095a7da8f0dfc0533ca37d63e4.png)

単純な屈折をしない場合は、かさね方を Additive するか

![](https://gyazo.com/218b86f721b0c4a5034f5e9689861cfa.png)

MixShader を使用して、Alpha チャンネルをセットし（テスト的には Color をさしてる）

![](https://gyazo.com/575cc4fafd09640df79478eaa73cb5b1.png)

Settings の「BlendMode」を「AlphaBlend」に変更することで透明にすることができる。  
しかし、この場合は、ガラスのような屈折表現を作成することができない。

## 屈折表現をする

そのため、EEVEE では疑似的な ScreenSpaceRefraction を使用して  
屈折を表現する。

![](https://gyazo.com/ce0fa591abe05ce0c5f9e27c7070ac45.png)

まず、シーン設定内の「Screen Space Reflections」の  
Refraction と Half Res Trace のチェックを入れる。

![](https://gyazo.com/deb751e6455464850f5cba86c53b7eba.png)

次に、Material 設定内の ScreenSpaceReflections のチェックを入れて、  
その中の「Refraction」のチェックを ON にする。  
BlendMode は、Opaque。

![](https://gyazo.com/575d5f85e781d27971976eb2386bf2dc.png)

以上の設定をすると、疑似的な屈折表現を指定することができる。

ScreenSpaceReflaction については
[凹み Tips さんの Unity で Screen Space Reflection の実装をしてみた](http://tips.hecomi.com/entry/2016/04/04/022550)  
の内容が非常に参考になりました。

ScreenSpaceReflaction の注意点として、オブジェクトと透明オブジェクトは反射・屈折するが  
オブジェクトに移りこんだものは反映されない。

### Principled BSDF を使用したときの関係パラメーター

#### BaseColor

ガラスの色。  
透明の映り込みに対して掛け算で乗る。

#### Metallic

![](https://gyazo.com/8e35e0e6720268d007bb78375439a611.gif)

0 にすると、透明になる。  
1 になるにつれて透明度が下がりマットなメタル質感になり、不透明になる。

#### Transmission

1 にすることで、ガラスのような質感になる。

#### Roughness

![](https://gyazo.com/4f946bdbf9041e481360d180b05730a7.git)

表面のざらざら度。
0 ならつるつる、1 になるほどすりガラスのような質感にかわり  
1 場合は Lambert 的な不透明質感になる。

#### IOR

屈折率。  
デフォルトは 1.45  
水なら 0.85

## 参考

- http://bibinbaleo.hatenablog.com/entry/2017/10/11/200629
