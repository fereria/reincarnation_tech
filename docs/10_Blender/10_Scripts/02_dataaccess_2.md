---
title: BlenderPythonの基本(2) linkする
---

Blenderの各種データは、 Data API (ID?) という形で保存されています。

![](https://gyazo.com/f7631d7f21ca82e2f30c84ad2cad3c1b.png)

CurrentFile (.blend) 以下がこのようになっていて、これらのデータは
bpy_strunct - ID を継承したクラスによって管理されています。

このデータは、データどうしを「リンク」することで、親子関係やどれに何が属しているかなどをコントロールしているようです。

![](https://gyazo.com/0101015ed6c2fb5a17d1f4c94bbff1cc.png)

たとえばSceneの場合。

https://docs.blender.org/api/current/bpy.types.Scene.html#bpy.types.Scene

Sceneも、IDを継承したSceneクラスから扱います。

```python
scene = bpy.data.scenes['Scene']
```

なので、 bpy.data から取得可能です。

```python
print(scene.collection)
print(scene.camera)
print(scene.render)
```

```bat
<bpy_struct, Collection("Master Collection") at 0x00000214B6CB5808>
None
<bpy_struct, RenderSettings at 0x00000214B6CD0208>
```

必要な情報もここから取得します。

## シーンに対してオブジェクト等を追加

例えば、シーンに対してCollectionを追加したい場合。
この場合は、DataAPI側にCollectionを作成し、作成したCollectionをSceneに対してリンクする必要があります。

![](https://gyazo.com/666a70b8694b4f5f21be30f7b5163a62.png)

```python
bpy.ops.collection.create(name='hoge')
col = bpy.data.collections['hoge']
```

Operatorを使用してCollectionを作成するとDataAPIにCollectionが追加されます。

![](https://gyazo.com/e0859f5a034876f569cd71766ae272f8.png)

```python
col = bpy.data.collections['hoge']
scene.collection.children.link(col)

```

その追加したCollectionを指定のSceneに追加する場合は、
このように、SceneのCollectionの子供にCollectionを「リンク」します。

### さらに子どもにCollectionを追加

![](https://gyazo.com/e96cb60241ff8e3503373c7c3cda9058.png)

```python
bpy.ops.collection.create(name='childCollections')
child = bpy.data.collections['childCollections']
col.children.link(child)
```

さらに子供にCollectionを追加する場合なども同様です。
追加したい親Collectionに対してリンクすれば、同様に親子化をつくることができます。

### Objectの場合(追加、削除、取得)

```python
cube = bpy.data.objects['Cube']
bpy.data.collections['hoge'].objects.link(cube)
```

オブジェクトの場合も、基本の考え方は同じです。
追加したいCollectionのobjects に対して、追加したいObjectを「リンク」します。

```python
print([x for x in child.objects])
```
```bat
[bpy.data.objects['Cube'], bpy.data.objects['Light'], bpy.data.objects['Camera']]
```

オブジェクトを取得したい場合は、このようにします。

```python
cube = bpy.data.objects['Cube']
bpy.data.collections['hoge'].objects.unlink(cube)
```

削除したい場合は、unlinkでOKです。

## まとめ

各Dataは、IDから継承されたクラスでアクセスが可能。
そして、それぞれを接続したい場合は、どのDataも link / unlink すれば構築することができます。