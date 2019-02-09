# DepthOfFuild を使用する

<!-- SUMMARY:DepthOfFuild を使用する -->

## DOF を有効にする

![](https://gyazo.com/f61ddcee8fdba6b0692a60f1443544ac.png)

まず、EEVEE の設定内で、Depth of Fuild のチェックを有効にする。  
これを有効にしないと、そもそも DOF はかからない。

DOF にある「MaxSize」は、大きくすればするほど、ボケがきれいになる。  
ただし、レンダリング速度は落ちる。

## カメラの設定

DOF の細かい設定は、指定のレンダリングカメラ内に存在している。

![](https://gyazo.com/57e8b0bef6d396038a0cc2c8b5095761.png)

Focus on Object に、ピントを合わせたいオブジェクトを指定する。  
続いて、Focus Distance でピントが合う範囲を指定する。

Aperture が、レンズ側の設定。

| Attribute | 意味                                                                  |
| --------- | --------------------------------------------------------------------- |
| F-stop    | 絞り？  現状は、数値が1以下くらいじゃないとボケがほとんど分からない。 |
| Blades    | 絞りの羽根枚数 数字が大きくなると丸ボケになる                         |
| Rotation  | ボケの回転3～5角形ぐりあのボケを回すことが出来る。                    |
| Ratio     | ボケの歪みの量の指定？                                                |

![](https://gyazo.com/6f0752302c2a9ae699f073cc2d1d3827.png)
