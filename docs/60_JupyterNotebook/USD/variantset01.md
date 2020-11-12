---
title: Variantの挙動を調べる_1
---
**ipynbFile** [variantset01__Variantの挙動を調べる_1.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/variantset01__Variantの挙動を調べる_1.ipynb)
#### [123]:


```python
from pxr import Usd,Sdf
```


#### [124]:


```python
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim("/VariantSet")
```


#### [125]:


```python
vset = prim.GetVariantSets().AddVariantSet('hogehoge')
vset.AddVariant('A')
vset.AddVariant('B')
vset.AddVariant('C')
print(vset)
```

!!! success
    ```

    <pxr.Usd.VariantSet object at 0x000002C0014160B8>
    

    ```


#### [126]:


```python
# VariantSetを取得
prim.GetVariantSets().GetNames()
```

!!! success
    ```




    ['hogehoge']



    ```


#### [127]:


```python
vset = prim.GetVariantSets().GetVariantSet("hogehoge")
vset.SetVariantSelection('A')
# 今選択されているものを表示
print(vset.GetVariantSelection())
# VariatnSetがあるPrimを取得
print(vset.GetPrim())
```

!!! success
    ```

    A
    Usd.Prim(</VariantSet>)
    

    ```


#### [128]:


```python
vset.SetVariantSelection('A')
with vset.GetVariantEditContext():
    # VariantSet「A」を選んでいる時には VariantSet/hoge というPrimができあがる
    childPrim = stage.DefinePrim(prim.GetPath().AppendChild("hoge"))
```


#### [129]:


```python
vset.SetVariantSelection('B')
with vset.GetVariantEditContext():
    childPrim = stage.DefinePrim(prim.GetPath().AppendChild("hogeB"))
    childPrim.GetReferences().AddReference(r"D:\work\usd_py36\usd\layerB.usda")
```


#### [130]:


```python
vset.SetVariantSelection('C')
with vset.GetVariantEditContext():
    prim.CreateAttribute("TEST",Sdf.ValueTypeNames.String).Set("HOGE")

```


#### [131]:


```python
print(stage.GetRootLayer().ExportToString())
```

!!! success
    ```

    #usda 1.0
    
    def "VariantSet" (
        variants = {
            string hogehoge = "C"
        }
        prepend variantSets = "hogehoge"
    )
    {
        variantSet "hogehoge" = {
            "A" {
                def "hoge"
                {
                }
    
            }
            "B" {
                def "hogeB" (
                    prepend references = @D:\work\usd_py36\usd\layerB.usda@
                )
                {
                }
    
            }
            "C" {
                custom string TEST = "HOGE"
    
            }
        }
    }
    
    
    

    ```


#### [132]:


```python
vset.SetVariantSelection('A')
print(stage.Flatten().ExportToString())
```

!!! success
    ```

    #usda 1.0
    (
        doc = """Generated from Composed Stage of root layer 
    """
    )
    
    def "VariantSet"
    {
        def "hoge"
        {
        }
    }
    
    
    

    ```


#### [133]:


```python
vset.SetVariantSelection('B')
print(stage.Flatten().ExportToString())
```

!!! success
    ```

    #usda 1.0
    (
        doc = """Generated from Composed Stage of root layer 
    """
    )
    
    def "VariantSet"
    {
        def "hogeB"
        {
        }
    }
    
    
    

    ```


#### [134]:


```python
vset.SetVariantSelection('C')
print(stage.Flatten().ExportToString())
```

!!! success
    ```

    #usda 1.0
    (
        doc = """Generated from Composed Stage of root layer 
    """
    )
    
    def "VariantSet"
    {
        custom string TEST = "HOGE"
    }
    
    
    

    ```


#### [135]:


```python
stage.GetRootLayer().Export("D:/test.usda")
```

!!! success
    ```




    True



    ```


#### [136]:


```python
prim.GetPrimStack()
```

!!! success
    ```




    [Sdf.Find('anon:000002C06682DA70:tmp.usda', '/VariantSet'),
     Sdf.Find('anon:000002C06682DA70:tmp.usda', '/VariantSet{hogehoge=C}')]



    ```


#### [138]:


```python
vset.SetVariantSelection('B')
a = stage.GetPrimAtPath("/VariantSet/hogeB")
print(a.GetPrimStack())
```

!!! success
    ```

    [Sdf.Find('anon:000002C06682DA70:tmp.usda', '/VariantSet{hogehoge=B}hogeB')]
    

    ```


#### [139]:


```python
spec = a.GetPrimStack()[0] #PrimSpecを取得できる
```


#### [140]:


```python
# PrimSpecからReferenceのUSDAは取得できるっぽい
for ref in spec.referenceList.prependedItems:
    print(ref.assetPath)
```

!!! success
    ```

    D:\work\usd_py36\usd\layerB.usda
    

    ```