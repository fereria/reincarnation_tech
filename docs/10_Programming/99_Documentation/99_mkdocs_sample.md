---
title: mkdocsでのMarkdown記載サンプル
---

# mkdocs での Markdown 記載サンプル

FootNote のテスト [^1]

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

++ctrl+alt+delete++

:fa-external-link: [MkDocs](http://www.mkdocs.org/)

:smile:  
:fa-coffee:

==MARK TEST== hogehoge
~~sample~~

![](https://gyazo.com/42ff00b4fe5ad7bc8e1742cdad3aaafc.png)

- [ ] test
- [ ] check2
- [ ] check3

1. A
2. B
3. C
   1. D
   2. E
      1. F
      2. G

| table | A   | B   | C   |
| ----- | --- | --- | --- |
| あ    | い  | う  | え  |

## マクロを作る

{{ 'https://twitter.com/fereria/status/1164544426967875584'|twitter }}
{{ fontstyle('hoge',1.5,'#00ff00') }}

[^1]: 一番下に解説が追加される
