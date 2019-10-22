# PythonUSDチートシート

<!-- SUMMARY: PythonUSDチートシート-->

Pythonを使用してUSDを操作するやり方がだいぶ分かってきたので  
よく使う物とかをまとめ。  

## 全般

### Import

```python
import os.path
from pxr import Usd, UsdGeom, Sdf, Gf
```

## Stage関係

### Newシーン

```python
stage = Usd.Stage.CreateInMemory()
```
usdaを作らずにとりあえずステージを作る場合。  

```python
stage = Usd.Stage.CreateNew(USD_PATH_ROOT + '/HelloWorld.usda')
```
usdaを作って、新しいステージを作る。  

### USDを開く

```python
stage = Usd.Stage.Open(USD_PATH_ROOT + '/HelloWorld.usda')
```
すでにあるUSDファイルをステージとして開く。

### 保存する

```python
stage = Usd.Stage.CreateNew(USD_PATH_ROOT + '/HelloWorld.usda')
stage.Save()
```
開いているusdをそのまま保存。  
  
```python
stage = Usd.Stage.CreateInMemory()
stage.GetRootLayer().Export(USD_PATH_ROOT + '/HelloWorld.usda')
```
メモリ上のみで作成しているUSDをExportする。  
CreateNewして開いて保存する場合、すでにUSDがあるとErrorになってしまうが  
こちらの場合はエラーにならない。

### 現在のUSDの中身を確認する

```python
print(stage.GetRootLayer().ExportToString())
```
ExportToStringをすると、げんざいのUSDをプリントすることができる  
  
### 全コンポ結果を反映したUSDを確認する

```python
stage.Flatten().ExporToString()
```
通常のExportToString()の場合、コンポ情報が残った状態で表示される。  
が、すべてのコンポジションの結果をすべて判定（Flatten)した状態で見たい場合は  
上のようにする。
当然のことながら、複雑なコンポを行っている場合Flattenするとファイルサイズは増大する。  

## Prim操作

### Prim/Class/Overを作る

