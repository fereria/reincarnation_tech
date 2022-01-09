import bpy

"""
BlenderのPropertyを追加するAddon

Groupを定義する場合は、 bpy.types.PropertyGroup に対して
追加するPropertyを指定する。

name : 追加する型
必用に応じて関数の引数でPropertyを定義する。

autoload を使用している場合、クラスを登録する部分以外は
register関数に定義する。

クラスを定義しただけではPropertyは使用できない。
使うには、 bpy.types の指定Type に properyName = Props のように代入する必要がある。
"""


class SAMPLE_PT_PropGroup(bpy.types.PropertyGroup):
    # PropertyGroupを追加
    my_int: bpy.props.IntProperty()
    my_float: bpy.props.FloatProperty()
    my_string: bpy.props.StringProperty()


def register():
    # Materialに対して登録
    bpy.types.Material.my_settings = bpy.props.PointerProperty(type=SAMPLE_PT_PropGroup)
    # 登録したら
    #  bpy.data.materials[1].my_settings.my_int = 10
    # こんな感じで、各MaterialにPropertyを追加することができる。
    # Groupではなく、直接Propertyも追加できる。
    bpy.types.Material.hoge = bpy.props.IntProperty()
    # 別のDataへのリンクを定義するときも PointerProperty
    bpy.types.Object.sample = bpy.props.PointerProperty(type=bpy.types.Material)
