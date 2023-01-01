---
title: Propertyを追加する
tags:
    - Blender
    - Python
---

Blender では、Mesh や Camera、Material 等プロジェクトを構成するデータは Data Block と呼ばれる単位で
扱われます。

![](https://gyazo.com/c596e05e454798da8f0235c9f1717182.png)

そのデータは、 Data API で確認することができて、各 Type 以下に Data-Block があります。

![](https://gyazo.com/248a76bb844e0de867ad3535a9304c27.png)

たとえば、Objects の場合。
Objects 以下にはプロジェクトに含まれる Objects の Data-Block があります。

![](https://gyazo.com/62adceeb8aa4db2e00e3b41b814efe05.png)

この Data-block に、この DataType を構成するための Property があります。

Blender ではこの Data-block を Add-on で拡張することができて
何かしら処理を実行したい場、Property を指定し
GUI から変更するできるようにパネルを用意することで、様々なツールを作ることができます。

## Property を追加する

### 基本

Data-Block は、プログラミング的に言うとクラスのインスタンスのようなもので
指定の型（bpy.types ) をひな形として作成されるオブジェクトです。

```python
bpy.types.Object.hoge = bpy.props.IntProperty()
```

:fa-external-link: [Types(bpy.types)](https://docs.blender.org/api/current/bpy.types.html)を確認すると、types の中に ID を継承した型があるのがわかります。
これらが、Data-Block の元になるタイプなので、
拡張する場合は、この bpy.types に指定の名前の property を用意し、作成したい型の :fa-external-link: [Property Definitions (bpy.props)](https://docs.blender.org/api/current/bpy.props.html) を代入します。

![](https://gyazo.com/723d784055e4a83edb06a3b3acae3ea9.png)

ObjectType に対して hoge の IntProperty を追加しました。

```python
# 代入
 bpy.data.objects[0].hoge = 100
 # 取得
 print(bpy.data.objects[0].hoge)
```

types に追加されると、Data-Block に Property が追加され、取得したり代入したりすることが可能になります。

### ある Data-Block への参照

Property には、Int や Float のような値以外に
別の Data-Block への参照を定義することができます。
（Object への Data 指定、Material の Assing 情報なども同様の方法で定義されています）

```python
bpy.types.Object.sample = bpy.props.PointerProperty(type=bpy.types.Material)
```

PointerProperty は、指定の Type を指定すると
その Type の Data-Block を指定できるようになります。

![](https://gyazo.com/2a97ca84a54dbe4d41ed057e9bc0e52d.png)

PointerProperty を定義すると、このように特定の Type への接続口が作成されます。

```python
bpy.data.objects[0].sample = bpy.data.materials[0]
```

その作成した PointerProperty に、指定の Type の Data-Block を代入すると

![](https://gyazo.com/f654a92d1056a6401e39d3d3900f7eef.png)

リンクが作成できました。

![](https://gyazo.com/b19b93325fc40974ae113a606d00f161.png)

Property から、指定の Data-Block を取得できました。

## PropertyGroup

最後に、PropertyGroup を使用すると、Property を１つの構造体として定義することができます。

```python
class PropGroup(bpy.types.PropertyGroup):
    # PropetyGroupを追加
    my_int: bpy.props.IntProperty()
    my_float: bpy.props.FloatProperty()
    my_string: bpy.props.StringProperty()
```

作成するには、bpy.types.PropertyGroup を継承したクラスに
クラス変数として Property を定義します。
( : は Python3 の型指定をするためのもの)

```python
bpy.types.Material.my_settings = bpy.props.PointerProperty(type=PropGroup)
```

そして、追加したい Type に対して POinterProperty で PropertyGroup を追加します。

![](https://gyazo.com/19e6ba3fd10950117e477b6228157f8f.png)

```python
bpy.data.materials[0].my_settings.my_int = 10
```

PropertyGroup を作成すると、このように groupName.prop のような
グループ階層を追加することができます。

## Addon で追加する

Blender の Addon で追加する場合は

{{markdown_link('addProps')}} のように、 クラス定義と Property への登録処理をする構造を
作成すれば OK です。
