# [cmds] Maya の SetProject をする

<!-- SUMMARY:cmds_MayaのSetProjectをする -->

```python
# -*- coding: utf-8 -*-

import maya.cmds as mc
import os


def set_project(path):
    """
    Mayaのプロジェクトを作成する
    """
    if os.path.exists(path) is False:
        os.makedirs(path)
    if os.path.exists(path + "/workspace.mel") is True:
        mc.workspace(path, openWorkspace=True)
    else:
        mc.workspace(path, openWorkspace=True)
        default_rules = {"scene": "scenes",
                        "images": "images",
                        "movie": "playblast",
                        "sourceImages": "sourceimages"}
        for key in default_rules:
            mc.workspace(fr=(key, default_rules[key]))
            if os.path.exists(os.path.join(path, default_rules[key])) is False:
                os.makedirs(os.path.join(path, default_rules[key]))
            mc.workspace(saveWorkspace=True)
        return path
```

プロジェクトセット自体は、

```
mc.workspace(path, openWorkspace=True)
```

で指定をすることが出来る。

しかし、
指定フォルダ以下の設定がされていない場合は、 scene や sourceimages などの  
サブフォルダは作成されないので、新規でプロジェクトを作りたい場合などは

```
mc.workspace(fr=(key, default_rules[key]))
```

このコマンドを使用して、追加をする必要がある。
![](https://gyazo.com/2cae6e476f298864e5120d2b7b11132b.png)
この場合の key は、ProjectSets 画面のパスを指定している文字の頭を小文字にしたもの。
