---
title: SOLARISでXformからUsdSkeletonを作る
---
**ipynbFile** [UsdSkel_01__SOLARISでXformからUsdSkeletonを作る.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/UsdSkel_01__SOLARISでXformからUsdSkeletonを作る.ipynb)
#### [44]:


```python

from pxr import Usd, UsdGeom, Sdf, UsdSkel
import re

stage = Usd.Stage.Open("D:/work/usd_py36/usd/char_base.usda")

hipRoot = "/xbot_fbx/mixamorig_Hips"


```


#### [45]:


```python

# Skelを作る
skelRoot = UsdSkel.Root.Define(stage, "/SkelRoot")
skel = UsdSkel.Skeleton.Define(stage, "/SkelRoot/Skeleton")

```


#### [46]:


```python

# XformになってるFbxのJoint階層をUsdSkel.Skeletoににするために
# 必要な情報取得

joints = []
jointsName = []
jointTransforms = []

ns = "mixamorig"

for prim in stage.Traverse():
    primStr = prim.GetPath().pathString
    if re.search("^" + hipRoot, primStr) is None:
        continue
    # NSなくす
    joint = re.sub(f"{ns}_", "", primStr.replace("/xbot_fbx/", ""))
    jointName = joint.split("/")[-1]
    transformMatrix = UsdGeom.Xform.Get(stage, prim.GetPath()).GetLocalTransformation(True)
    joints.append(joint)
    jointsName.append(jointName)
    jointTransforms.append(transformMatrix)

```


#### [47]:


```python

# SKelに値をセット
skel.CreateJointsAttr().Set(joints)
skel.CreateJointNamesAttr().Set(jointsName)
skel.CreateRestTransformsAttr(jointTransforms)
skel.CreateBindTransformsAttr(jointTransforms)

```

!!! success
    ```




    Usd.Prim(</SkelRoot/Skeleton>).GetAttribute('bindTransforms')



    ```


#### [48]:


```python
stage.GetRootLayer().Export("D:/work/usd_py36/usd/createSkel.usda")

```

!!! success
    ```




    True



    ```