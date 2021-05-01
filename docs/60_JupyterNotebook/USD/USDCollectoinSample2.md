---
title: USDCollection応用編
---
**ipynbFile** [USDCollectoinSample2__USDCollection応用編.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/USDCollectoinSample2__USDCollection応用編.ipynb)
#### [24]:


```python
from pxr import Usd,Sdf
```


#### [25]:


```python
stage = Usd.Stage.Open(r"D:\Kitchen_set\Kitchen_set.usd")
stage.Reload()
layer = stage.GetSessionLayer()

```


#### [26]:


```python
# テスト用の編集をSessionLayerに書く
target = stage.GetEditTargetForLocalLayer(layer)
stage.SetEditTarget(target)
```


#### [36]:


```python
# Collectionを作る
collection = stage.DefinePrim("/collectionSample")
prim = stage.GetPrimAtPath("/Kitchen_set/Props_grp/West_grp")
collectionName = "sampleCollection"
api = Usd.CollectionAPI.Apply(collection,collectionName)
print(api.GetName())
```

!!! success
    ```

    sampleCollection
    

    ```


#### [28]:


```python
# WestGrp以下をCollectionに入れる
api.IncludePath(prim.GetPath())
# ただしそのなかの SteamCooker_1 は除外
api.ExcludePath(Sdf.Path("/Kitchen_set/Props_grp/West_grp/SteamCooker_1"))
```

!!! success
    ```




    True



    ```


#### [29]:


```python
# ExpansionRuleとは、Collectionに入れているPrimの展開方法（Prim以下すべてなのかそれだけなのか）などを指定するもの。
expansionRule = api.CreateExpansionRuleAttr()
print(expansionRule)
# 取得
print(api.GetExpansionRuleAttr())

print(expansionRule.Get())
# explicitOnly/expandPrims/expandPrimsAndProperties
#expansionRule.Set("expandPrims")
expansionRule.Set("explicitOnly")
api.IncludePath("/Kitchen_set/Props_grp/West_grp/Ball_1")
```

!!! success
    ```

    Usd.Prim(</collectionSample>).GetAttribute('collection:sampleCollection:expansionRule')
    Usd.Prim(</collectionSample>).GetAttribute('collection:sampleCollection:expansionRule')
    expandPrims
    

    ```

!!! success
    ```




    True



    ```


#### [30]:


```python
# 条件に見合うPrimをStageから探す
query = api.ComputeMembershipQuery()
# emplicitOnlyだと、IncludePathに入れたPrimのみが検索対象
print(Usd.CollectionAPI.ComputeIncludedObjects(query,stage))
```

!!! success
    ```

    [Usd.Prim(</Kitchen_set/Props_grp/West_grp>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/Ball_1>)]
    

    ```


#### [33]:


```python
# ExpansionRuleを変えてみる
expansionRule.Set("expandPrims")
queryB = api.ComputeMembershipQuery()
# expandPrimsで指定されてるので、IncludePath以下にありExcludeに含まれないPrimがリストされる
print(Usd.CollectionAPI.ComputeIncludedObjects(queryB,stage))
```

!!! success
    ```

    [Usd.Prim(</Kitchen_set/Props_grp/West_grp>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/Ball_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/Ball_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/Ball_1/Geom/Ball>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/BottleTall_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/BottleTall_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/BottleTall_1/Geom/Bottle>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookBlue_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookBlue_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookBlue_1/Geom/Book>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookBlue_1/Geom/pCube134>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookGreen_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookGreen_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookGreen_1/Geom/Book>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookGreen_1/Geom/pCube134>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookGreen_2>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookGreen_2/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookGreen_2/Geom/Book>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookGreen_2/Geom/pCube134>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookTan_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookTan_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookTan_1/Geom/Book>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookTan_1/Geom/pCube134>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookTan_2>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookTan_2/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookTan_2/Geom/Book>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BookTan_2/Geom/pCube134>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BreadBag_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BreadBag_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/BreadBag_1/Geom/Bread>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube371>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube372>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube373>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube374>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube375>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube376>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube377>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube378>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube379>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube380>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube381>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube382>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube383>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube385>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube386>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube387>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube388>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube389>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube390>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube391>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube392>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube393>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube394>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube395>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube396>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube397>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube398>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group6/pCube399>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube371>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube372>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube373>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube374>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube375>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube376>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube377>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube378>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube379>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube380>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube381>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube382>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube383>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube385>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube386>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube387>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube388>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube389>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube390>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube391>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube392>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube393>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube394>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube395>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube396>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube397>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube398>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/group7/pCube399>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/pCube413>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/pCube414>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/pCube415>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/pCube70>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/FoldingTable_1/Geom/pCube76>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_1/Geom/pCube615>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_1/Geom/pCylinder316>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_2>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_2/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_2/Geom/pCube615>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_2/Geom/pCylinder316>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_3>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_3/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_3/Geom/pCube615>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrownDirty_3/Geom/pCylinder316>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrown_2>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrown_2/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrown_2/Geom/pCube615>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrown_2/Geom/pCylinder316>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrown_3>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrown_3/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrown_3/Geom/pCube615>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/HangerLightBrown_3/Geom/pCylinder316>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/IronWire>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/IronWire/pCube618>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/IronWire/pCylinder350>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/IronWire/pPipe31>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/pCylinder348>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/pCylinder349>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/pPipe30>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/pPlane338>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/pPlane339>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/FoldingTable_grp/Iron_1/Geom/pPlane340>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/HangerLightBrown_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/HangerLightBrown_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/HangerLightBrown_1/Geom/pCube615>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/HangerLightBrown_1/Geom/pCylinder316>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard/pPipe29>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard/polySurface78>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard/polySurface79>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard1/pPipe29>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard1/polySurface78>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard1/polySurface79>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard1/polySurface94>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/HandleIronBoard1/polySurface95>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder326>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder328>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder333>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder334>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder335>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder336>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder338>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder339>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder340>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pCylinder341>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pPlane311>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pPlane312>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pPlane314>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pPlane316>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pPlane318>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pPlane326>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/IronBoard_1/Geom/IroningBoard/pPlane327>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/PaperBagCrumpled_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/PaperBagCrumpled_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/PaperBagCrumpled_1/Geom/GroceryBag>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/ShellLarge_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/ShellLarge_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/ShellLarge_1/Geom/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/StoolMetalWire_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/StoolMetalWire_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/StoolMetalWire_1/Geom/Ball1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/StoolMetalWire_1/Geom/Ball1/polySurface91>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/StoolMetalWire_1/Geom/Ball1/polySurface92>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/StoolMetalWire_1/Geom/Ball1/polySurface93>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/StoolMetalWire_1/Geom/chair_top_polySurface1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/StoolMetalWire_1/Geom/polySurface63>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/TinCanA_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/TinCanA_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/TinCanA_1/Geom/TinCan>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/TinCanA_2>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/TinCanA_2/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/TinCanA_2/Geom/TinCan>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/FramePictureB_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/FramePictureB_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/FramePictureB_1/Geom/FramePicture>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/FramePictureD_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/FramePictureD_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/FramePictureD_1/Geom/FramePicture>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/FramePictureOval_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/FramePictureOval_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/FramePictureOval_1/Geom/FramePictureOval>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/PaperLarge_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/PaperLarge_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/PaperLarge_1/Geom/PaperLarge>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/PaperSmall_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/PaperSmall_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/PaperSmall_1/Geom/PaperSmall>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/ShellSmall_1>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/ShellSmall_1/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/ShellSmall_1/Geom/ShellSmall>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/ShellSmall_2>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/ShellSmall_2/Geom>), Usd.Prim(</Kitchen_set/Props_grp/West_grp/WestWall_grp/ShellSmall_2/Geom/ShellSmall>)]
    

    ```


