---
title: VEX を VOP に置き換える 01 ノイズ
---

VEX チュートリアルをもとにして VOP に置き換えてみました。
参考元のチュートリアルは [こちらを参考](https://houdini.prisms.xyz/wiki/index.php?title=JoyOfVex8)にしました。

置きかえるのは

```
@Cd = curlnoise(@P*chv('fancyscale')+@Time);
```

このコード。

![](https://i.gyazo.com/c63bddc184ec97c2cd4dd97804b7cc4c.gif)

結果。  
VEX で作成したときは pointwrangle で作成したので、VOP で作成するときは pointVOP を使用します。

![](https://gyazo.com/889b0e6f04c8b1bcdf8956a5032463f7.png)

fancyscale 以外は単純にノードをつければ OK ですが  
VOP の場合はどうすればいいのかぱっと見つからずだったので、調べました。

## パラメーターを追加する

![](https://gyazo.com/dd6af9a662e3c843efe9c6eeac7a0ad4.png)

まず、globalvop と add との間に multiply を追加。

![](https://gyazo.com/820436ce2d6a6cdb54cb2428f3a1f852.png)

input1 に P をさして、input2 の ○ 部分で中ボタン →Promote Parameter をクリックする。

![](https://gyazo.com/16cb99034e9d44d981c18bb571983f4a.png)

U で上の pointVOP に移動してノードを確認すると

![](https://gyazo.com/22ef6faf2f1ee0568d4c8aaed1779483.png)

inputNumber が増えています。  
追加されたプロパティはそのままだと Label もわかりにくい上に Vector じゃないので  
vector になるように変更します。

![](https://gyazo.com/a48233f85ccd67c89ab246bf4838bfcb.png)

右上の歯車マークを右クリック →Edit Parameter Interface... を選択。

![](https://gyazo.com/2fbfed772b10e51df628bb8ff7ac78f1.png)

新しく追加されている Input Number2 を選択し、

![](https://gyazo.com/6a4642efb499a202d674198c9060be48.png)

Name と Label を fancyscale、Type を Vector に変更する。

![](https://gyazo.com/028a7f3fb88801f10fc6beda1329ab33.png)

これで、pointVOP に Vector のチャンネルが出来る。

![](https://gyazo.com/2079a53e0c526c3c909f3f08ada73b08.png)

これで、

```
@Cd = curlnoise(@P*chv('fancyscale')+@Time);
```

これと同じ挙動になる。

## まとめ

...どう考えても VEX で書いた方が楽な気がする...
