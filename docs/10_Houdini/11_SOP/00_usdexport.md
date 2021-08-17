---
title: PackPrimitiveとUSDExport
tags:
    - USD
    - SOP
    - Houdini
description: SOPからUSDを出力する
---

普段はLOPを使用してUSDを扱っていましたが、  
SOPからもUSDの出力ができるというのと、HoudiniのPackPrimitiveについて教えてもらったので  
SOPの勉強とデータの構造を理解するのを兼ねて  
SOPのUSDExportを試してみようと思います。

## 基本

![](https://gyazo.com/0ebcfc13f33f77e8d0d4c300c025707f.png)

まず、SOPには「usdexport」ノードがあります。
ので、このノードに接続するとUSDを出力することができます。

![](https://gyazo.com/3094adfd910c7687e7e56b69890f1a8a.png)

シンプルなキューブをOutputFileのみを指定して出力すると、

![](https://gyazo.com/e2afc8c4abcbc12b2bd635ce43ab15d5.png)

この場合、
![](https://gyazo.com/f58a31947d173d16ede4f675654cb927.png)

Relative Path Prefixの指定（この場合、usdexportのノード名）のXform＋mesh_0という名前のMesh  
が出力されました。

SOPのGeometry以下は、Mayaでいうところ１つのMeshノードのような扱いなので  
出力されるUSDファイルは、１つのUSDファイルに対して Xform + Mesh の組み合わせで
出力されました。

![](https://gyazo.com/e09502d09f9abf093677da7e321b0c1a.png)

![](https://gyazo.com/eee610190469acb60518e69e3c2a3828.png)

確認のため、このようにDuplicateを使用してモデルを複製したのち、出力しても  
1つのXform＋Meshにまとめられた形で出力されます。

## PackPrimitive

次はPackPrimitiveがあった場合。
https://www.sidefx.com/ja/docs/houdini/model/packed.html
PackPrimitiveは、

> パックプリミティブをコピーすると、ジオメトリ自身がコピーされるのではなく、 
> 参照 がコピーされます

とある通り、いわゆるインスタンスです。

![](https://gyazo.com/56d4539232dedbb243f91ac08f2afbf1.png)

BoxをPackしてGeometrySpreadSheetを見ると、

![](https://gyazo.com/005369573c9a850fa0d3f5bea4a60972.png)

↓

![](https://gyazo.com/ffbc4e84bbec8b11fc659c8c1f5133da.png)

Point等はパックしたジオメトリの位置情報をPointに持つようになります。

![](https://gyazo.com/c7130d2cd4955580bb62a99b02d7c44d.png)

PackしたジオメトリをDuplicateして、Exportをしてみます。

![](https://gyazo.com/6ca9817c55159543010c043dbdca73fb.png)

結果。
青になっているのは、USDのインスタンスになっているからで  
そのインスタンスの元Meshが、 Prototypes/obj_0 として出力されているのがわかります。

![](https://gyazo.com/a9953ec644235d017120332260d7f9b3.png)

デフォルトではインスタンスになっていますが、USDExportの Packed Primitivesを  
変更することで、実体のMeshにすることも、Point Instancerにすることも、Unpackすることも可能です。

![](https://gyazo.com/3a15feab78819496136833a1e660f010.png)

実体化した場合は、 Relative Path Prefix 以下に obj_### で出力されます。

![](https://gyazo.com/e6b6cad639740eec9b4e9c05101e5f8b.png)

最後に、Unpackした場合。

![](https://gyazo.com/055a91f62fa1bb8489bacc1eb5a99b1e.png)

Packed Primitivesがある状態で、ExportUSDでUnpackすると  
Xformが作成されずに、Primitivesが個別のMeshPrimとして出力されます。


## Path/Nameの指定

PackedPrimitive を使用して複製したデータを出力した場合でも  
各Primitiveに名前を付けて出力したい...というケースがあると思いおます。
その場合は、指定のAttributeをつけることで  
個別のPathを指定することができます。

![](https://gyazo.com/eb26b5980d0650f7b8f6e4455a31fce3.png)

まずは Attribute Wrangleを追加して

```
s@path = "/sampleSdfPath/Cube";
```

path を追加します。

![](https://gyazo.com/6511e2dc1ff0740ac0e98c7ad03aaf77.png)

こうなって

![](https://gyazo.com/5413ffb43e67d5a0700bda7a14ddde54.png)

結果。
この場合は、pathがUSDのSdfPathになり、このPathに＋して数字が割り振られます。

```
s@name = "hogehoge";
```
あるいは、 nameを指定すると、

![](https://gyazo.com/fbe493fb010f735fedd66904d09e46dd.png)

Relative Path Prefix で指定したPath以下に name のXformが作成されます。

## Mergeした場合

最後にMergeした場合を確認します。

![](https://gyazo.com/97dc9097e7434bbff8d8824ca749baec.png)

ノードはこんな感じで、それぞれのBoxに hogehoge と fugafugaという名前を付けます。
その２つをMergeします。

![](https://gyazo.com/285e783897f2ee5209b3b7cdf98ba3d5.png)

SpreadSheetはこんな感じです。

![](https://gyazo.com/59a2179bfa9d5d6d253f0115826c0880.png)

結果。
それぞれのジオメトリが、別のXform＋Meshの構造で出力できました。
つまりは、SOP側だけでも  
pathアトリビュートあるいはnameアトリビュートを使用して  USDのシーングラフを  
作ることができるのがわかりました。  
（それが使いやすいかは別問題として）

## まとめ

もともとはSOPで使われているPackedPrimitivesとはなんぞ？？？
追加するとどういう意味があるんだろう？？？という疑問から調べ始めましたが  
その挙動や、GeometrySpreadSheetを確認したときの変化  
その意味するところなどが理解できました。

次はAttribute回り？