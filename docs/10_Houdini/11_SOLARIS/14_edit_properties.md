---
title: SOLARISでAttributeを編集する
tags:
    - SOLARIS
    - USD
---

SOLARISでUSDのAttributeをノードで編集する方法がわかりにくかったのでメモ

![](https://gyazo.com/602f1aa125ca16354f7a3c3bee199be1.png)

## 新しくプロパティを追加する

まず、編集するにはEditPropertiesノードを使用します。

![](https://gyazo.com/1c9f019b22ff0405825a97fff1284a95.png)

ノードを作成したら、 Edit Parameter Interface...あるいは

![](https://gyazo.com/51bc402cfc5aae077d3acb807a77cae0.png)

Edit Propertiesを選びます。

![](https://gyazo.com/ae2d3ad3130e4347d44752e5dbc2264a.png)

From USDの Properties から、追加したい型をExistingParametersに
追加します。

![](https://gyazo.com/762f0fa7677997edef31fa1ca2126368.png)

あとは、値を変更すればOKです。

![](https://gyazo.com/4ef3693800c56c3c95b7daf7d258b926.png)

USDのプロパティが指定できました。

## すでにあるプロパティを編集する

![](https://gyazo.com/bdc359a981b4ff35d9ea16265d72c8fd.png)

すでにあるプロパティを編集したい場合は、
Scene Graph Detail から、Edit Property を選びます。

![](https://gyazo.com/fdb27c3f6de94facdb5031f94065f9c1.png)

すると、 Edit Properties が作成されます。

![](https://gyazo.com/312751150a7654daf99518a3146de20c.png)

Edit Propereties には、先程選択したプロパティがすでに指定されています。
デフォルトだと Do Nothing(なにもしない)なので、

![](https://gyazo.com/53d92a12b0ae8f43b3c0381768780a9e.png)

Set or Create にして、編集をします。

## Blockする

Blockとは、USDの機能の１つで、現在のレイヤーまでの編集した値を
その名の通り「Block」することができます。

![](https://gyazo.com/93e02a39bed30a6fcf59e7689c69ae86.png)

たとえば先程つかしたプロパティをBlockしてみます。

![](https://gyazo.com/123df21696012385b877993b9550cc51.png)

ノードの構成はこんなかんじ。

![](https://gyazo.com/5c5426f164336025df6f008aa079326c.png)

Edit Properties で、Blockしたいプロパティを追加して、選択を「Block」にします。

![](https://gyazo.com/bb06690d774826dfecaa3f4180cc33f8.png)

Block_Prop ノード後のScehe Graph Detail を見ると、
sampleProp が None になっていることがわかります。
Blockすると、Blockされるより前（弱いレイヤー）のオピニオンはすべて無効になります。

## 編集対象のPrimを変更する

![](https://gyazo.com/ac63370a95ef80c6f703a07a2b512f2b.png)

デフォルトだと、Inputで指定されたPrimが指定されています。
Primitivesを変更することで、指定したPrimを編集することができます。

### 指定した名前

![](https://gyazo.com/00da0ce63fb79bedd70a6291cf0c7c65.png)

指定した名前のPrimの場合は、編集したいPrimを右クリック→ Copy Paths で、SdfPathを取得します。

## 指定Prim以下すべて

![](https://gyazo.com/0b57cce4903d2e3b723498bff4f27681.png)

このような構造で、 sample_cube 以下すべてを編集したい場合

![](https://gyazo.com/229a41d0f72a29f24272f132b6cc88a3.png)

Primitivesに、 /path/* とするとそのPrim以下がすべて対象になります。

## Collectionに含まれるノードすべて

![](https://gyazo.com/ac5c40ec06c6fc29451798a2ce0fdffe.png)

事前にCollectionを作成しておいて、このCollectionに含まれるPrimをセットする場合、

![](https://gyazo.com/912b4f70dd9deb4b5d86f571acd8860d.png)

Primitivesの→の[▼]ボタンを押して、Collection Nameを指定します。

このように、単純にSdfPathを指定するだけではなく
Collectionやワイルドカードなどを使用することで、まとめてアトリビュートを
編集することができます。