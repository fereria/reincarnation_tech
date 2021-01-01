---
title: Face単位でシェーダーをアサイン
---
**ipynbFile** [geomsubset_01__Face単位でシェーダーをアサイン.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/Material/geomsubset_01__Face単位でシェーダーをアサイン.ipynb)
![](https://gyazo.com/f56b3e96e1104eac0636a9ffc142e634.png)

こういう9のFaceがあるMeshでテスト。


#### [56]:


```python
from pxr import Usd,UsdGeom,UsdShade,Sdf,Gf
```


#### [38]:


```python
stage = Usd.Stage.Open(r"D:\work\py37\sampleUSD\usdPlane.usd")
prim = stage.GetPrimAtPath('/grid2/mesh_0')
path = prim.GetPath()
# PrimからGeomMeshを取得
mesh = UsdGeom.Mesh(prim)
```


#### [39]:


```python
stage.Reload()
```


#### [40]:


```python
# Meshの情報を取得
print(mesh.GetFaceCount())
# PointBasedで取得 頂点の座標
print(mesh.GetPointsAttr().Get())
# Faceを構成する頂点ID
print(mesh.GetFaceVertexIndicesAttr().Get())
# Face単位の頂点数
print(mesh.GetFaceVertexCountsAttr().Get())
# Faceの数
print(mesh.GetFaceCount())
```

!!! success
    ```

    9
    [(-1, 0, -1), (-0.3333333, 0, -1), (0.33333337, 0, -1), (1, 0, -1), (-1, 0, -0.3333333), (-0.3333333, 0, -0.3333333), (0.33333337, 0, -0.3333333), (1, 0, -0.3333333), (-1, 0, 0.33333337), (-0.3333333, 0, 0.33333337), (0.33333337, 0, 0.33333337), (1, 0, 0.33333337), (-1, 0, 1), (-0.3333333, 0, 1), (0.33333337, 0, 1), (1, 0, 1)]
    [0, 1, 5, 4, 1, 2, 6, 5, 2, 3, 7, 6, 4, 5, 9, 8, 5, 6, 10, 9, 6, 7, 11, 10, 8, 9, 13, 12, 9, 10, 14, 13, 10, 11, 15, 14]
    [4, 4, 4, 4, 4, 4, 4, 4, 4]
    9
    

    ```


#### [41]:


```python
# Subsetを定義する
subset = UsdGeom.Subset.Define(stage,path.AppendChild('subset'))
```


#### [42]:


```python
print(mesh)
```

!!! success
    ```

    UsdGeom.Mesh(Usd.Prim(</grid2/mesh_0>))
    

    ```


#### [43]:


```python
# 指定IndexをSubsetに追加
subset.CreateIndicesAttr([0,1,2])
```

!!! success
    ```




    Usd.Prim(</grid2/mesh_0/subset>).GetAttribute('indices')



    ```


#### [60]:


```python
# Shaderを作る
mat = UsdShade.Material.Define(stage,"/Looks/sampleMat")
shader = UsdShade.Shader.Define(stage,"/Looks/sampleMat/sampleShader")
shader.CreateIdAttr('UsdPreviewSurface')
# わかりやすい色をセット
shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1,0,0))
mat.CreateSurfaceOutput().ConnectToSource(shader, "surface")
# subsetにアサイン
UsdShade.MaterialBindingAPI(subset).Bind(mat)
```

!!! success
    ```




    True



    ```


#### [61]:


```python
print(stage.GetRootLayer().ExportToString())
```

!!! success
    ```

    #usda 1.0
    (
        defaultPrim = "grid2"
        endTimeCode = 1
        framesPerSecond = 24
        metersPerUnit = 1
        startTimeCode = 1
        timeCodesPerSecond = 24
        upAxis = "Y"
    )
    
    def Xform "grid2" (
        kind = "component"
    )
    {
        matrix4d xformOp:transform:xform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
        uniform token[] xformOpOrder = ["xformOp:transform:xform"]
    
        def Mesh "mesh_0"
        {
            float3[] extent = [(-1, 0, -1), (1, 0, 1)]
            int[] faceVertexCounts = [4, 4, 4, 4, 4, 4, 4, 4, 4]
            int[] faceVertexIndices = [0, 1, 5, 4, 1, 2, 6, 5, 2, 3, 7, 6, 4, 5, 9, 8, 5, 6, 10, 9, 6, 7, 11, 10, 8, 9, 13, 12, 9, 10, 14, 13, 10, 11, 15, 14]
            uniform token orientation = "leftHanded"
            point3f[] points = [(-1, 0, -1), (-0.3333333, 0, -1), (0.33333337, 0, -1), (1, 0, -1), (-1, 0, -0.3333333), (-0.3333333, 0, -0.3333333), (0.33333337, 0, -0.3333333), (1, 0, -0.3333333), (-1, 0, 0.33333337), (-0.3333333, 0, 0.33333337), (0.33333337, 0, 0.33333337), (1, 0, 0.33333337), (-1, 0, 1), (-0.3333333, 0, 1), (0.33333337, 0, 1), (1, 0, 1)] (
                interpolation = "vertex"
            )
            uniform token subdivisionScheme = "none"
    
            def GeomSubset "subset"
            {
                int[] indices = [0, 1, 2]
                rel material:binding = </Looks/sampleMat>
            }
        }
    }
    
    def "Looks"
    {
        def Material "sampleMat"
        {
            token outputs:surface.connect = </Looks/sampleMat/sampleShader.outputs:surface>
    
            def Shader "sampleShader"
            {
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = (1, 0, 0)
                token outputs:surface
            }
        }
    }
    
    
    

    ```


#### [62]:


```python
stage.GetRootLayer().Export(r"D:\work\py37\sampleUSD\subset_addMat.usd")
```

!!! success
    ```




    True



    ```

![](https://gyazo.com/cb0f205d1aa00b5650aaf4f403e70de8.png)

こうなって

![](https://gyazo.com/56a96ca6816a98490360d0814702f98b.png)

こうなる。