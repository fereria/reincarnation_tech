import bpy

"""
![](https://gyazo.com/0fea7c1e09784740a9648a68eb65fa50.png)
"""


class SAMPLE_PT_Props(bpy.types.PropertyGroup):
    # PropertyGroupを追加
    my_int: bpy.props.IntProperty()
    my_float: bpy.props.FloatProperty()
    my_string: bpy.props.StringProperty()


class SAMPLE_PT_samplePanel(bpy.types.Panel):
    bl_label = "PropSample"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SamplePanel"

    def draw(self, context):

        layout = self.layout

        layout.prop(context.object.sampleValue, 'my_int')
        layout.prop(context.object, 'sample')


def register():

    bpy.types.Object.sampleValue = bpy.props.PointerProperty(type=SAMPLE_PT_Props)


def unregister():
    pass
