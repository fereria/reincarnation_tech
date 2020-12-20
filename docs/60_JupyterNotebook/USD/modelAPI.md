---
title: modelAPIとKind
---
**ipynbFile** [modelAPI__modelAPIとKind.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/modelAPI__modelAPIとKind.ipynb)
#### [36]:


```python
from pxr import Usd,Sdf
```


#### [2]:


```python
stage = Usd.Stage.CreateInMemory()
```


#### [9]:


```python
prim = stage.DefinePrim("/testPrim")
stage.SetDefaultPrim(prim)
```


#### [47]:


```python
# APIを取得する
Usd.ModelAPI.Get(stage,Sdf.Path('/testPrim'))
```

!!! success
    ```




    Usd.ModelAPI(Usd.Prim(</testPrim>))



    ```


#### [5]:


```python
# ModelAPI にPrimを渡してAPIを取得する
api = Usd.ModelAPI(prim)
```


#### [39]:


```python
# Primに対していろんなシーンに関連するMetadataを入れる
api.SetAssetName('testAsset')
api.SetAssetVersion('1.0')
api.SetAssetInfo({'test':'hello world',
                  'num':10,
                  'hoge':[10,11,12]})
```


#### [40]:


```python
# Kindを設定
api.SetKind('component')
```

!!! success
    ```




    True



    ```


#### [41]:


```python
print(api.IsKind('component'))
print(api.IsModel())
print(api.IsGroup())
```

!!! success
    ```

    True
    True
    False
    

    ```


#### [42]:


```python
print(stage.GetRootLayer().ExportToString())
```

!!! success
    ```

    #usda 1.0
    (
        defaultPrim = "testPrim"
    )
    
    def "testPrim" (
        assetInfo = {
             hoge = [10, 11, 12]
            int num = 10
            string test = "hello world"
        }
        kind = "component"
    )
    {
    }
    
    
    

    ```

## Kindを取得する方法


#### [48]:


```python
from pxr import Kind
```


#### [51]:


```python
# 登録されているKindを取得する
Kind.Registry().GetAllKinds()
```

!!! success
    ```




    ['charprop',
     'chargroup',
     'subcomponent',
     'model',
     'component',
     'group',
     'assembly',
     'newRootKind']



    ```


#### [52]:


```python
# Kindの階層構造を取得できる
Kind.Registry().GetBaseKind('component')
```

!!! success
    ```




    'model'



    ```


#### [54]:


```python
print(Kind.Registry().HasKind('hoge'))
print(Kind.Registry().HasKind('charprop'))
```

!!! success
    ```

    False
    True
    

    ```