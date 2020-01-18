# Volumetric(Fog)を使用する

<!-- SUMMARY:Volumetric(Fog)を使用する -->

シーン内で FOG を使用したい場合は EEVEE 設定の「Volumetric」を ON にする。

![](https://gyazo.com/301bceb01a190446a9326ffe4a304eb1.png)

StartEnd で、カメラからみたどのぐらいの距離までに FOG を出すかを制限できる  
（かめらの NearFar と同じ）

## シーンに FOG を配置する

シーンに配置するときは、発生したい範囲を囲むような MeshObject（Cube など）を作成し  
作成した Object に新しく Material を作成する。

![](https://gyazo.com/1aa87cebc55a0d3a6c0f44eeb302a037.png)

NodeEditor で、Principled Volume を作成し、それを  
MaterialOutput の Volume に接続する。

## 設定パラメーター

### Color と Density

![](https://gyazo.com/2ac653ff9c3eda2cc6d4d5565f818fe5.png)

主に指定するのは Color と Density。  
Color が Fog そのものの色を指し、Density は密度を指す。  
デフォルトの Density だとも濃すぎるので、現状だと小数点以下の数値を入れると良い。

![](https://gyazo.com/9d76f47391af8e8f2dae06802eecd4bb.png)

Color には、ボロノイテクスチャなどもさすことができるので、一定の色ではなく  
若干のまばら感を出したい場合などはテクスチャを指すと雰囲気が出る。

![](https://gyazo.com/59e6dff60ff14a36ea2d0ca12d074cb3.png)

Color は、Light を照らされた時の FOG の色。  
Light が白であっても、

![](https://gyazo.com/15b4c3e5e58c9d2bf5551dc89d637698.png)

Color に色がはいっていればライトが当たっている所は、Color になる。

濃度は、Density の数値と MeshObject のサイズによっても大きく変わる。  
あまりにも大きな Mesh だと、Density の数値をかなり下げたとしても真っ黒になってしまうので注意。

!!! info
    Blender のスケールは、デフォルト「メートル」になっている。  
    ので、このオブジェクトの数値が実世界と比較してあまりにも広すぎると、Density が真っ黒になってしまうので  
    注意が必要（かなりハマる）

あとは、必要に応じて Light を配置する。

### EmissionColor

![](https://gyazo.com/155635a5c613aec7e993e15ec175800d.png)

EmissionColor と EmissionStrength は、FOG 全体の色（Light があたっていないところ含めての Fog の色）  
を加算で全体的にのせる。  
なので、EmissionColor そのものに明るい色を入れると、簡単に白飛びを起こす。  
EmissionColor が黒の場合は、なにをしてもいろは変わらない。

### AbsorptionColor

吸収色。  
現状どうしてかは分からないが、この数値を上げると、FOG 全体が Light の補色になる。

![](https://gyazo.com/0846277aa74eeee63a74140406c327af.png)

![](https://gyazo.com/badf109cb65dda4966ab69bfb7c3f765.png)

FOGColor が黄色で、吸収色を白とすると、FOG は補色の青になっている。  
白ではなく、RGB それぞれの色を入れると、それぞれの色が表示される。

## その他謎アトリビュートについてのメモ

Blackbody とは「黒体」  
すべての波長の可視光を放射する光源は「白」く見え、  
可視光を全く放射しない光源（もはや「光源」とは呼べないが）は「黒」く見えることになる。  
実際の光は可視光以外の波長も含んでおり、  
また光は電磁波であることがわかっている。  
全ての波長にわたって電磁波を全く反射をしない物体を黒体と呼ぶ。
（Wikipedia）

炭火やろうそくの炎などが「黒体」と呼ばれるものらしい。

※FOG では子のパラメーターは使われていない？※

黒体の参考

- https://www.ccs-inc.co.jp/guide/column/light_color/vol33.html

tint は「色合い」

Temperature も使用していない？（Fluid 関係用のパラメーター？）

### IrradianceVolume との組み合わせ

![](https://gyazo.com/b18a0d2f2f84a2e28fb5fd00e4cfc7e5.png)

真っ赤な Emission オブジェクトを作成し、IrradianceVolume を配置してみたが  
Light ベイクの効果は Volumetric には乗らない。
