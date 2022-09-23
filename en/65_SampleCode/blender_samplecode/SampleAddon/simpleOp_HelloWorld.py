import bpy
"""
Hello World をするだけのButtonをBlenderに追加する
"""


class SAMPLE_OT_HelloWorld(bpy.types.Operator):

    bl_idname = "object.hello_world"
    bl_label = "Hello World"
    bl_options = {'REGISTER', 'UNDO'}

    # メニューを実行したときに呼ばれるメソッド
    def execute(self, context):

        print('hello world!!!')

        return {'FINISHED'}


class samplePanel(bpy.types.Panel):
    bl_label = "SamplePanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SampleAddon"

    def draw(self, context):
        layout = self.layout
        layout.operator('object.hello_world')


def register():
    pass


def unregister():
    pass
