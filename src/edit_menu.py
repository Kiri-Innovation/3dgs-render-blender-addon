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
        col_05CDB.alert = False
        col_05CDB.enabled = True
        col_05CDB.active = True
        col_05CDB.use_property_split = False
        col_05CDB.use_property_decorate = False
        col_05CDB.scale_x = 1.0
        col_05CDB.scale_y = 1.0
        col_05CDB.alignment = 'Expand'.upper()
        col_05CDB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if (bpy.context.scene.sna_dgs_scene_properties.active_mode == 'Edit'):
            box_09ED1 = col_05CDB.box()
            box_09ED1.alert = False
            box_09ED1.enabled = True
            box_09ED1.active = True
            box_09ED1.use_property_split = False
            box_09ED1.use_property_decorate = False
            box_09ED1.alignment = 'Expand'.upper()
            box_09ED1.scale_x = 1.0
            box_09ED1.scale_y = 1.0
            if not True: box_09ED1.operator_context = "EXEC_DEFAULT"
            grid_B53F5 = box_09ED1.grid_flow(columns=2, row_major=True, even_columns=False, even_rows=False, align=True)
            grid_B53F5.enabled = True
            grid_B53F5.active = True
            grid_B53F5.use_property_split = False
            grid_B53F5.use_property_decorate = False
            grid_B53F5.alignment = 'Expand'.upper()
            grid_B53F5.scale_x = 1.0
            grid_B53F5.scale_y = 1.0
            if not True: grid_B53F5.operator_context = "EXEC_DEFAULT"
            grid_B53F5.prop(bpy.context.scene.sna_dgs_scene_properties, 'edit_mode_menu', text=bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu, icon_value=0, emboss=True, expand=True)
        if bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Import":
            box_456A0 = col_05CDB.box()
            box_456A0.alert = False
            box_456A0.enabled = True
            box_456A0.active = True
            box_456A0.use_property_split = False
            box_456A0.use_property_decorate = False
            box_456A0.alignment = 'Expand'.upper()
            box_456A0.scale_x = 1.0
            box_456A0.scale_y = 1.0
            if not True: box_456A0.operator_context = "EXEC_DEFAULT"
            layout_function = box_456A0
            sna_import_menu_94FB1(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Modifiers":
            if (bpy.context.view_layer.objects.active == None):
                box_BCC27 = col_05CDB.box()
                box_BCC27.alert = False
                box_BCC27.enabled = True
                box_BCC27.active = True
                box_BCC27.use_property_split = False
                box_BCC27.use_property_decorate = False
                box_BCC27.alignment = 'Expand'.upper()
                box_BCC27.scale_x = 1.0
                box_BCC27.scale_y = 1.0
                if not True: box_BCC27.operator_context = "EXEC_DEFAULT"
                box_BCC27.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            else:
                box_15E02 = col_05CDB.box()
                box_15E02.alert = False
                box_15E02.enabled = True
                box_15E02.active = True
                box_15E02.use_property_split = False
                box_15E02.use_property_decorate = False
                box_15E02.alignment = 'Expand'.upper()
                box_15E02.scale_x = 1.0
                box_15E02.scale_y = 1.0
                if not True: box_15E02.operator_context = "EXEC_DEFAULT"
                layout_function = box_15E02
                sna_modify_menu_AEA26(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Colour":
            if (bpy.context.view_layer.objects.active == None):
                box_7DC02 = col_05CDB.box()
                box_7DC02.alert = False
                box_7DC02.enabled = True
                box_7DC02.active = True
                box_7DC02.use_property_split = False
                box_7DC02.use_property_decorate = False
                box_7DC02.alignment = 'Expand'.upper()
                box_7DC02.scale_x = 1.0
                box_7DC02.scale_y = 1.0
                if not True: box_7DC02.operator_context = "EXEC_DEFAULT"
                box_7DC02.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            else:
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Colour_And_Material' in bpy.context.view_layer.objects.active.modifiers):
                    box_FB8A4 = col_05CDB.box()
                    box_FB8A4.alert = False
                    box_FB8A4.enabled = True
                    box_FB8A4.active = True
                    box_FB8A4.use_property_split = False
                    box_FB8A4.use_property_decorate = False
                    box_FB8A4.alignment = 'Expand'.upper()
                    box_FB8A4.scale_x = 1.0
                    box_FB8A4.scale_y = 1.0
                    if not True: box_FB8A4.operator_context = "EXEC_DEFAULT"
                    layout_function = box_FB8A4
                    sna_colour_function_interface_3A6A5(layout_function, )
                else:
                    box_6F020 = col_05CDB.box()
                    box_6F020.alert = False
                    box_6F020.enabled = True
                    box_6F020.active = True
                    box_6F020.use_property_split = False
                    box_6F020.use_property_decorate = False
                    box_6F020.alignment = 'Expand'.upper()
                    box_6F020.scale_x = 1.0
                    box_6F020.scale_y = 1.0
                    if not True: box_6F020.operator_context = "EXEC_DEFAULT"
                    box_6F020.label(text='Active Object is missing the ', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    box_6F020.label(text='Adjust_Colour_And_Material modifier', icon_value=0)
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Animate":
            if (bpy.context.view_layer.objects.active == None):
                box_36685 = col_05CDB.box()
                box_36685.alert = False
                box_36685.enabled = True
                box_36685.active = True
                box_36685.use_property_split = False
                box_36685.use_property_decorate = False
                box_36685.alignment = 'Expand'.upper()
                box_36685.scale_x = 1.0
                box_36685.scale_y = 1.0
                if not True: box_36685.operator_context = "EXEC_DEFAULT"
                box_36685.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            else:
                box_2B760 = col_05CDB.box()
                box_2B760.alert = False
                box_2B760.enabled = True
                box_2B760.active = True
                box_2B760.use_property_split = False
                box_2B760.use_property_decorate = False
                box_2B760.alignment = 'Expand'.upper()
                box_2B760.scale_x = 1.0
                box_2B760.scale_y = 1.0
                if not True: box_2B760.operator_context = "EXEC_DEFAULT"
                layout_function = box_2B760
                sna_animate_function_interface_57F9E(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "HQ / LQ":
            box_50BC2 = col_05CDB.box()
            box_50BC2.alert = False
            box_50BC2.enabled = True
            box_50BC2.active = True
            box_50BC2.use_property_split = False
            box_50BC2.use_property_decorate = False
            box_50BC2.alignment = 'Expand'.upper()
            box_50BC2.scale_x = 1.0
            box_50BC2.scale_y = 1.0
            if not True: box_50BC2.operator_context = "EXEC_DEFAULT"
            layout_function = box_50BC2
            sna_hq_mode_function_interface_17C41(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Export":
            if (bpy.context.view_layer.objects.active == None):
                box_A093C = col_05CDB.box()
                box_A093C.alert = False
                box_A093C.enabled = True
                box_A093C.active = True
                box_A093C.use_property_split = False
                box_A093C.use_property_decorate = False
                box_A093C.alignment = 'Expand'.upper()
                box_A093C.scale_x = 1.0
                box_A093C.scale_y = 1.0
                if not True: box_A093C.operator_context = "EXEC_DEFAULT"
                box_A093C.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            else:
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.view_layer.objects.active.modifiers):
                    if (len(bpy.context.view_layer.objects.selected) > 1):
                        box_7DD8C = col_05CDB.box()
                        box_7DD8C.alert = False
                        box_7DD8C.enabled = True
                        box_7DD8C.active = True
                        box_7DD8C.use_property_split = False
                        box_7DD8C.use_property_decorate = False
                        box_7DD8C.alignment = 'Expand'.upper()
                        box_7DD8C.scale_x = 1.0
                        box_7DD8C.scale_y = 1.0
                        if not True: box_7DD8C.operator_context = "EXEC_DEFAULT"
                        box_7DD8C.label(text='Only select 1 object for export', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    else:
                        box_3E038 = col_05CDB.box()
                        box_3E038.alert = False
                        box_3E038.enabled = True
                        box_3E038.active = True
                        box_3E038.use_property_split = False
                        box_3E038.use_property_decorate = False
                        box_3E038.alignment = 'Expand'.upper()
                        box_3E038.scale_x = 1.0
                        box_3E038.scale_y = 1.0
                        if not True: box_3E038.operator_context = "EXEC_DEFAULT"
                        layout_function = box_3E038
                        sna_export_3dgs_function_interface_CDF59(layout_function, )
                else:
                    box_DE950 = col_05CDB.box()
                    box_DE950.alert = False
                    box_DE950.enabled = True
                    box_DE950.active = True
                    box_DE950.use_property_split = False
                    box_DE950.use_property_decorate = False
                    box_DE950.alignment = 'Expand'.upper()
                    box_DE950.scale_x = 1.0
                    box_DE950.scale_y = 1.0
                    if not True: box_DE950.operator_context = "EXEC_DEFAULT"
                    box_DE950.label(text='The Active Object is missing the', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    box_DE950.label(text='Write F_DC_And_Merge modifier', icon_value=0)
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Rig":
            box_D5082 = col_05CDB.box()
            box_D5082.alert = False
            box_D5082.enabled = True
            box_D5082.active = True
            box_D5082.use_property_split = False
            box_D5082.use_property_decorate = False
            box_D5082.alignment = 'Expand'.upper()
            box_D5082.scale_x = 1.0
            box_D5082.scale_y = 1.0
            if not True: box_D5082.operator_context = "EXEC_DEFAULT"
            layout_function = box_D5082
            sna_rig_891FC(layout_function, )
        elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Light Bake":
            box_6F2D7 = col_05CDB.box()
            box_6F2D7.alert = False
            box_6F2D7.enabled = True
            box_6F2D7.active = True
            box_6F2D7.use_property_split = False
            box_6F2D7.use_property_decorate = False
            box_6F2D7.alignment = 'Expand'.upper()
            box_6F2D7.scale_x = 1.0
            box_6F2D7.scale_y = 1.0
            if not True: box_6F2D7.operator_context = "EXEC_DEFAULT"
            layout_function = box_6F2D7
            sna_light_bake_8F346(layout_function, )
        else:
            pass
