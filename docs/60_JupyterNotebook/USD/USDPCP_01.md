---
title: PcpAPIでコンポジションアークを調べる
---
**ipynbFile** [USDPCP_01__PcpAPIでコンポジションアークを調べる.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/USDPCP_01__PcpAPIでコンポジションアークを調べる.ipynb)
#### [2]:


```python
from pxr import Usd,Pcp
```


#### [3]:


```python
stage = Usd.Stage.Open(r"D:\Kitchen_set\Kitchen_set.usd")
```


#### [4]:


```python
# PrimからIndexを取得し、PcpNodeRefを取得する
prim = stage.GetPrimAtPath("/Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1")
index = prim.GetPrimIndex()
index.DumpToDotGraph("D:/graph.dot")
rootRef = index.rootNode
print(rootRef)
```

!!! success
    ```

    <pxr.Pcp.NodeRef object at 0x00000252D7561608>
    

    ```


#### [30]:


```python
layerTree = layerStack.layerTree
# subLayerも木構造を取得できる
def traverse(node):
    print(node.layer)
    print(node.offset)
    for child in node.childTrees:
        print(child)
traverse(layerTree)
```

!!! success
    ```

    Sdf.Find('d:/Kitchen_set/Kitchen_set.usd')
    Sdf.LayerOffset()
    

    ```


#### [31]:


```python
# identifier経由でLayerを取得する場合
identifier = layerStack.identifier
print(identifier.rootLayer)
```

!!! success
    ```

    Sdf.Find('d:/Kitchen_set/Kitchen_set.usd')
    

    ```


#### [16]:


```python
# PrimIndexのPrimの子Prim,Propertyを取得
print(index.ComputePrimChildNames())
print(index.ComputePrimPropertyNames())
print(index.primStack)
print(index.hasAnyPayloads)
```

!!! success
    ```

    (['Geom'], [])
    ['xformOp:translate', 'xformOpOrder']
    []
    True
    

    ```


#### [12]:


```python
help(index)
```

!!! success
    ```

    Help on PrimIndex in module pxr.Pcp object:
    
    class PrimIndex(Boost.Python.instance)
     |  Method resolution order:
     |      PrimIndex
     |      Boost.Python.instance
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  ComposeAuthoredVariantSelections(...)
     |  
     |  ComputePrimChildNames(...)
     |  
     |  ComputePrimPropertyNames(...)
     |  
     |  DumpToDotGraph(...)
     |  
     |  DumpToString(...)
     |  
     |  GetSelectionAppliedForVariantSet(...)
     |  
     |  IsInstanceable(...)
     |  
     |  IsValid(...)
     |  
     |  PrintStatistics(...)
     |  
     |  __init__(...)
     |      Raises an exception
     |      This class cannot be instantiated from Python
     |  
     |  __reduce__ = <unnamed Boost.Python function>(...)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  hasAnyPayloads
     |  
     |  localErrors
     |  
     |  primStack
     |  
     |  rootNode
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Boost.Python.instance:
     |  
     |  __new__(*args, **kwargs) from Boost.Python.class
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from Boost.Python.instance:
     |  
     |  __dict__
     |  
     |  __weakref__
    
    

    ```


#### [6]:


```python
# EditTarget取得してTargetLayerに指定する
et = Usd.EditTarget(rootRef.layerStack.layers[0],rootRef)
stage.SetEditTarget(et)
```


#### [44]:


```python
# コンポジションを再帰で検索
def traverse(node):
    # コンポジションタイプ
    print(node.arcType) #CompositionArc
    print(node.path) #SdfPath
    print(node.site) #Layer + SdfPath
    print(node.GetRootNode()) # RootNode
    layer = node.layerStack.layers[0] # Layer取得
    print(layer)
    for child in node.children:
        traverse(child)
traverse(rootRef)
```

!!! success
    ```

    Pcp.ArcTypeRoot
    /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
    @d:/Kitchen_set/Kitchen_set.usd@,@anon:0000027614F5B360:Kitchen_set-session.usda@</Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1>
    <pxr.Pcp.NodeRef object at 0x00000276493A73A0>
    Sdf.Find('anon:0000027614F5B360:Kitchen_set-session.usda')
    Pcp.ArcTypeReference
    /Refridgerator
    @d:/Kitchen_set/assets/Refridgerator/Refridgerator.usd@</Refridgerator>
    <pxr.Pcp.NodeRef object at 0x00000276493A71E8>
    Sdf.Find('d:/Kitchen_set/assets/Refridgerator/Refridgerator.usd')
    Pcp.ArcTypeVariant
    /Refridgerator{modelingVariant=Decorated}
    @d:/Kitchen_set/assets/Refridgerator/Refridgerator.usd@</Refridgerator{modelingVariant=Decorated}>
    <pxr.Pcp.NodeRef object at 0x00000276493A7920>
    Sdf.Find('d:/Kitchen_set/assets/Refridgerator/Refridgerator.usd')
    Pcp.ArcTypePayload
    /Refridgerator
    @d:/Kitchen_set/assets/Refridgerator/Refridgerator_payload.usd@</Refridgerator>
    <pxr.Pcp.NodeRef object at 0x00000276493A7920>
    Sdf.Find('d:/Kitchen_set/assets/Refridgerator/Refridgerator_payload.usd')
    Pcp.ArcTypeReference
    /Refridgerator
    @d:/Kitchen_set/assets/Refridgerator/Refridgerator.geom.usd@</Refridgerator>
    <pxr.Pcp.NodeRef object at 0x00000276493A7710>
    Sdf.Find('d:/Kitchen_set/assets/Refridgerator/Refridgerator.geom.usd')
    Pcp.ArcTypeVariant
    /Refridgerator{modelingVariant=Decorated}
    @d:/Kitchen_set/assets/Refridgerator/Refridgerator.geom.usd@</Refridgerator{modelingVariant=Decorated}>
    <pxr.Pcp.NodeRef object at 0x0000027648AEAFA8>
    Sdf.Find('d:/Kitchen_set/assets/Refridgerator/Refridgerator.geom.usd')
    

    ```


