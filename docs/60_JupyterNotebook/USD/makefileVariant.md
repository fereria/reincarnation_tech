---
title: USDAssetsの作り方、基本構造メモ
---
**ipynbFile** [makefileVariant__USDAssetsの作り方、基本構造メモ.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/makefileVariant__USDAssetsの作り方、基本構造メモ.ipynb)
USDのサンプル examples/usdMakeFileVariantModelAsset/usdMakeFIleVarinatModelAsset.py
の中身を確認する。

このサンプルはコマンドラインで実行できる。

python usdMakeFileVariantModelAsset\usdMakeFileVariantModelAsset.py  --kind model  -i D:/test.usda -v cube sphere testProps D:\USDsample\modelAsset\cube.usda D:\USDsample\modelAsset\sphere.usda

基本構造は

![](https://gyazo.com/1ae86bbb15940f345a30dbd468a968a7.png)

RootPrim - Variant - Payload - <Model.usda>
         - __class_assetName
         
VariantとPayloadとInheritsの組み合わせ。

以下はサンプルの気になる部分の実行テスト。


#### [1]:


```python
from pxr import Tf, Kind, Sdf, Usd 
```


#### [2]:


```python
Tf.IsValidIdentifier('sample')
```

!!! success
    ```




    True



    ```


#### [3]:


```python
assetName = "sampleData"
```


#### [4]:


```python
filename = f"D:/{assetName}.usd"
```


#### [5]:


```python
layer = Sdf.Layer.CreateNew(filename,args= {'format':'usda'})
```


#### [6]:


```python
stage = Usd.Stage.Open(layer)

```


#### [9]:


```python
print(rootPath.AppendChild(assetName))
```

!!! success
    ```

    /sampleData
    

    ```


#### [10]:


```python
rootPath = Sdf.Path.absoluteRootPath
modelRootPrim = stage.DefinePrim(rootPath.AppendChild(assetName))
```


#### [27]:


```python
modelAPI = Usd.ModelAPI(modelRootPrim)
```


#### [28]:


```python
# Option用のResolvePathをセットする
# （あくまでもOptionとして使用されるもの？もの？）
modelAPI.SetAssetIdentifier('D:/test.usda')
# AssetPathで取得できる
print(modelAPI.GetAssetIdentifier())

modelAPI.SetAssetName(assetName)
```


#### [39]:


```python
# 引数で指定したKindかどうかを判定
modelAPI.IsKind('model')
```

!!! success
    ```




    True



    ```


#### [40]:


```python
classPrim = stage.CreateClassPrim(rootPath.AppendChild("_class_"+assetName))
modelRootPrim.GetInherits().AddInherit(classPrim.GetPath())
```

!!! success
    ```




    True



    ```


#### [42]:


```python
print(stage.GetRootLayer().ExportToString())
```

!!! success
    ```

    #usda 1.0
    (
        defaultPrim = "sampleData"
    )
    
    def "sampleData" (
        assetInfo = {
            asset identifier = @D:/test.usda@
        }
        prepend inherits = </_class_sampleData>
        kind = "model"
    )
    {
    }
    
    class "_class_sampleData"
    {
    }
    
    
    

    ```