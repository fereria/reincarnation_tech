# Blender のマテリアルノードを作成する（1）

<!-- SUMMARY:Blenderのマテリアルノードを作成する（1） -->

Blender のノードエディタにメモを書けるノードが欲しいなぁと思ったけど  
2.80 に対応しているのが見つからなかったので、  
Blender のスクリプト勉強がてら調べつつ作って見ることにしました。  
まずは、実際に作る前段階の最小の構成はどうすれば良いのかからチェックしていきます。

## Template を確認してざっくり把握

![](https://gyazo.com/89b88e40d5d6410de36d399727a7db08.png)

Scripts 内の Template で、CustomNodes を表示すると、  
ノードを作成するスクリプトテンプレートが表示されます。  
が...Materials じゃないパネルを新規で作ってからそこにノードを追加するスクリプトだったので  
そこからいらない所をけして、Materials に追加するための最小コードをつくってみました。

## スクリプト本体

```python
# -*- coding: utf-8 -*-
"""
BlenderのMaterialsノードを自作する時の最小構成
"""


import bpy
from bpy.types import  Node
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# Add-onsのロード時に表示される情報
bl_info = {
    "name": "test_simple_Node",
    "author": "megumi ando",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Generic"
}
# ノード作成
class MyCustomNode(Node):

    bl_idname = 'SimpleCustomNode'
    bl_label  = "Simple Custom Node"
    bl_icon   = 'SOUND'


# NodeEditorの追加メニューにノードを作成するメニューを追加する。
node_categories = [
    NodeCategory('OTHERNODES', 'Other Nodes', items=[NodeItem("SimpleCustomNode", label="Node A")])
]

# Pluginsを登録する処理

classes = (MyCustomNode,)

def register():
    from bpy.utils import register_class
    print(classes)
    for cls in classes:
        print(cls)
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
```

以上。

Blender の Addons スクリプトは大きく分けて 3 つのタームがあります。  
1 つが、Addons 画面にある情報を登録する部分
2 つが、指定のクラスを継承して、実装する部分
最後が、プラグインを Blender に登録する部分

## Addons 画面の情報を登録する

![](https://gyazo.com/7c316ce2b06cbb5edf6bb568343de554.png)

まず、Add-ons 画面内に表示されるプラグイン名や説明などは  
.py ファイルの Globals 変数で「bl_info」を定義する。

```python
bl_info = {
    "name": "test_simple_Node",
    "author": "megumi ando",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Generic"
}
```

この情報はあくまで Add-ons 内に表示されるものなので、  
以降のコードとは関係ない。  
blender で指定するバージョンが、読み込む Blender のバージョンと同じ出ないと  
エラーになるので注意。

## カスタムノードを作る

```python
class MyCustomNode(Node):

    bl_idname = 'SimpleCustomNode'
    bl_label  = "Simple Custom Node"
    bl_icon   = 'SOUND'
```

ノードを作りたいときは、指定のクラス（Node）を継承して  
クラスを作成する。

定義している変数は、  
bl_idname は Blender 内で使用する ID 名。  
Blender の各コマンドはクラス名ではなくこの id_name を使用してアクセスする。  
ので、基本ユニークなものにする。  
bl_label は表示上の名前。  
Node の場合は NodeEditor に表示される名前はここで指定した物になる。  
icon は、ノード上に表示されるアイコン。

## Blender に登録する

### メニューへの登録

2.80 とそれ以前だと登録するタームは大きく変わっている模様。

```python
# NodeEditorの追加メニューにノードを作成するメニューを追加する。
node_categories = [
    NodeCategory('OTHERNODES', 'Other Nodes', items=[NodeItem("SimpleCustomNode", label="Node A")])
]
```

まず、作成したノードを Materials 内の Add メニューに追加する。  
追加するための処理は、==nodeitems_utils==でいいかんじにラクに出来るようにしてくれているので  
コレを使用する。

引数は、1 つめは登録用の ID、2 つめがカテゴリ名、items が、実際に登録するノード。

![](https://gyazo.com/f646082a3d1b3fa3da1853eb07798424.png)

NodeCategory でカテゴリ追加、そのカテゴリ内に items 引数にある NodeItem を追加  
その配列を、register 関数内でまとめて登録・削除する。

### ロード・アンロード処理

最後にロード・アンロード時の処理を定義をする。

```python

classes = (MyCustomNode,)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
```

register_class が、作成したノード本体の登録を行う。  
その後の、メニューに登録する部分が　 nodeitems_utils.register_node_categories。  
unregister はその逆処理になっている。

注意点が、classes をタプルで記入しているが、末に , が入っていないと  
配列扱いにならず、==for cls in classes:== 部分でエラーになった。

![](https://gyazo.com/32753e2dd906b5a3ba504564105b1c72.png)

プラグインをロードして、ノードを作成してみた結果。  
とくにプラグをつくったわけえはないので、ただの箱ができあがった。

## まとめ

プラグインの基本的な構造や、クラスの作り方が理解出来た（はず）  
次は、実際の中の処理を作ってみようかと思います。
