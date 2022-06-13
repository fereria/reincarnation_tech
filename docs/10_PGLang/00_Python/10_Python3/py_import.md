---
title: Import 関係の構造
---
# Import 関係の構造

Blender の Addon 基本構造を確認しつつ、  
Module 下にある.py ファイルのクラス本体のロードを出来るようにする。

```python
from pathlib import Path
# 自分のパス
print(Path(__file__))
# 自分のフォルダ
print(Path(__file__).parent)
```
