---
title: Operator と Context
---

Blenderでは、「Operator」と呼ばれるPythonやC等で書かれたコマンドにアクセスするための
機能があります。

https://docs.blender.org/api/current/bpy.ops.html

デフォルトでは bpy.ops～ で使用することができて、SubModuleとして
Blenderのオブジェクトを作成したり、ファイルにアクセスしたりといった各種機能を提供しています。

たとえば、FileをExportしたい場合。
https://docs.blender.org/api/current/bpy.ops.export_scene.html
Export Scene Operator に fbx関数が用意されています。

```python
bpy.ops.export_scene.fbx(filepath='D:/sample.fbx')
```

これを利用すると、シーンのオブジェクトをFBXでExportすることができます。

## AddonでOperatorを自作する

このOperatorは自分で自作することができます。
作成するときは、 bpy.types.Operatorを継承したクラスを作成して、
registerをします。（そのあたりは [前回](03_vscode_addon_dev.md)参考に。）

```python
import bpy


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        print(context.active_object)
        return {'FINISHED'}
```

作成するのに、最低限必要なのが、execute 関数です。
ともに contextを引数に受け取ります。

このContextとは、
https://docs.blender.org/api/current/bpy.context.html
Blenderの各種情報を取得するための読み取り専用オブジェクトです。
つまり、OperatorはこのContextを介して、Blenderからの情報を受け取ります。

上のサンプルを実際に実行する場合。

```python
bpy.ops.object.simple_operator()
```

bl_idname が、Pythonでの関数名と一致します。
なので、上のように実行すると、 execute が実行されて、 ActiveObjectがプリントされます。

### 引数を受け取る

Operatorに引数を渡したい場合は、executeに引数を追加するのではなく
Propertyを作成します。

```python
import bpy


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    sampleProps: bpy.props.StringProperty(
        default="Sample",
        name="Sample Property"
    )

    def execute(self, context):
        print(self.sampleProps)
        return {'FINISHED'}
```

実行時は
```python
 bpy.ops.object.simple_operator(sampleProps="hoge")
```
作成したPropertyを、呼び出し時の関数の引数で渡します。

### エラーチェック

次に、この execute が実行可能かどうかを事前に判定するのが poll 関数です。

```python
    @classmethod
    def poll(cls, context):
        # エラーになる条件を書く
        return context.active_object is not None
```

このようにして、このOperatorが実行可能かどうかチェックをして、
Trueの場合例外をだします。

## Copy Context

OperatorのContextは、デフォルトだと 読み取り専用の bpy.context になりますが、
そうではなく、コピーしたContextを引数渡して処理をすることができます。

例えば、 context.active_object をプリントするOperatorを作成した場合、

![](https://gyazo.com/4ffcffa518f000cf4c9c97f3738334eb.png)

active_object が Cubeならば、

![](https://gyazo.com/fa31ce5519855063fb1d8725ce71ba83.png)

Cubeになります。

```python
over = bpy.context.copy()
over['active_object'] = bpy.data.objects['Camera']
bpy.ops.object.simple_operator(over)
```

それを、Contextを複製して、該当の値を書き換えたコピーContextを作成し
作成したContextをOperatorの引数として渡します。

![](https://gyazo.com/a61c884c0a2b002411581f1f0039437b.png)

すると、現在のactive_objectを書き換えることなく処理をすることができます。

## まとめ

これで、Operatorの基本構造と作り方がわかりました。
あとは、カスタムGUIからこのOperatorを呼び出せるようにすれば
BlenderのAddonをいろいろ作ることができます。

Contextまわりが当初よくわからなくて、
「なんで選択中のオブジェクトを書き換えるだけでこんなめんどくさいんだ...」
と思いましたが、OperatorとPropertyと、実行部分などが理解できれば
割とわかりやすいかな？と思いました。