---
title: mkdocsでのMarkdown記載サンプル
---
# mkdocsでのMarkdown記載サンプル

FootNoteのテスト [^1]

!!! note "ほげほげ"
    テスト
    
!!! info
    いんふぉ
    
!!! tip
    tip
    
!!! success
    Success

!!! example
    Example
    

```python
from pxr import Usd, UsdGeom, Sdf, Gf, OrigSchema

stage = Usd.Stage.CreateInMemory()
hogePrim = OrigSchema.ConcreteBasePrim.Define(stage,'/hoge')
stage.GetRootLayer().Export("I:/test.usda")
```


blockdiag {
    A -> B -> C -> D;
    A -> E -> F -> G;
}


[^1]:
    一番下に解説が追加される