---
title: ReferenceをしているPrimからUsdのFilePathを取得
---
**ipynbFile** [UsdReference1__ReferenceをしているPrimからUsdのFilePathを取得.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/UsdReference1__ReferenceをしているPrimからUsdのFilePathを取得.ipynb)
#### [18]:


```python

from pxr import Usd, UsdGeom, Sdf

sample_usd = "D:/work/usd_py36/usd/ref.usda"

stage = Usd.Stage.Open(sample_usd)

```


#### [19]:


```python

prim = stage.GetPrimAtPath("/ref")
# PrimがReferencによって定義されてるか
print(prim.HasAuthoredReferences())
# Primを構成するLayerを取得
print(prim.GetPrimStack())
for findLayer in prim.GetPrimStack():
    print(findLayer)
    # SdfPathを取得
    print(findLayer.path)
    # AssetPathを取得
    for ref in findLayer.referenceList.prependedItems:
        print(ref.assetPath)
        
```

!!! success
    ```

    True
    [Sdf.Find('d:/work/usd_py36/usd/ref.usda', '/ref'), Sdf.Find('d:/work/usd_py36/usd/testDD.usda', '/hogehoge')]
    Sdf.Find('d:/work/usd_py36/usd/ref.usda', '/ref')
    /ref
    D:/work/usd_py36/usd/testDD.usda
    Sdf.Find('d:/work/usd_py36/usd/testDD.usda', '/hogehoge')
    /hogehoge
    

    ```

GetPrimStackで得られる Sdf.Find は、Primを構成するPrimSpec？と  
その元になるAssetPathを取得できる。  
リファレンスで読み込んでいるPrimの場合、  
このFindで取得できるSdfPathは、Referenceの場合はReferenceで読み込んでるファイル内の  
SdfPath。  