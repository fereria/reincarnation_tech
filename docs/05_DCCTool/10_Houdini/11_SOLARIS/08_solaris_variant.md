---
title: SOLARIS で VariantSet
tags:
    - USD
    - SOLARIS
    - Houdini
---

HoudiniSOLARIS で VariantSet を作りたい場合の方法について、
作り方がわかりにくかったのでメモ。

まず、VariantSet は USD のコンポジションアークの１つで、
USD の説明詳細は {{markdown_link('comp_arc_variant')}} にまとめてあります。
かんたんに説明すると、ある Prim に対してスイッチを作る事ができる機能です。

![](https://gyazo.com/bb23a224f991cad38ad858df64f25869.png)

こんなかんじで、ある Prim に対してスイッチを作り、

![](https://gyazo.com/26784267376a283397f2db3862844b3f.png)

切り替えられるようにできます。

![](https://i.gyazo.com/751b299f50f6ed910a1e217ff5b70d43.gif)

このサンプルの場合、スフィアとキューブとコーンのモデルを
スイッチできるようにしています。

## SOLARIS の VariantSet ノードについて

SOLARIS で VariantSet を作りたい場合は、

![](https://gyazo.com/3b7be98df33dd78273bae3bc92fa30e1.png)

ノードは Add Variants to Existing Primitive と Add Variants to New Primitive
のいずれかを使用することで作ることができます。

VariantSet を作るというのは同じですが、この２つでは若干得られる結果が
変わります。

### Add Variants to New Primitive

まずはこちらから。
こちらのノードはその名の通り VariantSet で新しいノードを作り
切り替えをできるようにします。

![](https://gyazo.com/60eec0c7b4ec69a83977802e848c406b.png)

使い方はとてもかんたんで、input2 に対して
切り替えするモデルをコネクトします。

![](https://gyazo.com/a8a56691990a618966a0cd70f1f222f5.png)

設定はデフォルトのままで OK です。

![](https://gyazo.com/777fc35410d45c093a539158d6c4751d.png)

出来上がった結果のシーングラフ。
Primitive Path で指定した場所に（この場合 addvariant1）に対して
VariantSet が追加されます。
特徴は、この Primitive Path で指定した Prim の子に対して
input2 で入力した Prim のうち選択されているもののみ表示されます。

![](https://gyazo.com/53e8916a6c123f44d5cfe241ee0fbbb2.png)

この VariantSet がどのように作られているか Inspect Active Layer で確認してみると

![](https://gyazo.com/05fd6550411584192ded23c7b31ea5b9.png)

Primitive Path 以下に VariantSet が作られ
その VariantSet 以下の各選択肢に対して、input2 で入力した Prim が
作られています。

なので、シーングラフをみると選択されている Prim がけが表示されている状態
になっているわけですね。

## Add Variants to Existing Primitive

対して、もう一つの Existing Primitive。
こちらは **Existing**とあるとおり、すでにあるシーングラフの Prim に対して
VariantSet で設定を変更するような場合に使用します。

![](https://gyazo.com/3f8712bb1342f8d9caaa600e951e9bf6.png)

まず、同じような挙動をするようにノードを構築。

![](https://gyazo.com/f8c14d85736dfa564e3d2286257f630c.png)

まず、Graft を使ってある Prim 下に切り替え用 Prim を配置しておきます。

![](https://gyazo.com/cf8a97378381f15c9c772cd3f97494dd.png)

結果。
variant ノード以下に 3 つの Prim が配置されました。

![](https://gyazo.com/0a7fab22efbbc5cbe476694848041d99.png)

その variant Prim を VariantBLock に対してコネクト。

![](https://gyazo.com/dec82c4bac1eeab14f42722fcdd67ac2.png)

Prune を使用して、表示したい Prim 以外は非表示になるようにします。

![](https://gyazo.com/65fcd5ba01e8a7938278b551cdd04298.png)

Prim をみると、Prune ノードの効果で指定 Prim 以外は非アクティブになっています。

![](https://gyazo.com/b90315e4bb020644f4d1a23bc9569db0.png)

そして、 VariantBlock End ノードの Primitive Path を
入力に入れた Primitive Path （variant）に変更します。

最後に、 input1 に対して Graft ノードをコネクトします。

![](https://gyazo.com/97e40f697a2b3c86832e44219be01819.png)

結果。
先ほどとは違い、全部の Prim が variant 以下にあるものの
VariantSet で選択された Prim のみが Active になった状態になります。

![](https://gyazo.com/791591ce7dd1710b6357ea9d95b102d8.png)

中身を確認してみると、
VariantSet 下の選択肢の中は active の変更ののみが入っていて、
Prim 定義自体は VariantSet 外に定義されています。

つまり、 VariantBlock のノードで挟まれている間部分のみの差分が
VariantSet 内に定義サれるのが Existing Primitive ということになります。

なので、

![](https://gyazo.com/e11e073c2c7772f87b1cd0711f89b712.png)

こんな感じで input1 に何も入力されていない場合

![](https://gyazo.com/6156a4d7b32af5b13cf8af77118c6f51.png)

こんな感じで over になっているので

![](https://gyazo.com/ecebf14b25fc0e20a4a0937a4962d476.png)

Prim の定義がないためモデルが表示されない状態になってしまいます。
（これにきづけずめっちゃハマる）

## まとめ

SOLARIS 内で構築されたシーングラフに Variant を入れたい場合は Exists で
Variant を定義することによって、差分情報のみでコンポジションが作れる...
というのに今回調べていてようやく気が付きました。
（こちらのパターンを使うほうが多そう）

New のほうは、Reference でモデルを読んできてから...とか
そういうパターンで使うのがメインになる感じと想像していました。

使い分けることによって、いろいろなバリエーション構築が
できるようになりそうです。
