import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .animate_function_interface import sna_animate_function_interface_57F9E
from .colour_function_interface import sna_colour_function_interface_3A6A5
from .edit_select_tools import sna_edit_select_tools_D0175
from .export_3dgs_function_interface import sna_export_3dgs_function_interface_CDF59
from .hq_mode_function_interface import sna_hq_mode_function_interface_17C41
from .import_menu import sna_import_menu_94FB1
from .light_bake import sna_light_bake_8F346
from .modify_menu import sna_modify_menu_AEA26
from .rig import sna_rig_891FC

__package__ = __package__.rsplit('.', 1)[0]


def sna_edit_menu_D3299(layout_function, ):
    if 'EDIT_MESH'==bpy.context.mode:
        layout_function = layout_function
        sna_edit_select_tools_D0175(layout_function, )
    else:
        col_05CDB = layout_function.column(heading='', align=False)
        if (bpy.context.scene.sna_dgs_scene_properties.active_mode == 'Edit'):
            box_09ED1 = col_05CDB.box()
            grid_B53F5 = box_09ED1.grid_flow(columns=2, row_major=True, even_columns=False, even_rows=False, align=True)
            grid_B53F5.prop(bpy.context.scene.sna_dgs_scene_properties, 'edit_mode_menu', text=bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu, icon_value=0, emboss=True, expand=True)
        if bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Import":
            box_456A0 = col_05CDB.box()
            layout_function = box_456A0
            sna_import_menu_94FB1(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Modifiers":
            if (bpy.context.view_layer.objects.active == None):
                box_BCC27 = col_05CDB.box()
                box_BCC27.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            else:
                box_15E02 = col_05CDB.box()
                layout_function = box_15E02
                sna_modify_menu_AEA26(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Colour":
            if (bpy.context.view_layer.objects.active == None):
                box_7DC02 = col_05CDB.box()
                box_7DC02.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            else:
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Colour_And_Material' in bpy.context.view_layer.objects.active.modifiers):
                    box_FB8A4 = col_05CDB.box()
                    layout_function = box_FB8A4
                    sna_colour_function_interface_3A6A5(layout_function, )
                else:
                    box_6F020 = col_05CDB.box()
                    box_6F020.label(text='Active Object is missing the ', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    box_6F020.label(text='Adjust_Colour_And_Material modifier', icon_value=0)
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Animate":
            if (bpy.context.view_layer.objects.active == None):
                box_36685 = col_05CDB.box()
                box_36685.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            else:
                box_2B760 = col_05CDB.box()
                layout_function = box_2B760
                sna_animate_function_interface_57F9E(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "HQ / LQ":
            box_50BC2 = col_05CDB.box()
            layout_function = box_50BC2
            sna_hq_mode_function_interface_17C41(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Export":
            if (bpy.context.view_layer.objects.active == None):
                box_A093C = col_05CDB.box()
                box_A093C.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            else:
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.view_layer.objects.active.modifiers):
                    if (len(bpy.context.view_layer.objects.selected) > 1):
                        box_7DD8C = col_05CDB.box()
                        box_7DD8C.label(text='Only select 1 object for export', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    else:
                        box_3E038 = col_05CDB.box()
                        layout_function = box_3E038
                        sna_export_3dgs_function_interface_CDF59(layout_function, )
                else:
                    box_DE950 = col_05CDB.box()
                    box_DE950.label(text='The Active Object is missing the', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    box_DE950.label(text='Write F_DC_And_Merge modifier', icon_value=0)
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Rig":
            box_D5082 = col_05CDB.box()
            layout_function = box_D5082
            sna_rig_891FC(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Light Bake":
            box_6F2D7 = col_05CDB.box()
            layout_function = box_6F2D7
            sna_light_bake_8F346(layout_function, )
        else:
            pass
