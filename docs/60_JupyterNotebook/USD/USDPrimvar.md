---
title: AttributeにPrimvarを指定する
---
**ipynbFile** [USDPrimvar__AttributeにPrimvarを指定する.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/USDPrimvar__AttributeにPrimvarを指定する.ipynb)
#### [116]:


```python
from pxr import Usd,UsdGeom,Sdf,Vt
```


#### [117]:


```python
stage = Usd.Stage.CreateInMemory()
```


#### [118]:


```python
prim = stage.DefinePrim("/testPrim")
```


#### [119]:


```python
attr = prim.CreateAttribute('hoge',Sdf.ValueTypeNames.Float)
```


#### [120]:


```python
# Attributeに対してPrimvarを設定
primvar = UsdGeom.Primvar(attr)
# 補間方法 constant/uniform/varying/vertex/faceVarying
primvar.SetInterpolation(UsdGeom.Tokens.varying)
```

!!! success
    ```




    True



    ```


#### [121]:


```python
primvar.Set(100,Usd.TimeCode(180))
primvar.Set(120,Usd.TimeCode(181))
```

!!! success
    ```




    True



    ```


#### [122]:


```python
print(stage.GetRootLayer().ExportToString())
```

!!! success
    ```

    #usda 1.0
    
    def "testPrim"
    {
        custom float hoge (
            interpolation = "varying"
        )
        float hoge.timeSamples = {
            180: 100,
            181: 120,
        }
    }
    
    
    

    ```


#### [123]:


```python
primvar.Get(180.8)
```

!!! success
    ```




    116.0



    ```


#### [124]:


```python
# IndexなしならGetとComputeFlattenedは同じになる？
primvar.ComputeFlattened(Usd.TimeCode(180.8))
```

!!! success
    ```




    116.0



    ```

PrimvarのGetは、TimeCodeでセットした値をバイリニア補間してくれる
（補間方法について）
* https://imagingsolution.net/imaging/interpolation/