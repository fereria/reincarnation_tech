---
title: USDでアニメーション
---
**ipynbFile** [animation__USDでアニメーション.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/animation__USDでアニメーション.ipynb)
# USDでTransform/Rotateのアニメーション


#### [39]:


```python
from pxr import Usd,UsdGeom,Gf,Sdf
```


#### [18]:


```python
stage = Usd.Stage.CreateInMemory()
stage.SetStartTimeCode(1)
stage.SetEndTimeCode(30)
```


#### [19]:


```python
UsdGeom.Xform.Define(stage,"/sampleXform")
UsdGeom.Cube.Define(stage,"/sampleXform/Cube")
```

!!! success
    ```




    UsdGeom.Cube(Usd.Prim(</sampleXform/Cube>))



    ```


#### [20]:


```python
prim = stage.GetPrimAtPath("/sampleXform")
```


#### [21]:


```python
api = UsdGeom.XformCommonAPI(prim)
```


#### [35]:


```python
UsdGeom.XformCommonAPI.RotationOrderXYZ
```

!!! success
    ```




    UsdGeom.XformCommonAPI.RotationOrderXYZ



    ```


#### [36]:


```python
# アニメーションのキーを作る
api.SetTranslate(Gf.Vec3d(0,0,0),1)
api.SetTranslate(Gf.Vec3d(0,10,0),30)
api.SetRotate(Gf.Vec3f(0,0,0),UsdGeom.XformCommonAPI.RotationOrderXYZ,1)
api.SetRotate(Gf.Vec3f(0,0,360),UsdGeom.XformCommonAPI.RotationOrderXYZ,30)
```

!!! success
    ```




    True



    ```


#### [52]:


```python
# 自分で作ったアトリビュート
attr = prim.CreateAttribute("sample",Sdf.ValueTypeNames.Int)
for i in range(1,30):
    attr.Set(i,i)
```


#### [53]:


```python
print(stage.GetRootLayer().ExportToString())
```

!!! success
    ```

    #usda 1.0
    (
        endTimeCode = 30
        startTimeCode = 1
    )
    
    def Xform "sampleXform"
    {
        custom int sample
        int sample.timeSamples = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            11: 11,
            12: 12,
            13: 13,
            14: 14,
            15: 15,
            16: 16,
            17: 17,
            18: 18,
            19: 19,
            20: 20,
            21: 21,
            22: 22,
            23: 23,
            24: 24,
            25: 25,
            26: 26,
            27: 27,
            28: 28,
            29: 29,
            30: 30,
        }
        float3 xformOp:rotateXYZ.timeSamples = {
            1: (0, 0, 0),
            30: (0, 0, 360),
        }
        double3 xformOp:translate.timeSamples = {
            1: (0, 0, 0),
            30: (0, 10, 0),
        }
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ"]
    
        def Cube "Cube"
        {
        }
    }
    
    
    

    ```


#### [54]:


```python
stage.GetRootLayer().Export("D:/animSample.usda")
```

!!! success
    ```




    True



    ```