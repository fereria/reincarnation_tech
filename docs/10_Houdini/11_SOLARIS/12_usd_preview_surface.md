---
title: UsdPreviewSurfaceでマテリアルを設定する
---

HoudiniでのUsdPreviewSurfaceを使用したマテリアルの指定方法について
まとめてみます。

![](https://gyazo.com/4740ab62509e647eb6231622e997d251.png)

まずは、MaterialNetを作成。

![](https://gyazo.com/4b98de76ff12a97b337943654cd2504e.png)

そして、UsdPreviewSurfaceを作ります。

![](https://gyazo.com/c5bb57de760d03a352058d1c7cad9a0b.png)

まずはわかりやすい色をつけておきます。

![](https://gyazo.com/d3b42e47c0e8d758401363c7a742a2da.png)

Stageに戻って、MaterialLibraryを作り、

![](https://gyazo.com/1d6f5afa50c0c68209a0f7f887174e7c.png)

Material VOP で

![](https://gyazo.com/5886fc12a5f8b75aa0cf194a43eac509.png)


先ほど作成したPreviewSurfaceを選び、MaterialPathを適当な名前にします。

あとはMaterialPathPrefixを Looks としておきます。

![](https://gyazo.com/e5406cff2767da36878cdf6cc4f1a348.png)

結果。
Looks下にMaterialが作られました。
ここのScopeは何でも良いですが、今回はMayaのExportツール準拠でLooksにしました。

![](https://gyazo.com/cedffd55327e22b6c7b7ffc6c9decada.png)

あとはアサインするには、 Assign to Geomteryにチェックを入れて
アサインしたいノードを選択すればOKです。

## 基本構造

![](https://gyazo.com/9e9a36cc5c617802928cac7e9b41f9b4.png)

USDの場合のマテリアル関係の基本構造は、ざっくりこうなっています。
ジオメトリに対してアサインするのはMaterialPrim。
これはMayaでいうところのShadingEngineに近い感じです。
シェーダー本体は、 ShaderPrimでこれがMaterialPrimと接続されています。

USDのシェーダー関連の特徴として、シェーダー関連のPrimはShaderでひとくくりに
されていて、その区別はIDによって行われます。
どういうことかというと、

![](https://gyazo.com/52704d8598417cb8d1a605c687cb6073.png)

ShaderPrimのアトリビュートを見ると、 id という項目があって
そこに「UsdPreviewSurface」が指定されています。
なので、同じShaderPrimであっても役割が異なることがあります。

デフォルトで用意されているのが

* Preview Surface
* Texture Reader
* Primvar Reader
* Transform2d

の４つです。
（PrimvarReaderはこれ１つでも複数の役割を持つ）

それを踏まえて、テクスチャのアサイン方法で
UsdPreviewSurface以外をみてみます。

## テクスチャを使用する

![](https://gyazo.com/252dea7e68b8b7ac4938812636dd7b24.png)

さきほどのPreviewSurfaceにUVTextureと PrimVarReaderを作成します。

![](https://gyazo.com/5ff25022d094721dbffab2f49ee1fe12.png)

PrimVarReaderは、SignatureをFloat2、VarName を **st** にします。

![](https://gyazo.com/cf663121c44b4897a7cc44ed69a8d5dd.jpg)

こんなかんじです。

![](https://gyazo.com/66f5f54d082e014cdaf6652ddda6f497.png)

シーングラフはこちら。

テクスチャは [こちら](https://texturehaven.com/tex/?t=castle_brick_07)を使用しました。

ここで使用するのが Texture Readerと Primvar Readerです。
シーングラフを見て分かる通り、すべてShaderですが、それぞれが id によって役割が
指定されています。

![](https://gyazo.com/825b54993db4ad3f5e5bacbb9220daa5.png)

例えばテクスチャは、idは「UsdUVTexture」になっています。

### Primvar Readerとは

UVTextureに関しては、TextureColorをShaderに対して接続しているのでなんとなく
わかりますが、もう１つのPrimVarReaderとはなんでしょうか。

まずPrimVarがなにかというと

> Rendermanに由来するもので、「Primitive Variable(プリミティブ変数)」の略
> レンダラーとプリミティブを関連付ける特別なアトリビュートで
> プリミティブの表面/体積に渡ってアトリビュートの値を補間することができるもの
> （公式Glossaryより引用）

です。
つまり、テクスチャのマッピングに使用するUVであったり頂点カラーであったり
ジオメトリ上で定義された各種値を供給する機能を持つのがPrimvar Readerです。

![](https://gyazo.com/a5d453dce7eef8eb203f471faf6103a5.png)

UVの座標を取得するためのPrimvarReaderをみてみると
「varname」を「st」としています。
USDの記述側で、MeshPrimではどういうアトリビュートになっているかというと

![](https://gyazo.com/33521f349604af8fc3370763abac1d53.png)

Meshには「 primvars:st というアトリビュートがあり、そこにはMeshのUV座標が
記述されています。

Primvar Readerとは、このジオメトリ側のPrimversの値を
Shader側で使えるようにしているというのがわかりました。

![](https://gyazo.com/af46853c6fe1102496f0fd72d0819fa5.png)

作成したテクスチャつきのUSDは当然のようにusdviewなどでも確認ができます。

## まとめ

primvarReaderとUSD側に定義されたprimvars:st～といった記述が
どういう関係性になっているのかが理解できていませんでしたが
一通り組み立てたおかげでようやく理解できたきがします。

USDPreviewSurfaceまわりの詳細の仕様は
https://graphics.pixar.com/usd/docs/UsdPreviewSurface-Proposal.html
こちらを参考にしました。