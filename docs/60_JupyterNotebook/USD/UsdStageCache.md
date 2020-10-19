---
title: usdCacheを使う_Stageをリロードする
---
**ipynbFile** [UsdStageCache__usdCacheを使う_Stageをリロードする.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/UsdStageCache__usdCacheを使う_Stageをリロードする.ipynb)
USDのステージを依頼たあとにアップデートする方法がようやくわかった。  
ついでにCacheまわり。  
開いたStageはキャッシュに入れることができる。  
  
UsdUtils.StageCache（シングルトンのUsdCache）を取得してから、  
そのStageCacheにステージを入れておくと  
あとでそのStageを取得できたりするらしい。  


#### [1]:


```python
from pxr import Usd,Pcp,UsdUtils
```


#### [2]:


```python
stage = Usd.Stage.Open(r'S:\fav\work\programming\python\JupyterUSD\pyDev\usd\root.usda')
# 一度ロードした内容を更新したい場合は、Reloadを実行する
# これを実行しないと、途中でusdをアップデートしてもロードされない
stage.Reload()
# UsdUtils.StageCache はシングルトン
cache = UsdUtils.StageCache.Get()
cacheID = cache.Insert(stage)
```


#### [3]:


```python
prim = stage.GetPrimAtPath('/sublayerReference')
```


#### [4]:


```python
for i in stage.Traverse():
    print(i)
```

!!! success
    ```

    Usd.Prim(</subLayerB>)
    Usd.Prim(</subLayerA>)
    Usd.Prim(</sublayerReference>)
    Usd.Prim(</Cube>)
    

    ```


#### [5]:


```python
# キャッシュに入れていたStageを確認する
for s in cache.GetAllStages():
    print(s)
```

!!! success
    ```

    Usd.Stage.Open(rootLayer=Sdf.Find('s:/fav/work/programming/python/JupyterUSD/pyDev/usd/root.usda'), sessionLayer=Sdf.Find('anon:000002C12DA6C1B0:root-session.usda'), pathResolverContext=Ar.DefaultResolverContext(['S:\\fav\\work\\programming\\python\\JupyterUSD\\pyDev\\usd\\']))
    

    ```


#### [6]:


```python
# キャッシュからStageを探して取得
stage = cache.Find(cacheID)
```


#### [7]:


```python
# Stage内のPrimを確認
for i in stage.Traverse():
    print(i)
```

!!! success
    ```

    Usd.Prim(</subLayerB>)
    Usd.Prim(</subLayerA>)
    Usd.Prim(</sublayerReference>)
    Usd.Prim(</Cube>)
    

    ```


#### [8]:


```python
# キャッシュをクリア
cache.Clear()
```