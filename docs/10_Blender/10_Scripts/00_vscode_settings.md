---
title: VSCodeでBlenderPython開発をしよう
tags:
    - Blender
    - Python
    - VSCode
---

## 設定

まずは、VSCodeのアドオンをインストールします。

![](https://gyazo.com/fc18c1c6c8756c0f91c517d747806c59.png)

インストールするのは、 Blender Development。

```json
  "blender.executables": [
    {
      "path": "d:\\blender-2.93.2-windows-x64\\blender.exe",
      "name": "",
      "isDebug": false
    }
  ]
```

インストールしたら、settings.json にBlenderのexeのパス指定を追加します。
複数のバージョンを使い分けたい場合は、 executables の中に
複数の設定を追加することができます。

## AutoComplete

![](https://gyazo.com/06c66f823ce7d571464ea82a028b0f47.png)

次にAutoCompleteをできるようにします。
BlenderのPythonと同じバージョンをインストールして、

```bat
pip install fake-bpy-module-2.93
```

使用するBlenderのバージョンの fake-moduleをpipを使用してインストールします。

![](https://gyazo.com/51d8c14566223cad172c78e5ce5c1cfb.png)

これでBlenderPtyhonのAutoCompleteができるようになります。

## 実行する

![](https://gyazo.com/6f602d0cd81bb4ef59a5ab2319edf295.png)

まず、Blender:Start を実行して、

![](https://gyazo.com/2a231244e6524113edd4edee4259031c.png)

実行するBlenderを選択します。

![](https://gyazo.com/d8d71c30d3d4ea709bf0350948f8420b.png)

すると、Blenderが起動して、
実行結果はVSCode側のコンソールに表示されるようになります。

![](https://gyazo.com/aaf5551fa13a9c238169ac3de3b5698b.png)

以降は、Run Script を実行することで
VSCode側でBlenderPtyhonのコードを実行できるようになります。

