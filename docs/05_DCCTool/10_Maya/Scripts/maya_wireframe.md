---
title: Maya のビューポートの描画をワイヤーフレームにする
---

```python
import pymel.core as pm

def changeWireFrame():
    """
    強制的にワイヤーフレーム表示に変更
    """
    selectPanel = pm.getPanel(wf=True)
    if selectPanel is not None:
        if selectPanel.type() == "modelEditor":
            pm.modelEditor(selectPanel, e=True, da="wireframe")
            pm.refresh()
```
