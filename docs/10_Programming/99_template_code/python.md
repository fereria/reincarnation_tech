---
title: Python
---

## PySide

### 基本構造

```python
# -*- coding: utf-8 -*-

import os.path
import sys

from PySide2.QtWidgets import QApplication, QDialog, QTreeView, QVBoxLayout


class UISample(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = UISample()
    a.show()
    sys.exit(app.exec_())

```