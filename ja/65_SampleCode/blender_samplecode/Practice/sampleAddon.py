
import bpy
import re
import string


# --------------------------------------------------------- #
# Property
# --------------------------------------------------------- #

# ComboBoxのCallback/setter/getter
def callback_renameProp(scene=None, context=None):
    # identifier / name / icon / index
    return [("Number", "_<num>", "", 1),
            ("Alphabet", "_<abc>", "", 3)]


def set_renameProp(self, context):
    self['combo'] = context


def get_renameProp(self):
    return self['combo']


class RENAMER_PT_RenameProperty(bpy.types.PropertyGroup):

    renameStr: bpy.props.StringProperty(name='rename')
    toStr: bpy.props.StringProperty(name='replaceString')
    replaceFlg: bpy.props.BoolProperty(name='Replace String')
    digits: bpy.props.IntProperty(name='Number of digits', default=3, min=1, max=10)
    combo: bpy.props.EnumProperty(
        name="Suffix",
        items=callback_renameProp,
        set=set_renameProp,
        get=get_renameProp
    )


# --------------------------------------------------------- #
# Operator
# --------------------------------------------------------- #
class RENAMER_OT_Rename(bpy.types.Operator):

    bl_idname = "renamer.rename"
    bl_label = "Rename"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.scene.renamer.replaceFlg:
            # 末尾に数字やらを入れてリネーム
            for num, obj in enumerate(context.selected_objects):
                if context.scene.renamer.combo == "Number":
                    suffix = str(num + 1).zfill(context.scene.renamer.digits)
                else:
                    suffix = string.ascii_uppercase[num]
                obj.name = context.scene.renamer.renameStr + "_" + suffix
        else:
            # ReplaceString
            for num, obj in enumerate(context.selected_objects):
                obj.name = re.sub(context.scene.renamer.renameStr, context.scene.renamer.toStr, obj.name)

        return {'FINISHED'}

# --------------------------------------------------------- #
# GUI
# --------------------------------------------------------- #


class RENAMER_PT_SamplePanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tutrial"
    bl_label = "Rename Tool"

    #--- draw ---#
    def draw(self, context):
        layout = self.layout
        props = bpy.context.scene.renamer

        layout.prop(props, 'replaceFlg')
        layout.prop(props, 'renameStr')

        if props.replaceFlg:
            layout.prop(props, 'toStr')
        else:
            layout.prop(props, 'combo')
            if props.combo == "Number":
                layout.prop(props, 'digits')

        layout.operator(RENAMER_OT_Rename.bl_idname, text="Rename Selection")


def register():
    bpy.types.Scene.renamer = bpy.props.PointerProperty(type=RENAMER_PT_RenameProperty)
