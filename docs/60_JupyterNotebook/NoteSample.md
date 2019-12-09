---
title: テストノートブック
---
```python
# Change directory to VSCode workspace root so that relative path loads work correctly. Turn this addition off with the DataScience.changeDirOnImportExport setting

# ms-python.python added

import os

try:

	os.chdir(os.path.join(os.getcwd(), '..\\..\pyEnv\JupyterUSD_py27'))

	print(os.getcwd())

except:

	pass


```


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

!!! success
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

!!! success
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

!!! error


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    c:\pyEnv\JupyterUSD_py27\usd\pyDev\usdJupyter.py in <module>()
    ----> 1 test
    

    NameError: name 'test' is not defined


