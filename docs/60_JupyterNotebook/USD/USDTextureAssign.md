---
title: USDでTextureAssign
---
**ipynbFile** [USDTextureAssign__USDでTextureAssign.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/USDTextureAssign__USDでTextureAssign.ipynb)
#### [1]:


```python
from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade
```


#### [7]:


```python
stage = Usd.Stage.CreateInMemory()
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

modelRoot = UsdGeom.Xform.Define(stage, "/TexModel")
Usd.ModelAPI(modelRoot).SetKind(Kind.Tokens.component)
billboard = UsdGeom.Mesh.Define(stage, "/TexModel/card")
billboard.CreatePointsAttr([(-430, -145, 0), (430, -145, 0), (430, 145, 0), (-430, 145, 0)])
billboard.CreateFaceVertexCountsAttr([4])
billboard.CreateFaceVertexIndicesAttr([0,1,2,3])
billboard.CreateExtentAttr([(-430, -145, 0), (430, 145, 0)])
texCoords = billboard.CreatePrimvar("st", 
                                    Sdf.ValueTypeNames.TexCoord2fArray, 
                                    UsdGeom.Tokens.varying)
texCoords.Set([(0, 0), (1, 0), (1,1), (0, 1)])


```

!!! success
    ```




    True



    ```


#### [8]:


```python
material = UsdShade.Material.Define(stage, '/TexModel/boardMat')

pbrShader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/PBRShader')
pbrShader.CreateIdAttr("UsdPreviewSurface")
pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
pbrShader.CreateInput("opacity",Sdf.ValueTypeNames.Float).Set(1.0)

material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
```

!!! success
    ```




    True



    ```


#### [9]:


```python
stReader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/PBRShader/stReader')
stReader.CreateIdAttr('UsdPrimvarReader_float2')

diffuseTextureSampler = UsdShade.Shader.Define(stage,'/TexModel/boardMat/PBRShader/diffuseTexture')
diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("D:/USD_Logo.png")
diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader, 'result')
diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
diffuseTextureSampler.CreateOutput('a', Sdf.ValueTypeNames.Float)
pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler, 'rgb')
pbrShader.CreateInput("opacity", Sdf.ValueTypeNames.Float).ConnectToSource(diffuseTextureSampler, 'a')
```

!!! success
    ```




    True



    ```


#### [11]:


```python
stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
stInput.Set('st')

stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)
```

!!! success
    ```




    True



    ```


#### [12]:


```python
UsdShade.MaterialBindingAPI(billboard).Bind(material)

stage.Export("D:/addTexture.usda")
```

!!! success
    ```




    True



    ```