#### [21]:


```python
# PcpNodeRefをGraphvizでビジュアライズ
index.DumpToDotGraph("D:/test.dot")
```

![](https://gyazo.com/5f2f50f295856a245262f85d87f65e9f.png)


#### [30]:


```python
# PcpNdoeRefをテキストでDump
print(index.DumpToString())
```

!!! success
    ```

    Node 0:
        Parent node:              NONE
        Type:                     root
        DependencyType:           root
        Source path:              </Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1>
        Source layer stack:       @d:/Kitchen_set/Kitchen_set.usd@,@anon:0000027614F5B360:Kitchen_set-session.usda@
        Target path:              <NONE>
        Target layer stack:       NONE
        Map to parent:
            / -> /
        Map to root:
            / -> /
        Namespace depth:          0
        Depth below introduction: 0
        Permission:               Public
        Is restricted:            FALSE
        Is inert:                 FALSE
        Contribute specs:         TRUE
        Has specs:                TRUE
        Has symmetry:             FALSE
    Node 1:
        Parent node:              0
        Type:                     reference
        DependencyType:           non-virtual, purely-direct
        Source path:              </Refridgerator>
        Source layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator.usd@
        Target path:              </Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1>
        Target layer stack:       @d:/Kitchen_set/Kitchen_set.usd@,@anon:0000027614F5B360:Kitchen_set-session.usda@
        Map to parent:
            /Refridgerator -> /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
        Map to root:
            /Refridgerator -> /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
        Namespace depth:          5
        Depth below introduction: 0
        Permission:               Public
        Is restricted:            FALSE
        Is inert:                 FALSE
        Contribute specs:         TRUE
        Has specs:                TRUE
        Has symmetry:             FALSE
    Node 2:
        Parent node:              1
        Type:                     variant
        DependencyType:           non-virtual, purely-direct
        Source path:              </Refridgerator{modelingVariant=Decorated}>
        Source layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator.usd@
        Target path:              </Refridgerator>
        Target layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator.usd@
        Map to parent:
            / -> /
        Map to root:
            /Refridgerator -> /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
        Namespace depth:          1
        Depth below introduction: 0
        Permission:               Public
        Is restricted:            FALSE
        Is inert:                 FALSE
        Contribute specs:         TRUE
        Has specs:                TRUE
        Has symmetry:             FALSE
    
    Node 3:
        Parent node:              1
        Type:                     payload
        DependencyType:           non-virtual, purely-direct
        Source path:              </Refridgerator>
        Source layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator_payload.usd@
        Target path:              </Refridgerator>
        Target layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator.usd@
        Map to parent:
            /Refridgerator -> /Refridgerator
        Map to root:
            /Refridgerator -> /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
        Namespace depth:          1
        Depth below introduction: 0
        Permission:               Public
        Is restricted:            FALSE
        Is inert:                 FALSE
        Contribute specs:         TRUE
        Has specs:                TRUE
        Has symmetry:             FALSE
    Node 4:
        Parent node:              3
        Type:                     reference
        DependencyType:           non-virtual, purely-direct
        Source path:              </Refridgerator>
        Source layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator.geom.usd@
        Target path:              </Refridgerator>
        Target layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator_payload.usd@
        Map to parent:
            /Refridgerator -> /Refridgerator
        Map to root:
            /Refridgerator -> /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
        Namespace depth:          1
        Depth below introduction: 0
        Permission:               Public
        Is restricted:            FALSE
        Is inert:                 FALSE
        Contribute specs:         TRUE
        Has specs:                TRUE
        Has symmetry:             FALSE
    Node 5:
        Parent node:              4
        Type:                     variant
        DependencyType:           non-virtual, purely-direct
        Source path:              </Refridgerator{modelingVariant=Decorated}>
        Source layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator.geom.usd@
        Target path:              </Refridgerator>
        Target layer stack:       @d:/Kitchen_set/assets/Refridgerator/Refridgerator.geom.usd@
        Map to parent:
            / -> /
        Map to root:
            /Refridgerator -> /Kitchen_set/Props_grp/North_grp/FridgeArea_grp/Refridgerator_1
        Namespace depth:          1
        Depth below introduction: 0
        Permission:               Public
        Is restricted:            FALSE
        Is inert:                 FALSE
        Contribute specs:         TRUE
        Has specs:                TRUE
        Has symmetry:             FALSE
    
    
    
    
    
    
    

    ```