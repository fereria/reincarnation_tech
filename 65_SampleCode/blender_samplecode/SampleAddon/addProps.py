import bpy


class SAMPLE_PT_PropGroup(bpy.types.PropertyGroup):
    # PropetyGroupを追加
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
