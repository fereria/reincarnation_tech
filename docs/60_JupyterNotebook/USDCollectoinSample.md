---
title: USDCollectionの基本操作
---
#### [45]:


```python
from pxr import Usd, UsdGeom, Sdf, Gf, UsdUtils

newScn = Usd.Stage.CreateInMemory()

path = Sdf.Path("/World")
worldGeom = UsdGeom.Xform.Define(newScn, path)
sphereGeom = UsdGeom.Sphere.Define(newScn, path.AppendChild("Sphere"))
prim = worldGeom.GetPrim()
spherePrim = sphereGeom.GetPrim()

```


#### [46]:


```python

api = Usd.CollectionAPI.ApplyCollection(prim, 'test')
api.IncludePath(spherePrim.GetPath())

```

!!! success
    ```




    True



    ```


#### [47]:


```python
# expansionRule は explicitOnly(指定Pathを明確に指定？)
# expandPrims は rel-targets以下のすべてのPrim こっちがデフォルト
print(newScn.GetRootLayer().ExportToString())

```

!!! success
    ```

    #usda 1.0
    
    def Xform "World" (
        prepend apiSchemas = ["CollectionAPI:test"]
    )
    {
        uniform token collection:test:expansionRule = "expandPrims"
        prepend rel collection:test:includes = </World/Sphere>
    
        def Sphere "Sphere"
        {
        }
    }
    
    
    

    ```


#### [48]:


```python
collection = Usd.CollectionAPI.GetCollection(prim, 'test')
# Collection名取得
print(collection.GetName())
# CollectionまでのPathを取得
print(collection.GetCollectionPath())
# CollectionはRelation構造になってるので、ソレを利用してPrimを取得
print(collection.GetIncludesRel().GetTargets())
```

!!! success
    ```

    test
    /World.collection:test
    [Sdf.Path('/World/Sphere')]
    

    ```


#### [49]:


```python
# Getでも取得できるぽい
print(Usd.CollectionAPI.Get(prim, 'test'))

```

!!! success
    ```

    <pxr.Usd.CollectionAPI object at 0x0000000006CD5C48>
    

    ```