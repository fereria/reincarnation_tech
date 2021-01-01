---
title: gltfからUsdMeshを作る
---
**ipynbFile** [gltf2UsdMesh__gltfからUsdMeshを作る.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/Mesh/gltf2UsdMesh__gltfからUsdMeshを作る.ipynb)
#### [91]:


```python
import trimesh
from pxr import Usd, UsdGeom, Sdf

gltf_file = r"D:\work\data_sample\susanne.glb"
gltf = trimesh.load(gltf_file)
geo_name = list(gltf.geometry.keys())[0]
geo = gltf.geometry[geo_name]

```

!!! success
    ```

    unable to load textures without pillow!
    

    ```


#### [92]:


```python
# 頂点取得
vtx = []
for v in geo.vertices:
    vtx.append(list(v))

```


#### [93]:


```python
# Faceを構成するIndexとVertexCountを取得
indexes = []
vtxcount = []

for f in geo.faces:
    indexes += [int(x) for x in f]
    vtxcount.append(len(f))
    

```


#### [94]:


```python
# to USDMesh
stage = Usd.Stage.CreateInMemory()
UsdGeom.Xform.Define(stage, f'/{geo_name}')
mesh = UsdGeom.Mesh.Define(stage, f'/{geo_name}/{geo_name}Mesh')

mesh.CreatePointsAttr(vtx)
# 1FaceあたりのVertex数
mesh.CreateFaceVertexCountsAttr(vtxcount)
# 結線情報？
mesh.CreateFaceVertexIndicesAttr(indexes)
# BoundingBoxをセット？
mesh.CreateExtentAttr(UsdGeom.PointBased(mesh).ComputeExtent(mesh.GetPointsAttr().Get()))

```

!!! success
    ```




    Usd.Prim(</Suzanne/SuzanneMesh>).GetAttribute('extent')



    ```