# USDPythonドキュメントの読み方

<!-- SUMMARY:USDPythonドキュメントの読み方 -->

~~概要まわりの文章化がうまくいかないので~~ 最近大分USDをPythonで弄るのも分かってきた  
ので、よく使うコマンド類とざっくりと公式ドキュメントから  
Pythonのコードを書く時にはまったりわかりにくいところなどをメモをば。
  
## モジュールのImportと、使い方

USDのAPIドキュメントは  
https://graphics.pixar.com/usd/docs/api/index.html  
こちらにあるのですが、基本C++なのと説明もとても難解なのでわかりにくいです。  
ので、ものすごいざっくりとPythonへの読み替え方を説明。  
  
まず、PythonのImportについて。  

```python
from pxr import Usd, UsdGeom, Sdf, Gf
```

USDのモジュールは pxr モジュールで、その中の各種スキーマやツール類を  
インポートします。  
  
![](https://gyazo.com/a6223e72a11b46a286779c46daea2a19.png)

ドキュメントの「Classes」下にライブラリのクラスや各種関数が並んでいるのですが  
Pythonから使用する場合は頭の文字がimportで読み込むモジュール名になります。  
上の画像のよく使う UsdStage の場合は UsdモジュールのStageになります。  

```python
from pxr import Usd
prim = Usd.Stage.CreateInMemory()
```

こうなります。  
  
### スキーマ関係の継承関係について

![](https://gyazo.com/6e06ca52d8d759eed3011690a2eeaa75.png)

スキーマを定義したい場合、主にUsdGeomを使用することになります。  
UsdGeom等のスキーマクラスは、クラスの継承によって構造化されています。  
「Inheritance diagram for #### 」を確認するとその継承関係がどのようになっているのか  
ダイアグラムで確認することが出来ます。  
  
このスキーマの定義は「IsASchema」と呼ばれる　「AはBです」の関係によって定義されています。  
たとえば、  
UsdGeomXformは、**UsdGeomImageableで UsdXformable** です。  
これらのダイアグラムの末端以外は「AbstractSchema」と呼ばれるもので  
共通の定義をしてある基底クラスです。  
ので、これらのクラスのインスタンスを作る事はできません。  
  
これに対して、末端の UsdGeomXform や UsdLuxDistantLight 、UsdGeomCameraなどのスキーマは  
「ConcreteSchema」と呼ばれるスキーマで  
実際にスキーマとして定義（Define）することができるスキーマになります。  
  
```python
stage = Usd.Stage.CreateInMemory()
xform = UsdGeom.Xform.Define(stage, "/hello")
```
たとえばXformスキーマを定義したい場合はこうなります。  

UsdGeom.Xformable.Define(stage,'/hello')  

これはエラーになります。  
  
```python
stage = Usd.Stage.CreateInMemory()
xform = UsdGeom.Xform.Define(stage, "/hello")
xform.GetXformOpOrderAttr() # Xformableで定義
xform.GetPrim() # UsdSchemaBaseで定義
```
当然のことですが、XformはXformableの関数も使えます。  
すべてのスキーマで共通して使用する GetPrimなどのような関数は UsdSchemaBaseに定義されているので  
ドキュメントを見るときは、継承関係を確認します。  
  
### TfToken について

https://graphics.pixar.com/usd/docs/api/class_tf_token.html

TfTokenとは、C++で文字列を扱うためのクラスです。  
Usdでは文字列を非常に多く扱いますが、きちんと扱わないと非常に効率が悪くなってしまいます。  
ので、PythonのディクショナリのようにIndexを作成して文字列を扱うのがTfTokenです。  
（あまりC++詳しくないので具体的にどうとかはワカラナイ）  
  
![](https://gyazo.com/b6d706932981298e6b528f5fdb4bbcc1.png)

ドキュメントを見ると、このように引数でTfToken型を求められることがありますが  
Pythonの場合はそもそもこのTf.Tokenは存在しませんので  
基本str型として読み替えを行います。  
  
では、Python側ではTokenは無関係かというとそんなこともなくて  
  
```python
print(UsdGeom.Tokens.type)
```
![](https://gyazo.com/0f14eee8eac5c49370c6f0d8e4fd53bf.png)

各クラス内にはTokenクラスを取得定義されている関数名などを、文字列で取得することができます。  

### UsdのAttributeType定義について

Primに対してアトリビュートを追加したい場合には  
そのアトリビュートの型がなにかを定義する必要があります。  
  
https://graphics.pixar.com/usd/docs/api/class_usd_prim.html#a1e25b831b0e54e1d59ba2da969e165fa

![](https://gyazo.com/2db056429f55dba14faeb6787ef66b07.png)

ドキュメントを見ると、 SdfValueTypeName で定義しろと書いてありますが  
このSdfValueTypeもPythonとC++では大きく違っていて、クラスメソッドの構成そのものがだいぶ  
違うのでうまくいきません。  
  
ではPythonの場合はどうするかというと

```python
str_attr = prim.CreateAttribute("testStr", Sdf.ValueTypeNames.String)
```
Pythonの場合、 Sdf.ValueTypeNames というEnumが存在していて  
これを使用して型を定義します。  
（しかしドキュメントにこの ValueTypeNames はない）  
  

Asset AssetArray Bool BoolArray Color3d Color3dArray Color3f Color3fArray Color3h  
Color3hArray Color4d Color4dArray Color4f Color4fArray Color4h Color4hArray Double  
Double2 Double2Array Double3 Double3Array Double4 Double4Array DoubleArray Find  
Float Float2  Float2Array  Float3  Float3Array  Float4  Float4Array  FloatArray  Frame4d  
Frame4dArray  Half  Half2  Half2Array  Half3  Half3Array  Half4  Half4Array  HalfArray  
Int  Int2  Int2Array  Int3  Int3Array  Int4  Int4Array  Int64  Int64Array  IntArray  
Matrix2d  Matrix2dArray  Matrix3d  Matrix3dArray  Matrix4d  Matrix4dArray  Normal3d  Normal3dArray  
Normal3f  Normal3fArray  Normal3h  Normal3hArray  Point3d  Point3dArray  Point3f  Point3fArray  
Point3h  Point3hArray  Quatd  QuatdArray  Quatf  QuatfArray  Quath  QuathArray  String  
StringArray  TexCoord2d  TexCoord2dArray  TexCoord2f  TexCoord2fArray  TexCoord2h  TexCoord2hArray  
TexCoord3d  TexCoord3dArray  TexCoord3f  TexCoord3fArray  TexCoord3h  TexCoord3hArray  Token  
TokenArray  UChar  UCharArray  UInt  UInt64  UInt64Array  UIntArray  Vector3d  Vector3dArray  
Vector3f  Vector3fArray  Vector3h  Vector3hArray  
  
print(dir(Sdf.ValueTypeNames))をすると、一応使える型がリストできるので  
これを見ながら頑張ってCreateAttributeの型定義をします。  
（しました）