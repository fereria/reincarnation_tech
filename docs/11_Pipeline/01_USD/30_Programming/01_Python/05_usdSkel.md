---
title: UsdSkelについて
---

原則 RIG は持てない USD ですが、Joint と Skinbind に関しては対応していてキャラクターなどは
Skeleton を使用して作成することができます。

現状だと、Omniverse の MayaExport または SOLARIS の群衆の Agent のいずれかのみできますが
今回は Omniverse で出力したデータを確認しながら
USD における Joint のデータ構造を見ていこうと思います。

## UsdSkel の基本構造

まず、USD で Joint と SkinBind を使用する場合は

1. UsdSkelRoot
2. UsdSkeleton
3. UsdSKelAnimation

この３つの構造を利用します。

![](https://gyazo.com/fc344acb67317ebd62d9ff3b09e4e588.png)

基本はこのような構造になります。
（Animation に関してはこことは限らない）

### UsdSkelRoot

UsdSKelRoot は、Joint を使用する場合に Skeleton の親ノードとして作成します。
SkelRoot は Boundabule（BoundingBox を持つ）Prim で、これ以下に Skel が定義されている
Prim があると識別するための Prim です。
また、SkinBind されたモデルを配置する時などは
この SkelRoot を動かすことで、シーン内に配置することができます。

### UsdSkelSkeleton

次が Skeleton。
この Skeleton は、Joint のトポロジを定義し、BindPose を保持します。
UsdSkel は、Maya のように Joint ごとに Prim があるわけではなく
この SkeletonPrim 以下に Joint の構造を持ちます。

![](https://gyazo.com/f7dad2bc1c75d7fbf79c8778815db426.png)

Skeleton には、このように jointsJoint を持ちます。
Joint1 つごとに Index が割り振られ、親子構造は / で表されます。

### UsdSkelAnimation

最後の Animation。
UsdSkel の Animation は、この AnimationPrim という形で別途定義されます。
（Skeleton はあくまでも BindPose のみを持つ）

### それをふまえて

以上のような Root Skeleton Animation の 3 つで構成された UsdSkel で
シーンを構成する場合は、このようになります。

![](https://gyazo.com/9b444a9a78bf063ee6d12545d3004233.png)

多くの場合は、キャラクターモデルの usd と各 Shot ごとのキャラアニメーションの usd
という構成になります。

上で説明したとおり、UsdSkel は Maya の Joint とは違い、
構造すべてをまとめたものが１つの Prim として表現されます。
なので、Joint の間に Group ノードなどの、Joint 以外のノードが混ざることが
許容されていません。
なので、Maya でモデルを作る段階から Skeleton だけの構造として切り分けておく必要があります。

そして、その SkeletonPrim を動かすための Animation は別 Prim になるので
各 Shot ごとの Animation は
別レイヤー扱いにして、Reference またはサブレイヤーで合成して
Skeleton に対して Relationship で Prim を指定すれば
モデル部分は共通化した上で、Shot ごとは別のレイヤーでデータを切り分けることができます。

## データ構造を理解する

ざっくりと Prim の関係性などはわかりましたが、
ここからは Skel に関係するデータがどのように定義されていているのかを
もう少し詳しく確認してみます。

### Skeleton と Joint

まず Joint について。

上の Skeleton で書いたとおり、Skeleton は、joints アトリビュートに
この Skeleton が持つ Joint のリストを持ちます。

![](https://gyazo.com/e0e6841dcb7768ea7f4ccae88e6a1fb3.png)

たとえば、このようなキャラクターの Skeleton があった場合。
この Skeleton は１つの SkeletonPrim になっていて、

![](https://gyazo.com/e4e76c60ef470025cc52bddbda61c557.png)

このように、Skelton の階層構造のフルパスのリストを持ちます。
この各 Joint がどの位置にあるかは、

![](https://gyazo.com/ce3bea8767e1443a63b5b7061979eb86.png)

BindTransforms アトリビュートに保存されています。
この Transforms は Matrix の配列になっていて、
joints の Index（0:Hips とある場合は :より前の数字が Index）にそれぞれ対応しています。
そのため、 bindTransforms と joints の要素数は同じになります。

#### Animation

Skeleton は、BindPose のみなのでアニメーションは保持しません。
アニメーションをセットしたい場合は、SkeletonPrim に対して AnimationPrim を
Relation で接続します。

```python
skelPrim = skel.GetPrim()
# SkeletonのAnimationはRelationでAnimationPrimが指定されている
animPath = skelPrim.GetRelationship("skel:animationSource").GetTargets()[0]
# Animationの値はVector
print(anim.GetRotationsAttr().Get())
print(anim.GetTranslationsAttr().Get())
print(anim.GetScalesAttr().Get())
```

Relation 接続先は skel:animationSource なので、
GetRelationship で Relation を取得し、AddTarget で、AnimationPrim の SdfPath を
指定します。

### Topology

Joint は、SkeletonPrim では /root/a/b のような / で区切られたパスで記述されます。
この Joint 内の親子階層を検索したり、現在の Joint の Path がどこにあたるのかを
調べたい場合、文字列で検索したりするのはさすがに面倒です。

この Skeleton 内の Joint の構造は UsdSkelTopology を利用することで
把握することができます。

```python
# Skelの構造は Topology を利用すると解析できる
joints = skel.GetJointsAttr().Get()
topology = UsdSkel.Topology(skel.GetJointsAttr().Get())

# Joint数を取得
print(topology.GetNumJoints())
# 引数のIndexがRootかどうか返す
print(topology.IsRoot(0))
# 引数のIndexのParentのIndexを取得する
print(joints[1])
parentIndex = topology.GetParent(1)
print(joints[parentIndex])
```

Topology に対して、joints のリストを渡すと、
それ以降は ある Joint の親がどれなのか などを、Topology に指定したリストの
Index で取得できます。

親 Joint を探したりする場合も、joints の Index の数字でコントロールするというのが
最初はわかりにくいですが
Skeleton で Joint をリストとして持ち、親子階層の確認は UsdSkelTopology を
利用するというところを押さえれば、UsdSkeleton の Joint の構造は理解しやすいです。

### BindSkin

最後に BindSkin。
USD の場合は、SkinWeight の情報は MeshPrim が持ちます。
その情報が、 primvars:skel:jointIndices と primvars:skel:jointWeights の２つです。

他のアトリビュートとは違い、Weight のアトリビュートは「primvars」になっています。
primvar とは、「プリミティブ変数」の略で
プリミティブの表面・体積にわたって値を変化させる（補完する）ものです（例：UV）

つまり、Weight 情報は各 Vertex ごとに持っていますが
Vertex と Vertex の間は primvar によって補完されることになります。

jointIndeces と jointWeights は、 Skeleton の Joint 数 × 頂点数分持ちます。
並び順は、Mesh の Vertex の Index 順になっているようで

jointIndices は、Skeleton の Index jointWeights はその頂点の SkeletonIndex の Weight 値を 0-1 で持ちます。

![](https://gyazo.com/43f5faa59188bd1205718bb32beba74e.png)

たとえば、ある Mesh に Joint が２つある Skeleton を Bind したとすると
構造的にはこのように Mesh の Vertex 順に Skeleton の数だけ並び、、、というふうになります。
Joint の Index は順不同で、かならず 0 1 2 ... と増えていくわけではありません。
あくまでもある Vertex に対しての joitnWeights との組み合わせになります。

```python
meshPrim = stage.GetPrimAtPath("/World/Root/Geom/pCube1")
bindingAPI = UsdSkel.BindingAPI(meshPrim)

indicesPrimvar = bindingAPI.GetJointIndicesPrimvar() # UsdGeomPrimvar
weightPrimvar = bindingAPI.GetJointWeightsPrimvar() # UsdGeomPrimvar
# Indexの並び順は
# 上の頂点のWeight
print(indicesPrimvar.Get(0)[4:6])
print(weightPrimvar.Get(0)[4:6])
# 下の頂点のWeight
print(indicesPrimvar.Get(0)[0:2])
print(weightPrimvar.Get(0)[0:2])
```

Bind したり、Bind 情報を取得する場合は、BindingAPI を経由して取得します。
bindingAPI の GetJoitIndicesPrimvar と GetJointWeightsAttr を使用すると
値が取得できるし、CreateJointIndicesPrimvar CreateJointWeightsPrimvar で
値をセットすることもできます。

## まとめ

ここまでで、Skeleton - Joint - Animation - SkinBind の関係性が
ざっくりと理解できました。

1. Joint は SkeletonPrim が持つ
2. Animation は Skeleton とは別に AnimationPrim が持つ
3. SkinBind は Mesh が持つ

これを踏まえて USD のコンポジションと組み合わせて考えると
Skeleton と Mesh は別レイヤーにして
同じキャラでも服や髪型違いがあったときに Skeleton は別レイヤーにしておいて共有し
コンポジションで合成させたり、
SkinWeight と Skeleton と Mesh を別レイヤーにしておいてコンポジションで組み合わせたり
といったことができるようになります。

Animation も、キャラモデルは共有しつつ、Shot ごとの Animation は別レイヤーとして出力
（Omniverse 的には AnimationClip と呼ぶ）そのファイルを Reference して
Skeleton の animationSource に接続すれば
キャラとモーションを別ファイルにすることで
モデルが更新されたときに、Shot のレイヤーのモデルも更新する...
みたいなことができるようになります。

欠点として、Joint の階層の間に Joint 以外の階層が入るのは NG なので
それを踏まえて構造を考える必要があります。

## 参考・実験資料

-   https://graphics.pixar.com/usd/docs/api/usd_skel_page_front.html
-   {{markdown_link('Usdskel_02')}}
