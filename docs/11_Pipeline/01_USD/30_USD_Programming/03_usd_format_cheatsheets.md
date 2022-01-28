---
title: USDフォーマットチートシート
tags:
    - USD
---

# USDフォーマットチートシート

[PythonUSDチートシート](02_usd_py_cheatsheets.md) では、Pythonコマンドのチートシートをまとめましたが  
こちらはUSDフォーマットの内部構造の記述についてのAsciiファイルとして記述した場合のチートシートです。  

## Usdファイル内でのPathの記述方法

USD内で外部ファイルを読んでいる場合は @@ で囲う。  
例）Reference等
```
#usda 1.0

def "sphereA" (
    prepend references = @sphere.usda@
)
{
}
```
USD内のSdfPathを指定する場合は

```
def "hoge" (
    prepend inherits = </TestClass>
)
{
}
```
<>で囲う。  
/ から始まる場合はRootからの絶対パス、なにもない場合は現在のPrimからの相対パスになる。  

## 最低限の構造

```
#usda 1.0
```

USDファイルを記述する場合は、一番頭に #usda 1.0 と書きます。  
コレがあれば、すべてUSDファイルとしてロードできます。  

## Primを定義する

### スキーマなしでPrimを定義

```
#usda 1.0

def "sphereA"
{
}
```
Primと呼ばれるタグを作成する

```
def "sphereA"
{
    def "sub"
    {
    }
}
```
Primは、このように {} の中に def を記述することでネストできる。  

  
### スキーマ（Type指定）付きでPrimを定義する

```
def Xform "hoge"
{
}
```

## クラスを定義する

```
class "className"
{
}
```
クラスで定義されているものは、usdview等でシーンを読んでもシーングラフには表示されない。  
  
## Overを定義する

```
over "name"
{
}
```
Overの場合は、Primと違い  
すでにPrimがある場合のみ値を上書きする。  
定義されているPrimがない場合はなにもしない。

## DefaultPrimを指定する

```
#usda 1.0
(
    defaultPrim = "sphereA"
)

def "sphereA"
{
}
```

DefaultPrimとは、リファレンスでusdを読み込んだ場合の起点になるPrimの事。  

## アトリビュートに値をセットする

```
#usda 1.0

def Xform "base"
{
    bool test = false
}
```
アトリビュートを追加する場合、Primの{}の中に 型 名前 = 値  
のように指定する。  

## Metadataを追加する

```
#usda 1.0
(
    "Hello World"
    defaultPrim = "sphereA"
)

def "sphereA" (
    "Hoge Hoge"
)
{
    custom bool testVal (
        "Attribute Comment"
    )
}
```

Metadataはレイヤー、プリム、アトリビュートそれぞれに付加情報として設定できる。  
指定したい場合は それぞれの定義の後に () を入れて、その中にアトリビュートを追加するように  
記述する。  

## CustomDataを追加する

```
#usda 1.0

def "defPrim" (
    customData = {
        string hoge = "test"
    }
)
{
}
```
customData = {} を使うと、好きに自分の入れたいMeta情報をレイヤー、プリム、アトリビュートに対して  
追加できる。  

## リファレンスでモデルを読み込む

### DefaultPrimが指定されている場合

```
#usda 1.0

def "sphereA" (
    prepend references = @sphere.usda@
)
{
}
```
リファレンスで読み込む場合は、読み込む先のPrimのMetadataに prepend references = ### で  
ファイルを指定する。  
ファイルパスは @@でかこって表現する。  
ファイルパスは、現在の usd ファイルからの相対または絶対パスで指定する。  
  
### references時にPrimを指定する場合

```
#usda 1.0

def "sphereA" (
    prepend references = @sphere.usda@</Model>
)
{
}
```
DefaultPrimの指定がない、あるいはそれ以外のPrimを狙ってリファレンスしたい場合は  
ファイル指定の後に <>で囲ってSdfPathを指定する。  

## SubLayerで読み込む

```
#usda 1.0
(
    subLayers = [
        @D:/usdClass.usda@
    ]
)
```

サブレイヤーで読み込むときは、レイヤーのMetadataに対して subLayers = []  
を追加して、配列で読み込みたいファイルパスを指定する。  
ファイルパスは @@ で囲う。  

## リレーションを追加する

```
#usda 1.0

def "test"
{
    def Xform "param"
    {
        prepend rel test = [
            </rel/data>,
        ]
    }
}

def "rel"
{
    def Xform "data"
    {
    }
}
```

リレーションを追加したい場合は、 アトリビュートを rel で宣言して、  
リレーション先のSdfPathを配列で指定する。  

## 継承(Inherits)する

```
def "hoge" (
    prepend inherits = </TestClass>
)
{
}
```

継承の場合は、継承したいPrimのMetadataに対して prepend inherits = SdfPath を追加する。  
  
```
#usda 1.0
(
    subLayers = [
        @D:/usdClass.usda@
    ]
)

def "hoge" (
    prepend inherits = </TestClass>
)
{
}
```

継承は、SdfPathで指定する。  
ので、例えば別ファイルに定義されているclass や defを継承したい場合は  
subLayerで読み込んでから inheritsで指定をする。  

## VariantSetを定義する

```
#usda 1.0
(
    "Hello World"
)

def Xform "World"
{
    def Cube "Cube" (
        variants = {
            string hogehoge = "green"
        }
        prepend variantSets = "hogehoge"
    )
    {
        variantSet "hogehoge" = {
            "blue" {
                color3f[] primvars:displayColor = [(0, 0, 1)]

            }
            "green" {
                color3f[] primvars:displayColor = [(0, 1, 0)]

            }
            "red" {
                color3f[] primvars:displayColor = [(1, 0, 0)]

            }
        }
    }
}
```
variantSetは、 variantSet で定義する。  
定義したvariantSetをPrimで使う場合は、Metadata内に prepend variantSets = "名前"  
を追加する。  
そのvariantSetのうち、選択されているセットは variants で、選択中の値を指定する。  
  
## アニメーションの定義

```
#usda 1.0
(
    endTimeCode = 100
    startTimeCode = 0
)

def Xform "World"
{
    def Cube "Cube"
    {
        float xformOp:rotateZ:spin.timeSamples = {
            0: 0,
            100: 360,
        }
        uniform token[] xformOpOrder = ["xformOp:rotateZ:spin"]
    }
}
```
コレを手で書くことはないと思うけど念のため。  
スタートフレームとエンドフレームは、レイヤーのMetadataに記載。  
Key情報は、timeSamplesにDict型で記載。  
  
xformOpOrderは、どういう順序でTransformを行うのかを指定する。  
  

## マテリアルのアサイン

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
                color3f inputs:diffuseColor = (0, 1, 0)
                float inputs:metalic = 0.9
                float inputs:roughness = 0.2
                token outputs:surface
            }
        }
    }
}
```
これもまぁ手では書かないけど念のため。  
  
Materialアサインはリレーションによって定義されている。  
MeshデータはリレーションでBind先のMaterial情報を保持し、  
Materialは、ShaderとのConnectionで値を受け取る。  
  
