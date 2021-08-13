# ReflectionProbe と IrradianceVolume

<!-- SUMMARY:ReflectionProbe と IrradianceVolume -->

![](https://gyazo.com/6d346896e38283402c4f86d9ac98eb54.png)

LightProbe 下にあるオブジェクトを使用して、  
EEVEE の反射や間接光などの表現を行う。

## リフレクション表現（ReflectionProbe）

ScreenSpaceReflection ではなく、ReflectionProbe を使用して  
反射表現を作成する。

![](https://gyazo.com/2c9f60bc6b530df603933e23a7a13dbd.png)

まず、スフィアを作成し  
同位置に ReflectonProbe を作成する。

![](https://gyazo.com/910c5610c470540d13e7835ce013394b.png)

次に、新しい Material を作成して Sphere にアサインする。  
パラメーターは、Metalic を 1 に、Roughness を 0 にする。  
これだけだと、まだなにも表示されない。

![](https://gyazo.com/5fc459ac7495a670a51479e3d0cd644f.png)

わかりやすいように、床にチェッカーをはりつけ。

![](https://gyazo.com/2d774884411b42efb0f1359b04bc21f6.png)

準備ができたら、Eevee 内の **Indirect Lighting** にある **Bake Cubemap Only** を押す。  
さらに AutoBake にチェックを入れておく。

![](https://gyazo.com/2c2499e8b7adc2cec84c21b5d1b0556e.png)

実行すると、このように ReflectionCube の内容が Sphere に適応される。  
しかし、デフォルトの場合  
画像のように黒い丸のようなものが移りこんでしまう。  
これは、LightProbe の CubeMap に、自分自身が移りこんでしまうために発生する。  
これを解消するために、LightProbe の設定を調整する。

![](https://gyazo.com/22e12e51bdbb7e3f629f2981a15d005d.png)

Viewport Display の Clipping のチェックをオンにする。  
次に、Probe の ClippingStart の数値を調整して

![](https://gyazo.com/a14bab25dfa6c47741cd6c940ff28c5a.png)

上のチェックを入れた時に表示される Clipping のガイドが、  
Sphere にかからにぐらいになるように 調整する。

![](https://gyazo.com/c8558864e372b54f319b6a636e2f4270.png)

Start の数値を Sphere にかからないようにすることで  
黒い映り込みは解消される。

RightProbe が影響されるのは、Probe の Radius の範囲内のみ。
そのため、

![](https://gyazo.com/a2e471cce61dbcf1da77849af4addf90.png)

中途半端に Probe がかかってしまうと、Reflection の表示がおかしなことになる。

![](https://gyazo.com/8eeb1b18fe3f15b9e4940b0cf6603085.png)

Probe の End を小さくすると、範囲外にあるオブジェクトは映り込まなくなる。  
ので、天球などを Probe には反映したくない場合などは、End 側を調整して  
どこまでを映り込みに含めるかを調整する。

### 現状改善・理由がちゃんと分かっていない現象

![](https://gyazo.com/35cdc7303c9da89a9fb75b8f21a6e357.png)

映り込んでいるオブジェクトの Material が Metalic1 の場合、真っ黒表示になってしまう。

![](https://gyazo.com/8fb5481ea8595edcef972cabebfbb85e.png)

Metalic が 0 の場合は、映りこむ。

## Emission の間接照明の表現(IrradianceVolume)

Emission を使用した証明を作成したい場合、

![](https://gyazo.com/54a10bf2ef1abd420eff39470684b3dd.png)

板ポリを作成し、

![](https://gyazo.com/e12ba80912d86f1106da806f0f661f11.png)

EmissionShader を作成し、Strength を上げる（これが Light の強度）  
しかしこれだけだと、照明に反映されない。  
反映させるために IrradianceVolume を作成する。

![](https://gyazo.com/1a93b09cff7927c1d1737349db7e997b.png)

作成した Volume を、ライトを反映させたい範囲に配置する。  
配置をしたら、Eevee の設定タブ内の Indirect Lighting 内の  
**Bake Indirect Lighting** をクリックする。

![](https://gyazo.com/9b3a2783e295b53c7024371989e7ec3f.png)

実行すると、間接光などのキャッシュが作成され、  
Emission の影響が適応される。  
キャッシュ作成後に Emission の Strength 等を変更しても  
キャッシュが更新されていなければ変更は適応されない。
