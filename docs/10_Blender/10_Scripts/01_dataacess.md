---
title: BlenderPythonの基本(1) dataアクセス
---

```python
import bpy

print(bpy.data) # BlendData
```

## BlenderPythonの全体図

![](blenddata.drawio#0)

BlenderのAPIは、ざっくりと書き出すとこのようになっています。
まず、すべての親クラスとして bpy_struct があります。
これは、直接このクラスを使うことはなく、継承したクラスを介して使用します。

たとえば、そのオブジェクトがさすポインタ( as_pointer )であったり、
カスタムアトリビュート関連の関数などがこれにあたります。

そしてそれを継承して、WindowであったりBlendDataCollections、Node（NodeEditorのノードなど）といった
Blenderを構成する各クラスが作成されます。

その中で、DataBlock関係のクラスは[「ID」クラス](https://docs.blender.org/api/current/bpy.types.ID.html#bpy.types.ID)を継承して作成されています。
userの指定、ノード名、といったDataBlockに関連する関数やプロパティは
このIDにまとめられています。
そして、このIDを継承したクラスが、各Data Block用のクラスです。

こののDataは、bpy.data の BlendDataオブジェクトから取得できます。

```python
for obj in bpy.data.objects:
    print(obj)
```

```bat
<bpy_struct, Object("Camera") at 0x0000013851AF5608>
<bpy_struct, Object("Cube") at 0x0000013851AF4808>
<bpy_struct, Object("Light") at 0x0000013851AF4108>
```

### dataAPI

![](https://gyazo.com/964809b6cd36115714390c743401604a.png)

bpy.dataで取得できる値は、Blend-File Dataをみると構造がわかりやすいです。

例えば、 versionであれば

```python
print(bpy.data.version)
```
で、現在のバージョンのタプルを取得できます。

```python
print(bpy.data.meshes)
```

で、Meshを取得できます。
Mesh等は、bpy_collection という型になっていて、indexまたはNodeNameで取得できます。

```python
print(bpy.data.meshes['Cube'])
print(bpy.data.meshes[0])
```

### bpy.data.objectsから関係オブジェクトを探す

例えば、コンストレインのようにオブジェクトに対して指定されるような
設定を取得したい場合。

![](https://gyazo.com/aa2af9f49561659553dbe2e12e9b20f1.png)

```python
cube = bpy.data.objects['Cube']
# Objectから、Constraintオブジェクトを取得
for const in cube.constraints:
    print(const.name)
    targetObject = const.target
    print(targetObject.name)
```

Objectには、constraints があるので
これを利用して指定されたコンストレインオブジェクトを取得します。

[Constraint](https://docs.blender.org/api/current/bpy.types.Constraint.html#bpy.types.Constraint)のページを見ると、Blenderで対応しているConstraintの一覧があるので
プロパティや関数を使用すると、Pythonから取得したい値を取得することができます。

