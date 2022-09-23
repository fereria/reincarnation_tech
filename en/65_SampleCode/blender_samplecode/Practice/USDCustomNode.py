import bpy

from pxr import Usd, UsdGeom

from .base_node import USDNode


class CubeNode(USDNode):
    """Merges two USD streams"""
    bl_idname = 'usd.CubeNode'
    bl_label = "Cube"

    def update_data(self, context):
        self.reset()

    sdf_path: bpy.props.StringProperty(
        name="SdfPath",
        default="",
        update=update_data
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, 'sdf_path')

    def compute(self, **kwargs):

        input_stage = self.get_input_link('Input', **kwargs)

        if not self.sdf_path:
            return None

        stage = self.cached_stage.create()

        if input_stage:
            layer = input_stage.GetRootLayer()
            stage.GetRootLayer().subLayerPaths = [layer.realPath]

        UsdGeom.Cube.Define(stage, self.sdf_path)

        return stage
