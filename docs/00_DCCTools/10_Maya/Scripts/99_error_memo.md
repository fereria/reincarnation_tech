---
title: スクリプト関係の問題が起きたときの対処法
---

## PySide2 で Maya の MainWindow を取得したい

```python
from Qt import QtCompat
QtCompat.wrapInstance(～～～～～～)
```

shiboken2 だと ==You need a shiboken-based type.== エラーが出てしまう場合は  
QtCompat を使用すれば OK。

- http://discourse.techart.online/t/maya-2017-pyside-2-wrapinstance/6033/12
