---
title: Metadataを仕込む
---
**ipynbFile** [USDMetadata__Metadataを仕込む.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/USDMetadata__Metadataを仕込む.ipynb)
#### [67]:


```python
from pxr import Usd,Vt
```


#### [68]:


```python
stage = Usd.Stage.CreateInMemory()
layer = stage.GetRootLayer()
prim = stage.DefinePrim('/testPrim')
path = prim.GetPath()

layer.defaultPrim = '/testPrim'
```


#### [69]:


```python
# レイヤーに対して色々Metadataを入れる
layer.comment = 'hello world'
layer.documentation = 'docs'
layer.startTimeCode = 1
layer.endTimeCode = 30
```


#### [70]:


```python
# Primに対しても入れる
# 配列の場合は Vt.～～Arrayを使う必要あり。
prim.SetCustomDataByKey('value', 10) # Int
prim.SetCustomDataByKey('listdata',Vt.StringArray(['a','b','c']))
prim.SetCustomDataByKey('intlist',Vt.IntArray([1,2,3,4,5]))
prim.SetDocumentation('hello world')
```

!!! success
    ```




    True



    ```


#### [71]:


```python
# AttributeにもMetadataを入れられる
attr = prim.CreateAttribute('testAttr',Sdf.ValueTypeNames.String)
attr.Set('hoge')
# Attributeに対してもMetadataを仕込める
attr.SetCustomDataByKey('meta','data')
```


#### [72]:


```python
prim.GetAllMetadata()
```

!!! success
    ```




    {'customData': {'intlist': Vt.IntArray(5, (1, 2, 3, 4, 5)),
      'listdata': Vt.StringArray(3, ('a', 'b', 'c')),
      'value': 10},
     'documentation': 'hello world',
     'specifier': Sdf.SpecifierDef}



    ```


#### [73]:


```python
print(layer.ExportToString())
```

!!! success
    ```

    #usda 1.0
    (
        "hello world"
        defaultPrim = "/testPrim"
        doc = "docs"
        endTimeCode = 30
        startTimeCode = 1
    )
    
    def "testPrim" (
        customData = {
            int[] intlist = [1, 2, 3, 4, 5]
            string[] listdata = ["a", "b", "c"]
            int value = 10
        }
        doc = "hello world"
    )
    {
        custom string testAttr = "hoge" (
            customData = {
                string meta = "data"
            }
        )
    }
    
    
    

    ```