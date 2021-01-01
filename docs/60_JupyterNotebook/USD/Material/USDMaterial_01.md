---
title: USDでMaterial_ShadingNetwork
---
**ipynbFile** [USDMaterial_01__USDでMaterial_ShadingNetwork.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/USD/Material/USDMaterial_01__USDでMaterial_ShadingNetwork.ipynb)
#### [32]:


```python
import os.path
from pxr import Usd, UsdGeom, Sdf, Gf, UsdShade

```


#### [33]:


```python


stage = Usd.Stage.CreateInMemory()
rootLayer = stage.GetRootLayer()

# Mesh作成
sphere = UsdGeom.Sphere.Define(stage, '/test/sphere')

matPath = Sdf.Path("/Model/Material/MyMat")
mat = UsdShade.Material.Define(stage, matPath)
shader = UsdShade.Shader.Define(stage, matPath.AppendChild('testShader'))


# Shaderのアトリビュート設定
# 色をつけただけの基本のPBRシェーダーを作る
shader.CreateIdAttr('UsdPreviewSurface')
shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f)
shader.CreateInput('metalic', Sdf.ValueTypeNames.Float).Set(0.9)
shader.CreateInput('roughness', Sdf.ValueTypeNames.Float).Set(0.2)
# カスタムパラメーターもつくれる
shader.CreateInput('test', Sdf.ValueTypeNames.Float).Set(1.0)

# Shaderの結果をMatにつなげる
mat.CreateSurfaceOutput().ConnectToSource(shader, "surface")
# 別のノードを作って、接続する
colorPrim = UsdShade.Shader.Define(stage, '/node/outColor')
colorOut = colorPrim.CreateInput('color', Sdf.ValueTypeNames.Color3f)
colorOut.Set(Gf.Vec3f(1, 0, 0))
shader.GetInput('diffuseColor').ConnectToSource(colorOut)

# Bind
UsdShade.MaterialBindingAPI(sphere.GetPrim()).Bind(mat)

```

!!! success
    ```




    True



    ```


#### [34]:


```python

print(stage.GetRootLayer().ExportToString())

stage.GetRootLayer().Export("D:/matTest.usda")

```

!!! success
    ```

    #usda 1.0
    
    def "test"
    {
        def Sphere "sphere"
        {
            rel material:binding = </Model/Material/MyMat>
        }
    }
    
    def "Model"
    {
        def "Material"
        {
            def Material "MyMat"
            {
                token outputs:surface.connect = </Model/Material/MyMat/testShader.outputs:surface>
    
                def Shader "testShader"
                {
                    uniform token info:id = "UsdPreviewSurface"
                    color3f inputs:diffuseColor.connect = </node/outColor.inputs:color>
                    float inputs:metalic = 0.9
                    float inputs:roughness = 0.2
                    float inputs:test = 1
                    token outputs:surface
                }
            }
        }
    }
    
    def "node"
    {
        def Shader "outColor"
        {
            color3f inputs:color = (1, 0, 0)
        }
    }
    
    
    

    ```

!!! success
    ```




    True



    ```

![](https://i.gyazo.com/62970445bf4df3ac356150956fe457f9.jpg)
こんな感じ？

![](https://gyazo.com/a0af6171ddcf33b7188539928a40b1b3.png)
ShadingNetworkも CreateInput と ConnectToSource で表現できる