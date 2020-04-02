---
title: USDEditTarget_EditTargetで指定レイヤーを操作
---
**ipynbFile** [USDEditTarget_EditTargetで指定レイヤーを操作.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/USDEditTarget_EditTargetで指定レイヤーを操作.ipynb)
hoge

Root - layerA - layerB のようなサブレイヤー構成で  
各レイヤーを取得する方法とかテスト。


#### [1]:


```python

from pxr import Usd, UsdGeom, Sdf

```


#### [2]:


```python
Usd.StageCache().Clear()
stage = Usd.Stage.Open(r"D:\work\usd_py36\usd\rootLayer.usda")
# RootLayerのターゲット取得

```


#### [3]:


```python
# レイヤー取得

layers = stage.GetUsedLayers()
print(layers)

```

!!! success
    ```

    [Sdf.Find('d:/work/usd_py36/usd/layerA.usda'), Sdf.Find('anon:000001C85E39D3E0:rootLayer-session.usda'), Sdf.Find('d:/work/usd_py36/usd/rootLayer.usda'), Sdf.Find('d:/work/usd_py36/usd/layerB.usda')]
    

    ```


#### [4]:


```python
# EditTarget関係
# EditTarget取得　デフォルトはRoot
target = stage.GetEditTarget()

```


#### [5]:


```python

# Spec取得
prim = stage.GetPrimAtPath("/testPrim")
attr = prim.GetAttribute("hoge")
attrB = prim.GetAttribute("val")

# Path指定でEditTarget取得したい
# GetUsedLayers()の引数では Sdf.Findの配列なので、これを使う手もある。
targetB = stage.GetEditTargetForLocalLayer(Sdf.Find('d:/work/usd_py36/usd/layerB.usda'))
# それからPrimSpecを取得
targetBPrim = targetB.GetLayer().GetPrimAtPath('/testPrim')

# アトリビュートが定義されてるか
print('val' in targetBPrim.attributes)
# セットされている値を取得
print(targetBPrim.attributes['val'].default)

```

!!! success
    ```

    True
    10
    

    ```


#### [6]:


```python
# Root以外のレイヤーを編集ターゲットにする
stage.SetEditTarget(targetB)
# 試しに追加
stage.DefinePrim("/addTest")
# そして保存
targetB.GetLayer().Save()



```

!!! success
    ```




    True



    ```