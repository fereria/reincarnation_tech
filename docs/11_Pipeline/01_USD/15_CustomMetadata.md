---
title: Plugin Metadataを使おう
tags:
    - CEDEC2022
---

Plugin Metadata とは、Prim や Layer、Attribute などに対して Metadata を
指定できるようにする機能です。

Plugin で特に指定がない場合、

```python
prim.SetMetadata('metadata_name',100)
```

このように Metadata を指定しようとしても、エラーになります。
(自由に指定をしたい場合は、CustomData を使う)

Plugin Metadata を使用すれば、指定の名前・型の Metadata を定義して
使用できるようになります。

## plugInfo.json

Plugin Metadata は、 plugInfo.json で定義します。

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

### plugInfo.json を保存する

![](https://gyazo.com/7ac46193c9de0e9a480d8bdb4098ce2c.png)

作成した plugInfo.json は、PXR_PLUGINPATH_NAME で指定したフォルダ以下の
pluginDirName/resources/plugInfo.json
に保存します。

### Metadata を使用する

{{embedIpynb("docs/11_Pipeline/01_USD/ipynb/custom_metadata.ipynb",[2])}}

まずは Prim を指定する場合。
appliesTo で、 prims を指定することで Prim に Metadata を追加できます。

{{embedIpynb("docs/11_Pipeline/01_USD/ipynb/custom_metadata.ipynb",[3])}}

次に Layer の場合。
SdfLayer には SetMetadata はありません。
Layer に対して Layer を指定したい場合は、GetPseudoRoot で RootPrim を取得して
その Prim に対して Metadata を指定すると、Layer に対して Metadata を指定できます。

{{embedIpynb("docs/11_Pipeline/01_USD/ipynb/custom_metadata.ipynb",[1])}}

Attribute/Propertis に対しての場合。
appliesTo は複数指定することができて、複数の場合は配列で渡せば OK です。
