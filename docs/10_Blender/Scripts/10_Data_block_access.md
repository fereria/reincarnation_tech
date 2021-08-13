# Data-Block をスクリプトから確認

<!-- SUMMARY:Data-Blockをスクリプトから確認 -->

![](https://gyazo.com/e91fda5afd2928d2bda150c867f73f29.png)

まず、BlenderFile に含まれている Data-Block の構造を UI 上で確認する。

![](https://gyazo.com/ed8929b8274400ac354a47634963e326.png)

Blend ファイル内の DataBlock はこのようになっている。

この Data-Block は、Maya でいうところの「ノード」が近い。  
Brushes や Cameras 等が、ノードの種類にあたり  
それぞれが、それぞれの機能を持っている。

## スクリプトからアクセスする

Blender の Data-Block は、 **bpy.types.BlendData** というクラスを継承した  
各 Data-BLock のクラスオブジェクトを利用してアクセスする。  
自分の取得したい Data-Block の BlendData オブジェクトを取得する場合は、

```python
# -*- coding: utf-8 -*-

import bpy
from mathutils import *
D = bpy.data
C = bpy.context

for i in D.objects:
    print(i)
```

bpy.data.<取得したい Data-Block>　このように書く。
タイプ名は
https://docs.blender.org/api/blender2.8/bpy.types.BlendData.html  
公式 Help の BlendData を確認。

## BlendData の構造

BlendData クラスは、

![](https://gyazo.com/e659bc446513a1a9a02fb9cc2cbd6919.png)

このような構造になっている。  
Data-Block の種類ごとに Class が存在しているので  
取得したい値や関係する Data-Block は  
指定のクラスのメソッドから取得できる。

### ID

この ID クラスは、すべての Data-Block の基本の型になっている。  
この ID が

- ユニークネーム
- 他ライブラリからのリンク
- ガベージコレクション

などの、BlendData のノードのリンク関係の管理をしている。

### 各 Data-Block

Object、Light、Mesh などの Data-Block は、BlendData - ID のクラスを継承している。  
Data-Block の数分クラスがあるので  
自分がアクセスしたいタイプのクラスのメソッドを  
確認することで、いろいろと操作できる。

## Blend ファイル内にある Mesh の情報を取得

Mesh アクセスは  
https://docs.blender.org/api/blender2.8/bpy.types.Mesh.html#bpy.types.Mesh  
ここにあるので、実際にアクセスしてみる。

```python
# -*- coding: utf-8 -*-

import bpy
from mathutils import *

D = bpy.data # Data-Blockの作成・取得は bpy.dataから。

for ob in D.objects:
    print(ob.type)

for i in D.meshes:  # bpy.types.bpy_prop_collection いわゆるData-Blockを取得用の配列
    print(i.name)
    print(i.users)
    # アサインされてるMaterialsを取得
    for mat in i.materials:
        print(mat)
    # 頂点取得
    print(i.vertices)
    # Edge取得
    print(i.edges)
```

## 参考

- https://qiita.com/kenyoshi17/items/b93bbba6451e3c6017e5
- http://sy.hatenablog.jp/entry/blender-python-basic
