---
title: UsdSkelの構造を理解する
---
**ipynbFile** [usdskel_01__UsdSkelの構造を理解する.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/usdskel_01__UsdSkelの構造を理解する.ipynb)
#### [118]:


```python
from pxr import Usd,UsdSkel,UsdGeom
```


#### [107]:


```python
stage = Usd.Stage.Open(r"D:\SimpleSkelB.usd")
```


#### [108]:


```python
rootPrim = stage.GetPrimAtPath("/World/Root")
usdRoot = UsdSkel.Root(rootPrim)
```


#### [109]:


```python
# UsdSkelSkeleton は、Skeletonのトポロジー定義し、BindPoseを保持する
skel = UsdSkel.Skeleton(stage.GetPrimAtPath("/World/Root/joint1"))
# Animation は、SkeletonとBlendShapeのアニメーションを保持する
anim = UsdSkel.Animation(stage.GetPrimAtPath("/World/Root/joint1/Animation"))
```


#### [110]:


```python
skelPrim = skel.GetPrim()
# SkeletonのAnimationはRelationでAnimationPrimが指定されている
animPath = skelPrim.GetRelationship("skel:animationSource").GetTargets()[0]
# Animationの値はVector
print(anim.GetRotationsAttr().Get())
print(anim.GetTranslationsAttr().Get())
print(anim.GetScalesAttr().Get())
```

!!! success
    ```

    [(1, 0, 0, 0), (1, 0, 0, 0)]
    [(0, 0, 0), (0, 2, 0)]
    [(1, 1, 1), (1, 1, 1)]
    

    ```


#### [111]:


```python
# UsdSkelの構造を取得
# UsdSkelは、SkeletonPrimのアトリビュートとしてSkeletonの構造を持つ
for i in skel.GetJointsAttr().Get():
    print(i)
```

!!! success
    ```

    joint1
    joint1/joint2
    

    ```


#### [112]:


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

# ParentのIndexを全部取得 -1 がRoot
# print(topology.GetParentIndices())
```

!!! success
    ```

    2
    True
    joint1/joint2
    joint1
    

    ```


#### [113]:


```python
# JointsAttr の配列に対応するTransformのリスト
# 配列はWorldSpaceのMatrix(GfMatrix4d)
for i in skel.GetBindTransformsAttr().Get():
    print(i)
```

!!! success
    ```

    ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1) )
    

    ```


#### [114]:


```python
meshPrim = stage.GetPrimAtPath("/World/Root/Geom/pCube1")

bindingAPI = UsdSkel.BindingAPI(meshPrim)
```


#### [115]:


```python
# Mesh にBindされているJointをリストできる
print(bindingAPI.GetJointsAttr().Get())
# SkeletonPrimのPathを取得する
bindingAPI.GetSkeletonRel().GetTargets() 
```

!!! success
    ```

    [joint1, joint1/joint2]
    

    ```

!!! success
    ```




    [Sdf.Path('/World/Root/joint1')]



    ```


#### [119]:


```python
# WeightのついているMeshのVertexの値を確認してみる
mesh = UsdGeom.Mesh(stage.GetPrimAtPath("/World/Root/Geom/pCube1"))
```


#### [125]:


```python
# 上の頂点のIndexは 2 3 4 5
for i in mesh.GetPointsAttr().Get():
    print(i)
```

!!! success
    ```

    (-0.5, -0.5, 0.5)
    (0.5, -0.5, 0.5)
    (-0.5, 0.5, 0.5)
    (0.5, 0.5, 0.5)
    (-0.5, 0.5, -0.5)
    (0.5, 0.5, -0.5)
    (-0.5, -0.5, -0.5)
    (0.5, -0.5, -0.5)
    

    ```


#### [129]:


```python
# MeshのSkin情報は primvars:skel:jointIndices と primvars:skel:jointWeights で保持されている。
# indeces は、あるVtxの影響をしているJointのIndex weightはそのIndexの影響力のWeightを持つ
# このIndexは、 VertexSize * JointNum 分のIndex
indicesPrimvar = bindingAPI.GetJointIndicesPrimvar() # UsdGeomPrimvar
weightPrimvar = bindingAPI.GetJointWeightsAttr() # UsdGeomPrimvar
# Indexの並び順は
# 上の頂点のWeight
print(indicesPrimvar.Get(0)[4:6])
print(weightPrimvar.Get(0)[4:6])
# 下の頂点のWeight
print(indicesPrimvar.Get(0)[0:2])
print(weightPrimvar.Get(0)[0:2])
```

!!! success
    ```

    [1, 0]
    [0.9998923, 0.00010770559]
    [0, 1]
    [0.99999505, 0.0000049471855]
    

    ```