---
title: VSCodeでAddon開発
---

まず、事前に [VSCode の事前準備](00_vscode_settings.md)をしておきます。
そして、VSCode のワークスペースを作ります。

![](https://gyazo.com/b166d25f88ebee60d973d9c14e160727.png)

コマンドパレットから Blender: New Addon を選びます。

![](https://gyazo.com/695da395f575b9b3d88dadcc84f81d43.png)

Template は、With Auto Load を選びます。

![](https://gyazo.com/f721acc56876b5e14e87ce550853a855.png)

Addon の名前と

![](https://gyazo.com/c0dbb117c127358c705a7f36e41325ca.png)

名前を入れて、

![](https://gyazo.com/cb1ac1563b77fe47531d3353a7d7675c.png)

どこに Addon を作るか聞かれるので、現在のワークスペース以下を指定します。

![](https://gyazo.com/1c8cc72894009e1882e09b6df5afd277.png)

OpenFile は、 \_\_init\_\_.py を選びます。

```python
bl_info = {
    "name" : "SampleAddon",
    "author" : "MegumiAndo",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

from . import auto_load

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()
```

すると、 \_\_init\_\_.py に、 bl_info や、 register unregister の構造が
自動で作られます。

最初に auto_load.py を選んだ場合、現在のプロジェクト以下にある Python ファイルを自動で検索し、Addon 用のクラスが含まれている場合文字通り「自動で」ロードしてくれます。

試しに、プロジェクト以下に sampleUI.py を作り、

```python
import bpy


class samplePanel(bpy.types.Panel):
    bl_label = "SamplePanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SampleAddon"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello World!!!!")

```

中身をこのようにして保存します。

![](https://gyazo.com/3d22729f5c1bb1de63fcce033d2625ee.png)

保存したら、Blender:Start で Blender を起動します。

![](https://gyazo.com/114b537d4de97d4aa86ccf36bb147c47.png)

Blender を起動すると、先ほどの Addon は自動で AppData 以下にコピーされ
ロードされた状態になります。

![](https://gyazo.com/1118781771c2e6d7af01d7aa2c6b1c20.png)

無事 Addon がロードされ、先ほどの sampleUI にある SamplePanel が追加されました。

## 自動ロード

無事追加できましたが、編集するたびに Blender を再起動するのはめんどくさいです。
ので、ファイルを保存したら自動で Addon をリロードするようにしておきます。

![](https://gyazo.com/7b5e07b46be8e55a0012fe63109c665a.png)

VSCode の設定から、 Blender>Addon: Reload On Save をオンにしておきます。
ON にすると、ファイルが変更されるたびに Addon がリロードされ
Blender 側で確認をすることができます。

## デバッグ

VSCode から Start した場合、VSCode のデバッグ機能を使うことができます。

![](https://gyazo.com/44f6fbc967e0eb7baa463ec78480b9fe.png)

たとえば、ブレークポイントをセットした状態で適当に編集 → 保存します。
すると、ブレークポイント部分で止めることができました。
{{markdown_link('vscode_debug')}}

あとはこちらにあるとおり、VSCode の機能を使ってデバッグできます。

## まとめ

VSCode を使うと、Blender の Addon 開発も
だいぶ効率的に進められそうです。