#### [35]:


```python
# 引数で指定したSdfPathがCollectionに含まれるか
print(queryB.IsPathIncluded("/Kitchen_set/Props_grp/West_grp/ShellLarge_1"))
# Collectionより親のPrim
print(queryB.IsPathIncluded("/Kitchen_set"))
# Excludeに指定されているPrim以下
print(queryB.IsPathIncluded("/Kitchen_set/Props_grp/West_grp/SteamCooker_1/Geom/pCylinder55"))
```

!!! success
    ```

    True
    False
    False
    

    ```


#### [10]:


```python
print(expansionRule.Get())
```

!!! success
    ```

    expandPrims
    

    ```


#### [11]:


```python
# CollectionにセットされているPrimを取得
# CollectionはRelationで指定されている
print(api.GetExcludesRel().GetTargets())
print(api.GetIncludesRel().GetTargets())
```

!!! success
    ```

    [Sdf.Path('/Kitchen_set/Props_grp/West_grp/SteamCooker_1')]
    [Sdf.Path('/Kitchen_set/Props_grp/West_grp'), Sdf.Path('/Kitchen_set/Props_grp/West_grp/Ball_1')]
    

    ```


#### [12]:


```python
# どういうルールでQueryされるか確認
print(query.GetAsPathExpansionRuleMap())
```

!!! success
    ```

    {Sdf.Path('/Kitchen_set/Props_grp/West_grp'): 'explicitOnly', Sdf.Path('/Kitchen_set/Props_grp/West_grp/Ball_1'): 'explicitOnly', Sdf.Path('/Kitchen_set/Props_grp/West_grp/SteamCooker_1'): 'exclude'}
    

    ```


#### [13]:


```python
# APIで指定されているCollectionのPath
print(api.GetCollectionPath())
```

!!! success
    ```

    /collectionSample.collection:sampleCollection
    

    ```


#### [37]:


```python
# MultipleApplyのテスト
# とりあえず空のPrimを作る。もちろんCollectionAPIは適応されていない。
collectionB = stage.DefinePrim("/collectionB")
print(collection.HasAPI(Usd.CollectionAPI))
print(collectionB.HasAPI(Usd.CollectionAPI))
```

!!! success
    ```

    True
    False
    

    ```


#### [15]:


```python
# 同じPrimに対して別のCollectionを指定
api.Apply(collectionB,'sampleCollectionA')
```

!!! success
    ```




    Usd.CollectionAPI(Usd.Prim(</collectionB>), 'sampleCollectionA')



    ```


#### [16]:


```python
# Primに対してAPIがあるかどうかをチェック
stage.GetPrimAtPath("/collectionB").HasAPI(Usd.CollectionAPI)
```

!!! success
    ```




    True



    ```


#### [22]:


```python
# 結果を確認
print(layer.ExportToString())
```

!!! success
    ```

    #usda 1.0
    
    def "collectionSample" (
        prepend apiSchemas = ["CollectionAPI:collectionName"]
    )
    {
        prepend rel collection:sampleCollection:excludes = </Kitchen_set/Props_grp/West_grp/SteamCooker_1>
        uniform token collection:sampleCollection:expansionRule = "expandPrims"
        prepend rel collection:sampleCollection:includes = [
            </Kitchen_set/Props_grp/West_grp>,
            </Kitchen_set/Props_grp/West_grp/Ball_1>,
        ]
    }
    
    def "collectionB" (
        prepend apiSchemas = ["CollectionAPI:sampleCollectionA"]
    )
    {
    }
    
    
    

    ```