---
title: UsdSkelについて
---

原則RIGは持てないUSDですが、JointとSkinbindに関しては対応していてキャラクターなどは
Skeletonを使用して作成することができます。

現状だと、OmniverseのMayaExportまたはSOLARISの群衆のAgentのいずれかのみできますが
今回はOmniverseで出力したデータを確認しながら
USDにおけるJointのデータ構造を見ていこうと思います。

## UsdSkelの基本構造

まず、USDでJointとSkinBindを使用する場合は

1. UsdSkelRoot
2. UsdSkeleton
3. UsdSKelAnimation

この３つの構造を利用します。

![](https://gyazo.com/fc344acb67317ebd62d9ff3b09e4e588.png)

基本はこのような構造になります。
（Animationに関してはこことは限らない）

### UsdSkelRoot

UsdSKelRootは、Jointを使用する場合にSkeletonの親ノードとして作成します。
SkelRootはBoundabule（BoundingBoxを持つ）Primで、これ以下にSkelが定義されている
Primがあると識別するためのPrimです。
また、SkinBindされたモデルを配置する時などは
このSkelRootを動かすことで、シーン内に配置することができます。

### UsdSkelSkeleton

次がSkeleton。
このSkeletonは、Jointのトポロジを定義し、BindPoseを保持します。
UsdSkelは、MayaのようにJointごとにPrimがあるわけではなく
このSkeletonPrim以下にJointの構造を持ちます。

![](https://gyazo.com/f7dad2bc1c75d7fbf79c8778815db426.png)

Skeletonには、このようにjointsJointを持ちます。
Joint1つごとにIndexが割り振られ、親子構造は / で表されます。


### UsdSkelAnimation

最後のAnimation。
UsdSkelのAnimationは、このAnimationPrimという形で別途定義されます。
（SkeletonはあくまでもBindPoseのみを持つ）

### それをふまえて

以上のようなRoot Skeleton Animation の3つで構成されたUsdSkelで
シーンを構成する場合は、このようになります。

![](https://gyazo.com/9b444a9a78bf063ee6d12545d3004233.png)

多くの場合は、キャラクターモデルのusdと各Shotごとのキャラアニメーションのusd
という構成になります。

上で説明したとおり、UsdSkelはMayaのJointとは違い、
構造すべてをまとめたものが１つのPrimとして表現されます。
なので、Jointの間にGroupノードなどの、Joint以外のノードが混ざることが
許容されていません。
なので、Mayaでモデルを作る段階からSkeletonだけの構造として切り分けておく必要があります。

そして、そのSkeletonPrimを動かすためのAnimationは別Primになるので
各ShotごとのAnimationは
別レイヤー扱いにして、Referenceまたはサブレイヤーで合成して
Skeletonに対してRelationshipでPrimを指定すれば
モデル部分は共通化した上で、Shotごとは別のレイヤーでデータを切り分けることができます。

## データ構造を理解する

ざっくりとPrimの関係性などはわかりましたが、
ここからはSkelに関係するデータがどのように定義されていているのかを
もう少し詳しく確認してみます。

### SkeletonとJoint

まずJointについて。

上のSkeletonで書いたとおり、Skeletonは、jointsアトリビュートに
このSkeletonが持つJointのリストを持ちます。

![](https://gyazo.com/e0e6841dcb7768ea7f4ccae88e6a1fb3.png)

たとえば、このようなキャラクターのSkeletonがあった場合。
このSkeletonは１つのSkeletonPrimになっていて、

![](https://gyazo.com/e4e76c60ef470025cc52bddbda61c557.png)

このように、Skeltonの階層構造のフルパスのリストを持ちます。
この各Jointがどの位置にあるかは、

![](https://gyazo.com/ce3bea8767e1443a63b5b7061979eb86.png)

BindTransformsアトリビュートに保存されています。
このTransformsはMatrixの配列になっていて、
jointsのIndex（0:Hips とある場合は :より前の数字がIndex）にそれぞれ対応しています。
そのため、 bindTransforms と joints の要素数は同じになります。

#### Animation

Skeletonは、BindPoseのみなのでアニメーションは保持しません。
アニメーションをセットしたい場合は、SkeletonPrimに対してAnimationPrimを
Relationで接続します。
```python
skelPrim = skel.GetPrim()
# SkeletonのAnimationはRelationでAnimationPrimが指定されている
animPath = skelPrim.GetRelationship("skel:animationSource").GetTargets()[0]
# Animationの値はVector
print(anim.GetRotationsAttr().Get())
print(anim.GetTranslationsAttr().Get())
print(anim.GetScalesAttr().Get())
```

Relation接続先は skel:animationSource なので、
GetRelationshipでRelationを取得し、AddTarget で、AnimationPrimのSdfPathを
指定します。

### Topology

Jointは、SkeletonPrimでは /root/a/b のような / で区切られたパスで記述されます。
このJoint内の親子階層を検索したり、現在のJointのPathがどこにあたるのかを
調べたい場合、文字列で検索したりするのはさすがに面倒です。

このSkeleton内のJointの構造は UsdSkelTopologyを利用することで
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

Topologyに対して、jointsのリストを渡すと、
それ以降は あるJointの親がどれなのか などを、Topologyに指定したリストの
Indexで取得できます。

親Jointを探したりする場合も、jointsのIndexの数字でコントロールするというのが
最初はわかりにくいですが
SkeletonでJointをリストとして持ち、親子階層の確認はUsdSkelTopologyを
利用するというところを押さえれば、UsdSkeletonのJointの構造は理解しやすいです。

### BindSkin

最後にBindSkin。
USDの場合は、SkinWeightの情報はMeshPrimが持ちます。
その情報が、 primvars:skel:jointIndices と primvars:skel:jointWeights の２つです。

他のアトリビュートとは違い、Weightのアトリビュートは「primvars」になっています。
primvarとは、「プリミティブ変数」の略で
プリミティブの表面・体積にわたって値を変化させる（補完する）ものです（例：UV）

つまり、Weight情報は各Vertexごとに持っていますが
VertexとVertexの間はprimvarによって補完されることになります。

jointIndeces と jointWeights は、 SkeletonのJoint数 × 頂点数分持ちます。
並び順は、MeshのVertexのIndex順になっているようで

jointIndicesは、SkeletonのIndex jointWeights はその頂点のSkeletonIndexのWeight値を 0-1で持ちます。

![](https://gyazo.com/43f5faa59188bd1205718bb32beba74e.png)

たとえば、あるMeshにJointが２つあるSkeletonをBindしたとすると
構造的にはこのように Mesh の Vertex 順に Skeleton の数だけ並び、、、というふうになります。
JointのIndexは順不同で、かならず 0 1 2 ... と増えていくわけではありません。
あくまでもあるVertexに対してのjoitnWeightsとの組み合わせになります。

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

Bindしたり、Bind情報を取得する場合は、BindingAPIを経由して取得します。
bindingAPIの GetJoitIndicesPrimvar と GetJointWeightsAttr を使用すると
値が取得できるし、CreateJointIndicesPrimvar CreateJointWeightsPrimvar で
値をセットすることもできます。

## まとめ

ここまでで、Skeleton - Joint - Animation - SkinBind の関係性が
ざっくりと理解できました。

1. Joint はSkeletonPrimが持つ
2. AnimationはSkeletonとは別にAnimationPrimが持つ
3. SkinBindはMeshが持つ

これを踏まえてUSDのコンポジションと組み合わせて考えると
SkeletonとMeshは別レイヤーにして
同じキャラでも服や髪型違いがあったときにSkeletonは別レイヤーにしておいて共有し
コンポジションで合成させたり、
SkinWeightとSkeletonとMeshを別レイヤーにしておいてコンポジションで組み合わせたり
といったことができるようになります。

Animationも、キャラモデルは共有しつつ、ShotごとのAnimationは別レイヤーとして出力
（Omniverse的にはAnimationClipと呼ぶ）そのファイルをReferenceして
Skeletonの animationSourceに接続すれば
キャラとモーションを別ファイルにすることで
モデルが更新されたときに、Shotのレイヤーのモデルも更新する...
みたいなことができるようになります。

欠点として、Jointの階層の間にJoint以外の階層が入るのはNGなので
それを踏まえて構造を考える必要があります。

## 参考・実験資料

* https://graphics.pixar.com/usd/docs/api/usd_skel_page_front.html
* https://fereria.github.io/reincarnation_tech/60_JupyterNotebook/USD/Usdskel_02