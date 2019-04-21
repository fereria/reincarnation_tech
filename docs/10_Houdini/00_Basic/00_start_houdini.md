# 初めての Houdini 基本用語と構造

<!-- SUMMARY:初めてのHoudini_基本操作01 -->

Maya使いでHoudini完全初心者が、使い方で調べていった内容を書きためていきます。  
  
## 基本的な用語
  
基本的な所ですが、SOP・VOP・COP…という謎の3文字が並んで最初からわからない。  
  
「OP」とは、Operatorの略。  
Houdiniのノードの分類のようなもので、  

|      |                    |
| ---- | ------------------ |
| SOP  | Surface Operator   |
| VOP  | VEX Operator       |
| COP  | Composite Operator |
| CHOP | Channel Operator   |
| ROP  | Render Operator    |

それぞれが上の意味になっている。  
SurfaceOoeratorが、Geometry（Mesh）を扱うオペレーター  
VEXというのは、C++ライクなHoudiniのプログラム言語で、  
MayaでいうところのExpressionに近い（もっといろいろできるけど）  
VOPは、そのVEXをノードベースで組み立てられるもの。

![](https://i.gyazo.com/acbe156be6af66a38bd29b4409386c0a.png)

公式Helpのノードを見ると、このOperatorごとにノードがまとめられている。  

## データ構造について

Houdiniは、基本的に「ノード」という単位を基本として出来ている。  
そしてそのノードは入れ子構造になっている。  
  
![](https://i.gyazo.com/d3a830b3ca2a60c1e9e41dc064dfd257.png)

シーンの構造を確認するのたTreeView  
そしてこの階層は、Folder階層のように obj/geo1/attribvop1 のように表すことができる。  
パラメーターにアクセスするときもこのパスが基本になる。  

![](https://gyazo.com/604e6b248f232a1d2ebec0098b033c9e.png)

TreeViewのこのアイコンが、上記のOperatorに対応していて  
各Operatorごとにノードがグループ化されている。  
  
このなかのOBJというのは、MayaのDAGノードにおけるTransformノードのようなもの。  
あるいは、BlenderのObjectのほうが近い。  
GeometryやLight、Cameraなどを配置する「場所」であり  
内包する各ノード（SOP等々）を実体化するための出口的な役割を持つ。

![](https://gyazo.com/784596a253781f283d042ed91d73b0b4.png)

また、このOBJノードをつなぐことで親子化をすることができる。  


### Network

そして、Houdiniの最も重要な部分になるのがNetwork。  
Networkに表示されているハコがノードで、そのノードそれぞれがさまざまな機能を持っている。  
そのノードを接続していくことで、データを編集・構築していくことができる。  

![](https://i.gyazo.com/db6fc91ffbad79f2e96b0e2681e67ac8.png)

Maya使いの考え方で表すと、TreeViewはアウトライナはハイパーグラフのヒエラルキ  
表示をしているのがTreeViewで、Networkは、ハイパーグラフをConnection表示にしたようなもの。  
まずInputからデータが入力され、それぞれのノードがそのノード内でゴニョゴニョしたあと  
Outputとしてデータが出力される。  
その繰り返しでデータが構築されていく。  
  
Houdiniのすごいところはこのノードの種類が多用なことと  
ノードからアクセスできる内容がMayaの比ではないのが大きい。
（OpenMayaのイテレータで処理するような内容をノードベースで組める）  

