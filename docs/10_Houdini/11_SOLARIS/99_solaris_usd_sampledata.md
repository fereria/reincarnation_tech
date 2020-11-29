---
title: SOLARISのサンプルhipデータ
---

## USDオーサリング

### SubLayerでレイヤー分割

#### やりたいこと

ある編集部分だけを別レイヤーとして出力したい

![](https://gyazo.com/61ed9dd0f5db8eeae9c187d65d04c328.png)

:fa-download: [SampleHip](https://1drv.ms/u/s!AlUBmJYsMwMhhOZmr5VyTeeRR26_DA?e=3SPKki)

編集の差分だけを over で合成したい、ただしそのままだと入力側がないためErrorになる。
ので、編集差分を作成する手前（サンプルでいうところの edit1ノード）前に
layerBreak1を作成する。
このノードを使用すると、USDExport時はそれの前のPrimが出力されないで
overで出力される。

結果、 cube(オブジェクト側)は cube.usda 移動値側は cube_B.usda に出力され
その２つが cube_export.suda でサブレイヤー合成される構造ができる。

## Material

### MaterialAssignをVariantで設定

![](https://gyazo.com/c8aba76afc6fc4be3570f79546e96bae.png)

VariantBlock内にAssignMaterialを作成。
注意点はVarinatで切り替える階層は、VariantのAttribute以下にある必要があるので
VariantBlockは、 grid1 あたりに指定する。

:fa-download: [SampleHip](https://1drv.ms/u/s!AlUBmJYsMwMhhOZk4NQ3UT8yrcD3Yg?e=ixIyWT)
