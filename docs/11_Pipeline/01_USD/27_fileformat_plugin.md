---
title: FileFormatPluginについて
tags:
    - USD
    - AdventCalendar2021
---

[Universal Scene Description AdventCalendar2021](https://qiita.com/advent-calendar/2021/usd) 24日目は、FileFormatPlugin についてです。

## File Format Plugin とは

https://graphics.pixar.com/usd/release/glossary.html#crate-file-format

FileFormatPluginとは、USDの特徴的な機能の１つで
usd以外のファイルフォーマット（FBX,OBJ,Alembic等）をUSDとしてロードできるようにする機能です。

USDは、繰り返しになりますが 複数のUSDファイル（レイヤー）をコンポジションアークによって合成し
１つのStageになります。
このときのLayerは、 usdc (バイナリ) であったり usda(アスキー) 形式のファイルですが
FileFormatPluginを使用することで、別のファイルフォーマットであっても
あたかもUSDのレイヤーを読んだかのように、別のフォーマットをロードできるようにできます。

### Alembic FileFormat Pluginを使う

USDのリポジトリには、デフォルトでAlembicのFileFormatPluginが含まれています。
https://graphics.pixar.com/usd/release/api/usdabc_page_front.html

```
python build_scripts\build_usd.py --alembic C:\USD
```

USDをビルドするときに、 --alembic オプションを追加すると、AlembicFileFormatを使用できるようになります。

![](https://gyazo.com/bd7ca4245bfbe7ea0f43de4155a64a32.gif)

試しに、Blenderからこんな感じのSuzanneを

![](https://gyazo.com/b5a2c270388d444bbb44366f397ac740.png)

Alembicで出力します。

{{'bed418960fb87912b9f31f1dd4d8c662'|gist}}

そして、このようにabcファイルをリファレンスするレイヤーを用意します。

AlembicPluginを使用した結果、

![](https://gyazo.com/66fb1c46638fd121124a4a6c56be6c50.gif)

Alembicをリファレンスでロードすることができました。
アニメーションも持ち込みできているのがわかります。

このように、USD以外のファイルフォーマットを **「さもUSDかのように」** リファレンスにロードすることができました。

{{'ee68e70cbd5268b893210c5a051cdde7'|gist}}

ロードしたAlembicファイルは、USDとして扱うことができるので、
このようにMaterialをAssignすることができます。

![](https://gyazo.com/8bfa39d071cdbba8dc8dc9985e33f827.png)

Alembic を Reference したあとに、MaterialAssignができました。

![](https://gyazo.com/cb4447c65b854d22eaeb53f8d4fb553b.png)

図に表すとこのようになります。
Alembic であっても、ファイルはLayerとして扱われ、コンポジションされ、Stageになります。


このように FileFormatPlugin をしようすることで、異なるファイルフォーマットを
事前にコンバートすることなく、USDファイルと同様にできるようになります。

デフォルトで使用できるのは、AlembicPluginですが
たとえばFbxFileFormat等を作れば、すでにあるFbxアセットをUSDとして配置できるようになります。
もちろん、AlembicとFbx、その他対応するプラグインがあれば
様々なファイルをUSDに取り込みシーンを構築することが可能になります。

FileFormatPluginを拡張すれば、USDへの導入がやりやすくなるのではないかと思います。

## FileFormatPlugin と DynamicFileFormat

FileFormatPlugin は、上のAlembicFileFormatPluginのように「ある別のフォーマットをUSDとしてロードする」FileFormatPluginと
もう１つ **「ある指定の拡張子にすることでプロシージャルにシーングラフを構築する」** DynamicFileFormat が存在しています。

> extras/usd/examples/usdDancingCubesExample

それが、この DancingCubesExample です。
このプラグインを使用して、 DynamicFileFormatがどんなものかを見ていきます。

### DancingCubeExample を試してみる

まずは、[こちらの方法](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/24_asset_resolution/#_1)でUSDをビルドしておきます。

![](https://gyazo.com/bd3e094b341951524a1eb3b301676f81.png)

そして、 USD/share/usd/examples/plugin 以下の usdDancingCubesExample と usdDancingCubesExample.dll を plugin/usd フォルダにコピーします。
コピーしたら準備完了です。

> ＜InstallDir＞/plugin/usd/usdDancingCubesExample/resources/usdDancingCubesExample/dancingCubes.usda

このDancingCubeExampleプラグインを使用したサンプルは、上記のフォルダにあるので、
ンプルの usda ファイルがあるので、usdviewでロードしてみます。

![](https://gyazo.com/634089300e1e08705b39fe2211b86a73.gif)

実行するとこのようになります。
DancingしているCubeのStageを開くことができました。
dancingCubes.usda を開いて中を確認すると、

```
    Usd_DCE_Params = {
        int perSide = 15
        int framesPerCycle = 36
        int numFrames = 200
        double distance = 6.0
        double moveScale = 1.5
        token geomType = "Cube"
    }
    payload = @anon:dummy:cubes.usddancingcubesexample@
```

Payloadでロードされているのは anon: つまりは 自動生成された無名レイヤの識別子で([参考](https://qiita.com/takahito-tejima/items/c065c7cd5c3a7abe14f1#tf_debugsdf_layer))
usddancingcubesexample という拡張子のファイルは存在していませんし、 Root 以下の prim_0～を含むような
USDのレイヤーは存在していません。
しかし、実際にはCubeが動くStageが生成されています。

このDancingCubeExampleは、PrimやSchema、AttributeがすでにUSDファイルに保存されているのではなく、
pluginfo.json で追加した Metadata (PluginでCustomMetaDataを追加する方法については[こちら](https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/15_CustomMetadata/))の情報を介して、USDのシーングラフを動的に、プロシージャルに生成しています。

動的に生成しているので、
例えば、 dancingCubes.usda の Usd_DCE_Params の perSide を 5 にしてみます。

![](https://gyazo.com/c5703c25778d4569daeb4b34ee7c070c.gif)

結果、Cubeの数が 5 個に変化しました。
このように、シーングラフをPlugin内で動的に構築できるのがFileFormatPluginです。
これを利用すれば、わざわざファイルを用意しなくても
なにかしらの情報をもとにしてUSDのシーングラフを生成することができます。
そしてそれをコンポジションで合成することができますので、
例えばレイアウトした各Shotのデータを動的に生成させたりといったことも可能になります。

## SdfFileFormat

最後に軽く実装について触れておきます。
FileFormatPlugin も DynamicFileFormatPlugin も、 SdfFileFormatクラスを継承することで実装します。

!!! info 

    > USD/extras/usd/examples/usdObj/fileFormat.cpp
    
    の、_ReadFromStreamを参考。
    UsdObjTranslateObjToUsd クラスで obj ファイル→USDのシーングラフに変換していて、
    その結果を layer->TransforContenxt(objAsUsd); で渡しています。


DynamicFileFormatも、SdfFileFormatクラスを継承して実装するのは共通ですが、

[DynamicFileFormat](https://graphics.pixar.com/usd/release/api/_usd__page__dynamic_file_format.html)は、ReadでStageを作りLayerを返すようにするか、あるいは
完全プロシージャルに生成するのであれば（DancingCubeExampleのように）
SdfAbstractDataクラスを使用することでプロシージャルに生成することが可能です。

[SdfAbstractData](https://graphics.pixar.com/usd/release/api/class_sdf_abstract_data.html)は、シーンディスクリプションを格納するためのインターフェースで
あるSdfPath,Field をキーにしてある値のペアを持ちます。

![](https://gyazo.com/d51122769d32ae951f7a15ee53a5d28b.png)

たとえば、上記のようなシーングラフの場合(DancingCubeExampleの生成例)

SdfPath /Root/prim_0/prim_0/prim_0 の Field が TypeName なら Cubeを返すし
SdfPath /Root の PrimChildren なら Rootの子Primを返すし、
SdfPath / (RootPath) で、 Field が DefaultPrim なら DefaultPrim を返します。

このように、SdfAbstractDataは ある問い合わせ(key)に対しての結果を 返すことで
動的にシーングラフを構築しています。

!!! info
    
    DancingCubeExampleの場合は、
    
    > USD/extras/usd/examples/usdDancingCubesExample/data.cpp

    にて、SdfAbstractData クラスが実装されています。

### PcpDynamicFileFormatInterface 

また、DynamicFileFormatPluginの場合
MetaDataから動的精製用のパラメータ（Usd_DCE_Params）を受け取るために
SdfFileFormat とともに、 PcpDynamicFileFormatInterface を実装します。
PcpDynamicFileFormatInterface を実装すると、アセットへのPayloadがある場合
ComposeFieldsForFileFormatArguments を呼び出して、
FileFormatPluginへの引数を生成します。

!!! info

    DancingCubeExample の場合、 
    
    > USD/extras/usd/examples/usdDancingCubesExample/fileFormat.cpp
    
    上記ファイルで ComposeFieldsForFileFormatArguments が実装されています。
    この中で、MetaDataの辞書型から FileFormatArguments を生成して、 FileFormatPlugin の引数にしています。
    
このあたりの実装は、私自身もまだ勉強中ではあるので
別途カスタムなFormatPlugin実装の記事を書こうと思います。
    
## まとめ

以上がFileFormatPluginでした。
実装についてはかなり端折りましたが、FileFormatPluginがどんなものかわかったでしょうか。

FileFormatPluginを使用すれば、USD以外のファイルもUSDとして扱うことができるようになるので
わざわざUSDにコンバートしなくても、今までのアセットを有効活用したり、異なるFileFormatをUSDで合成したり
できるようになるとわかりました。

また DynamicFileFormat Pluginを使用すれば、USDのPlugin内で動的にシーングラフを構築できるので
ファイルをわざわざ作らなくても、決められた処理をプロシージャルに構築が可能になります。

この機能は、CompositionArc・Schema・AssetResolutionといったこれまで解説してきた機能と同じく
USDのパイプラインを構築する上で強力な武器になりますので
パイプライン構築の際にはぜひとも取り入れてほしい機能です。