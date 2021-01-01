---
title: Variantの挙動を調べる_2
---
**ipynbFile** [variantset02__Variantの挙動を調べる_2.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/CompArc/variantset02__Variantの挙動を調べる_2.ipynb)
#### [23]:


```python
from pxr import Usd,Sdf
```


#### [24]:


```python
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim('/testPrim')
primB = stage.DefinePrim('/refPrim')

primB.CreateAttribute('refPrimAddAttr',Sdf.ValueTypeNames.String).Set('refPrim')
```

!!! success
    ```




    True



    ```


#### [25]:


```python
# VariantSetを定義する
vset = prim.GetVariantSets().AddVariantSet('hogehoge')
vset.AddVariant('hoge')
vset.AddVariant('fuga')
# 名前の取得
print(vset.GetName())
# VariantSetが設定されているPrimの取得
print(vset.GetPrim())
```

!!! success
    ```

    hogehoge
    Usd.Prim(</testPrim>)
    

    ```


#### [26]:


```python
# VarinatSetのリストを取得
print(prim.GetVariantSets().GetNames())
```

!!! success
    ```

    ['hogehoge']
    

    ```


#### [27]:


```python
# Variantで選択される値をセットする
# セットするときは設定したいVariantを選択状態にする
vset.SetVariantSelection('fuga')
with vset.GetVariantEditContext():
    # Variantが指定されたPrimに対してアトリビュートを追加定義
    vset.GetPrim().CreateAttribute('test',Sdf.ValueTypeNames.Bool).Set(True)
    # with内でPrimをDefineすると、このVarinat以下にPrimを追加できる
    childPath = vset.GetPrim().GetPath().AppendChild('hoge')
    cPrim = stage.DefinePrim(childPath)
```


#### [28]:


```python
vset.SetVariantSelection('hoge')
with vset.GetVariantEditContext():
    # Variantが指定されているPrimに対してReferenceを追加したい場合も
    # with 内でGetReference AddReferenceすることでReferenceを追加できる。
    # MEMO:同じレイヤー内のPrimをリファレンスする場合は AddInternalReference を使う。
    vset.GetPrim().GetReferences().AddInternalReference('/refPrim')
```


#### [29]:


```python
# 今の選択しているVariantNameを取得
print(vset.GetVariantSelection())
```

!!! success
    ```

    hoge
    

    ```


#### [30]:


```python
print(stage.GetRootLayer().ExportToString())
stage.GetRootLayer().Export("D:/test.usda")
```

!!! success
    ```

    #usda 1.0
    
    def "testPrim" (
        variants = {
            string hogehoge = "hoge"
        }
        prepend variantSets = "hogehoge"
    )
    {
        variantSet "hogehoge" = {
            "fuga" {
                custom bool test = 1
    
                def "hoge"
                {
                }
    
            }
            "hoge" (
                prepend references = </refPrim>
            ) {
    
            }
        }
    }
    
    def "refPrim"
    {
        custom string refPrimAddAttr = "refPrim"
    }
    
    
    

    ```

!!! success
    ```




    True



    ```