# Houdini の Group

<!-- SUMMARY:HoudiniのGroup_01 -->

Houdini の機能でまず最初に面食らったのがこの Group。  
Maya とかだと単純にノードをまとめるとか、Null として空ノードとして  
使用印象しかないのだが、  
Houdini の場合もっと多機能でありとあらゆる物のベースになっているなと  
触ってて思いました。

## マテリアルのアサイン

![](https://i.gyazo.com/1751f2950f23dd4e73672821e9943951.png)

単純な例として。  
Group ノードにさすと、刺したノードをグループに入れることができる。

![](https://i.gyazo.com/3eb1b898973337a9956a5f4ce7a1e801.png)

Material ノード側で Group に対して Material をアサインすることができる。

![](https://i.gyazo.com/d6cc5826565aba43862bd826ee327587.png)

やっていることはこれと同じ。  
上の例だと、単純にノードをグループ化しているだけなので  
あまり面白みはないですね。

## Expression でグループを作る

![](https://i.gyazo.com/fda35b3fb5643d7dbe9615b1d2346b56.png)

Houdini はありとあらゆる所に Expression やらスクリプトを挟むことが出来る。  
それは Group も例外ではない。  
GroupExpression を使用すると、Expression にマッチするプリミティブやポイントやバーテックス  
のグループを生成してくれる。

![](https://gyazo.com/c0e3623cd4626f299cae61a9c0e12d9b.png)

Y が 0 以上のものをグループ化して、そのグループに入っているポイントの Y をすべて 0 にした例。

## 範囲指定でグループを作る

GroupByRange ノードを使用すると、指定の ID から指定の ID までの範囲を指定の数とばしで  
グループを作ることが出来る。

![](https://gyazo.com/bc12cc849373e5762fb65c39bea833df.png)

この設定だと、

![](https://gyazo.com/66a37cdc88626c44ebb29e56672c3f7a.png)

このように 1 つ飛ばしのプリミティブが選択されるようになる。

## 新規に追加されたポリゴンのグループ

PolyExtrude などで、ノードによって新しく追加されたポリゴンを  
1 つのグループに追加することができる。

![](https://gyazo.com/d4dc7a46aad115847a0fcbe65678585c.png)

Output Geometry and Groups の項目でグループを作成したい部分を選択する。  
Extrude の場合、Extrude してできた側面・表面などの単位で  
指定が出来る。

![](https://gyazo.com/016b78476d6efc1af6a92409b83a9ada.png)

extrudeFront を BaseGroup としてグループを作成した結果。

## 2 つのグループを組み合わせる

上の extrudeFront の結果を、1 つおきに選択したグループを作成したい場合。

![](https://gyazo.com/530280fca2adefc46cf070155328d35f.png)

GroupRange で１つおきに選択したグループを作成する。  
extrudeFront とこの GroupRange の結果の「かぶっている部分のみ」を選択した  
グループを作成したい場合「GroupCombine」を使用する。

![](https://gyazo.com/6f290072c1a28da5546422aeb17af5f8.png)

Intersect(And) を使用すると、両方のグループに属するプリミティブのみ  
グループ化することができる。

![](https://gyazo.com/5b218b3a03adedf960db315e665234dd.png)

結果。

groupCombine は、 Group で指定した名前のグループに、 → で指定したグループと、その下の条件で指定した  
項目をグループに入れる。  
extrudeFront と extrudeFront のように同じ名前にしていると  
元の extrudeFront の結果が上書きされる。

![](https://gyazo.com/ab949af12d8745b7f9e4fef17fe535a2.png)

新しい名前を追加した場合は、

![](https://gyazo.com/d4f864bc1d0b5d49eacbbc8cf782d0a3.png)

新しいグループとして、新しいグループが追加される。
