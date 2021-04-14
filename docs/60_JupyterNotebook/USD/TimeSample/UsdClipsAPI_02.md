---
title: TemplateAssetPathを使う
---
**ipynbFile** [UsdClipsAPI_02__TemplateAssetPathを使う.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/TimeSample/UsdClipsAPI_02__TemplateAssetPathを使う.ipynb)
#### [1]:


```python
from pxr import Usd,Sdf
```


#### [2]:


```python
ROOT_PATH = "d:/work/py37/USD/clip/"
```


#### [5]:


```python
# Clipを作る
A_1 = Sdf.Layer.FindOrOpen(ROOT_PATH + 'A/clip.1.usda')
A_2 = Sdf.Layer.FindOrOpen(ROOT_PATH + 'A/clip.2.usda')
A_3 = Sdf.Layer.FindOrOpen(ROOT_PATH + 'A/clip.3.usda')
A_4 = Sdf.Layer.FindOrOpen(ROOT_PATH + 'A/clip.4.usda')
manifestA = Usd.ClipsAPI.GenerateClipManifestFromLayers([A_1,A_2,A_3,A_4],'/ModelA')
print(manifestA.ExportToString())
manifestA.Export(ROOT_PATH + "/A/manifest_sample.usda")
B_1 = Sdf.Layer.FindOrOpen(ROOT_PATH + 'B/clip.1.usda')
B_2 = Sdf.Layer.FindOrOpen(ROOT_PATH + 'B/clip.2.usda')
manifestB = Usd.ClipsAPI.GenerateClipManifestFromLayers([B_1,B_2],'/ModelB')
manifestB.Export(ROOT_PATH + "/B/manifest_sample.usda")
print(manifestB.ExportToString())
```

!!! success
    ```

    #usda 1.0
    
    over "ModelA"
    {
        double a
    }
    
    
    #usda 1.0
    
    over "ModelB"
    {
        double b
    }
    
    
    

    ```


#### [6]:


```python
# Clipを作るためのレイヤーを用意。
stage = Usd.Stage.Open(ROOT_PATH + "stage.usda")
stage.Reload()
print(stage.GetRootLayer().ExportToString())
prim = stage.GetPrimAtPath('/TestModel')
# ClipsAPIの引数で、Clipを追加したいSdfPathを指定する
clipAPI = Usd.ClipsAPI(prim)
```

!!! success
    ```

    #usda 1.0
    (
        endTimeCode = 4
        startTimeCode = 1
    )
    
    def "TestModel"
    {
        double a
        double b
    }
    
    
    

    ```


#### [7]:


```python
# Clipのレイヤーをセット
clipAPI.SetClipAssetPaths([Sdf.AssetPath(ROOT_PATH + 'A/clip.1.usda'),
                           Sdf.AssetPath(ROOT_PATH + 'A/clip.2.usda'),
                           Sdf.AssetPath(ROOT_PATH + 'A/clip.3.usda'),
                           Sdf.AssetPath(ROOT_PATH + 'A/clip.4.usda')],'A')
clipAPI.SetClipManifestAssetPath(Sdf.AssetPath(ROOT_PATH + 'A/manifest_sample.usda'),'A')
```

!!! success
    ```




    True



    ```


#### [8]:


```python
# Templateの場合。
# Templateを使用すると hogehoge.#.usda のように連番部分を # で表せる。
clipAPI.SetClipTemplateAssetPath(ROOT_PATH + 'B/clip.#.usda','B')
clipAPI.SetClipTemplateStartTime(1,'B')
clipAPI.SetClipTemplateEndTime(4,'B')
clipAPI.SetClipTemplateStride(1,'B')
clipAPI.SetClipManifestAssetPath(Sdf.AssetPath(ROOT_PATH + 'B/manifest_sample.usda'),'B')
```

!!! success
    ```




    True



    ```


#### [9]:


```python
# Clip側にある読み先のPrimを指定する
clipAPI.SetClipPrimPath('/ModelA','A')
clipAPI.SetClipPrimPath('/ModelB','B')
```

!!! success
    ```




    True



    ```


#### [10]:


```python
# CurrentTime時にどのClipを使用するかIndexを指定する
for num,c in enumerate([A_1,A_2,A_3,A_4]):
    currentActive  = list(clipAPI.GetClipActive('A'))
    currentActive.append([num+1,num])
    clipAPI.SetClipActive(currentActive,'A')

```


#### [11]:


```python
# 複数Clipsetを指定する場合。
clipAPI.SetClipSets(Sdf.StringListOp.Create(['A','B']))
```

!!! success
    ```




    True



    ```


#### [12]:


```python
print(stage.GetRootLayer().ExportToString())
stage.GetRootLayer().Export(ROOT_PATH + 'result.usda')
```

!!! success
    ```

    #usda 1.0
    (
        endTimeCode = 4
        startTimeCode = 1
    )
    
    def "TestModel" (
        clips = {
            dictionary A = {
                double2[] active = [(1, 0), (2, 1), (3, 2), (4, 3)]
                asset[] assetPaths = [@d:/work/py37/USD/clip/A/clip.1.usda@, @d:/work/py37/USD/clip/A/clip.2.usda@, @d:/work/py37/USD/clip/A/clip.3.usda@, @d:/work/py37/USD/clip/A/clip.4.usda@]
                asset manifestAssetPath = @d:/work/py37/USD/clip/A/manifest_sample.usda@
                string primPath = "/ModelA"
            }
            dictionary B = {
                asset manifestAssetPath = @d:/work/py37/USD/clip/B/manifest_sample.usda@
                string primPath = "/ModelB"
                string templateAssetPath = "d:/work/py37/USD/clip/B/clip.#.usda"
                double templateEndTime = 4
                double templateStartTime = 1
                double templateStride = 1
            }
        }
        prepend clipSets = ["A", "B"]
    )
    {
        double a
        double b
    }
    
    
    

    ```

!!! success
    ```




    True



    ```

![](https://gyazo.com/8a8b2889c355eb800b352855b433faea.png)
clipSetsを指定すると、１つのPrimに対して複数のValueClipを指定できる