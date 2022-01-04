import bpy


class PropGroup(bpy.types.PropertyGroup):
    # PropetyGroupを追加
    my_int: bpy.props.IntProperty()
    my_float: bpy.props.FloatProperty()
    my_string: bpy.props.StringProperty()


def register():
    # Materialに対して登録
    bpy.types.Material.my_settings = bpy.props.PointerProperty(type=PropGroup)
    # 登録したら
    #  bpy.data.materials[1].my_settings.my_int = 10
    # こんな感じで、各MaterialにPropertyを追加することができる。
    # Groupではなく、直接Propertyも追加できる。
    bpy.types.Material.hoge = bpy.props.IntProperty()
