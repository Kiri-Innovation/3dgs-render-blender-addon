import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_dgs_mods_uv_edit_7D8A8(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_UV_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_9FF77 = layout_function.box()
        box_9FF77.alert = False
        box_9FF77.enabled = True
        box_9FF77.active = True
        box_9FF77.use_property_split = False
        box_9FF77.use_property_decorate = False
        box_9FF77.alignment = 'Expand'.upper()
        box_9FF77.scale_x = 1.0
        box_9FF77.scale_y = 1.0
        if not True: box_9FF77.operator_context = "EXEC_DEFAULT"
        split_CE162 = box_9FF77.split(factor=0.5, align=False)
        split_CE162.alert = False
        split_CE162.enabled = True
        split_CE162.active = True
        split_CE162.use_property_split = False
        split_CE162.use_property_decorate = False
        split_CE162.scale_x = 1.0
        split_CE162.scale_y = 1.0
        split_CE162.alignment = 'Expand'.upper()
        if not True: split_CE162.operator_context = "EXEC_DEFAULT"
        split_CE162.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], 'show_viewport', text='UV Edit', icon_value=0, emboss=True, toggle=True)
        row_DE4FE = split_CE162.row(heading='', align=True)
        row_DE4FE.alert = False
        row_DE4FE.enabled = True
        row_DE4FE.active = True
        row_DE4FE.use_property_split = False
        row_DE4FE.use_property_decorate = False
        row_DE4FE.scale_x = 1.0
        row_DE4FE.scale_y = 1.0
        row_DE4FE.alignment = 'Right'.upper()
        row_DE4FE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_DE4FE.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_DE4FE.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Render_UV_Edit_GN'
        op = row_DE4FE.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Render_UV_Edit_GN'
        box_E2654 = box_9FF77.box()
        box_E2654.alert = False
        box_E2654.enabled = True
        box_E2654.active = True
        box_E2654.use_property_split = False
        box_E2654.use_property_decorate = False
        box_E2654.alignment = 'Expand'.upper()
        box_E2654.scale_x = 1.0
        box_E2654.scale_y = 1.0
        if not True: box_E2654.operator_context = "EXEC_DEFAULT"
        attr_B95E2 = '["' + str('Socket_101' + '"]') 
        box_E2654.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_B95E2), text='UV Name', icon_value=0, emboss=True, toggle=True)
        attr_5057A = '["' + str('Socket_81' + '"]') 
        box_E2654.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_5057A), text='', icon_value=0, emboss=True, toggle=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN']['Socket_81'] == 1):
            col_B844C = box_E2654.column(heading='', align=True)
            col_B844C.alert = False
            col_B844C.enabled = True
            col_B844C.active = True
            col_B844C.use_property_split = False
            col_B844C.use_property_decorate = False
            col_B844C.scale_x = 1.0
            col_B844C.scale_y = 1.0
            col_B844C.alignment = 'Expand'.upper()
            col_B844C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_09238 = '["' + str('Socket_79' + '"]') 
            col_B844C.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_09238), text='', icon_value=0, emboss=True, toggle=True)
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN']['Socket_79'] == 1):
                attr_67DDE = '["' + str('Socket_80' + '"]') 
                col_B844C.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_67DDE), text='', icon_value=0, emboss=True, toggle=True)
            attr_BB6E4 = '["' + str('Socket_105' + '"]') 
            col_B844C.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_BB6E4), text='', icon_value=0, emboss=True, toggle=True)
        box_06FCC = box_9FF77.box()
        box_06FCC.alert = False
        box_06FCC.enabled = True
        box_06FCC.active = True
        box_06FCC.use_property_split = False
        box_06FCC.use_property_decorate = False
        box_06FCC.alignment = 'Expand'.upper()
        box_06FCC.scale_x = 1.0
        box_06FCC.scale_y = 1.0
        if not True: box_06FCC.operator_context = "EXEC_DEFAULT"
        attr_86FBB = '["' + str('Socket_83' + '"]') 
        box_06FCC.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_86FBB), text='Align to direction', icon_value=0, emboss=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN']['Socket_83']:
            col_9BFFE = box_06FCC.column(heading='', align=True)
            col_9BFFE.alert = False
            col_9BFFE.enabled = True
            col_9BFFE.active = True
            col_9BFFE.use_property_split = False
            col_9BFFE.use_property_decorate = False
            col_9BFFE.scale_x = 1.0
            col_9BFFE.scale_y = 1.0
            col_9BFFE.alignment = 'Expand'.upper()
            col_9BFFE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_9BFFE.label(text='Axis', icon_value=0)
            row_A1034 = col_9BFFE.row(heading='', align=False)
            row_A1034.alert = False
            row_A1034.enabled = True
            row_A1034.active = True
            row_A1034.use_property_split = False
            row_A1034.use_property_decorate = False
            row_A1034.scale_x = 1.0
            row_A1034.scale_y = 1.0
            row_A1034.alignment = 'Expand'.upper()
            row_A1034.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_9CCDE = '["' + str('Socket_85' + '"]') 
            row_A1034.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_9CCDE), text='.', icon_value=0, emboss=True, expand=True)
            attr_1E2BC = '["' + str('Socket_84' + '"]') 
            col_9BFFE.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_1E2BC), text='Direction', icon_value=0, emboss=True)
            attr_81350 = '["' + str('Socket_86' + '"]') 
            col_9BFFE.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_81350), text='Rotation', icon_value=0, emboss=True, toggle=True)
        box_3BC41 = box_9FF77.box()
        box_3BC41.alert = False
        box_3BC41.enabled = True
        box_3BC41.active = True
        box_3BC41.use_property_split = False
        box_3BC41.use_property_decorate = False
        box_3BC41.alignment = 'Expand'.upper()
        box_3BC41.scale_x = 1.0
        box_3BC41.scale_y = 1.0
        if not True: box_3BC41.operator_context = "EXEC_DEFAULT"
        attr_6A5D2 = '["' + str('Socket_106' + '"]') 
        box_3BC41.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_6A5D2), text='Transform', icon_value=0, emboss=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN']['Socket_106']:
            col_A8AB9 = box_3BC41.column(heading='', align=False)
            col_A8AB9.alert = False
            col_A8AB9.enabled = True
            col_A8AB9.active = True
            col_A8AB9.use_property_split = False
            col_A8AB9.use_property_decorate = False
            col_A8AB9.scale_x = 1.0
            col_A8AB9.scale_y = 1.0
            col_A8AB9.alignment = 'Expand'.upper()
            col_A8AB9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_082AE = '["' + str('Socket_87' + '"]') 
            col_A8AB9.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_082AE), text='Translation', icon_value=0, emboss=True, expand=True)
            attr_1AE94 = '["' + str('Socket_88' + '"]') 
            col_A8AB9.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_1AE94), text='Rotation', icon_value=0, emboss=True)
            attr_0F93F = '["' + str('Socket_89' + '"]') 
            col_A8AB9.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_0F93F), text='Scale', icon_value=0, emboss=True, toggle=True)
            row_77081 = col_A8AB9.row(heading='', align=False)
            row_77081.alert = False
            row_77081.enabled = True
            row_77081.active = True
            row_77081.use_property_split = False
            row_77081.use_property_decorate = False
            row_77081.scale_x = 1.0
            row_77081.scale_y = 1.0
            row_77081.alignment = 'Expand'.upper()
            row_77081.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_20D92 = '["' + str('Socket_91' + '"]') 
            row_77081.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_20D92), text='Flip U', icon_value=0, emboss=True, toggle=True)
            attr_55098 = '["' + str('Socket_92' + '"]') 
            row_77081.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_55098), text='Flip V', icon_value=0, emboss=True, toggle=True)
            attr_65309 = '["' + str('Socket_95' + '"]') 
            col_A8AB9.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_65309), text='Randomize', icon_value=0, emboss=True, toggle=False)
            if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN']['Socket_95']:
                col_06A74 = col_A8AB9.column(heading='', align=False)
                col_06A74.alert = False
                col_06A74.enabled = True
                col_06A74.active = True
                col_06A74.use_property_split = False
                col_06A74.use_property_decorate = False
                col_06A74.scale_x = 1.0
                col_06A74.scale_y = 1.0
                col_06A74.alignment = 'Expand'.upper()
                col_06A74.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                attr_38294 = '["' + str('Socket_96' + '"]') 
                col_06A74.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_38294), text='Offset', icon_value=0, emboss=True, toggle=True)
                attr_850DC = '["' + str('Socket_97' + '"]') 
                col_06A74.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_850DC), text='Rotation', icon_value=0, emboss=True, toggle=True)
                attr_CF180 = '["' + str('Socket_98' + '"]') 
                col_06A74.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_UV_Edit_GN'], attr_CF180), text='Seed', icon_value=0, emboss=True, toggle=True)
    else:
        box_01F2C = layout_function.box()
        box_01F2C.alert = False
        box_01F2C.enabled = 'OBJECT'==bpy.context.mode
        box_01F2C.active = True
        box_01F2C.use_property_split = False
        box_01F2C.use_property_decorate = False
        box_01F2C.alignment = 'Expand'.upper()
        box_01F2C.scale_x = 1.0
        box_01F2C.scale_y = 1.0
        if not True: box_01F2C.operator_context = "EXEC_DEFAULT"
        row_34CC5 = box_01F2C.row(heading='', align=False)
        row_34CC5.alert = False
        row_34CC5.enabled = True
        row_34CC5.active = True
        row_34CC5.use_property_split = False
        row_34CC5.use_property_decorate = False
        row_34CC5.scale_x = 1.0
        row_34CC5.scale_y = 1.0
        row_34CC5.alignment = 'Expand'.upper()
        row_34CC5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_34CC5.label(text='UV Edit', icon_value=0)
        op = row_34CC5.operator('sna.dgs_render_add_uv_edit_modifier_e8ae6', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
