---
title: Plugin Metadataを使おう
---

Plugin Metadataとは、PrimやLayer、Attributeなどに対してMetadataを
指定できるようにする機能です。

Pluginで特に指定がない場合、

```python
prim.SetMetadata('metadata_name',100)
```
このようにMetadataを指定しようとしても、エラーになります。
(自由に指定をしたい場合は、CustomDataを使う)

Plugin Metadataを使用すれば、指定の名前・型のMetadataを定義して
使用できるようになります。

## plugInfo.json

Plugin Metadataは、 plugInfo.json で定義します。

```json
{
  "Plugins": [
    {
      "Name": "MetadataPlugin",
      "Type": "resource",
      "Info": {
        "SdfMetadata": {
          "sample_metadata": {
            "type": "string",
            "appliesTo": "prims",
            "default": "hello world!!"
          },
          "layer_metadata": {
            "type": "string",
            "appliesTo": "layers",
            "default": "layer sample!!"
          },
          "attr_metadata": {
            "type": "int",
            "appliesTo": ["properties", "attributes"],
            "default": 100
          }
        }
      }
    }
  ]
}
```

基本構造はこんな感じになります。

https://graphics.pixar.com/usd/docs/api/sdf_page_front.html#sdf_metadata_types
使える型一覧はこのページにまとめてあります。
"type" value で型を指定して、appliesTo で、適応する対象を指定します。

### plugInfo.jsonを保存する

![](https://gyazo.com/7ac46193c9de0e9a480d8bdb4098ce2c.png)

作成した plugInfo.jsonは、PXR_PLUGINPATH_NAME で指定したフォルダ以下の
pluginDirName/resources/plugInfo.json
に保存します。

### Metadataを使用する

{{embedIpynb("docs/11_Pipeline/01_USD/ipynb/custom_metadata.ipynb",[2])}}

まずはPrimを指定する場合。
appliesTo で、 prims を指定することでPrimにMetadataを追加できます。

{{embedIpynb("docs/11_Pipeline/01_USD/ipynb/custom_metadata.ipynb",[3])}}

次にLayerの場合。
SdfLayerには SetMetadataはありません。
Layerに対してLayerを指定したい場合は、GetPseudoRoot で RootPrimを取得して
そのPrimに対してMetadataを指定すると、Layerに対してMetadataを指定できます。

{{embedIpynb("docs/11_Pipeline/01_USD/ipynb/custom_metadata.ipynb",[1])}}

Attribute/Propertisに対しての場合。
appliesToは複数指定することができて、複数の場合は配列で渡せばOKです。
