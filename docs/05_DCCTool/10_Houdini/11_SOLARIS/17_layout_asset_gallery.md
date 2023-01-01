---
title: LayoutAssetGalleryとLayout
---

ComponentBuilder で USD アセットの作り方を紹介しましたが、
Houdini19 では、作ったアセットを配置する（レイアウトする）きのうも大幅に強化されていたので
そのあたりを紹介しようと思います。

## Layout

18.5 では、USD アセットのレイアウトを使用とした場合
Stage に対してオブジェクトを 1 つずつ読み込んで配置するしかありませんでした。
PointInstancer なども {{markdown_link('05_point_instancer')}}が、SOP で Point を作成してから SOLARIS 上で
ノードを作るなど、なかなか直感的ではありませんでした。

ですが、Houdini19 で新しく追加された Layout ノードと、LayoutAssetGallery を使用すると
かなり直感的にインスタンスの配置ができるようになっています。

### 使ってみる

![](https://gyazo.com/ae31bae6e789e2147f35fbbe974779b8.png)

まず、SOLARIS の Stage で、Layout ノードを作成します。

![](https://gyazo.com/65fde9dcf1394b835996d938dc93933f.png)

Layout ノードを作ると、PointInstancer ノードが作成できました。
次に、Layout ノードにインスタンス配置したいアセットを読み込みます。

![](https://gyazo.com/d5dc1f36228622ab866293ebac1a05da.png)

NewPaneTabType から Solaris ＞ LayoutAssetGallery を開きます。
デフォルトだと何も入っていないので、

![](https://gyazo.com/3d9f9d27943a0f44784b58759d5e2ce4.png)

フォルダマークから、アセットのディレクトリを指定して
USD アセットを登録します。
今回は、Kitchen_set の assets フォルダを指定します。

![](https://gyazo.com/a139d1e3b99392c2dd6e8fc5739c624e.png)

OK を押すと、サムネが自動で作成されます（そこそこ時間がかかる）

![](https://gyazo.com/68d47b46595809bb2522ef06b917094b.png)

終わると、このようにアセットの登録ができました。

> メモ
> Kitchen_set は Zup だけど、SOLARIS は Yup のようなのでサムネがおかしなことになった...

![](https://gyazo.com/887f5ffc1741aa0108dccf97751d0a8a.gif)

Tab を Brush にして、
登録したアセットから、レイアウトしたいアセットを Drag＆Drop で移動します。

![](https://gyazo.com/d98affeeb886e05a1a357f3e03610ccd.png)

Drag＆Drop すると、PointInstancer にオブジェクトが登録されます。

## Brush で配置する

これで配置する準備ができました。
配置するには、Brush を「Place1」に変更します。

![](https://gyazo.com/c5b67006156019d81b601e38320a0991.png)

使い方は、Viewport に表示されているので
それを参考にポチポチ置いてきます。
置いたところに Point が配置され、インスタンスオブジェクトが置かれます。

![](https://gyazo.com/0c4013e9e68669010abe0106b5c4fe4d.png)

Place Up/Forward を、配置するアセットに応じて変更し（Kitchen_set は Zup）
配置するアセットを選択します。

![](https://gyazo.com/6966e65c5357cc3367ba40c0407fdd5a.gif)

あとは、ビューポート上をポチポチすると、インスタンスオブジェクトの配置ができます。

![](https://gyazo.com/0f00a0128e142d18c399b562d3b02823.gif)

アセットを配置するときは、自動できちんと設置をしてくれます。

## 指定の範囲に配置する

![](https://gyazo.com/c993f8ed87ce3b8f81d8ef110de2c265.gif)

次に、指定範囲内にばらまきたい場合。
この場合は Fill1 を使用して、矩形を指定します。
この場合もオブジェクトに沿った形で（机の上のようなところに）配置できます。

配置した Point を削除するには DeleteBrush を使用します。

このあたりの操作は非常に直感的でわかりやすいです。

## アセットの追加

Layout 用のアセットを登録したい場合は、ComponentBuilder を使用すれば簡単に追加することができます。
{{markdown_link('16_component_builder')}}
追加方法や ComponentBuilder の使い方は、↑ のページにまとめましたので参考にしてください。

## 出力する・確認する

![](https://gyazo.com/16507f0923391b1a58fb649659950ecc.png)

配置したあとは、USDROP で出力が可能です。

![](https://gyazo.com/dcdc64429d8b68a79235ae4e3937a47c.png)

アセットは、PointInstancer 以下の Prototypes 以下に Reference で読み込まれ配置されています。
もちろん出力したファイルも USD なので、このファイルをどこかの Shot にリファレンスして使うことも可能です。

## まとめ

以上、Houdini19 で追加された Layout ノードをざっくり触ってみました。
{{markdown_link('05_point_instancer')}}
PointInstancer に関しては以前も調べていましたが、その時に比べて
Brush を使ったレイアウトになっていて、非常に扱いやすく強力でした。

アセットの管理も、Layout Asset Gallery を使用すれば

![](https://gyazo.com/7c04154ed7e675686de2618183cb7ebd.png)

カラータグや

![](https://gyazo.com/56cea2b72be3dfdc5fd11b7f6b517da0.png)

お気に入り（★）を追加して、

![](https://gyazo.com/8156b838bc9f9e2a502fd4b269ac3fb8.png)

細かくフィルタ表示もできるようになっているので、
USD ベースで作成したアセットライブリが簡単に扱えるようになっているので
ComponentBuilder と合わせれば、USD でのレイアウト環境が整ったと思います。

LayoutBrush は自作もできるようなので、カスタマイズしていけば
さらに効率的にレイアウトができそうです。
