---
title: ClipsAPIの基本構造をつくる
---
**ipynbFile** [UsdClipsAPI_01__ClipsAPIの基本構造をつくる.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/TimeSample/UsdClipsAPI_01__ClipsAPIの基本構造をつくる.ipynb)
#### [13]:


```python
from pxr import Usd,Sdf
```


#### [14]:


```python
ROOT_PATH = "d:/work/py37/USD/clip/"
```


#### [18]:


```python
# Clipを作る
a = Sdf.Layer.FindOrOpen(ROOT_PATH + 'clip1.usda')
b = Sdf.Layer.FindOrOpen(ROOT_PATH + 'clip2.usda')
print(a.ExportToString())
print(b.ExportToString())
```

!!! success
    ```

    #usda 1.0
    
    def "Model"
    {
        double a.timeSamples = {
            1: 1,
        }
        double b = 10
    }
    
    
    #usda 1.0
    
    def "Model"
    {
        double a.timeSamples = {
            1: 1234,
        }
        double b.timeSamples = {
            1: 10,
        }
    }
    
    
    

    ```


#### [16]:


```python
# ClipのレイヤーからManifestを作る。
# Manifestは、ClipsAPIを使用するときに、クリップでアクセスアトリビュートの
# インデックスを作るためのファイル。
# ClipのうちTimeSampleを持つアトリビュートの定義を作る。
manifest = Usd.ClipsAPI.GenerateClipManifestFromLayers([a,b],'/Model')
```


#### [17]:


```python
# 結果は、アノニマスレイヤーとして取得できるので
# このアノニマスレイヤーを保存して使用する。
print(manifest.ExportToString())
manifest.Export(ROOT_PATH + "/manifest_sample.usda")
```

!!! success
    ```

    #usda 1.0
    
    over "Model"
    {
        double a
        double b
    }
    
    
    

    ```

!!! success
    ```




    True



    ```


#### [7]:


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


#### [8]:


```python
# Clipのレイヤーをセット
clipAPI.SetClipAssetPaths([Sdf.AssetPath(ROOT_PATH + 'clip1.usda'),
                           Sdf.AssetPath(ROOT_PATH + 'clip2.usda')])
clipAPI.SetClipManifestAssetPath(Sdf.AssetPath(ROOT_PATH + 'manifest_sample.usda'),'default')
```

!!! success
    ```




    True



    ```


#### [9]:


```python
print(stage.GetRootLayer().ExportToString())
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
            dictionary default = {
                asset[] assetPaths = [@d:/work/py37/USD/clip/clip1.usda@, @d:/work/py37/USD/clip/clip2.usda@]
                asset manifestAssetPath = @d:/work/py37/USD/clip/manifest_sample.usda@
            }
        }
    )
    {
        double a
        double b
    }
    
    
    

    ```


#### [10]:


```python
# Clip側にある読み先のPrimを指定する
clipAPI.SetClipPrimPath('/Model')
```

!!! success
    ```




    True



    ```


#### [11]:


```python
# CurrentTime時にどのClipを使用するかIndexを指定する
for num,c in enumerate([a,b]):
    currentActive  = list(clipAPI.GetClipActive())
    currentActive.append([num+1,num])
    clipAPI.SetClipActive(currentActive)

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
            dictionary default = {
                double2[] active = [(1, 0), (2, 1)]
                asset[] assetPaths = [@d:/work/py37/USD/clip/clip1.usda@, @d:/work/py37/USD/clip/clip2.usda@]
                asset manifestAssetPath = @d:/work/py37/USD/clip/manifest_sample.usda@
                string primPath = "/Model"
            }
        }
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