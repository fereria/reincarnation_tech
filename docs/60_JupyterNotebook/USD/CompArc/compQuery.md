---
title: UsdPrimCompositionQueryを使ってみる
---
**ipynbFile** [compQuery__UsdPrimCompositionQueryを使ってみる.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/CompArc/compQuery__UsdPrimCompositionQueryを使ってみる.ipynb)
#### [98]:


```python
from pxr import Usd
```


#### [99]:


```python
stage = Usd.Stage.Open(r"D:\Kitchen_set\Kitchen_set.usd")
```


#### [100]:


```python
prim = stage.GetPrimAtPath("/Kitchen_set/Props_grp/North_grp/SinkArea_grp/Sink_grp/BowlF_3")
```


#### [101]:


```python
# PCPを使うより、かんたんにコンポジションを取得できる
query = Usd.PrimCompositionQuery(prim)
```


#### [102]:


```python
# フィルタをかけてコンポジションを取得@リファレンスの場合
filter = Usd.PrimCompositionQuery.Filter()
filter.arcTypeFilter = Usd.PrimCompositionQuery.ArcTypeFilter.Reference # Variant / Payload でも可 デフォルトはAllになっている
query = Usd.PrimCompositionQuery(prim,filter)
```


#### [103]:


```python
# これでもOK
query = Usd.PrimCompositionQuery.GetDirectReferences(prim)
```


#### [104]:


```python
# コンポジションを取得
compArc = query.GetCompositionArcs()
for comp in compArc:
    print(comp.HasSpecs())
    print(comp.GetArcType())
    print(comp.GetIntroducingPrimPath())
    print(comp.GetIntroducingListEditor())
    print(comp.GetIntroducingLayer())
    print(comp.IsIntroducedInRootLayerStack())
    print(comp.GetIntroducingListEditor()[0])
    print("---")
```

!!! success
    ```

    True
    Pcp.ArcTypeReference
    /Kitchen_set/Props_grp/North_grp/SinkArea_grp/Sink_grp/BowlF_3
    (<pxr.Sdf.ListEditorProxy_SdfReferenceTypePolicy object at 0x0000013E4AF2C0F0>, Sdf.Reference('./assets/Bowl/Bowl.usd'))
    Sdf.Find('d:/Kitchen_set/Kitchen_set.usd')
    True
    { 'added': [SdfReference(./assets/Bowl/Bowl.usd, , SdfLayerOffset(0, 1), {})]'prepended': []'appended': [], 'deleted': [], 'ordered': [] }
    ---
    True
    Pcp.ArcTypeReference
    /Bowl
    (<pxr.Sdf.ListEditorProxy_SdfReferenceTypePolicy object at 0x0000013E4AF2C510>, Sdf.Reference('./Bowl.geom.usd', Sdf.Path('/Bowl')))
    Sdf.Find('d:/Kitchen_set/assets/Bowl/Bowl_payload.usd')
    False
    { 'added': [SdfReference(./Bowl.geom.usd, /Bowl, SdfLayerOffset(0, 1), {})]'prepended': []'appended': [], 'deleted': [], 'ordered': [] }
    ---
    

    ```