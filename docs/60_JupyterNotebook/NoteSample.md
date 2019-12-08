---
title: テストノートブック
---
#### [1]:




```python

import os.path
from pxr import Usd, UsdGeom, Sdf, Gf

```




#### [2]:




```python

stg =Usd.Stage.Open(r"C:\Users\remiria\Downloads\UsdSkelExamples\UsdSkelExamples\HumanFemale\HumanFemale.walk.usd")
stg.GetRootLayer().Export("D:/test.usda")

```



!!! info
    ```




    True



    ```

#### [3]:




```python
# ファイルではなくメモリにシーンを作る
stage = Usd.Stage.CreateInMemory()
# シーンに対してPrimを追加する。
xf = UsdGeom.Sphere.Define(stage, "/hello")
# 結果を表示
print(stage.ExportToString())

```



!!! info
    ```

    #usda 1.0
    (
        doc = """Generated from Composed Stage of root layer 
    """
    )
    
    def Sphere "hello"
    {
    }
    
    
    

    ```

#### [5]:




```python

# hoge


```





#### [7]:




```python
test

```



!!! info
    ```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    c:\pyEnv\JupyterUSD_py27\usd\pyDev\usdJupyter.py in <module>()
    ----> 1 test
    

    NameError: name 'test' is not defined


    ```