```python
stage.DefinePrim("/hogehoge")
stage.OverridePrim("/over")
stage.CreateClassPrim("/class")
```
![](https://gyazo.com/722a355c20219131879a48102413e1c4.png)

スキーマなしのPrimが作成される。  
  
### StageからPrimを取得する

```python
prim = stage.GetPrimAtPath('/hogehoge')
print(prim)
```

### スキーマありのPrimを定義する

```python
stage = Usd.Stage.CreateInMemory()
# Xformを作る
xform = UsdGeom.Xform.Define(stage, '/xform')
# Cubeを作る
cube = UsdGeom.Cube.Define(stage, '/hello')
```
ConcreteSchemaにはDefine関数があるので、↑のように定義する。

### SchemaオブジェクトからPrimを取得

```python
prim = xform.GetPrim()
```

## Attribute操作

### Attributeを作る/セットする

```python
# Boolの場合
attr = prim.CreateAttribute("test", Sdf.ValueTypeNames.Bool)
attr.Set(False)
# Colorの場合
color_attr = prim.CreateAttribute("color", Sdf.ValueTypeNames.Color3d)
color_attr.Set(Gf.Vec3d(1, 1, 1))
```
ValueTypeNamesでの型指定方法は[こちら](01_01_usd_py_docs.md)を参照。  
ColorやVectorなどの型はGfモジュールにある定義を使用してセットする。

### Attributeから値を取得する

```python
attr = prim.GetAttribute('test')
print(attr.Get())
```

### Namespaceを使用する

```python
# Namespaceつきのアトリビュートを作る
prim.CreateAttribute("ns:testVal", Sdf.ValueTypeNames.Bool)
props = prim.GetPropertiesInNamespace('ns')
print(props)
```
プロパティ名・アトリビュート名にはNamespaceをつけることができる。  
つけかたは Namespace:hogehoge のように : で区切ればOK。  
Namespaceをつけておくと、GetPropertiesInNamespace関数を使用して  
指定のNamespaceのプロパティやアトリビュートを取得することができる。  

#### NamespaceやNmaespace無しのプロパティ名を取得
```python
print(attr.GetBaseName())
print(attr.GetNamespace())
print(attr.SplitName())
```
このNamespaceやプロパティ名は、プロパティオブジェクトで取得することができる。  

### Relationshipを使用する

#### Relationshipを作成
```python
# RelationshipでPrimを入れる
rel = prim.CreateRelationship('test')
rel.AddTarget(relSdfPath)
rel.AddTarget(relSdfPathB)
# AttributeもRelにできる
relAttr = prim.CreateRelationship('attr_test')
relAttr.AddTarget(attr.GetPath())
```
#### Relationship先を取得

```python
attrPath.GetTargets()
```
GetTargets()を使用すると、接続先のSdfPathを取得できる。

### SdfPathからAttributeの値を取得する

```python
relPrim = stage.GetObjectAtPath(attrPath.GetTargets()[0])
print(relPrim.Get())
```
SdfPathからPrimまたはAttributeを取得したい場合は、StageのGetObjectAtPath()を使用する。  
Objectで取得したばあい、Primの場合はPrimオブジェクトが帰ってくるし  
AttributeだったらAttributeオブジェクトが帰ってくる。

## Metadata

![](https://gyazo.com/84e24a33184e60510b56236622ad5508.png)

MetadataはPrimやAttributeなどに対して設定できる付加情報。  

### Metadataの取得
```python
# 指定のPrim・Attribute・PropertyのMetadataをDictで取得
print(prim.GetAllMetadata())
```

### Metadataに値をセットする

```python
newScn.SetMetadata('comment', 'Hello World')
```

### CustomDataを使用する

```python
# 指定のオブジェクトに対してCustomDataを指定する
prim.SetCustomDataByKey('userCustomMeta', 'fuga')
# 取得する
print(prim.GetCustomData())
# namespaceを指定した場合
prim.SetCustomDataByKey('test:userCustomMeta', 'fuga')
```
![](https://gyazo.com/23450b78037332d4b4022583c2efdb0b.png)
CustomDataでNamespaceをつけると、Dict型をネストできる。  
val['test']['userCustomData']  
アクセスするときはこんな感じにできる。  

## Transforrm操作

### Xformオブジェクトを使用する場合

```python
stage = Usd.Stage.CreateInMemory()
xform = UsdGeom.Xform.Define(stage, '/xform')
xform.AddTranslateOp().Set((50, 0, 0))
```
Xformableクラスに各種Tranlsform操作用の関数があるので  
それを使用すればTransformができる。  
  
### PrimからTransformする場合

```python
path = Sdf.Path("/xform")
prim = stage.GetPrimAtPath(path)
UsdGeom.XformCommonAPI(prim).SetRotate((90, 0, 0))
```
Xformオブジェクトではなく、Primオブジェクトから  
Transform処理をしたい場合はXformCommonAPIを使用する。
  
## コンポジション関係

### VariantSet

```python
vset = prim.GetVariantSets().AddVariantSet('hogehoge')
vset.AddVariant('red')
vset.AddVariant('blue')
vset.AddVariant('green')

colorAttr = UsdGeom.Gprim.Get(newScn, '/World/Cube').GetDisplayColorAttr()

vset.SetVariantSelection('red')
with vset.GetVariantEditContext():
    colorAttr.Set([(1, 0, 0)])
    
vset.SetVariantSelection('blue')
with vset.GetVariantEditContext():
    colorAttr.Set([(0, 0, 1)])

vset.SetVariantSelection('green')
with vset.GetVariantEditContext():
    colorAttr.Set([(0, 1, 0)])
```

### Reference

```python
refPrimA = stage.DefinePrim("/World/BookGrp/Book")
refPrimA.GetReferences().AddReference(kitchenSetRoot + 'Book/Book.usd')
```
Referenceで読み込みたいusdをPrimに対してセットする

### Inherits

### SubLayer

```python
stage = Usd.Stage.CreateInMemory()
rootLayer = stage.GetRootLayer()
rootLayer.subLayerPaths = [kitchenSetRoot + "/Book/Book.usd", kitchenSetRoot + "/Ball/Ball.usd"]
```

## アニメーション関係

```python
newScn.SetStartTimeCode(0)
newScn.SetEndTimeCode(100)
 
# Mem上に作成したUSDファイルを色々コントロール
worldGeom = UsdGeom.Xform.Define(newScn, "/World")
cubeGeom = UsdGeom.Cube.Define(newScn, "/World/Cube")
 
# PrimのPath（sdfPath）の作成。
worldPath = Sdf.Path("/World")
helloPath = worldPath.AppendChild("hello")
 
# Cubeをアニメーション
spin = cubeGeom.AddRotateZOp(opSuffix='spin')
spin.Set(time=0, value=0)
spin.Set(time=100, value=360)
```

## マテリアル関係

```python
stage = Usd.Stage.CreateInMemory()
rootLayer = stage.GetRootLayer()
 
sphere = UsdGeom.Sphere.Define(stage, '/test/sphere')
 
matPath = Sdf.Path("/Model/Material/MyMat")
mat = UsdShade.Material.Define(stage, matPath)
shader = UsdShade.Shader.Define(stage, matPath.AppendChild('testShader'))
 
# Shaderのアトリビュート設定
# 色をつけただけの基本のPBRシェーダーを作る
shader.CreateIdAttr('UsdPreviewSurface')
shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0, 1, 0))
shader.CreateInput('metalic', Sdf.ValueTypeNames.Float).Set(0.9)
shader.CreateInput('roughness', Sdf.ValueTypeNames.Float).Set(0.2)
# Shaderの結果をMatにつなげる
mat.CreateSurfaceOutput().ConnectToSource(shader, "surface")
 
# Bind
UsdShade.MaterialBindingAPI(sphere.GetPrim()).Bind(mat)
```

## Mesh関係
```python
UsdGeom.Xform.Define(stage, '/hoge')
mesh = UsdGeom.Mesh.Define(stage, '/hoge/hogehoge')
 
# %%
 
mesh.CreatePointsAttr([(-5, -5, 5), (5, -5, 5), (5, 5, 5), (-5, 5, 5)])
# 1Faceあたりの頂点数
mesh.CreateFaceVertexCountsAttr([3, 3])
# 結線情報？
mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 0, 2, 3])
# BoundingBoxをセット？
mesh.CreateExtentAttr(UsdGeom.PointBased(mesh).ComputeExtent(mesh.GetPointsAttr().Get()))
```