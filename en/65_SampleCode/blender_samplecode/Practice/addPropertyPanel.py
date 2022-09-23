import bpy


class MyIntPropertyGroup(bpy.types.PropertyGroup):
    bl_options = {'REGISTER', 'UNDO'}
    myint: bpy.props.IntProperty(
        name="testint_name",
        description="",
        default=1,
        min=1,
        max=10,
    )
    myintB: bpy.props.IntProperty(
        name="testint_nameB",
        description="",
        default=1,
        min=1,
        max=10,
    )

    strval: bpy.props.StringProperty(
        name="hoge"
    )


class UI_PT_RenderPanel(bpy.types.Panel):
    bl_idname = "RENDER_PT_sample"
    bl_label = "HOGEHOGE"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Header")

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Sample Property")

        props = bpy.context.scene.Sample

        box.prop(props, "myint")
        box.prop(props, "myintB")
        box.prop(props, 'strval')


def register():
    bpy.types.Scene.Sample = bpy.props.PointerProperty(type=MyIntPropertyGroup)
