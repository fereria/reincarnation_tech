---
title: USDのMeshをPythonで作る
---
ipynbFile: [USDMeshTest__USDのMeshをPythonで作る.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USDMeshTest__USDのMeshをPythonで作る.ipynb)
#### [9]:


```python

from pxr import Usd,UsdGeom,Sdf

```


#### [10]:


```python

stage = Usd.Stage.CreateInMemory()
UsdGeom.Xform.Define(stage, '/hoge')
mesh = UsdGeom.Mesh.Define(stage, '/hoge/TestMesh')

```


#### [11]:


```python

# Point設定
mesh.CreatePointsAttr([(-5, -5, 5), (5, -5, 5), (5, 5, 5), (-5, 5, 5)])
# 1FaceあたりのVertex数
mesh.CreateFaceVertexCountsAttr([3, 3])
# 結線情報？
mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 0, 2, 3])
# BoundingBoxをセット？
mesh.CreateExtentAttr(UsdGeom.PointBased(mesh).ComputeExtent(mesh.GetPointsAttr().Get()))
# UV作成
uv = mesh.CreatePrimvar('st',Sdf.ValueTypeNames.TexCoord2fArray,UsdGeom.Tokens.varying)
uv.Set([(0,0),(0,1),(1,1),(1,0)])

```

!!! success
    ```




    True



    ```


#### [12]:


```python

# 頂点取得
print(mesh.GetPointsAttr().Get())
print(mesh.GetFaceVertexCountsAttr().Get()) # 頂点数

print(mesh.GetNormalsInterpolation())

```

!!! success
    ```

    [(-5, -5, 5), (5, -5, 5), (5, 5, 5), (-5, 5, 5)]
    [3, 3]
    vertex
    

    ```


#### [13]:


```python

print(stage.GetRootLayer().ExportToString())
# stage.GetRootLayer().Export("D:/work/usd_py36/usd/usdSimpleMesh.usda")

```

!!! success
    ```

    #usda 1.0
    
    def Xform "hoge"
    {
        def Mesh "TestMesh"
        {
            float3[] extent = [(-5, -5, 5), (5, 5, 5)]
            int[] faceVertexCounts = [3, 3]
            int[] faceVertexIndices = [0, 1, 2, 0, 2, 3]
            point3f[] points = [(-5, -5, 5), (5, -5, 5), (5, 5, 5), (-5, 5, 5)]
            texCoord2f[] primvars:st = [(0, 0), (0, 1), (1, 1), (1, 0)] (
                interpolation = "varying"
            )
        }
    }
    
    
    

    ```